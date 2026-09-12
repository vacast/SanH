# SanH Modul B2 — Anki-Karten + Trainer-Konzepte

Sanitätshelfer-Ausbildungs-Material (Modul B2, 48 UE) nach dem Curriculum der
Hilfsorganisationen (JUH, BG, BEE). Stand: 2018.

Dieses Repo enthält zwei Bereiche:

- **Anki-Deck** für Teilnehmer:innen (`*.apkg`, `*.csv`, `*.py`)
- **Trainer-Konzepte** für Ausbilder:innen (`konzepte/*.md`)

## Inhalt

### Anki-Deck

| Datei | Beschreibung |
|---|---|
| `SanH_Modul_B2_Schueler.apkg` | Fertiges Anki-Deck zum Importieren (263 Karten) |
| `sanh-schueler-deck.csv` | Quell-CSV (Semikolon-getrennt, 4 Spalten) |
| `build_schueler_deck.py` | Generator-Skript (liest CSV, baut .apkg) |

### Trainer-Konzepte (`konzepte/`)

Vollständiges 48-UE-Konzept mit 7 Lernfeldern + Anhang + Gesamtkonzept.
Jedes Konzept folgt der gleichen Struktur: Lernziele, Material,
pädagogische Leitlinien, Gamification, UE-für-UE-Ablauf, Block-Abschluss,
Differenzierung, Trainer-Qualifikation, Druckvorlagen.

| Datei | Lernfeld | UE | Kommentar |
|---|---|---|---|
| `konzepte/LF-I-Basiskompetenzen.md` | Lernfeld I | 6 | S. 8–12 |
| `konzepte/LF-II-Atmung.md` | Lernfeld II | 6 | S. 12–17 |
| `konzepte/LF-III-Herz-Kreislauf.md` | Lernfeld III | 8 | S. 18–24 |
| `konzepte/LF-IV-Verletzt.md` | Lernfeld IV | 10 | S. 25–34 |
| `konzepte/LF-V-Bewusstsein.md` | Lernfeld V | 6 | S. 35–41 |
| `konzepte/LF-VI-Schmerzen.md` | Lernfeld VI | 4 | S. 41–44 |
| `konzepte/LF-VII-Sondersituationen.md` | Lernfeld VII | 4 | S. 45–46 |
| `konzepte/Anhang-Normwerte.md` | Schnellreferenz | — | S. 47–52 |
| `konzepte/Gesamtkonzept.md` | Master-Dokument (Kursfahrplan, Prüfung, Logistik) | 8 + Prüfung | alle |
| `konzepte/druckvorlagen/` | Druckfertige PDF-Karten (8 PDFs, 71 Seiten) | — | alle |

**Gesamtumfang:** 48 UE + Prüfungsvorbereitung, 36 Zeit-Stunden Präsenz.

## Karteikarten-Aufbau

Jede Karte hat vier Felder:

- **Frage** — prüfungsrelevante Frage in einfachem Deutsch
- **Antwort** — Antwort mit kompakten Fakten
- **Block** — Lernfeld-Tag (LF-I bis LF-VII, CRM, Pädagogik)
- **Quelle** — Seitenangabe im Begleitenden Kommentar 2018 (z.B. "Kommentar S. 13")

Über den **Quelle**-Tag lässt sich jede Antwort im Original-Skript nachschlagen.

## Karten-Verteilung (263 Karten gesamt)

| Lernfeld | Karten | Thema |
|---|---|---|
| LF-I Basiskompetenzen | 39 | ABCDE, PAKET, SAMPLER, Hygiene, Notruf, Bodycheck |
| LF-II Atmung | 25 | Anatomie, Atemstörungen, Asthma, Aspiration, O2 |
| LF-III Herz-Kreislauf | 58 | Puls, Blutdruck, Schock, ACS, HLW, AED, Larynx-Tubus |
| LF-IV Verletzt | 61 | Wunden, Blutungen, Tourniquet, Verbrennungen, SHT, Frakturen |
| LF-V Bewusstsein | 40 | Schlaganfall, Krampfanfall, Hypoglykämie, Hitze/Kälte |
| LF-VI Schmerzen | 18 | Akutes Abdomen, Schmerzarten, Schmerzskala |
| LF-VII Sondersituationen | 10 | MANV, Gewalt, Einsatznachsorge |
| CRM + Pädagogik | 12 | Querschnittsthemen |

## Für Teilnehmer:innen — so importierst du das Deck

### Variante A — Anki Desktop (empfohlen)

1. **Anki Desktop** installieren: <https://apps.ankiweb.net> (kostenlos)
2. Anki öffnen
3. **Datei → Importieren**
4. `SanH_Modul_B2_Schueler.apkg` auswählen
5. Deck-Name bestätigen: `SanH Modul B2 :: Schülerprüfung`
6. **Importieren** klicken
7. Karten lernen — fertig.

### Variante B — AnkiMobile (iOS, kostenpflichtig)

1. AnkiMobile aus dem App Store laden (24,99 € einmalig, Apple-Zwang)
2. AnkiWeb-Konto erstellen: <https://ankiweb.net/account/register>
3. In Anki Desktop synchronisieren (Button "Sync" oben)
4. Auf iOS in AnkiMobile mit demselben Konto anmelden
5. Deck erscheint automatisch auf dem Gerät

### Variante C — AnkiDroid (Android, kostenlos)

1. AnkiDroid aus dem Play Store laden
2. AnkiWeb-Konto erstellen
3. Wie Variante B synchronisieren

## Für Ausbilder:innen — Karten pflegen und erweitern

### Bestehende Karten anpassen

CSV direkt bearbeiten:

```bash
# Editor deiner Wahl
nano sanh-schueler-deck.csv
```

Vier Spalten:

```csv
Frage;Antwort;Block;Quelle
Was bedeutet TRF?;Tun – Retten – Frei machen;LF-I-Basiskompetenzen;Kommentar S. 9
```

Wichtig:

- **Trennzeichen** ist `;` (Semikolon)
- Interne Semikolons in Antworten vermeiden oder durch Komma ersetzen
- **Block** sollte einem existierenden Lernfeld-Tag entsprechen
- **Quelle** im Format `Kommentar S. X` für prüfbare Referenzen

### Deck neu generieren

```bash
# Voraussetzung: uv + venv (siehe unten)
/opt/data/venv-anki/.venv/bin/python build_schueler_deck.py
```

Das Skript erzeugt `SanH_Modul_B2_Schueler.apkg` neu aus der CSV.

### Voraussetzungen für das Build-Skript

```bash
# Einmalig
mkdir -p /opt/data/venv-anki
uv venv /opt/data/venv-anki/.venv
/opt/data/venv-anki/.venv/bin/pip install genanki
```

## Lerntempo-Empfehlung

| Phase | Karten/Tag | Dauer |
|---|---|---|
| Woche 1–2 (vor Kurs) | 10 neue + Wiederholungen | 1 Monat |
| Während 48-UE-Kurs | 15–20 neue + Wiederholungen | 4 Wochen |
| Prüfungsvorbereitung | Wiederholungen intensiv | 2 Wochen |

**Gesamtblastung:** ca. 5–10 Min Lernzeit pro Tag für nachhaltigen Effekt.

## Tags im Deck

Beim Import sind die Karten mit folgenden Tags versehen:

- `SanH` — alle Karten des Moduls
- `Modul-B2` — Curriculum-Identifikation
- `LF-I-Basiskompetenzen`, `LF-II-Atmung`, ... — Lernfeld-Zuordnung
- `Schueler-Deck` — Identifikation als Teilnehmer:innen-Deck

Im **AnkiBrowser** (Tastenkürzel `b`) kannst du nach Tags filtern
(z.B. nur LF-IV-Karten anzeigen).

## Lizenz und Nutzung

Die Karten wurden aus dem offiziellen **Begleitenden Kommentar zur
Sanitätshelferausbildung Modul B2** der Hilfsorganisationen
(JUH, BG, BEE, Stand 2018) abgeleitet. Die Original-Materialien unterliegen
dem Copyright der Hilfsorganisationen und sind **nicht** Teil dieses Repos.

Dieses Deck dient als **persönliches Lernwerkzeug für Teilnehmer:innen der
Sanitätshelfer-Ausbildung** und als **Arbeitsmaterial für Ausbilder:innen
zur Unterrichtsvorbereitung**. Eine Weiterverbreitung außerhalb dieses
Zwecks ist nicht vorgesehen.

Das Trainer-Konzept unter `konzepte/` ist als **Open Educational Resource**
für Sanitätshelfer-Ausbilder:innen aller Hilfsorganisationen gedacht und darf
für eigene nicht-kommerzielle Ausbildungszwecke frei verwendet und
angepasst werden — bitte mit Quellenangabe.

Bei Aktualisierung des Curriculums: bitte Issues oder Pull Requests
öffnen, damit das Deck aktualisiert werden kann.

## Mitwirkende

Erstellt von [Valentin Casas Stöldt](https://github.com/vacast) als
Digital-Sciences-Masterstudent (TH Köln) und Sanitätshelfer-Fachdozent.
