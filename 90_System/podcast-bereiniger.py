"""
Podcast-Bereiniger: Entfernt Markdown-Formatierung für Speechify.

Verwendung:
    python podcast-bereiniger.py input.md output.txt

Oder: Inhalt per Clipboard einfügen:
    python podcast-bereiniger.py --clipboard

Was entfernt wird:
- Sterne (fett/kursiv): **text** → text, *text* → text
- Rauten (Überschriften): ## Text → Text
- Wikilinks: [[Konzept - Name]] → Konzept - Name
- Literatur-Links: [[@Autor_Jahr|Anzeige]] → Anzeige
- Callout-Marker: > [!quote], > [!info] etc. → (entfernt)
- Blockquote-Zeichen: > am Zeilenanfang → (entfernt)
- Frontmatter (YAML): --- ... --- Block → (entfernt)
- Horizontale Linien: --- → (entfernt)
- Backticks: `code` → code
- Pipe-Tabellen → (entfernt, da nicht vorlesbar)
- Aufzählungszeichen: - Text → Text
- Nummerierte Listen: 1. Text → Text
- Checkboxen: - [x] Text → Text, - [ ] Text → Text

Was NICHT entfernt wird:
- Der eigentliche Text
- Zitate in Anführungszeichen
- Zahlen und Jahreszahlen
- Klammern mit Quellenangaben
"""

import re
import sys

def bereinige_podcast(text):
    # Frontmatter entfernen (YAML-Block)
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)

    # Callout-Marker entfernen: > [!quote], > [!info] etc.
    text = re.sub(r'>\s*\[!(quote|info|tip|warning|question|abstract|example|success|failure)\][-+]?\s*.*\n', '', text)

    # Blockquote-Zeichen entfernen
    text = re.sub(r'^>\s?', '', text, flags=re.MULTILINE)

    # Wikilinks mit Anzeigetext: [[Link|Anzeige]] → Anzeige
    text = re.sub(r'\[\[([^\]]*?\|)?([^\]]+?)\]\]', r'\2', text)

    # Literatur-Links: [[@Autor|Anzeige]] → Anzeige (falls nicht schon gefangen)
    text = re.sub(r'\[\[@[^\]]*?\|([^\]]+?)\]\]', r'\1', text)
    text = re.sub(r'\[\[@([^\]]+?)\]\]', r'\1', text)

    # Markdown-Links: [Text](URL) → Text
    text = re.sub(r'\[([^\]]+?)\]\([^\)]+?\)', r'\1', text)

    # Überschriften: ## Text → Text (mit Leerzeile davor für Pause)
    text = re.sub(r'^#{1,6}\s+', '\n', text, flags=re.MULTILINE)

    # Fett+Kursiv: ***text*** → text
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)

    # Fett: **text** → text
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)

    # Kursiv: *text* → text
    text = re.sub(r'\*(.+?)\*', r'\1', text)

    # Backticks: `code` → code
    text = re.sub(r'`([^`]+?)`', r'\1', text)

    # Code-Blöcke: ```...``` → (entfernen)
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)

    # Pipe-Tabellen entfernen (Zeilen die mit | beginnen)
    text = re.sub(r'^\|.*\|$', '', text, flags=re.MULTILINE)

    # Horizontale Linien
    text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)

    # Checkboxen
    text = re.sub(r'^-\s*\[[ x]\]\s*', '', text, flags=re.MULTILINE)

    # Aufzählungszeichen: - Text → Text
    text = re.sub(r'^-\s+', '', text, flags=re.MULTILINE)

    # Nummerierte Listen: 1. Text → Text
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)

    # Mehrfache Leerzeilen reduzieren
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Führende/trailing Whitespace pro Zeile
    text = '\n'.join(line.strip() for line in text.split('\n'))

    # Führende Leerzeilen entfernen
    text = text.strip()

    return text


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--clipboard':
        try:
            import pyperclip
            text = pyperclip.paste()
            result = bereinige_podcast(text)
            pyperclip.copy(result)
            print(f"Bereinigt: {len(text)} → {len(result)} Zeichen. Ergebnis in Zwischenablage.")
        except ImportError:
            print("pyperclip nicht installiert. Nutze: pip install pyperclip")

    elif len(sys.argv) == 3:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        result = bereinige_podcast(text)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Bereinigt: {input_file} → {output_file} ({len(text)} → {len(result)} Zeichen)")

    elif len(sys.argv) == 2:
        input_file = sys.argv[1]
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        result = bereinige_podcast(text)
        print(result)

    else:
        print("Verwendung:")
        print("  python podcast-bereiniger.py input.md              → Ausgabe auf Konsole")
        print("  python podcast-bereiniger.py input.md output.txt   → Ausgabe in Datei")
        print("  python podcast-bereiniger.py --clipboard           → Zwischenablage bereinigen")
