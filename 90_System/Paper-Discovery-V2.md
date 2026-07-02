---
tags: [system]
typ: system
---

# Paper-Discovery V2.2 — Multi-Plattform-Recherche mit Qualitätsfiltern

## Überblick

`paper-discovery.py` ist ein Research-Rabbit-Analogon mit 4 integrierten Plattformen + Qualitätsfiltern:

| Plattform | Stärke | Schwäche |
|---|---|---|
| **OpenAlex** | Concept-Kartierung, hohe Coverage | englischzentriert |
| **Semantic Scholar** | Citation Graph, CS/AI, Preprints | strenges Rate Limit (1/sec), 429 häufig |
| **CrossRef** | kanonische DOI-Metadata | sehr liberales Text-Matching (→ relevance-sort Pflicht!) |
| **DNB** | Deutscher Diskurs, graue Literatur, GSP | keine Zitationsdaten |

Ergänzend dazu **drei manuelle Schichten** (siehe Abschnitt IV): KI-Recherche-Tools, deutsche Zeitschriften-Archive, Grauliteratur.

## Nutzung

```bash
# Empfohlene Default-Suche (relevance-sort, min-cites=10)
python "90_System/Tools/paper-discovery.py" --thema '"capitalist realism"' --jahre 10

# Nur stark zitierte Klassiker (min-cites hochsetzen)
python "90_System/Tools/paper-discovery.py" --thema '"Ideologiekritik"' --min-cites 50 --jahre 15

# Multi-Platform-Validierung (nur Papers auf >=2 Plattformen)
python "90_System/Tools/paper-discovery.py" --thema "Kulturindustrie Adorno" --exclude-singletons

# Nur Peer-Reviewed Journal Articles
python "90_System/Tools/paper-discovery.py" --thema "Absorption Kapitalismus" --peer-reviewed

# Deutscher Fokus (DNB + OpenAlex)
python "90_System/Tools/paper-discovery.py" --thema "Ideologie" --plattform dnb,openalex

# DOI-basiertes Zitationsnetzwerk (Forward + Backward + Related)
python "90_System/Tools/paper-discovery.py" --doi "10.1215/9780822394136"

# Sortierung umstellen (wenn Sie klare Klassiker suchen)
python "90_System/Tools/paper-discovery.py" --thema "Adorno Kulturindustrie" --sort cited
```

## Query-Guide (wichtig!)

**Nicht** tun: `--thema "capitalist realism"`
- OpenAlex matcht auch Papers, die nur *critical realism* enthalten
- CrossRef liefert die meistzitierten Papers der letzten Jahre, die *irgendwo* eines der Wörter enthalten (Medizin-, Physik-Blockbuster)

**Stattdessen:** 
1. **Phrase mit Anführungszeichen:** `--thema '"capitalist realism"'` — erzwingt, dass beide Wörter zusammen erscheinen
2. **Zusätzliche spezifische Begriffe:** `--thema '"capitalist realism" Fisher neoliberalism'`
3. **`--sort relevance` (Default):** Ergebnisse werden nach Textrelevanz sortiert, nicht nach Rohzitationen
4. **`--min-cites N`:** Je spezifischer das Feld, desto niedriger (für Nischen 5–10; für Mainstream 30–50)
5. **`--exclude-singletons`:** Bei breiten Themen; zeigt nur Papers, die bei mindestens 2 Plattformen auftauchen

## Defaults erklärt

- `--min-cites 10` — filtert Longtail-Rauschen, ohne Nischen-Publikationen komplett zu verlieren
- `--sort relevance` — textlich passende Papers zuerst (nicht die hochzitiertesten Papers *überhaupt*, die zufällig ein Suchwort enthalten)
- `--top 15` — Genügend für Feld-Überblick, nicht zu viel zum Lesen
- `--jahre 5` — aktuell; für historische Rezeption `--jahre 20` o.ä.

## Output

Markdown-Datei in `04_Projekte/Paper Discovery/` mit:

- **YAML-Frontmatter** (Datum, Plattformen, Abfrage)
- **Plattform-Übersicht** (Treffer pro Plattform + Filter-Statistik)
- **Cross-Platform-Validierung:** Multi-Platform oben, Single-Platform unten
- **Jedes Paper:** Titel, Autor:innen, Jahr, Zitationen, DOI/ISBN, Venue, Concepts, Abstract

## Cross-Platform-Prinzip

**Papers auf mehreren Plattformen** = empirisch validierter Befund. Verschiedene Indizierungsstrategien konvergieren.

**Papers nur auf einer Plattform:**
- Nur OpenAlex → oft interdisziplinär, geisteswissenschaftlich
- Nur Semantic Scholar → CS/AI, neuere Preprints
- Nur CrossRef → frische DOI-Registrierungen
- Nur DNB → deutschsprachige Zeitschriftenartikel, graue Literatur

## IV. Manuelle Schicht — wo das Skript *nicht* hinkommt

### A. KI-basierte Recherche-Assistenten (besser als Keyword-Matching für komplexe Fragen)

| Tool | Besonderheit | Zugang | URL |
|---|---|---|---|
| **Undermind.ai** | Iterative, kontextsensitive KI-Suche — findet semantisch ähnliche Papers, nicht nur Keyword-Treffer | Web-Interface (freemium für Individuen, Enterprise-API für Orgs) | https://www.undermind.ai/ |
| **Elicit** | KI extrahiert direkt Methoden, Findings, Limitations aus Papers; Q&A über Korpus | Freemium, Web | https://elicit.com/ |
| **Consensus** | Konsens-Metriken: „Wie viele Papers stützen diese Aussage?" | Freemium, Web + Browser Extension | https://consensus.app/ |
| **scite.ai** | Classifiziert Zitate: supporting, contrasting, mentioning | Paywall, aber Trial | https://scite.ai/ |
| **Perplexity (Scholar-Mode)** | LLM + Web-Zitationen — für kurze explorative Fragen | Freemium, Web + API | https://perplexity.ai/ |
| **Connected Papers** | Visualisierung eines Paper-Netzwerks (Similar + Prior + Derivative Works) | Freemium, Web | https://www.connectedpapers.com/ |
| **ResearchRabbit** | Paper-Netzwerk-Visualisierung | Kostenlos, Web-App | https://www.researchrabbit.ai/ |

**Wann welches Tool?**
- `paper-discovery.py` → Broad Sweep: Viele Papers zu einem Thema
- **Undermind** → Enge Forschungsfrage, iteriert → nicht Keywords, sondern *Konzept*
- **Elicit/Consensus** → Empirische Fragen: „Welche Studien zeigen X?"
- **Connected Papers/ResearchRabbit** → Rezeptionsnetzwerke einzelner Schlüsselwerke visuell

### B. Deutsche Zeitschriftenarchive (direkter Web-Zugriff)

Siehe [[Deutscher-Diskurs-Quellen]] — vollständige Liste mit 13 Zeitschriften, Stiftungen und Debatten-Plattformen.

### C. Bibliothekskataloge

- **KVK (Karlsruher Virtueller Katalog):** https://kvk.bibliothek.kit.edu — alle deutschen Verbünde
- **WorldCat:** https://www.worldcat.org — international

## Empfehlung: 3-Stufen-Pipeline

1. **Broad Sweep** mit `paper-discovery.py` (Keywords + DNB + OpenAlex) → Überblick
2. **Iterative Vertiefung** mit Undermind oder Elicit (wenn Lücken oder spezifische Fragen) → gezielte Evidenz
3. **Netzwerk-Vertiefung** mit `--doi` Modus + Connected Papers → Rezeptionsnetzwerke

Keine Schicht allein reicht. Aber die Kombination deckt 90%+ des relevanten Diskurses ab.

## Rate Limits

- OpenAlex: entspannt (~10/sec via polite pool)
- Semantic Scholar: **1/sec ohne API-Key** — Script wartet 1.2 sec, Retry mit exp. Backoff bei 429
- CrossRef: entspannt
- DNB: moderat (0.3 sec)

Bei viel Traffic: Semantic Scholar API-Key beantragen (gratis) unter https://www.semanticscholar.org/product/api

## Version History

- **V1** (2026-04): OpenAlex only
- **V2** (2026-04): + Semantic Scholar, CrossRef, Cross-Platform-Dedup
- **V2.1** (2026-04-17): + DNB (deutscher Diskurs)
- **V2.2** (2026-04-17): + Qualitätsfilter (--min-cites, --sort relevance als Default, --exclude-singletons, --peer-reviewed)
