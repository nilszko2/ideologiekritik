# Ideologiekritik — LLM Wiki Schema

## Zweck & Domäne

Dieses Vault ist ein **LLM-gepflegtes Wissens-Wiki** für ideologiekritische Theorie, materialistische Kulturanalyse und linke Intellektualität. Es dient der systematischen Aneignung der Frankfurter Schule, des Marxismus, der Psychoanalyse als Gesellschaftstheorie, der materialistischen Filmanalyse (Schmitt) und der lacanianischen Kulturkritik (Žižek) — als Werkzeugkasten für die kritische Durchdringung von Alltagsideologie, Kulturindustrie und politischer Rhetorik.

**Nutzer:** Koordinator an einer Hochschule für einen Studiengang der Sozialwissenschaften. Theoretisch versiert (MA Organisationstheorie, Adorno/Luhmann-Kenner), sucht systematische Vertiefung der ideologiekritischen Tradition.

**GitHub-Sync:** Dieses Vault ist über `git push/pull` mit dem Obsidian Vault des Nutzers verbunden.
- GitHub Repo: `https://github.com/nilszko2/ideologiekritik.git`
- Lokaler Mirror: `/opt/data/ideologiekritik-github/`
- Nutzers Obsidian Vault: `/opt/data/ideologiekritik-vault/` (lokal, via `cp -r` + `git push` synchronisiert)
- Auto-Push alle 6 Stunden via Cronjob `Ideologiekritik-Vault Auto-Push`
- Abendbriefings schreiben direkt ins GitHub Repo (`00_Inbox/`) und pushen automatisch

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

Wie Kanonwissen: Anti-Stub, Dashboard prüfen, Querverweise, Lücken, Log. Plus: Podcast nach jeder Session neu bauen (siehe Abschnitt „Podcast-Regel" unten).

### Podcast-Regel (verpflichtend, gilt vault-übergreifend einheitlich)

Der Session-Podcast folgt der **Rubriken-Struktur des Exegese-Protokolls V17.0 mit voller analytischer Schärfe**, aber die Rubriken werden **komparativ aneinander angeglichen** gefüllt. Maßstab ist die Präzision einer einzelnen Exegese — mit Originalzitaten, Doppel-Beleg (Kernaussage vereinfacht + Originalzitat + Übersetzung + Quelle mit Seitenangabe), Herkunfts-Markierungen (direkt im Text formuliert vs. rekonstruktiv hergestellt vs. hypothetisch vs. komparative Ergänzung nicht im Quelltext), rhetorischer Tiefenanalyse, Schematischer Verortung, Anwendungs-Toolkit mit Szenario-Analyse-Grenzfall. **Nicht** narrativ zutode geglättet. **Nicht** prosaisch-erzählerisch. Wissenschaftlich dicht.

**Struktur (vierzehn Durchgänge in einer Reihe, nicht Text-Blöcke):**

1. Einleitung — welche Texte/Reden, welche Leitfrage.
2. Komparatives Glossar — dreigeteilt: Fachbegriffe, Neologismen, Stolpersteine.
3. Intention im Vergleich plus rhetorische Eröffnungsgesten.
4. Denkbewegung der Session.
5. Argumentations-Anatomie komparativ — 5–8 Thesen mit Doppel-Beleg + Herkunfts-Markierung.
6. Auffällige Auslassungen mit strategischer Motivation.
7. Grenzfälle komparativ — Theorie + Anwendung.
8. Rhetorische Tiefenanalyse — 2–3 Schlüsselzitate, jeweils mit ideologiekritischer Funktionsanalyse: welchen sozialen Ort nimmt die Rede ein, welche Herrschaftsverhältnisse legitimiert sie, welche Projektions- und Verleugnungsfiguren setzt sie ein.
9. Schematische Verortung — intern + ideengeschichtlich.
10. Aktualitätsbewertung.
11. Anwendungs-Toolkit — integriertes Szenario, Grenzfall, Übersetzungs-Beispiel für ein Kolleg:innen-Gespräch.
12. Weiterführende Ressourcen — 2–3 gezielt.
13. Offene Fragen — 3–6.
14. Empfehlung für die nächste Session.

**Stil:** Reintext, Speechify-tauglich. Rubriken klar angekündigt. Originalzitate explizit ausgesprochen. Herkunfts-Markierungen ausgesprochen.

**Länge:** 45–70 Minuten. **Datei-Ort:** `90_System/convert/podcast-YYYY-MM-DD.txt`.

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
