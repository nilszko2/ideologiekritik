---
tags: [system]
typ: system
---

# Podcast-Tools

Zwei Python-Skripte für die Konvertierung von Exegesen in Speechify-taugliche Texte.

## 1. Exegese-zu-Podcast-Konverter (Haupttool)

Sammelt alle Exegese-Blöcke eines Tages, bereinigt Markdown und erzeugt einen zusammenhängenden Podcast-Text.

Terminal-Befehle:

Alle Exegesen eines bestimmten Tages:
python "90_System/exegese-zu-podcast.py" 2026-04-12

Alle Exegesen insgesamt:
python "90_System/exegese-zu-podcast.py" --all

Heutiges Datum automatisch:
python "90_System/exegese-zu-podcast.py"

Ausgabe: 90_System/convert/podcast-DATUM.txt

Was es tut:
- Sammelt alle Exegese-Blöcke aus 04_Projekte/
- Filtert nach Datum (aus dem Frontmatter-Feld datum)
- Kopiert die Originale als .md in 90_System/convert/
- Bereinigt Markdown-Formatierung (Sterne, Rauten, Wikilinks, Callouts, Tabellen)
- Erzeugt einen zusammenhängenden Reintext als .txt
- Die .txt-Datei direkt in Speechify öffnen

## 2. Einzeltext-Bereiniger

Bereinigt eine einzelne Markdown-Datei.

Terminal-Befehle:

Ausgabe auf Konsole:
python "90_System/podcast-bereiniger.py" datei.md

Ausgabe in Datei:
python "90_System/podcast-bereiniger.py" datei.md ausgabe.txt

Zwischenablage bereinigen (braucht pip install pyperclip):
python "90_System/podcast-bereiniger.py" --clipboard

## Hinweis

Beide Skripte sind .py-Dateien und daher in Obsidian nicht sichtbar. Zugriff über Terminal oder Windows Explorer: 90_System/exegese-zu-podcast.py und 90_System/podcast-bereiniger.py
