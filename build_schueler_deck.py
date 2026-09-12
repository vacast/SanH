#!/usr/bin/env python3
"""Generate Anki .apkg for SanH students from CSV with Quelle references."""

import csv
import html
import genanki
from pathlib import Path

CSV_PATH = Path("/opt/data/SanH/sanh-schueler-deck.csv")
OUTPUT_PATH = Path("/opt/data/SanH/SanH_Modul_B2_Schueler.apkg")

# Stable, unique IDs (random 8-digit numbers)
DECK_ID = 1749000010
MODEL_ID = 1749000011

deck = genanki.Deck(DECK_ID, "SanH Modul B2 :: Schülerprüfung")

# Card model with Quelle field
model = genanki.Model(
    MODEL_ID,
    "SanH Karte mit Quelle",
    fields=[
        {"name": "Frage"},
        {"name": "Antwort"},
        {"name": "Block"},
        {"name": "Quelle"},
    ],
    templates=[
        {
            "name": "Karte",
            "qfmt": (
                '<div class="frage">{{Frage}}</div>'
                '<div class="tag">{{Block}}</div>'
            ),
            "afmt": (
                "{{FrontSide}}<hr id=answer>"
                '<div class="antwort">{{Antwort}}</div>'
                '<div class="quelle">📖 {{Quelle}}</div>'
            ),
        }
    ],
    css=(
        ".card { font-family: Arial; font-size: 18px; color: #222; "
        "background: #fafafa; }"
        ".frage { font-size: 20px; font-weight: 600; margin-bottom: 12px; }"
        ".tag { display: inline-block; padding: 2px 8px; background: #2c5aa0; "
        "color: white; border-radius: 4px; font-size: 12px; margin-bottom: 12px; }"
        ".antwort { font-size: 19px; line-height: 1.5; margin-bottom: 12px; }"
        ".quelle { font-size: 12px; color: #666; font-style: italic; "
        "border-top: 1px solid #ddd; padding-top: 8px; }"
    ),
)

# Load CSV
with CSV_PATH.open(encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    count = 0
    for row in reader:
        frage = row["Frage"].strip()
        antwort = row["Antwort"].strip()
        block = row["Block"].strip()
        quelle = row["Quelle"].strip()
        if not frage or not antwort:
            continue
        note = genanki.Note(
            model=model,
            fields=[
                html.escape(frage),
                html.escape(antwort).replace("\n", "<br>"),
                html.escape(block),
                html.escape(quelle),
            ],
            tags=[block.replace(" ", "_"), "SanH", "Modul-B2", "Schueler-Deck"],
        )
        deck.add_note(note)
        count += 1

# Write package
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
genanki.Package(deck).write_to_file(str(OUTPUT_PATH))

print(f"✅ {count} Karten exportiert nach {OUTPUT_PATH}")
print(f"   Dateigröße: {OUTPUT_PATH.stat().st_size:,} Bytes")
