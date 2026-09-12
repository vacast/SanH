#!/usr/bin/env python3
"""Generate print-ready PDFs of all Druckvorlagen from SanH Trainer-Konzepten.

Creates one PDF per Lernfeld with all its printable cards.
Output: /opt/data/SanH/druckvorlagen/<LF-name>.pdf
"""

import re
from pathlib import Path
from fpdf import FPDF

CONCEPTS_DIR = Path("/opt/data/SanH/konzepte")
OUTPUT_DIR = Path("/opt/data/SanH/druckvorlagen")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


class CardPDF(FPDF):
    """PDF generator for SanH printable cards."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Use Bold for italic since DejaVu Sans Italic is not installed
        self.add_font("DejaVu", "", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        self.add_font("DejaVu", "B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
        self.add_font("DejaVu", "I", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
        self.add_font("DejaVuMono", "", "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
        self.set_font("DejaVu", "", 12)

    def header(self):
        # Header strip with Lernfeld name
        if hasattr(self, "lf_title"):
            self.set_font("DejaVu", "B", 9)
            self.set_text_color(255, 255, 255)
            self.set_fill_color(44, 90, 160)
            self.cell(
                0,
                8,
                f"  {self.lf_title} - Druckvorlage",
                fill=True,
                new_x="LMARGIN",
                new_y="NEXT",
            )
            self.set_text_color(0, 0, 0)
            self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(120, 120, 120)
        self.cell(
            0,
            5,
            f"SanH Modul B2 - Druckvorlagen | Seite {self.page_no()}/{{nb}}",
            align="C",
        )
        self.set_text_color(0, 0, 0)


def extract_cards(md_path: Path) -> tuple[str, list[dict]]:
    """Extract all Druckvorlagen cards from a Trainer-Konzept Markdown file.

    Returns (lf_title, list_of_cards).
    each card = {title, lines, format_hint}
    """
    text = md_path.read_text(encoding="utf-8")

    # Find the Druckvorlagen section
    start_match = re.search(
        r"^##\s+\d+\.?\s*Anhang:?\s*Druckvorlagen?\s*$",
        text,
        re.MULTILINE,
    )
    if not start_match:
        return "", []

    start = start_match.end()

    # End at Versions-Historie (or end of file)
    end_match = re.search(
        r"^##\s+\d+\.?\s*Versions-Historie\s*$", text[start:], re.MULTILINE
    )
    end = start + end_match.start() if end_match else len(text)

    section = text[start:end]

    # Split into cards by ### headers
    cards = []
    current_card = None

    for line in section.split("\n"):
        # Detect card start: "### N.X Title (DIN A5)" or "### N.X Title (DIN A4)"
        h_match = re.match(r"^###\s+(\d+\.\d+)\s+(.+?)(?:\s+\(DIN\s+(A[45])\))?\s*$", line)
        if h_match:
            if current_card:
                cards.append(current_card)
            current_card = {
                "number": h_match.group(1),
                "title": h_match.group(2).strip(),
                "format": h_match.group(3) or "A5",
                "lines": [],
                "in_code_block": False,
            }
            continue

        if current_card is None:
            continue

        # Track code block boundaries
        if line.strip().startswith("```"):
            current_card["in_code_block"] = not current_card["in_code_block"]
            continue

        if current_card["in_code_block"]:
            current_card["lines"].append(line)

    if current_card:
        cards.append(current_card)

    # Clean lines (remove box-drawing chars for cleaner display)
    cleaned_cards = []
    for card in cards:
        # Filter empty lines at start/end, strip box-drawing
        text_lines = []
        for raw in card["lines"]:
            # Remove the box-drawing prefix/suffix but keep text
            # Strip leading │ and trailing │, plus surrounding space
            line_cleaned = raw.strip()
            # Replace unsupported glyphs with text equivalents
            line_cleaned = line_cleaned.replace("⏱", "[Zeit]")
            line_cleaned = line_cleaned.replace("⏰", "[Zeit]")
            # Remove the box-drawing corner/edge characters
            line_cleaned = re.sub(r"^[│┌└├┤┬┴┼─╭╮╰╯]+", "", line_cleaned)
            line_cleaned = re.sub(r"[│┐┘┤┬┴┼─╭╮╰╯]+$", "", line_cleaned)
            line_cleaned = line_cleaned.rstrip()
            if line_cleaned.strip():
                text_lines.append(line_cleaned)
        card["content_lines"] = text_lines
        cleaned_cards.append(card)

    # Derive LF title
    title_match = re.search(r"^#\s+(SanH.*?)$", text, re.MULTILINE)
    lf_title = title_match.group(1).strip() if title_match else md_path.stem

    return lf_title, cleaned_cards


def render_card(pdf: CardPDF, card: dict) -> None:
    """Render a single card on a new A4 page."""
    pdf.add_page()
    pdf.set_margins(left=15, top=20, right=15)

    # Card title (large, bold)
    pdf.set_font("DejaVu", "B", 16)
    pdf.set_text_color(44, 90, 160)
    title_with_num = f"{card['number']} {card['title']}"
    pdf.cell(0, 10, title_with_num, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)

    # Format hint
    pdf.set_font("DejaVu", "I", 9)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(0, 5, f"Format: {card['format']}", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    # Card box (bordered)
    box_x = 15
    box_y = pdf.get_y()
    box_w = 180

    # Calculate box height based on content
    pdf.set_font("DejaVu", "", 12)
    line_height = 6
    content_height = max(60, len(card["content_lines"]) * line_height + 10)
    pdf.set_draw_color(44, 90, 160)
    pdf.set_line_width(1.0)
    pdf.rect(box_x, box_y, box_w, content_height)

    # Content inside box
    pdf.set_xy(box_x + 5, box_y + 5)
    pdf.set_font("DejaVuMono", "", 11)
    for line in card["content_lines"]:
        # Truncate very long lines
        display = line if len(line) <= 80 else line[:77] + "..."
        pdf.cell(box_w - 10, line_height, display, new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(box_x + 5)

    # Footer source
    pdf.set_xy(15, box_y + content_height + 8)
    pdf.set_font("DejaVu", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(
        0,
        5,
        "Quelle: Begleitender Kommentar zur SanH-Ausbildung Modul B2 (JUH/BG/BEE 2018)",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.set_text_color(0, 0, 0)


def render_text_list_card(pdf: CardPDF, card: dict) -> None:
    """Render numbered/listed cards (Blockhefter-Inhalt etc.) cleanly."""
    pdf.add_page()
    pdf.set_margins(left=15, top=20, right=15)

    pdf.set_font("DejaVu", "B", 16)
    pdf.set_text_color(44, 90, 160)
    title_with_num = f"{card['number']} {card['title']}"
    pdf.cell(0, 10, title_with_num, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    pdf.set_font("DejaVu", "", 12)
    for line in card["content_lines"]:
        pdf.cell(0, 7, line, new_x="LMARGIN", new_y="NEXT")


def generate_lf_pdf(md_path: Path, output_path: Path) -> int:
    """Generate PDF for one LF. Returns number of cards rendered."""
    lf_title, cards = extract_cards(md_path)
    if not cards:
        return 0

    pdf = CardPDF(format="A4")
    pdf.lf_title = lf_title
    pdf.alias_nb_pages()  # Enable total page number in footer

    for card in cards:
        # Decide renderer: bordered box vs simple list
        if card.get("format") == "A4" and "Blockhefter" in card["title"]:
            render_text_list_card(pdf, card)
        elif any(
            keyword in card["title"]
            for keyword in ["Checkliste", "Bogen", "Blockhefter", "Selbsttest"]
        ):
            render_text_list_card(pdf, card)
        else:
            render_card(pdf, card)

    pdf.output(str(output_path))
    return len(cards)


def extract_anhang_cards(md_path: Path) -> tuple[str, list[dict]]:
    """Extract Anhang-Normwerte content as a list of reference cards.

    Returns (title, list_of_cards) where each card is {title, lines, format_hint}.
    """
    text = md_path.read_text(encoding="utf-8")
    cards = []
    current_card = None

    for line in text.split("\n"):
        # Section headers like "## 1 Normwertetabelle Vitalzeichen (Kommentar S. 47)"
        h_match = re.match(r"^##\s+(\d+)\s+(.+?)$", line)
        if h_match:
            if current_card:
                cards.append(current_card)
            current_card = {
                "number": h_match.group(1),
                "title": h_match.group(2).strip(),
                "format": "A5",
                "lines": [],
                "in_table": False,
                "in_code_block": False,
            }
            continue

        # Subsection headers (skip)
        sub_match = re.match(r"^###\s+\d+\.\d+\s+", line)
        if sub_match:
            if current_card is not None:
                current_card["lines"].append(("", "subheader", line.lstrip("# ")))
            continue

        # Code block boundaries
        if line.strip().startswith("```"):
            if current_card is not None:
                current_card["in_code_block"] = not current_card["in_code_block"]
            continue

        # Table boundaries
        if "|" in line and current_card is not None and not current_card["in_code_block"]:
            current_card["in_table"] = True
            cells = [c.strip() for c in line.split("|")]
            current_card["lines"].append(("|", "table", " | ".join(c for c in cells if c)))
            continue
        elif current_card is not None and current_card["in_table"] and "|" not in line:
            current_card["in_table"] = False

        # Regular text
        if current_card is not None and line.strip() and not current_card["in_code_block"]:
            current_card["lines"].append(("", "text", line.strip()))

    if current_card:
        cards.append(current_card)

    # Derive title
    title_match = re.search(r"^#\s+(.+?)$", text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else md_path.stem

    return title, cards


def render_anhang_card(pdf: CardPDF, card: dict) -> None:
    """Render an Anhang reference page."""
    pdf.add_page()
    pdf.set_margins(left=15, top=20, right=15)

    pdf.set_font("DejaVu", "B", 16)
    pdf.set_text_color(44, 90, 160)
    title_with_num = f"{card['number']} {card['title']}"
    pdf.cell(0, 10, title_with_num, new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(3)

    box_x = 15
    box_y = pdf.get_y()
    box_w = 180

    pdf.set_draw_color(44, 90, 160)
    pdf.set_line_width(1.0)

    line_height = 5
    content_height = max(80, len(card["lines"]) * line_height + 10)
    pdf.rect(box_x, box_y, box_w, content_height)

    pdf.set_xy(box_x + 5, box_y + 5)
    for line_type, content_type, content in card["lines"]:
        if content_type == "subheader":
            pdf.set_font("DejaVu", "B", 11)
            pdf.set_text_color(44, 90, 160)
            pdf.cell(box_w - 10, line_height + 1, content, new_x="LMARGIN", new_y="NEXT")
            pdf.set_x(box_x + 5)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("DejaVu", "", 10)
        elif content_type == "table":
            pdf.set_font("DejaVuMono", "", 9)
            pdf.cell(box_w - 10, line_height, content, new_x="LMARGIN", new_y="NEXT")
            pdf.set_x(box_x + 5)
        else:
            pdf.set_font("DejaVu", "", 10)
            display = content if len(content) <= 95 else content[:92] + "..."
            pdf.cell(box_w - 10, line_height, display, new_x="LMARGIN", new_y="NEXT")
            pdf.set_x(box_x + 5)

    # Footer source
    pdf.set_xy(15, box_y + content_height + 8)
    pdf.set_font("DejaVu", "I", 8)
    pdf.set_text_color(120, 120, 120)
    pdf.cell(
        0,
        5,
        "Quelle: Begleitender Kommentar zur SanH-Ausbildung Modul B2 (JUH/BG/BEE 2018), S. 47-52",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.set_text_color(0, 0, 0)


def generate_anhang_pdf(md_path: Path, output_path: Path) -> int:
    """Generate Anhang-Normwerte PDF."""
    title, cards = extract_anhang_cards(md_path)
    # Skip "Versions-Historie" and "Pädagogische Hinweise" cards (last 2)
    cards = cards[:-2] if len(cards) > 2 else cards

    pdf = CardPDF(format="A4")
    pdf.lf_title = title
    pdf.alias_nb_pages()

    for card in cards:
        render_anhang_card(pdf, card)

    pdf.output(str(output_path))
    return len(cards)


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    md_files = sorted(CONCEPTS_DIR.glob("LF-*.md"))

    print(f"Generiere Druckvorlagen-PDFs nach {OUTPUT_DIR}/")
    print("=" * 60)

    for md_path in md_files:
        out_name = md_path.stem + ".pdf"
        out_path = OUTPUT_DIR / out_name
        n = generate_lf_pdf(md_path, out_path)
        size_kb = out_path.stat().st_size / 1024
        print(f"✅ {out_name:40s} {n:>3} Karten  {size_kb:>6.1f} KB")

    # Anhang separately
    anhang_path = CONCEPTS_DIR / "Anhang-Normwerte.md"
    if anhang_path.exists():
        out_path = OUTPUT_DIR / "Anhang-Normwerte.pdf"
        n = generate_anhang_pdf(anhang_path, out_path)
        size_kb = out_path.stat().st_size / 1024
        print(f"✅ {'Anhang-Normwerte.pdf':40s} {n:>3} Karten  {size_kb:>6.1f} KB")

    print("=" * 60)
    print(f"Fertig. PDFs in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()
