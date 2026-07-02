---
tags: [system, landkarte, protokoll]
typ: system
aktualisiert: 2026-05-14
standard-protokoll: "V17.0 / Konsolidierte Marker-Systematik"
vault-spezifisches-spezialprotokoll: "ideologiekritik + methodenlehrbuch + em-fallstudie"
aktualisiert: 2026-04-16
standard-protokoll: "V17.0"
vault-spezifisches-spezialprotokoll: "methodenlehrbuch + em-fallstudie"
---

# Exegese-Landkarte

**Wegweiser durch die verfügbaren Exegese-Protokolle dieses Vaults.**

Seit dem **2026-05-14** gilt eine **konsolidierte Protokollarchitektur**: Eine kanonische generische Fassung (V17.0 / Konsolidierte Marker-Systematik) plus drei feldspezifische Spezialprotokolle. Die früheren Fassungen (V16.2 sowie das integrierte V17.0 mit drei Varianten A/B/C) sind archiviert.
Der Vault hat zwei Generationen von Protokollen:
- **V16.2** (bewährt, bis 2026-04-16 Standard) — bleibt *parallel verfügbar* als Testumgebung, bis V17.0 genügend Exegesen durchlaufen hat.
- **V17.0** (neuer Standard seit 2026-04-16) — integriert V16.2 und Close Reading; drei Varianten (A/B/C) + Spezialprotokolle.

## Welches Protokoll wählen?

### 1. Um welche Art von Text geht es?

```
Text-Typ                           → Empfohlenes Protokoll
────────────────────────────────────────────────────────
Politische Rede, Tweet, Leit-      → ideologiekritik (Spezial)
artikel, Diskurs mit ideolog.        ** Haupt-Protokoll in diesem Vault **
Gehalt
────────────────────────────────────────────────────────
Wissenschaftliche Analyse von      → V17.0 (generisch)
Ideologie (z.B. Barthes,
Wissenschaftliche Analyse von      → V17.0-B (monolithisch)
Ideologie (z.B. Barthes,             mit Situierung + Aktualität
Althusser, Butler über Gender)
────────────────────────────────────────────────────────
Methodologisches Lehrbuch          → methodenlehrbuch (Spezial)
(selten in diesem Vault)
────────────────────────────────────────────────────────
Ethnomethodologische Fallstudie    → em-fallstudie (Spezial)
(selten in diesem Vault)
────────────────────────────────────────────────────────
Buch mit klarer Kapitelstruktur    → V17.0 (generisch, iterativ)
(keine obigen Spezialtypen)
────────────────────────────────────────────────────────
Einzeltext, Aufsatz, Artikel,      → V17.0 (generisch, ggf. mit
dichter Essay                        Lastregel-Anpassung)
────────────────────────────────────────────────────────
Sammelband, Handbuch, Reader       → V17.0 (generisch, ggf. mit
                                     Dreierblöcken bei kurzen
                                     Beiträgen)
────────────────────────────────────────────────────────
Buch mit klarer Kapitelstruktur    → V17.0 Variante A (iterativ)
(keine obigen Spezialtypen)
────────────────────────────────────────────────────────
Einzeltext, Aufsatz, Artikel,      → V17.0 Variante B
dichter Essay                        (monolithisch)
────────────────────────────────────────────────────────
Sammelband, Handbuch, Reader       → V17.0 Variante C (Überblick)
────────────────────────────────────────────────────────
Testphase / Vergleich mit neuem    → V16.2 (alt, iterativ, rein)
Verfahren                            
```

### 2. Nach welchem Track exegieren?

- **Quali-Track:** methodologische Exegesen für den Weiterbildungskurs. Paper-Bezüge vermeiden / klar abgegrenzt.
- **Paper-Track:** Exegesen für das Paper-Projekt. Methodik-Bezüge erlaubt, aber klar abgegrenzt.
- **Gemeinsam:** Exegesen, die beiden Tracks dienen (selten).

## Verfügbare Protokolle

### V17.0 (Konsolidierte Marker-Systematik) — generisches Haupt-Toolkit

→ [[exegese-toolkit]]

**Kernarchitektur:**
- Eine kanonische **Marker-Tafel** mit vier Konfidenz-Markern (`[direkt]` / `[rekonstruiert]` / `[interpretativ]` / `[komparativ]`) und fünf Spezialfall-Markern (`[ENTFÄLLT]`, `[HYPOTHETISCH]`, `[MATERIAL FEHLT]`, `[ZITAT NICHT VERIFIZIERT]`, `[SPANNUNGSFORMEL STATT ANALOGIE]`).
- **Belegpflicht differenziert nach Marker** — nicht jede Aussage braucht ein Originalzitat; pauschale Zitatpflicht produzierte fabrizierte Zitate.
- **Block-Granularität**: Standard zwei Kapitel pro Antwort, Lastregel für Ausreißer (sehr lange Einzelkapitel → allein; sehr kurze → Dreierblöcke).
- **Glossar mit vier Kategorien**: Fachbegriffe, Neologismen, falsche Freunde, **Begriffsdrift**.
- **Meta-Reflexion verpflichtend** am Block-Ende.

**Anpassung statt Varianten:** Die früheren Varianten A/B/C wurden zugunsten einer einzigen Architektur mit expliziter Lastregel aufgegeben. Texttyp-Spezifika werden durch Block-Granularität und Materialprüfung geregelt, nicht durch parallele Verfahrensvarianten.
### V17.0 Haupt-Toolkit

→ [[exegese-toolkit-v17]]

**Drei Varianten** in einer Datei:
- A: Iterativ (Bücher, 2 Kapitel pro Block)
- B: Monolithisch (Einzeltexte, eine Antwort)
- C: Überblick (Sammelbände, reduzierte Tiefe)

**Verpflichtende Direktiven** für alle Varianten:
- Anti-Illusions, Anti-Fabrikations, Anti-Redundanz (von V16.2)
- Hermeneutische Charity (von Close Reading)
- Kontextualisierung, Hypothetik
- **Aktualitätsbewertung** (neu, verpflichtend)

### Spezialprotokolle

→ **[[exegese-protokoll-ideologiekritik]] — vault-spezifisches Hauptprotokoll.** Für politische Reden, populistische Diskurse, Leitartikel, Verschwörungsnarrative, mediale Framings. **Strukturierter Verdacht statt hermeneutischer Charity.** Vier Aussagentypen (Tatsachen / cherry picking / Framings / Werte), Strukturanalyse, Innere Widersprüche, Soziale Funktion, rhetorische Manipulationsfiguren, strukturell-psychoanalytische Kategorien, Entkräftungsstrategien.

→ [[exegese-protokoll-methodenlehrbuch]] — für didaktisch strukturierte Methoden-Einführungen. In diesem Vault selten primär relevant (außer bei Methoden der Diskursanalyse).

→ [[exegese-protokoll-em-fallstudie]] — für ethnomethodologische Fallstudien. In diesem Vault selten primär relevant.

### Archivierte Vorgänger

→ [[exegese-toolkit-v16.2-DEPRECATED]] — V16.2 (iteratives Analyse-Toolkit mit Doppel-Beleg). Verlangte pauschale Zitatpflicht; produzierte unter Last fabrizierte Zitate. Archiviert 2026-05-14.

→ [[exegese-toolkit-v17-integriert-DEPRECATED]] — V17.0 *integriert* (Verschmelzung V16.2 + Close Reading mit drei Varianten A/B/C). Die A/B/C-Variantenstruktur erwies sich als überdesigned; in der Praxis lief alles auf eine iterative Grundform mit Anpassungen hinaus. Archiviert 2026-05-14 zugunsten der schlankeren Marker-Systematik.

## Empfohlene Anwendung

### Für neue Exegesen

Verwende V17.0 oder das passende Spezialprotokoll. Trage im Frontmatter ein:

```yaml
verfahren: v17.0
# oder: v17.0-spezial-ideologiekritik
# oder: v17.0-spezial-methodenlehrbuch
# oder: v17.0-spezial-em-fallstudie
### Archivprotokoll (parallel verfügbar)

→ [[exegese-toolkit]] — V16.2 (iteratives Analyse-Toolkit mit Doppel-Beleg). Unverändert gelassen, bleibt für Test-/Vergleichsexegesen nutzbar. *Hat keine Aktualitätsbewertung.*

## Empfohlene Anwendung

### Für neue Exegesen (Regel)

Verwende V17.0 oder das passende Spezialprotokoll. Trage im Frontmatter ein:
```yaml
verfahren: v17.0-B
# oder: v17.0-A
# oder: v17.0-C
# oder: v17.0-spezial-methodenlehrbuch
# oder: v17.0-spezial-em-fallstudie
# oder: v16.2  (nur wenn bewusste Testphase)
```

### Für bestehende Exegesen (Rückwärts-Kompatibilität)

- Die bestehenden V16.2-Exegesen (Flick 1–4) und die Close-Reading-Exegesen (W/Z 1987, Garfinkel 1967, Garfinkel 1986) bleiben gültig.
- Exegesen, die mit dem integrierten V17.0 (Varianten A/B/C) erstellt wurden, bleiben gültig. Ihre Markersystematik ist mit der konsolidierten Fassung kompatibel (die Marker `[direkt]`, `[rekonstruiert]`, `[interpretativ]`, `[komparativ]` bleiben identisch).

### Neue Verfahrensregeln (seit 2026-05-14)

- **Marker-Pflicht** in den Feldern 2.4, 2.5, 2.6: Jede Analyse-Aussage erhält einen Konfidenz-Marker.
- **Anti-Fabrikations-Direktive durch Marker statt Direktiven-Block**: Der frühere Block „Anti-Illusions-Direktive" ist in die Marker-Tafel überführt — sie ist *die* Anti-Illusions-Logik.
Die bestehenden V16.2-Exegesen (Flick 1–4) und die Close-Reading-Exegesen (W/Z 1987, Garfinkel 1967, Garfinkel 1986) bleiben gültig. Nachträgliche Aktualitätsbewertungen wurden ergänzt.

### Für die Testphase V16.2 ↔ V17.0

Solange V17.0 noch nicht ausreichend erprobt ist:
1. Nutze V17.0 für *neue* Exegesen
2. Falls Probleme auftreten: dokumentiere sie in `90_System/log.md` mit Präfix `protokoll-fehler`
3. Im Zweifel: V16.2 als Rückfallebene verfügbar
4. Nach ca. 10 V17.0-Exegesen: Evaluation, ob V16.2 endgültig archiviert werden kann

## Neue Verfahrensregeln (seit 2026-04-16)

- **AKTUALITÄTS-DIREKTIVE** ist verpflichtend. Drei Fragen: (1) Was gilt heute noch? (2) Was ist überholt/revidiert? (3) Wie heute zu lesen?
- **Spezialprotokolle bei passenden Texttypen**: Nicht jeder Text bekommt das generische V17.0 — wenn eine Spezialisierung existiert, wird sie benutzt.
- **Track-Kennzeichnung** im Frontmatter: `track: quali / paper / gemeinsam`.
- **Dateinamen-Konvention**: `Exegese - [Werk] - Block [N].md` für Podcast-Integration.

## Querverweise

- [[exegese-toolkit]] — Generisches Haupt-Toolkit (V17.0 / Konsolidierte Marker-Systematik)
- [[exegese-protokoll-ideologiekritik]]
- [[exegese-protokoll-em-fallstudie]]
- [[exegese-protokoll-methodenlehrbuch]]
- [[exegese-toolkit-v16.2-DEPRECATED]] — Archiv
- [[exegese-toolkit-v17-integriert-DEPRECATED]] — Archiv
- [[exegese-toolkit-v17]] — Haupttoolkit
- [[exegese-protokoll-em-fallstudie]]
- [[exegese-protokoll-methodenlehrbuch]]
- [[exegese-toolkit]] — V16.2 (Archiv)
- [[Dashboard - Exegese-Fortschritt]]
