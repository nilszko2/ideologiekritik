# Ideologiekritik — LLM Wiki Schema

## Zweck & Domäne

Dieses Vault ist ein **LLM-gepflegtes Wissens-Wiki** für ideologiekritische Theorie, materialistische Kulturanalyse und linke Intellektualität. Es dient der systematischen Aneignung der Frankfurter Schule, des Marxismus, der Psychoanalyse als Gesellschaftstheorie, der materialistischen Filmanalyse (Schmitt) und der lacanianischen Kulturkritik (Žižek) — als Werkzeugkasten für die kritische Durchdringung von Alltagsideologie, Kulturindustrie und politischer Rhetorik.

**Nutzer:** Koordinator an einer Hochschule für einen Studiengang der Sozialwissenschaften. Theoretisch versiert (MA Organisationstheorie, Adorno/Luhmann-Kenner), sucht systematische Vertiefung der ideologiekritischen Tradition.

**Sechs Felder:**
- **Frankfurter Schule** (Horkheimer, Adorno, Marcuse, Benjamin, Habermas, Negt/Kluge)
- **Klassischer Marxismus** (Marx, Engels, Luxemburg, Gramsci, Lukács)
- **Psychoanalyse als Gesellschaftstheorie & Kritische Psychologie** (Freud, Lacan, Žižek, Fromm, Lorenzer; Holzkamp, Markard, Osterkamp)
- **Materialistische Kulturanalyse** (Benjamin, Kracauer, Schmitt [W.M.], Eagleton, Jameson)
- **Zeitgenössische Kritische Theorie** (Žižek, Fisher, Badiou, Rancière, Butler, Fraser, Jaeggi)
- **Politische Ökonomie** (Marx, Harvey, Piketty, Streeck, Dörre)

**Sprache:** Deutsch. Englische Fachbegriffe werden beibehalten, wenn sie im Feld etabliert sind.

**Verhältnis zu anderen Vaults:**
- **Kanonwissen** enthält Organisationstheorie (Luhmann, Weber) — Ideologiekritik enthält die *kritische Gegenposition* (Adorno gegen Luhmann, Marx gegen Weber)
- **Kompetenzvault** enthält angewandtes Methodenwissen — Ideologiekritik enthält die *theoretische Reflexion* über Methoden (Positivismuskritik, Werturteilsstreit)

---

## Ordner-Architektur

```
Ideologiekritik/
├── 00_Inbox/          ← Eingang
├── 01_Zettel/         ← Atomare permanente Notizen
├── 02_Literatur/      ← Eine Notiz pro Quelle
├── 03_MOCs/           ← Maps of Content
├── 04_Projekte/       ← Analysen, Essays, Filmkritiken
├── 05_Vorlagen/       ← Templates
├── 06_Archiv/         ← Abgeschlossenes
├── 07_Anhang/         ← PDFs, Filme, Dateien
│   └── Lesepläne/
└── 90_System/
    ├── Dashboards/
    ├── log.md
    └── exegese-toolkit.md
```

---

## Namenskonventionen

| Notiztyp | Dateiname | Ordner |
|----------|-----------|--------|
| Konzept | `Konzept - [Name].md` | `01_Zettel/` |
| Person | `Person - [Nachname, Vorname].md` | `01_Zettel/` |
| Theorie | `Theorie - [Name].md` | `01_Zettel/` |
| Film/Werk | `Werk - [Titel (Jahr)].md` | `01_Zettel/` |
| Filmanalyse | `Analyse - [Filmtitel (Jahr)].md` | `01_Zettel/` |
| Permanenter Zettel | `[Sprechender Titel].md` | `01_Zettel/` |
| Literaturnotiz | `@Nachname_Jahr_Kurztitel.md` | `02_Literatur/` |
| Map of Content | `MOC - [Thema].md` | `03_MOCs/` |
| Projekt | `Projekt - [Titel].md` | `04_Projekte/` |

---

## Tag-Hierarchie

| Kategorie | Tags | Zweck |
|-----------|------|-------|
| Status | `#status/entwurf` · `#status/reif` · `#status/überarbeiten` | Verarbeitungsgrad |
| Typ | `#typ/konzept` · `#typ/person` · `#typ/theorie` · `#typ/film` · `#typ/analyse` | Notizklassifikation |
| Quelle | `#quelle/primär` · `#quelle/sekundär` · `#quelle/grau` · `#quelle/film` · `#quelle/podcast` | Evidenzgrad |
| Thema | `#thema/[freitext]` | Inhaltliche Zuordnung |
| Feld | `#feld/frankfurter-schule` · `#feld/marxismus` · `#feld/psychoanalyse` · `#feld/kulturanalyse` · `#feld/zeitgenoessisch` · `#feld/politische-oekonomie` | Theorietradition |
| Register | `#register/film` · `#register/literatur` · `#register/musik` · `#register/politik` · `#register/alltag` | Gegenstandsbereich der Analyse |

---

## Zitationsformat (APA 7)

Identisch mit Kanonwissen-Vault. Alle Zitate mit Seitenzahl. Englische Zitate immer mit deutscher Übersetzung.

---

## Callout-Typen

| Callout | Verwendung |
|---------|------------|
| `[!quote]` | Direktzitate |
| `[!abstract]` | Kernthese |
| `[!info]` | Definitionen, Kontext |
| `[!tip]` | Anwendung: Wie lässt sich dieses Konzept auf aktuelle Phänomene anwenden? |
| `[!question]` | Offene Fragen, Widersprüche |
| `[!warning]` | Gegenargumente, Einschränkungen, blinde Flecken |
| `[!example]` | Filmbeispiele, Fallvignetten, Alltagsideologie |
| `[!success]` | Analytischer Gewinn: Was sieht man mit diesem Konzept, was man vorher nicht sah? |
| `[!failure]` | Gescheiterte Analysen, Sackgassen, Aporien |

---

## Spezial-Workflow: Filmanalyse (nach W.M. Schmitt)

Für die materialistische Filmanalyse im Stil von Wolfgang M. Schmitts *Die Filmanalyse*:

1. **Oberflächenbeschreibung:** Was zeigt der Film? Plot, Figuren, Setting — *deskriptiv, ohne Wertung*
2. **Formanalyse:** Wie zeigt er es? Kamera, Schnitt, Licht, Ton, Musik — *die Form als Inhalt*
3. **Ideologische Lektüre:** Was sagt der Film, *ohne es zu sagen?* Welche gesellschaftlichen Widersprüche verhandelt er? Welche Ideologie reproduziert oder subvertiert er?
4. **Symptomale Lektüre (Žižek/Althusser):** Was kann der Film *nicht* sagen? Welche Leerstellen, Brüche, Inkonsistenzen verraten die ideologische Struktur?
5. **Politische Ökonomie des Films:** Produktionsbedingungen, Markt, Zielgruppe — der Film als Ware
6. **Verbindungsarchitektur:** Querverweise zu anderen Filmen, zu theoretischen Konzepten, zu aktuellen politischen Phänomenen

Jede Filmanalyse wird als `Analyse - [Titel (Jahr)].md` in `01_Zettel/` abgelegt und mit den relevanten Konzepten verlinkt.

---

## Workflows

### 1. Aufnehmen (Ingest)

Wie Kanonwissen: Quelle → Literaturnotiz → Zettel → MOCs → Log.

### 2. Analysieren (Exegese)

Exegese-Toolkit V16.2 anwenden. Pro Antwort 2 Kapitel. Alle Behauptungen mit Seitenzahl.

### 3. Filmanalyse

Spezial-Workflow (s.o.). Ein Film = ein Analyse-Zettel + extrahierte Konzept-Zettel.

### 4. Pflegen (Lint)

Wie Kanonwissen: Anti-Stub, Dashboard prüfen, Querverweise, Lücken, Log.

---

## Anti-Stub-Mechanismus

Identisch mit Kanonwissen.

---

## Qualitäts-Checkliste (jede Notiz)

- [ ] YAML-Frontmatter vollständig
- [ ] Mindestens ein `[!quote]`-Callout mit Seitenzahl
- [ ] Hauptaussage in eigenen Worten
- [ ] Mindestens zwei ausgehende Wikilinks
- [ ] `[!tip]` oder `[!example]` — Anwendung auf konkretes Phänomen
- [ ] Keine KI-Artefakte

---

## Log-Format

Datei: `90_System/log.md`
Präfixe: `setup`, `ingest`, `exegese`, `analyse`, `query`, `lint`, `update`
