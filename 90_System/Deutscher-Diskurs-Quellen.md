---
tags: [system, recherche]
typ: system
erstellt: 2026-04-17
---

# Deutsche Diskurs-Quellen — jenseits von OpenAlex

**Kontext:** OpenAlex, Semantic Scholar und CrossRef erfassen den deutschsprachigen kritisch-theoretischen Diskurs systematisch schlecht. Null Treffer zu „Gegenstandpunkt" in OpenAlex vs. 1997 Treffer in der Deutschen Nationalbibliothek illustrieren die Lücke. Diese Datei bündelt die wichtigsten deutschen Quellen — programmatisch und manuell.

---

## I. Programmatisch zugänglich (in `paper-discovery.py` V2.1 integriert)

### DNB — Deutsche Nationalbibliothek (SRU API)

- **API:** https://services.dnb.de/sru/dnb
- **Format:** MARC21-XML (SRU-Protokoll)
- **Abdeckung:** **ALLE deutschen Publikationen** seit Ablieferungspflicht — Bücher, Zeitschriftenartikel, Dissertationen, Graue Literatur, Online-Publikationen
- **Stärke:** Einzige Quelle, die den GSP-Diskurs selbst erfasst (GegenStandpunkt-Verlagstexte)
- **Schwäche:** Keine Zitationsdaten, Abstract nur bei ~10% der Datensätze
- **Query-Syntax:** CQL mit explizitem `and`/`or` zwischen Begriffen; Jahresfilter: `jhr within "2010 2026"`
- **Nutzung im Skript:** `--plattform dnb` oder Standard (alle)

---

## II. Programmatisch zugänglich, aber noch nicht integriert

### SSOAR (GESIS Social Science Open Access Repository)

- **OAI-PMH:** https://www.ssoar.info/OAIHandler/
- **Web-Suche:** https://www.ssoar.info/ssoar/
- **Abdeckung:** 72.000+ OA-Dokumente aus den Sozialwissenschaften, überwiegend deutsch
- **Journals erfasst:** *PROKLA*, *Leviathan*, *Soziale Probleme*, *ZeFKO*, *Berliner Journal für Soziologie*, *Historische Sozialforschung*, *Österreichische Zeitschrift für Soziologie*
- **Integration:** Technisch möglich, aber komplex (OAI-PMH statt REST, Selektion nach Set-Struktur)
- **Empfehlung:** Als Priorität für V2.2

### pedocs (DIPF Education Research Repository)

- **OAI-PMH:** https://www.pedocs.de/oaip2/request.php
- **Abdeckung:** Erziehungswissenschaftliche Open-Access-Publikationen, deutschsprachig
- **Relevant für:** Organisationspädagogik, Bildungssoziologie, kritische Pädagogik

### FID (Fachinformationsdienste)

- **FID Soziologie:** https://sowiport.gesis.org (komplex, aber APIs verfügbar)
- **FID Philosophie:** https://www.fid-philosophie.de
- **FID Politikwissenschaft:** https://www.pollux-fid.de — hat eine [API](https://www.pollux-fid.de/api)!
- **Relevanz:** Fachspezifische Aggregatoren, teils bessere deutsche Coverage als internationale Aggregatoren

### DOAJ (Directory of Open Access Journals)

- **API:** https://doaj.org/api/v3/docs
- **Deutsche Journals erfasst:** *GENDER*, *Politix*, *PROKLA* (teilweise), *Zeitschrift für Theoretische Soziologie*
- **Relevanz:** Für OA-Zeitschriften übergreifend

### Europe PMC / PubMed

- Nur für biomedizinische/sozialmedizinische Fragen relevant
- Für Ideologiekritik irrelevant

---

## III. Nicht programmatisch zugänglich — Web-Recherche erforderlich

### Zeitschriften-Archive (direkt auf Verlagswebsites)

| Zeitschrift | Archiv-URL | Besonderheit |
|---|---|---|
| **PROKLA — Zeitschrift für kritische Sozialwissenschaft** | https://prokla.de | Volltexte ab 1973, frei durchsuchbar |
| **Das Argument** | https://inkrit.de/das-argument/ | Marxistisch-kritisch, Inkrit-Projekt |
| **Mittelweg 36** (HIS Hamburg) | https://www.mittelweg36.de | OA nur ausgewählte Hefte |
| **Merkur — Deutsche Zeitschrift für europäisches Denken** | https://www.merkur-zeitschrift.de | Archiv paywalled, aber guter Index |
| **Leviathan — Berliner Zeitschrift für Sozialwissenschaft** | https://www.nomos-elibrary.de/10.5771/0340-0425 | Teils in SSOAR, teils paywalled |
| **WestEnd — Neue Zeitschrift für Sozialforschung** | https://www.ifs.uni-frankfurt.de/westend | IfS Frankfurt, OA ab 2015 |
| **Polar — Halbjahresschrift** | https://www.polar-halbjahresschrift.de | Bereitgestellt von Bilger-Verlag |
| **Lettre International** | https://lettre.de | Paywalled, aber autoritativ |
| **Blätter für deutsche und internationale Politik** | https://www.blaetter.de | Teilweise frei |
| **Zeitschrift Marxistische Erneuerung** | http://www.zeitschrift-marxistische-erneuerung.de | Marxistisch-kommunistisch |
| **Z. Zeitschrift für Analyse und Kritik** | https://akweb.de | Links-radikal, Wochenzeitung |
| **Jungle World** | https://jungle.world | Antifaschistisch-links |
| **konkret** | https://konkret-magazin.de | Links, Printarchiv teils online |

### Stiftungs-Publikationen (Policy Papers & graue Literatur)

- **Rosa-Luxemburg-Stiftung:** https://www.rosalux.de/publikationen — extensiv, OA, deutsch
- **Friedrich-Ebert-Stiftung:** https://www.fes.de/ipa (International Policy Analysis)
- **Heinrich-Böll-Stiftung:** https://www.boell.de/de/publikationen
- **Konrad-Adenauer-Stiftung** (für konservatives Gegenmaterial): https://www.kas.de/publikationen
- **Hans-Böckler-Stiftung (WSI, IMK):** https://www.boeckler.de/de/wsi-mitteilungen-10940.htm

### Spezifische Linke Debatten-Plattformen

| Plattform | URL | Inhalt |
|---|---|---|
| **kritisch-lesen.de** | https://kritisch-lesen.de | Rezensionen linker Literatur |
| **contradictio.de** | https://www.contradictio.de/blog | GSP-nahe Diskussion + Kritik |
| **neoprene.blogsport.de (Walgesang)** | http://neoprene.blogsport.de | Langjähriger GSP-kritischer Blog |
| **kommunistische-organisation.de** | https://kommunistische-organisation.de | KO — Spanidis & Co. |
| **kommunistischepartei.de** | https://kommunistischepartei.de | Marxistisch-leninistisch |
| **Scharf Links** | https://www.scharf-links.de | Linke Theorie |
| **Untergrund-Blättle** | https://www.untergrund-blättle.ch | Sammelbecken linker Texte |
| **Infopartisan — trend onlinezeitung** | https://infopartisan.net/trend | Operaistisch-autonom |

### GegenStandpunkt selbst

- https://de.gegenstandpunkt.com — vollständiges Archiv aller Zeitschriftenhefte frei zugänglich
- **YouTube:** https://www.youtube.com/@DerGegenStandpunkt (offiziell)
- **Peter Decker Vorträge:** https://www.youtube.com/@PeterDeckerStgt
- **Schulungsmaterialien:** contradictio.de, teachingthenews.de

---

## IV. Spezielle Recherche-Techniken für deutsche Theorie

### 1. Google Scholar Operators (manuell)

Google Scholar indexiert deutsche Fachzeitschriften besser als die englischsprachigen APIs. Aber: kein API.

Manuelle Strategie: `site:prokla.de GegenStandpunkt` oder `"GegenStandpunkt" site:.de -site:gegenstandpunkt.com`

### 2. OAI-PMH-Aggregatoren

- **Europeana:** https://www.europeana.eu (kulturelles Erbe, inklusive Zeitschriftenscans)
- **BASE** (Bielefeld): IP-whitelist-gesperrt für API-Zugriff, aber Web-Suche ohne Auth

### 3. Bibliothekskataloge direkt

- **KVK (Karlsruher Virtueller Katalog):** https://kvk.bibliothek.kit.edu — aggregiert alle deutschen Bibliotheksverbünde
- **WorldCat:** https://www.worldcat.org — international, mit Fokus auf Buchbestände

### 4. Zitationssuche der Sekundärquellen

Wenn das Debattenpapier V13 sich auf **Kapfinger 2011**, **Spanidis 2018**, **Creydt 2015** stützt, lohnt eine Suche nach Texten, die *diese* zitieren — auch wenn OpenAlex sie nicht kennt. Das geht über Google Scholar (Backward-Search manuell) oder über die Zitationsfußnoten in den PDFs selbst.

Alle drei PDFs sind unter `07_Anhang/GSP-Sekundärliteratur/` im Vault gesichert.

---

## V. Empfohlene Folge-Recherchen

Für die GSP-Debatte speziell:

```bash
# Mit integriertem Tool:
python "90_System/Tools/paper-discovery.py" --thema "Gegenstandpunkt Kritik" --jahre 25 --top 20
python "90_System/Tools/paper-discovery.py" --thema "Marxistische Gruppe Kritik" --jahre 30 --top 15
python "90_System/Tools/paper-discovery.py" --thema "Kapitalismus Analyse Rationalität Marxismus" --jahre 10 --top 15
```

Manuell (weil nicht in API):

1. **GSP-Archiv durchsuchen:** https://de.gegenstandpunkt.com/archiv — z.B. alle Hefte zu „Staat"
2. **Spanidis-Text (2018) im PDF:** `07_Anhang/GSP-Sekundärliteratur/Spanidis_2018_Standpunkt_gegen_Marxismus.pdf` — Literaturverzeichnis durchgehen
3. **Contradictio-Foren:** Diskussionen zwischen GSP-Vertretern und Kritikern
4. **Kommunistische Organisation (KO):** Vollständige Veröffentlichungsreihe

Für den erweiterten Ideologiekritik-Vault:

```bash
python "90_System/Tools/paper-discovery.py" --thema "Kulturindustrie Adorno Rezeption" --jahre 10
python "90_System/Tools/paper-discovery.py" --thema "Unverfügbarkeit Rosa Beschleunigung" --jahre 5
python "90_System/Tools/paper-discovery.py" --thema "Anerkennung Honneth Kritik" --jahre 10
```

---

## VI. Methodische Reflexion

Die Recherche-Pipeline für deutschsprachige kritische Theorie braucht drei Schichten:

1. **Programmatisch** (automatisiert): OpenAlex + Semantic Scholar + CrossRef + DNB → 80% der publizierten wissenschaftlichen Literatur
2. **Semi-programmatisch** (Web-Fetch einzelner Archive): PROKLA, Argument, RLS, Mittelweg 36
3. **Manuell** (gezielte Volltextsuche): GSP-Archiv, contradictio, Spezial-Blogs

Keine der drei Schichten ist entbehrlich. Wer nur Schicht 1 nutzt, reproduziert den *publication bias* in englischsprachige, indizierte Mainstream-Literatur. Wer nur Schicht 3 nutzt, verliert die systematische Vergleichsbasis.

**Praktische Empfehlung:** Beginne mit `paper-discovery.py --thema "..." --plattform dnb,openalex`. Wenn DNB Treffer liefert, die OpenAlex nicht kennt → Anzeichen, dass das Thema deutsch dominiert ist; dann manuell in PROKLA/Argument/Mittelweg nachsehen.
