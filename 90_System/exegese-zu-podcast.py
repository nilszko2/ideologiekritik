"""
Exegese-zu-Podcast-Konverter

Sammelt alle Exegese-Blöcke eines Tages, bereinigt Markdown-Formatierung
und erzeugt einen zusammenhängenden Podcast-Text für Speechify.

Verwendung:
    python exegese-zu-podcast.py                    → heutiges Datum
    python exegese-zu-podcast.py 2026-04-12         → bestimmtes Datum
    python exegese-zu-podcast.py --all              → alle Exegese-Blöcke

Ausgabe:
    90_System/convert/podcast-YYYY-MM-DD.txt

Was passiert:
    1. Alle Exegese-Blöcke aus 04_Projekte/ werden gesammelt
    2. Nach Datum gefiltert (aus dem Frontmatter-Feld 'datum')
    3. Markdown-Formatierung wird entfernt
    4. Die Blöcke werden zu einem zusammenhängenden Text verbunden
    5. Ausgabe als reiner Text ohne Markdown
"""

import os
import re
import sys
import glob
from datetime import date


# === Konfiguration ===

VAULT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJEKTE_DIR = os.path.join(VAULT_ROOT, "04_Projekte")
CONVERT_DIR = os.path.join(VAULT_ROOT, "90_System", "convert")


# === Markdown-Bereinigung ===

def bereinige_markdown(text):
    """Entfernt alle Markdown-Formatierung für Speechify."""

    # Frontmatter entfernen
    text = re.sub(r'^---\n.*?\n---\n', '', text, flags=re.DOTALL)

    # Callout-Marker entfernen
    text = re.sub(
        r'>\s*\[!(quote|info|tip|warning|question|abstract|example|success|failure)\][-+]?\s*.*\n',
        '\n', text
    )

    # Blockquote-Zeichen entfernen
    text = re.sub(r'^>\s?', '', text, flags=re.MULTILINE)

    # Wikilinks: [[Link|Anzeige]] → Anzeige
    text = re.sub(r'\[\[([^\]]*?\|)([^\]]+?)\]\]', r'\2', text)
    # Wikilinks ohne Anzeige: [[Link]] → Link
    text = re.sub(r'\[\[([^\]]+?)\]\]', r'\1', text)

    # Markdown-Links: [Text](URL) → Text
    text = re.sub(r'\[([^\]]+?)\]\([^\)]+?\)', r'\1', text)

    # Überschriften: ## Text → Text (mit Leerzeile)
    text = re.sub(r'^#{1,6}\s+(.+)$', r'\n\1\n', text, flags=re.MULTILINE)

    # Fett+Kursiv: ***text*** → text
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\1', text)
    # Fett: **text** → text
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    # Kursiv: *text* → text
    text = re.sub(r'(?<!\w)\*([^\*\n]+?)\*(?!\w)', r'\1', text)

    # Backticks
    text = re.sub(r'`([^`]+?)`', r'\1', text)
    # Code-Blöcke
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)

    # Pipe-Tabellen → in lesbaren Text umwandeln
    lines = text.split('\n')
    cleaned_lines = []
    in_table = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            # Separator-Zeile (|---|---|) überspringen
            if re.match(r'^\|[\s\-:]+\|$', stripped):
                continue
            # Tabellen-Inhalt: Pipes durch Kommas ersetzen
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if cells and any(c for c in cells):
                cleaned_lines.append(', '.join(c for c in cells if c))
            in_table = True
        else:
            if in_table and stripped == '':
                in_table = False
            cleaned_lines.append(line)
    text = '\n'.join(cleaned_lines)

    # Horizontale Linien
    text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)

    # Checkboxen
    text = re.sub(r'^-\s*\[[ x]\]\s*', '', text, flags=re.MULTILINE)

    # Aufzählungszeichen
    text = re.sub(r'^-\s+', '', text, flags=re.MULTILINE)

    # Nummerierte Listen: 1. Text → Text
    text = re.sub(r'^\d+\.\s+', '', text, flags=re.MULTILINE)

    # Mehrfache Leerzeilen → maximal zwei
    text = re.sub(r'\n{3,}', '\n\n', text)

    # Führende/trailing Whitespace
    text = '\n'.join(line.strip() for line in text.split('\n'))
    text = text.strip()

    return text


# === Datum aus Frontmatter extrahieren ===

def extrahiere_datum(content):
    """Liest das datum-Feld aus dem YAML-Frontmatter."""
    match = re.search(r'^datum:\s*(\d{4}-\d{2}-\d{2})', content, re.MULTILINE)
    if match:
        return match.group(1)
    return None


def extrahiere_werk(content):
    """Liest das werk-Feld aus dem YAML-Frontmatter."""
    match = re.search(r'^werk:\s*(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return "Unbekanntes Werk"


def extrahiere_kapitel(content):
    """Liest das kapitel-Feld aus dem YAML-Frontmatter."""
    match = re.search(r'^kapitel:\s*(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return ""


# === Exegese-Blöcke sammeln ===

def sammle_exegesen(ziel_datum=None):
    """Sammelt alle Exegese-Blöcke, optional gefiltert nach Datum."""
    exegesen = []

    for root, dirs, files in os.walk(PROJEKTE_DIR):
        for f in sorted(files):
            if f.startswith("Exegese -") and f.endswith(".md") and "Block" in f:
                pfad = os.path.join(root, f)
                with open(pfad, 'r', encoding='utf-8') as fh:
                    content = fh.read()

                datum = extrahiere_datum(content)
                werk = extrahiere_werk(content)
                kapitel = extrahiere_kapitel(content)

                if ziel_datum is None or datum == ziel_datum:
                    exegesen.append({
                        'datei': f,
                        'pfad': pfad,
                        'datum': datum,
                        'werk': werk,
                        'kapitel': kapitel,
                        'content': content,
                    })

    return exegesen


# === Podcast-Text erzeugen ===

def erzeuge_uebergang(i, total, aktuell, naechster=None):
    """Erzeugt einen narrativen Übergang zwischen Blöcken."""
    uebergaenge_start = [
        f"Wir beginnen mit {aktuell['werk']}.",
        f"Den Anfang macht {aktuell['werk']}.",
        f"Starten wir mit {aktuell['werk']}.",
    ]
    uebergaenge_mitte = [
        f"Damit kommen wir zu {aktuell['werk']}.",
        f"Weiter geht es mit {aktuell['werk']}.",
        f"Als nächstes: {aktuell['werk']}.",
        f"Von hier aus wenden wir uns {aktuell['werk']} zu.",
        f"Der nächste Text: {aktuell['werk']}.",
        f"Nun zu {aktuell['werk']}.",
    ]
    uebergaenge_gleich = [
        f"Wir bleiben bei {aktuell['werk']} und kommen zum nächsten Abschnitt.",
        f"Weiter im selben Werk.",
        f"Der nächste Block aus demselben Text.",
    ]
    uebergaenge_ende = [
        f"Zum Abschluss: {aktuell['werk']}.",
        f"Der letzte Block: {aktuell['werk']}.",
        f"Wir schließen mit {aktuell['werk']}.",
    ]

    import random
    random.seed(i * 17 + total)  # deterministisch aber variiert

    if i == 0:
        text = random.choice(uebergaenge_start)
    elif i == total - 1:
        text = random.choice(uebergaenge_ende)
    elif naechster and aktuell['werk'] == naechster['werk']:
        text = random.choice(uebergaenge_gleich)
    else:
        text = random.choice(uebergaenge_mitte)

    if aktuell['kapitel']:
        text += f" {aktuell['kapitel']}."

    return text


def erzeuge_podcast(exegesen, datum_label):
    """Erzeugt einen zusammenhängenden Podcast-Text mit narrativen Übergängen."""

    teile = []

    # Intro
    werke = list(dict.fromkeys(ex['werk'] for ex in exegesen))  # unique, order preserved
    teile.append(f"Exegese-Podcast, {datum_label}.\n\n")
    teile.append(f"In diesem Podcast gehen wir durch {len(exegesen)} Exegese-Bloecke ")
    teile.append(f"aus {len(werke)} Werken. ")
    if len(werke) <= 6:
        teile.append("Die Texte: " + ", ".join(werke) + ".")
    teile.append("\n\n")

    vorgaenger_werk = None

    for i, ex in enumerate(exegesen):
        # Narrativer Übergang
        naechster = exegesen[i + 1] if i + 1 < len(exegesen) else None
        uebergang = erzeuge_uebergang(i, len(exegesen), ex, naechster)

        # Wenn neues Werk: deutlichere Pause
        if ex['werk'] != vorgaenger_werk:
            teile.append(f"\n\n{uebergang}\n\n")
        else:
            teile.append(f"\n{uebergang}\n\n")

        vorgaenger_werk = ex['werk']

        # Bereinigter Inhalt
        bereinigt = bereinige_markdown(ex['content'])
        teile.append(bereinigt)
        teile.append("\n")

    # Outro
    teile.append(f"\n\nDas war der Exegese-Podcast. ")
    teile.append(f"{len(exegesen)} Bloecke aus {len(werke)} Werken. ")
    teile.append(f"Bis zum naechsten Mal.\n")

    return ''.join(teile)


# === Hauptprogramm ===

def main():
    os.makedirs(CONVERT_DIR, exist_ok=True)

    # Datum bestimmen
    if len(sys.argv) > 1:
        if sys.argv[1] == '--all':
            ziel_datum = None
            datum_label = "Alle Exegesen"
            dateiname = "podcast-alle.txt"
        else:
            ziel_datum = sys.argv[1]
            datum_label = f"Session vom {ziel_datum}"
            dateiname = f"podcast-{ziel_datum}.txt"
    else:
        ziel_datum = date.today().isoformat()
        datum_label = f"Session vom {ziel_datum}"
        dateiname = f"podcast-{ziel_datum}.txt"

    # Exegesen sammeln
    exegesen = sammle_exegesen(ziel_datum)

    if not exegesen:
        print(f"Keine Exegese-Bloecke gefunden fuer {datum_label}.")
        if ziel_datum:
            print(f"Verfuegbare Daten:")
            alle = sammle_exegesen(None)
            daten = sorted(set(e['datum'] for e in alle if e['datum']))
            for d in daten:
                count = sum(1 for e in alle if e['datum'] == d)
                print(f"  {d}: {count} Bloecke")
        return

    print(f"Gefunden: {len(exegesen)} Exegese-Bloecke fuer {datum_label}")
    for ex in exegesen:
        print(f"  - {ex['datei']} ({ex['werk']})")

    # Podcast erzeugen
    podcast = erzeuge_podcast(exegesen, datum_label)

    # Schritt 1: Originale als Markdown in convert/ kopieren
    for ex in exegesen:
        ziel = os.path.join(CONVERT_DIR, ex['datei'])
        with open(ziel, 'w', encoding='utf-8') as fh:
            fh.write(ex['content'])

    # Schritt 2: Bereinigten Podcast schreiben
    ausgabe_pfad = os.path.join(CONVERT_DIR, dateiname)
    with open(ausgabe_pfad, 'w', encoding='utf-8') as fh:
        fh.write(podcast)

    print(f"\nAusgabe:")
    print(f"  Originale:  {CONVERT_DIR}/ ({len(exegesen)} .md-Dateien)")
    print(f"  Podcast:    {ausgabe_pfad}")
    print(f"  Laenge:     {len(podcast)} Zeichen (~{len(podcast)//1500} Minuten bei normalem Sprechtempo)")


if __name__ == '__main__':
    main()
