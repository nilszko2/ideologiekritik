"""
Paper Discovery V2.2 — Multi-Plattform mit Qualitätsfiltern.

Plattformen (alle kostenlos, keine Auth):
- OpenAlex         (api.openalex.org)     — 240M Works, starke Concept-Kartierung
- Semantic Scholar (api.semanticscholar.org) — 200M Papers, stark bei CS/AI und citation graphs
- CrossRef         (api.crossref.org)     — Kanonische DOI-Metadata, Publisher-basiert
- DNB              (services.dnb.de/sru)  — Deutsche Nationalbibliothek, ALLE deutschen Publikationen
- ResearchRabbit-Modus: kombiniert Similar + Citing aller Plattformen

Deutscher Diskurs: DNB deckt Zeitschriftenartikel, Bücher, Dissertationen, graue Literatur ab,
die in OpenAlex/Semantic Scholar *nicht* indiziert sind (Prokla, Das Argument, Mittelweg 36,
Leviathan, kritisch-lesen.de, Rosa-Luxemburg-Stiftung, GSP-Literatur etc.).

Nutzung:
    python paper-discovery.py --thema "capitalist realism"              → Multi-Plattform Topic Search
    python paper-discovery.py --doi "10.1215/9780822394136"             → Multi-Plattform Citation Network
    python paper-discovery.py --thema "..." --plattform openalex        → Nur eine Plattform
    python paper-discovery.py --doi "..." --rabbit                      → Research-Rabbit-Modus (Netzwerk 2. Ordnung)
    python paper-discovery.py --thema "..." --jahre 5 --top 15          → Standardfilter

Output: Markdown-Datei in 04_Projekte/Paper Discovery/

V2-Features:
- Cross-Platform-Validierung (zeigt, welches Paper bei welcher Plattform auftaucht)
- Deduplizierung über DOI
- Rate-Limiting mit Retry (Semantic Scholar drosselt auf 1 req/sec ohne API-Key)
- Konfigurierbare Plattform-Auswahl

V2.2-Qualitätsfilter (gegen Longtail-Rauschen):
- --min-cites N         : Mindestzitationen (default 10, DNB ausgenommen da keine Zitationen)
- --sort relevance|cited : Relevanz- vs. Zitationssortierung (default cited)
- --exclude-singletons  : Nur Papers, die auf >=2 Plattformen auftauchen
- --peer-reviewed       : Nur Journal Articles (verschärft OpenAlex type-Filter)
- Präzise Mehrwort-Queries empfohlen (s. Paper-Discovery-V2.md, Query-Guide)
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

# === Konfiguration ===

VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEFAULT_OUTPUT_DIR = os.path.join(VAULT_ROOT, "04_Projekte", "Paper Discovery")
USER_AGENT = "ideologiekritik-paper-discovery/2.0 (mailto:nilszko@hs-koblenz.de)"

OPENALEX_BASE = "https://api.openalex.org"
SEMANTIC_SCHOLAR_BASE = "https://api.semanticscholar.org/graph/v1"
CROSSREF_BASE = "https://api.crossref.org"
DNB_BASE = "https://services.dnb.de/sru/dnb"

# Rate Limits (conservative Defaults — Semantic Scholar ist am empfindlichsten)
RATE_LIMITS = {
    "openalex": 0.1,         # OpenAlex polite pool: ~10 req/sec erlaubt
    "semantic_scholar": 1.2,  # Semantic Scholar ohne API-Key: ~1 req/sec
    "crossref": 0.1,          # CrossRef: keine strikte Limitierung
    "dnb": 0.3,               # DNB: moderat, SRU nicht für Massenabfragen
}

# MARC21-XML Namespace für DNB
MARC_NS = {"m": "http://www.loc.gov/MARC21/slim", "srw": "http://www.loc.gov/zing/srw/"}


# === HTTP-Wrapper mit Retry ===

def http_get(url, platform="openalex", retries=3):
    """GET-Request mit Rate-Limiting und Retry bei 429."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                data = json.loads(r.read())
                time.sleep(RATE_LIMITS.get(platform, 0.5))
                return data
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = (2 ** attempt) * 2  # exponential backoff: 2s, 4s, 8s
                print(f"[{platform}] Rate limit (429), warte {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            print(f"[{platform} Fehler] HTTP {e.code} bei {url}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"[{platform} Fehler] {e} bei {url}", file=sys.stderr)
            return None
    return None


# === OpenAlex ===

def openalex_by_topic(thema, jahre=5, top=15, min_cites=0, sort="cited", peer_reviewed=False):
    aktuelles_jahr = datetime.now(timezone.utc).year
    start_jahr = aktuelles_jahr - jahre
    # Typen-Filter: verschärfen bei peer_reviewed
    if peer_reviewed:
        type_filter = "type:article"
    else:
        type_filter = "type:article|book|book-chapter|preprint"
    # Filter-String
    filters = [
        f"from_publication_date:{start_jahr}-01-01",
        type_filter,
    ]
    if min_cites > 0:
        filters.append(f"cited_by_count:>{min_cites - 1}")  # OpenAlex nutzt > statt >=
    sort_param = "relevance_score:desc" if sort == "relevance" else "cited_by_count:desc"
    params = urllib.parse.urlencode({
        "search": thema,
        "filter": ",".join(filters),
        "sort": sort_param,
        "per-page": top,
    })
    data = http_get(f"{OPENALEX_BASE}/works?{params}", "openalex")
    return data.get("results", []) if data else []


def openalex_by_doi(doi, top=10):
    doi_clean = doi.replace("https://doi.org/", "").strip()
    paper = http_get(f"{OPENALEX_BASE}/works/doi:{doi_clean}", "openalex")
    if not paper or paper.get("id") is None:
        return None, [], [], []
    oa_id = paper["id"].replace("https://openalex.org/", "")
    # Forward citations
    citing_data = http_get(
        f"{OPENALEX_BASE}/works?filter=cites:{oa_id}&sort=cited_by_count:desc&per-page={top}",
        "openalex"
    )
    citing = citing_data.get("results", []) if citing_data else []
    # Backward references
    ref_ids = paper.get("referenced_works", [])[:top]
    cited = []
    for rid in ref_ids:
        rid_short = rid.replace("https://openalex.org/", "")
        ref = http_get(f"{OPENALEX_BASE}/works/{rid_short}", "openalex")
        if ref:
            cited.append(ref)
    # Related works
    related_ids = paper.get("related_works", [])[:top]
    related = []
    for rid in related_ids:
        rid_short = rid.replace("https://openalex.org/", "")
        rel = http_get(f"{OPENALEX_BASE}/works/{rid_short}", "openalex")
        if rel:
            related.append(rel)
    return paper, citing, cited, related


def openalex_normalize(w):
    """Vereinheitlichtes Paper-Format."""
    if not w:
        return None
    authors = [a.get("author", {}).get("display_name", "?") for a in w.get("authorships", [])]
    abstract_idx = w.get("abstract_inverted_index")
    abstract = ""
    if abstract_idx:
        words = {}
        for word, positions in abstract_idx.items():
            for p in positions:
                words[p] = word
        abstract = " ".join(words[i] for i in sorted(words.keys()))
    venue = w.get("primary_location", {}) or {}
    source = venue.get("source", {}) or {}
    return {
        "title": w.get("display_name", "?"),
        "authors": authors,
        "year": w.get("publication_year"),
        "citations": w.get("cited_by_count", 0),
        "doi": (w.get("doi") or "").replace("https://doi.org/", ""),
        "venue": source.get("display_name", ""),
        "abstract": abstract,
        "concepts": [c["display_name"] for c in w.get("concepts", [])
                     if c.get("score", 0) >= 0.3][:6],
        "platforms": ["openalex"],
        "platform_ids": {"openalex": w.get("id", "").replace("https://openalex.org/", "")},
    }


# === Semantic Scholar ===

def semanticscholar_by_topic(thema, jahre=5, top=15, min_cites=0):
    aktuelles_jahr = datetime.now(timezone.utc).year
    start_jahr = aktuelles_jahr - jahre
    fields = "title,authors,year,citationCount,abstract,externalIds,venue,publicationVenue"
    query_params = {
        "query": thema,
        "limit": top,
        "year": f"{start_jahr}-{aktuelles_jahr}",
        "fields": fields,
    }
    if min_cites > 0:
        query_params["minCitationCount"] = min_cites
    params = urllib.parse.urlencode(query_params)
    data = http_get(f"{SEMANTIC_SCHOLAR_BASE}/paper/search?{params}", "semantic_scholar")
    return data.get("data", []) if data else []


def semanticscholar_by_doi(doi, top=10):
    doi_clean = doi.replace("https://doi.org/", "").strip()
    fields = "title,authors,year,citationCount,abstract,externalIds,venue,publicationVenue"
    paper = http_get(f"{SEMANTIC_SCHOLAR_BASE}/paper/DOI:{doi_clean}?fields={fields}", "semantic_scholar")
    if not paper:
        return None, [], [], []
    paper_id = paper.get("paperId")
    # Forward (citing)
    citing_data = http_get(
        f"{SEMANTIC_SCHOLAR_BASE}/paper/{paper_id}/citations?limit={top}&fields={fields}",
        "semantic_scholar"
    )
    citing = [c.get("citingPaper") for c in (citing_data.get("data", []) if citing_data else [])
              if c.get("citingPaper")]
    # Backward (references)
    ref_data = http_get(
        f"{SEMANTIC_SCHOLAR_BASE}/paper/{paper_id}/references?limit={top}&fields={fields}",
        "semantic_scholar"
    )
    cited = [r.get("citedPaper") for r in (ref_data.get("data", []) if ref_data else [])
             if r.get("citedPaper")]
    # Related (via /recommendations)
    rec_data = http_get(
        f"https://api.semanticscholar.org/recommendations/v1/papers/forpaper/{paper_id}?limit={top}&fields={fields}",
        "semantic_scholar"
    )
    related = rec_data.get("recommendedPapers", []) if rec_data else []
    return paper, citing, cited, related


def semanticscholar_normalize(p):
    """Vereinheitlichtes Paper-Format."""
    if not p:
        return None
    authors = [a.get("name", "?") for a in (p.get("authors") or [])]
    ext = p.get("externalIds") or {}
    venue_obj = p.get("publicationVenue") or {}
    return {
        "title": p.get("title", "?"),
        "authors": authors,
        "year": p.get("year"),
        "citations": p.get("citationCount", 0),
        "doi": ext.get("DOI", "") or "",
        "venue": (venue_obj.get("name") if isinstance(venue_obj, dict) else "") or p.get("venue", ""),
        "abstract": p.get("abstract") or "",
        "concepts": [],  # Semantic Scholar liefert Concepts nicht direkt
        "platforms": ["semantic_scholar"],
        "platform_ids": {"semantic_scholar": p.get("paperId", "")},
    }


# === CrossRef ===

def crossref_by_topic(thema, jahre=5, top=15, min_cites=0, sort="relevance"):
    """CrossRef: sort='relevance' (score) oder 'cited' (is-referenced-by-count).
    Bei breiten Queries ist 'relevance' fast immer besser — Zitationen-Sort zieht hochzitierte
    Medizin-/Physik-Blockbuster rein, die zufällig ein Suchwort enthalten."""
    aktuelles_jahr = datetime.now(timezone.utc).year
    start_jahr = aktuelles_jahr - jahre
    fetch_top = top * 3 if min_cites > 0 else top  # bei relevance-sort mehr holen, dann filtern
    sort_param = "is-referenced-by-count" if sort == "cited" else "score"
    params = urllib.parse.urlencode({
        "query": thema,
        "rows": fetch_top,
        "filter": f"from-pub-date:{start_jahr}-01-01,type:journal-article",
        "sort": sort_param,
        "order": "desc",
    })
    data = http_get(f"{CROSSREF_BASE}/works?{params}", "crossref")
    if not data:
        return []
    items = data.get("message", {}).get("items", [])
    if min_cites > 0:
        items = [w for w in items if w.get("is-referenced-by-count", 0) >= min_cites]
    return items[:top]


def crossref_by_doi(doi):
    """CrossRef liefert kanonische Metadaten + referenced works (backward)."""
    doi_clean = doi.replace("https://doi.org/", "").strip()
    paper = http_get(f"{CROSSREF_BASE}/works/{doi_clean}", "crossref")
    if not paper:
        return None, []
    work = paper.get("message", {})
    refs = work.get("reference", [])[:20]
    return work, refs


def crossref_normalize(w):
    """Vereinheitlichtes Paper-Format."""
    if not w:
        return None
    authors = []
    for a in w.get("author", []) or []:
        name = f"{a.get('given', '')} {a.get('family', '')}".strip()
        if name:
            authors.append(name)
    title_list = w.get("title", [])
    title = title_list[0] if title_list else "?"
    year = None
    issued = w.get("issued", {}).get("date-parts", [[]])
    if issued and issued[0]:
        year = issued[0][0]
    venue = ""
    container = w.get("container-title", [])
    if container:
        venue = container[0]
    return {
        "title": title,
        "authors": authors,
        "year": year,
        "citations": w.get("is-referenced-by-count", 0),
        "doi": w.get("DOI", ""),
        "venue": venue,
        "abstract": w.get("abstract", "") or "",
        "concepts": [],
        "platforms": ["crossref"],
        "platform_ids": {"crossref": w.get("DOI", "")},
    }


# === DNB (Deutsche Nationalbibliothek, SRU + MARC21-XML) ===

def http_get_xml(url, platform="dnb", retries=3):
    """GET-Request, gibt rohen XML-Body zurück (DNB liefert MARC21-XML, nicht JSON)."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                content = r.read()
                time.sleep(RATE_LIMITS.get(platform, 0.5))
                return content
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = (2 ** attempt) * 2
                print(f"[{platform}] Rate limit, warte {wait}s...", file=sys.stderr)
                time.sleep(wait)
                continue
            print(f"[{platform} Fehler] HTTP {e.code} bei {url}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"[{platform} Fehler] {e} bei {url}", file=sys.stderr)
            return None
    return None


def dnb_get_subfield(datafield, code):
    """Liest ein MARC-Subfield (z.B. 245$a = Haupttitel)."""
    sub = datafield.find(f"./m:subfield[@code='{code}']", MARC_NS)
    return sub.text if sub is not None else ""


def dnb_by_topic(thema, jahre=5, top=15):
    """DNB-Suche via SRU. Query-Sprache: explizites AND zwischen Begriffen erforderlich."""
    aktuelles_jahr = datetime.now(timezone.utc).year
    start_jahr = aktuelles_jahr - jahre
    # DNB CQL: Mehrere Wörter mit expliziten AND verbinden (Leerzeichen = phrase)
    words = [w.strip() for w in thema.split() if w.strip()]
    if len(words) == 1:
        term = words[0]
    else:
        term = " and ".join(words)
    query = f'({term}) and jhr within "{start_jahr} {aktuelles_jahr}"'
    params = urllib.parse.urlencode({
        "version": "1.1",
        "operation": "searchRetrieve",
        "query": query,
        "maximumRecords": top,
        "recordSchema": "MARC21-xml",
    })
    content = http_get_xml(f"{DNB_BASE}?{params}", "dnb")
    if not content:
        return []
    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        print(f"[dnb] XML-Parse-Fehler: {e}", file=sys.stderr)
        return []
    records = root.findall(".//srw:record/srw:recordData/m:record", MARC_NS)
    return records


def dnb_normalize(record):
    """DNB MARC21-XML → vereinheitlichtes Paper-Format."""
    if record is None:
        return None
    # 001: Record-ID
    record_id_elem = record.find("./m:controlfield[@tag='001']", MARC_NS)
    record_id = record_id_elem.text if record_id_elem is not None else ""
    # 245: Titel
    title_field = record.find("./m:datafield[@tag='245']", MARC_NS)
    title = ""
    if title_field is not None:
        title_a = dnb_get_subfield(title_field, "a")
        title_b = dnb_get_subfield(title_field, "b")
        title = title_a + (f": {title_b}" if title_b else "")
    # 100/700: Autor:innen
    authors = []
    for tag in ["100", "700"]:
        for df in record.findall(f"./m:datafield[@tag='{tag}']", MARC_NS):
            name = dnb_get_subfield(df, "a")
            if name:
                authors.append(name)
    # 264/260: Publikationsjahr
    year = None
    for tag in ["264", "260"]:
        df = record.find(f"./m:datafield[@tag='{tag}']", MARC_NS)
        if df is not None:
            year_str = dnb_get_subfield(df, "c")
            # Jahr extrahieren (Format variabel: "2023", "c2023", "[2023]")
            import re
            m = re.search(r'\b(19|20)\d{2}\b', year_str or "")
            if m:
                year = int(m.group(0))
                break
    # 490/830: Serie/Reihe (oft Zeitschriftentitel)
    venue = ""
    for tag in ["773", "490", "830"]:
        df = record.find(f"./m:datafield[@tag='{tag}']", MARC_NS)
        if df is not None:
            venue = dnb_get_subfield(df, "a") or dnb_get_subfield(df, "t") or ""
            if venue:
                break
    # 020: ISBN
    isbn_field = record.find("./m:datafield[@tag='020']", MARC_NS)
    isbn = dnb_get_subfield(isbn_field, "a") if isbn_field is not None else ""
    # 520: Zusammenfassung/Abstract (selten gefüllt)
    abstract = ""
    abs_field = record.find("./m:datafield[@tag='520']", MARC_NS)
    if abs_field is not None:
        abstract = dnb_get_subfield(abs_field, "a") or ""
    # 650: Schlagwörter (Concepts)
    concepts = []
    for df in record.findall("./m:datafield[@tag='650']", MARC_NS):
        kw = dnb_get_subfield(df, "a")
        if kw:
            concepts.append(kw)
    # 856: URL (bei OA)
    url = ""
    url_field = record.find("./m:datafield[@tag='856']", MARC_NS)
    if url_field is not None:
        url = dnb_get_subfield(url_field, "u") or ""

    return {
        "title": title or "?",
        "authors": authors,
        "year": year,
        "citations": 0,  # DNB liefert keine Zitationsdaten
        "doi": "",  # DNB hat oft keine DOIs, ISBN als Fallback
        "isbn": isbn,
        "venue": venue,
        "abstract": abstract,
        "concepts": concepts[:8],
        "url": url,
        "platforms": ["dnb"],
        "platform_ids": {"dnb": record_id},
    }


# === Deduplizierung & Merging ===

def dedupe_and_merge(papers_per_platform):
    """
    papers_per_platform: dict {platform_name: [normalized_papers]}
    Dedupliziert primär nach DOI; falls nicht vorhanden, nach Titel+Jahr.
    Merged Plattform-Zugehörigkeit.
    """
    merged = {}
    fallback = {}  # Für Papers ohne DOI: dedup nach Title+Year
    no_key = []
    for platform, papers in papers_per_platform.items():
        for p in papers:
            if not p:
                continue
            doi = (p.get("doi") or "").lower().strip()
            if doi:
                key = ("doi", doi)
                target = merged
            else:
                # Titel + Jahr als Fallback-Key
                title_norm = (p.get("title") or "").lower().strip()[:80]
                year = p.get("year") or "?"
                if title_norm:
                    key = ("title", f"{title_norm}__{year}")
                    target = fallback
                else:
                    no_key.append(p)
                    continue
            _, k = key
            if k in target:
                existing = target[k]
                if platform not in existing["platforms"]:
                    existing["platforms"].append(platform)
                existing["platform_ids"][platform] = p["platform_ids"].get(platform, "")
                if p.get("citations", 0) > existing.get("citations", 0):
                    existing["citations"] = p["citations"]
                if len(p.get("abstract", "")) > len(existing.get("abstract", "")):
                    existing["abstract"] = p["abstract"]
                if p.get("concepts") and not existing.get("concepts"):
                    existing["concepts"] = p["concepts"]
            else:
                target[k] = p.copy()
    # Vereinigung: DOI-basierte zuerst, dann Titel-basierte
    result = sorted(merged.values(), key=lambda x: x.get("citations", 0), reverse=True)
    result.extend(sorted(fallback.values(), key=lambda x: x.get("citations", 0), reverse=True))
    result.extend(no_key)
    return result


# === Markdown-Formatierung ===

def format_paper_md(p, rank=None):
    prefix = f"**#{rank}** — " if rank else ""
    title = p.get("title", "?")
    year = p.get("year", "?")
    authors = p.get("authors", [])
    authors_str = ", ".join(authors[:4])
    if len(authors) > 4:
        authors_str += ", et al."
    cites = p.get("citations", 0)
    doi = p.get("doi", "")
    venue = p.get("venue", "")
    platforms = p.get("platforms", [])
    platform_badges = " + ".join(f"`{pl}`" for pl in platforms)
    concepts = p.get("concepts", [])
    abstract = p.get("abstract", "")
    abs_preview = (abstract[:400] + "...") if len(abstract) > 400 else abstract

    lines = [
        f"### {prefix}{title} ({year})",
        f"- **Plattformen:** {platform_badges}",
        f"- **Autor:innen:** {authors_str or '?'}",
        f"- **Zitationen:** {cites}",
    ]
    if venue:
        lines.append(f"- **Publikation:** *{venue}*")
    if doi:
        lines.append(f"- **DOI:** https://doi.org/{doi}")
    if p.get("isbn"):
        lines.append(f"- **ISBN:** {p['isbn']}")
    if p.get("url"):
        lines.append(f"- **URL:** {p['url']}")
    if concepts:
        lines.append(f"- **Concepts/Schlagwörter:** {', '.join(concepts)}")
    if abs_preview:
        lines.append(f"- **Abstract:** {abs_preview}")
    return "\n".join(lines)


def render_topic_output(thema, jahre, merged_papers, platform_stats):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    plat_keys = [k for k in platform_stats.keys() if not k.startswith("_")]
    out = [
        "---",
        "typ: paper-discovery",
        "tags: [paper-discovery, multi-plattform]",
        f"erstellt: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        f'abfrage-thema: "{thema}"',
        f"abfrage-jahre: {jahre}",
        f'abfrage-zeitpunkt: "{ts}"',
        f"plattformen: [{', '.join(plat_keys)}]",
        "---",
        "",
        f'# Paper Discovery Multi-Plattform — „{thema}"',
        "",
        f'**Abfrage:** Top-Papers der letzten {jahre} Jahre zu „{thema}".',
        f"**Abgerufen:** {ts}",
        "",
        "## Plattform-Übersicht",
        "",
    ]
    for platform, count in platform_stats.items():
        if platform.startswith("_"):
            continue
        out.append(f"- **{platform}**: {count} Treffer")
    if "_filter_singletons_removed" in platform_stats:
        out.append(f"- *{platform_stats['_filter_singletons_removed']} Singletons per --exclude-singletons entfernt*")
    out.extend([
        "",
        f"**Nach Deduplizierung (DOI):** {len(merged_papers)} einzigartige Papers",
        "",
        "## Cross-Platform-Validierung",
        "",
        "Papers, die auf *mehreren* Plattformen auftauchen, sind besser validiert. Papers, die nur auf einer Plattform auftauchen, sind entweder spezifisch für diese Plattform oder weniger etabliert.",
        "",
    ])

    multi_platform = [p for p in merged_papers if len(p.get("platforms", [])) > 1]
    single_platform = [p for p in merged_papers if len(p.get("platforms", [])) == 1]

    if multi_platform:
        out.append(f"### Auf mehreren Plattformen ({len(multi_platform)})")
        out.append("")
        for i, p in enumerate(multi_platform, 1):
            out.append(format_paper_md(p, rank=i))
            out.append("")

    if single_platform:
        out.append(f"### Nur auf einer Plattform ({len(single_platform)})")
        out.append("")
        for i, p in enumerate(single_platform, 1):
            out.append(format_paper_md(p, rank=i))
            out.append("")

    out.extend([
        "---",
        "",
        "## Arbeitshinweise",
        "",
        "- **Multi-Platform-Treffer** = empirisch validierter Befund (verschiedene Indizierungsstrategien konvergieren).",
        "- **Semantic-Scholar-spezifisch** = oft stärkere CS/AI-Coverage und aktuellere Preprints.",
        "- **OpenAlex-spezifisch** = stärker bei interdisziplinären Concepts und Geisteswissenschaften.",
        "- **CrossRef-spezifisch** = kanonische Publisher-Metadata, enge DOI-Bindung.",
        "- **Nur auf einer Plattform** bei deutschsprachiger politischer Theorie (Prokla, Argument, Mittelweg 36) → APIs erfassen diese schlecht; manuelle Suche notwendig.",
    ])
    return "\n".join(out)


def render_rabbit_output(doi, paper, citing_merged, cited_merged, related_merged, platform_stats):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    title = paper.get("title", "?") if paper else "?"
    out = [
        "---",
        "typ: paper-discovery",
        "tags: [paper-discovery, multi-plattform, research-rabbit]",
        f"erstellt: {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
        f'abfrage-doi: "{doi}"',
        f'abfrage-zeitpunkt: "{ts}"',
        f"plattformen: [{', '.join(platform_stats.keys())}]",
        "---",
        "",
        f'# Research-Rabbit-Netzwerk — „{title}"',
        "",
        format_paper_md(paper) if paper else "_Paper nicht gefunden._",
        "",
        "---",
        "",
        "## Plattform-Statistik",
        "",
    ]
    for platform, counts in platform_stats.items():
        out.append(f"- **{platform}**: {counts.get('citing', 0)} Forward · {counts.get('cited', 0)} Backward · {counts.get('related', 0)} Related")
    out.append("")

    sections = [
        (f"## Forward (Zitierende) — {len(citing_merged)} nach Deduplizierung",
         "Wer zitiert dieses Paper? Papers mit hoher eigener Zitation = Rezeptions-Knotenpunkte.",
         citing_merged),
        (f"## Backward (Referenzen) — {len(cited_merged)} nach Deduplizierung",
         "Was zitiert dieses Paper? = theoretisch-empirische Wurzeln.",
         cited_merged),
        (f"## Related (Seitwärts) — {len(related_merged)} nach Deduplizierung",
         "Empfehlungen für thematisch verwandte Arbeiten — aus Concept-Graphen von OpenAlex + Semantic Scholar.",
         related_merged),
    ]

    for heading, intro, papers in sections:
        out.extend(["---", "", heading, "", intro, ""])
        for i, p in enumerate(papers, 1):
            out.append(format_paper_md(p, rank=i))
            out.append("")

    out.extend([
        "---",
        "",
        "## Arbeitshinweise",
        "",
        "- **Research-Rabbit-Prinzip:** Forward + Backward + Related = vollständiges Zitationsumfeld.",
        "- **Multi-Platform-Deduplizierung:** Papers, die von mehreren Plattformen gemeldet werden, sind robuster indiziert.",
        "- **Traditions-Kartierung:** Häufige Backward-Zitate mehrerer eigener Forward-Papers = Klassiker des Feldes.",
    ])
    return "\n".join(out)


# === Hauptfunktionen ===

AVAILABLE_PLATFORMS = ["openalex", "semantic_scholar", "crossref", "dnb"]


def discover_topic_multi(thema, jahre, top, platforms, min_cites=0, sort="cited",
                         peer_reviewed=False, exclude_singletons=False):
    """Multi-Platform Topic-Suche mit Qualitätsfiltern."""
    results = {}
    stats = {}
    if "openalex" in platforms:
        print(f"[openalex] Suche: {thema} (min_cites={min_cites}, sort={sort})", file=sys.stderr)
        raw = openalex_by_topic(thema, jahre, top, min_cites=min_cites, sort=sort,
                                peer_reviewed=peer_reviewed)
        results["openalex"] = [openalex_normalize(w) for w in raw]
        stats["openalex"] = len(results["openalex"])
    if "semantic_scholar" in platforms:
        print(f"[semantic_scholar] Suche: {thema} (min_cites={min_cites})", file=sys.stderr)
        raw = semanticscholar_by_topic(thema, jahre, top, min_cites=min_cites)
        results["semantic_scholar"] = [semanticscholar_normalize(p) for p in raw]
        stats["semantic_scholar"] = len(results["semantic_scholar"])
    if "crossref" in platforms:
        print(f"[crossref] Suche: {thema} (min_cites={min_cites}, sort={sort})", file=sys.stderr)
        raw = crossref_by_topic(thema, jahre, top, min_cites=min_cites, sort=sort)
        results["crossref"] = [crossref_normalize(w) for w in raw]
        stats["crossref"] = len(results["crossref"])
    if "dnb" in platforms:
        print(f"[dnb] Suche: {thema} (DNB liefert keine Zitationen → min_cites ignoriert)",
              file=sys.stderr)
        raw = dnb_by_topic(thema, jahre, top)
        results["dnb"] = [dnb_normalize(r) for r in raw]
        stats["dnb"] = len(results["dnb"])
    merged = dedupe_and_merge(results)
    # Exclude singletons (auf nur einer Plattform gefunden)
    if exclude_singletons:
        before = len(merged)
        merged = [p for p in merged if len(p.get("platforms", [])) >= 2]
        stats["_filter_singletons_removed"] = before - len(merged)
    return merged, stats


def discover_doi_rabbit(doi, top, platforms):
    """Multi-Platform DOI-Netzwerk (ResearchRabbit-Modus)."""
    main_paper = None
    citing_per_platform = {}
    cited_per_platform = {}
    related_per_platform = {}
    platform_stats = {}

    if "openalex" in platforms:
        print(f"[openalex] DOI: {doi}", file=sys.stderr)
        p, cit, ref, rel = openalex_by_doi(doi, top)
        if p:
            main_paper = main_paper or openalex_normalize(p)
        citing_per_platform["openalex"] = [openalex_normalize(x) for x in cit]
        cited_per_platform["openalex"] = [openalex_normalize(x) for x in ref]
        related_per_platform["openalex"] = [openalex_normalize(x) for x in rel]
        platform_stats["openalex"] = {
            "citing": len(citing_per_platform["openalex"]),
            "cited": len(cited_per_platform["openalex"]),
            "related": len(related_per_platform["openalex"]),
        }

    if "semantic_scholar" in platforms:
        print(f"[semantic_scholar] DOI: {doi}", file=sys.stderr)
        p, cit, ref, rel = semanticscholar_by_doi(doi, top)
        if p and not main_paper:
            main_paper = semanticscholar_normalize(p)
        citing_per_platform["semantic_scholar"] = [semanticscholar_normalize(x) for x in cit]
        cited_per_platform["semantic_scholar"] = [semanticscholar_normalize(x) for x in ref]
        related_per_platform["semantic_scholar"] = [semanticscholar_normalize(x) for x in rel]
        platform_stats["semantic_scholar"] = {
            "citing": len(citing_per_platform["semantic_scholar"]),
            "cited": len(cited_per_platform["semantic_scholar"]),
            "related": len(related_per_platform["semantic_scholar"]),
        }

    if "crossref" in platforms:
        print(f"[crossref] DOI: {doi}", file=sys.stderr)
        work, refs = crossref_by_doi(doi)
        if work and not main_paper:
            main_paper = crossref_normalize(work)
        cited_per_platform["crossref"] = []
        for r in refs:
            ref_doi = r.get("DOI", "")
            if ref_doi:
                cited_per_platform["crossref"].append({
                    "title": r.get("article-title") or r.get("volume-title") or "?",
                    "authors": [r.get("author", "?")] if r.get("author") else [],
                    "year": int(r.get("year", "0")) if r.get("year", "").isdigit() else None,
                    "citations": 0,
                    "doi": ref_doi,
                    "venue": r.get("journal-title", ""),
                    "abstract": "",
                    "concepts": [],
                    "platforms": ["crossref"],
                    "platform_ids": {"crossref": ref_doi},
                })
        platform_stats["crossref"] = {
            "citing": 0,
            "cited": len(cited_per_platform["crossref"]),
            "related": 0,
        }

    citing_merged = dedupe_and_merge(citing_per_platform)
    cited_merged = dedupe_and_merge(cited_per_platform)
    related_merged = dedupe_and_merge(related_per_platform)
    return main_paper, citing_merged, cited_merged, related_merged, platform_stats


# === Main ===

def main():
    parser = argparse.ArgumentParser(description="Multi-Platform Paper Discovery (OpenAlex + Semantic Scholar + CrossRef)")
    parser.add_argument("--thema", type=str, help="Suchthema (Keyword-Suche)")
    parser.add_argument("--doi", type=str, help="DOI für Zitations-Netzwerk")
    parser.add_argument("--jahre", type=int, default=5, help="Zeitfenster (nur bei --thema); default 5")
    parser.add_argument("--top", type=int, default=15, help="Top-N Papers pro Plattform; default 15")
    parser.add_argument("--plattform", type=str, default="all",
                        help="Kommagetrennt: openalex,semantic_scholar,crossref,dnb — oder 'all' (default). "
                             "dnb = Deutsche Nationalbibliothek (deutscher Diskurs).")
    parser.add_argument("--rabbit", action="store_true",
                        help="Research-Rabbit-Modus (Forward + Backward + Related); nur mit --doi")
    parser.add_argument("--min-cites", type=int, default=10,
                        help="Mindestzitationen (default 10, DNB ausgenommen). Auf 0 für keine Filterung.")
    parser.add_argument("--sort", type=str, default="relevance", choices=["cited", "relevance"],
                        help="Sortierung: 'relevance' (default, textlich relevante Papers zuerst) oder 'cited' (zitationsstarke zuerst)")
    parser.add_argument("--peer-reviewed", action="store_true",
                        help="Nur Journal Articles (verschärfter Typfilter bei OpenAlex)")
    parser.add_argument("--exclude-singletons", action="store_true",
                        help="Nur Papers zeigen, die auf >=2 Plattformen gefunden wurden (stärker validiert)")
    parser.add_argument("--output-dir", type=str, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--name", type=str, default=None)
    args = parser.parse_args()

    if not args.thema and not args.doi:
        parser.error("Entweder --thema oder --doi angeben.")

    if args.plattform == "all":
        platforms = AVAILABLE_PLATFORMS
    else:
        platforms = [p.strip() for p in args.plattform.split(",") if p.strip() in AVAILABLE_PLATFORMS]
        if not platforms:
            parser.error(f"Ungültige Plattform. Verfügbar: {AVAILABLE_PLATFORMS}")

    os.makedirs(args.output_dir, exist_ok=True)

    if args.doi:
        main_paper, citing, cited, related, stats = discover_doi_rabbit(args.doi, args.top, platforms)
        if not main_paper and all(not lst for lst in [citing, cited, related]):
            print("Nichts gefunden.", file=sys.stderr)
            sys.exit(1)
        md = render_rabbit_output(args.doi, main_paper, citing, cited, related, stats)
        default_name = f"rabbit-{args.doi.replace('/', '_')[:50]}"
    else:
        merged, stats = discover_topic_multi(
            args.thema, args.jahre, args.top, platforms,
            min_cites=args.min_cites, sort=args.sort,
            peer_reviewed=args.peer_reviewed,
            exclude_singletons=args.exclude_singletons,
        )
        if not merged:
            print("Nichts gefunden.", file=sys.stderr)
            sys.exit(1)
        md = render_topic_output(args.thema, args.jahre, merged, stats)
        default_name = args.thema[:40].replace(" ", "-").replace("/", "-")

    name = args.name or default_name
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    out_path = os.path.join(args.output_dir, f"discovery-{name}-{timestamp}.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
    print(f"Geschrieben: {out_path}")


if __name__ == "__main__":
    main()
