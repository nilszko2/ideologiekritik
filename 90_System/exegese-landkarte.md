---
tags: [system, landkarte, protokoll]
typ: system
aktualisiert: 2026-04-16
standard-protokoll: "V17.0"
vault-spezifisches-spezialprotokoll: "methodenlehrbuch + em-fallstudie"
---

# Exegese-Landkarte

**Wegweiser durch die verfügbaren Exegese-Protokolle dieses Vaults.**

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

- [[exegese-toolkit-v17]] — Haupttoolkit
- [[exegese-protokoll-em-fallstudie]]
- [[exegese-protokoll-methodenlehrbuch]]
- [[exegese-toolkit]] — V16.2 (Archiv)
- [[Dashboard - Exegese-Fortschritt]]
