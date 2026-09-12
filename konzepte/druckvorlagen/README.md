# Druckvorlagen — SanH Modul B2

Druckfertige PDF-Karten für die Ausbildungspraxis. Jede PDF enthält alle
Druckvorlagen eines Lernfelds, eine Karte pro A4-Seite.

## Inhalt

| Datei | Lernfeld | Karten | Seiten | Verwendung |
|---|---|---|---|---|
| `LF-I-Basiskompetenzen.pdf` | LF I | 5 | 6 | SAMPLER-, 5-W-, PAKET-Karten, Übergabe-Checkliste |
| `LF-II-Atmung.pdf` | LF II | 7 | 8 | Atemwegs-Anatomie, O2-Berechnung, Asthma-Schema |
| `LF-III-Herz-Kreislauf.pdf` | LF III | 9 | 10 | Puls-Taststellen, HLW-Schemata, AED-Schritte |
| `LF-IV-Verletzt.pdf` | LF IV | 9 | 10 | Wundarten, Stop-the-Bleed, Tourniquet-Anlage |
| `LF-V-Bewusstsein.pdf` | LF V | 7 | 8 | FAST-Test, Krampfanfall, BZ-Messung |
| `LF-VI-Schmerzen.pdf` | LF VI | 6 | 7 | Akutes Abdomen, Schmerzarten, Schmerzskala |
| `LF-VII-Sondersituationen.pdf` | LF VII | 7 | 8 | MANV-Lagekarte, Deeskalation, OSCE-Bogen |
| `Anhang-Normwerte.pdf` | Anhang | 11 | 12 | Normwerte, 9er-Regel, HLW-Schemata, CRM, Telefonnummern |

**Gesamt:** 71 Druckseiten für 8 PDFs.

## Verwendung

### Ausdruck

1. PDF öffnen
2. Auf A4-Papier drucken (empfohlen: 120 g/m² für bessere Haltbarkeit)
3. Am besten **doppelseitig** drucken (Vorder-/Rückseite nutzbar)
4. Optional: Laminieren oder in Klarsichthülle für Sanitätsdienst-Tasche

### Empfohlene Druckqualität

| Karte | Druck-Tipp |
|---|---|
| **Karten mit Wissen** (SAMPLER, 5-W, PAKET) | einseitig, laminiert — dauerhaft im Blockhefter |
| **Schemata** (HLW, Tourniquet) | farbig wenn möglich — erleichtert Memorieren |
| **Checklisten** (Übergabe, OSCE) | einseitig, kopierfest (für TN zum Ankreuzen) |
| **Schnellreferenz-Tabellen** (Normwerte, 9er-Regel) | A5 zuschneiden, laminieren |

### Für den Sanitätsdienst

Die Karten sind so designed, dass sie **im Brustbeutel** oder in der
**Sanitätstasche** mitgeführt werden können. Empfohlene Auswahl:

- 5-W-Karte (LF-I)
- SAMPLER-Karte (LF-I)
- HLW-Ablaufschema (LF-III oder Anhang)
- Stop-the-Bleed-Reihenfolge (LF-IV)
- Tourniquet-Anlage-Spickzettel (LF-IV)

## Skript-Generierung

Die PDFs werden automatisch aus den Druckvorlagen-Sektionen der Trainer-Konzepte in `konzepte/LF-*.md` und `konzepte/Anhang-Normwerte.md` generiert.

```bash
# Voraussetzung: fpdf2 in venv installiert
uv pip install --python /opt/data/venv-anki/.venv/bin/python fpdf2

# Generierung
/opt/data/venv-anki/.venv/bin/python /opt/data/SanH/build_druckvorlagen.py
```

Das Skript:
- Parst alle LF-*.md und Anhang-Normwerte.md
- Extrahiert die Druckvorlagen-Sektionen (### N.X Kartenname)
- Rendert jede Karte als A4-Seite mit Titel, Inhalt und Quellenangabe
- Verwendet DejaVu Sans für volle Unicode-Unterstützung (ä, ö, ü, ß, —)

## Versions-Historie

| Version | Datum | Änderung | Autor |
|---|---|---|---|
| 1.0 | 2026-09-12 | Erstgenerierung | Valentin Casas Stöldt |

## Lizenz

OER (Open Educational Resource) — frei für nicht-kommerzielle
Ausbildungszwecke, mit Quellenangabe. Druck für eigene
Ausbildungsveranstaltungen ausdrücklich erlaubt.
