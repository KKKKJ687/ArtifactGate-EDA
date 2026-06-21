from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "paper" / "figures"

BG = (248, 250, 252)
INK = (20, 31, 44)
BLUE = (43, 108, 176)
GREEN = (47, 133, 90)
ORANGE = (221, 107, 32)
RED = (197, 48, 48)
GRAY = (100, 116, 139)
LIGHT = (226, 232, 240)


def font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", size=size)
    except OSError:
        return ImageFont.load_default()


def draw_centered(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, fill=INK, size=22) -> None:
    fnt = font(size)
    lines = text.split("\n")
    heights = []
    widths = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=fnt)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])
    total_h = sum(heights) + (len(lines) - 1) * 6
    y = box[1] + ((box[3] - box[1]) - total_h) // 2
    for line, width, height in zip(lines, widths, heights, strict=True):
        x = box[0] + ((box[2] - box[0]) - width) // 2
        draw.text((x, y), line, font=fnt, fill=fill)
        y += height + 6


def rounded_box(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, color, text_size=20) -> None:
    draw.rounded_rectangle(box, radius=10, fill=(255, 255, 255), outline=color, width=3)
    draw_centered(draw, box, text, fill=INK, size=text_size)


def arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], color=GRAY) -> None:
    draw.line((start, end), fill=color, width=3)
    x2, y2 = end
    draw.polygon([(x2, y2), (x2 - 12, y2 - 7), (x2 - 12, y2 + 7)], fill=color)


def title(draw: ImageDraw.ImageDraw, text: str) -> None:
    draw.text((50, 28), text, font=font(30), fill=INK)


def architecture() -> None:
    img = Image.new("RGB", (1400, 820), BG)
    draw = ImageDraw.Draw(img)
    title(draw, "ArtifactGate-EDA Software Architecture")
    boxes = [
        ((70, 160, 300, 260), "CLI\nartifactgate", BLUE),
        ((410, 120, 650, 220), "Core\nindex, hash, validate", GREEN),
        ((410, 270, 650, 370), "Policy Engine\nevidence + claims", ORANGE),
        ((760, 120, 1010, 220), "Adapters\nngspice / HDL / Yosys", BLUE),
        ((760, 270, 1010, 370), "Replay + Reports\nmanifest + markdown", GREEN),
        ((1110, 190, 1320, 320), "Capsule\nzip + metadata", ORANGE),
    ]
    for box, text, color in boxes:
        rounded_box(draw, box, text, color)
    arrow(draw, (300, 210), (410, 170))
    arrow(draw, (300, 210), (410, 320))
    arrow(draw, (650, 170), (760, 170))
    arrow(draw, (650, 320), (760, 320))
    arrow(draw, (1010, 170), (1110, 245))
    arrow(draw, (1010, 320), (1110, 245))
    draw.text((90, 500), "Boundary rule: SoftwareX core evidence ceiling is L4_SYNTHESIS.", font=font(24), fill=INK)
    draw.text((90, 545), "L5 vendor reports, L6 bitstreams, and L7 board measurements remain unsupported in this package.", font=font(22), fill=GRAY)
    img.save(OUT / "architecture.png")


def workflow() -> None:
    img = Image.new("RGB", (1400, 700), BG)
    draw = ImageDraw.Draw(img)
    title(draw, "Claim-Safe Artifact Evaluation Workflow")
    steps = [
        "ingest\nartifacts",
        "validate\nhash + paths",
        "replay\nmanifest",
        "claim-check\nevidence levels",
        "report\nreviewer tables",
        "package\ncapsule",
    ]
    x = 70
    y = 250
    for idx, step in enumerate(steps):
        box = (x, y, x + 180, y + 110)
        rounded_box(draw, box, step, [BLUE, GREEN, ORANGE, RED, GREEN, BLUE][idx], 18)
        if idx < len(steps) - 1:
            arrow(draw, (x + 180, y + 55), (x + 235, y + 55))
        x += 235
    draw.text((80, 480), "Outputs: artifact_index.json/csv, provenance.json, run_manifest.json, unsupported_ledger.md, release zip", font=font(22), fill=INK)
    img.save(OUT / "workflow.png")


def evidence_levels() -> None:
    img = Image.new("RGB", (1000, 980), BG)
    draw = ImageDraw.Draw(img)
    title(draw, "EDA Evidence-Level Ladder")
    levels = [
        ("L7", "Board measurement", RED, "unsupported"),
        ("L6", "Bitstream artifact", RED, "unsupported"),
        ("L5", "Vendor implementation", RED, "unsupported"),
        ("L4", "Open synthesis", GREEN, "SoftwareX ceiling"),
        ("L3", "Software simulation", GREEN, "supported"),
        ("L2", "Reference/interface", BLUE, "supported"),
        ("L1", "Source exists", BLUE, "supported"),
        ("L0", "Metadata only", GRAY, "metadata"),
    ]
    y = 120
    for level, label, color, status in levels:
        draw.rounded_rectangle((120, y, 880, y + 82), radius=9, fill=(255, 255, 255), outline=color, width=3)
        draw.text((150, y + 22), level, font=font(26), fill=color)
        draw.text((250, y + 18), label, font=font(24), fill=INK)
        draw.text((650, y + 22), status, font=font(20), fill=GRAY)
        y += 96
    img.save(OUT / "evidence_levels.png")


def experiment_matrix() -> None:
    img = Image.new("RGB", (1350, 860), BG)
    draw = ImageDraw.Draw(img)
    title(draw, "Experiment and Gate Matrix")
    rows = [
        ("E0", "install + smoke", "PASS"),
        ("E1", "multi-adapter ingestion", "PASS"),
        ("E2", "core replay reports", "PASS"),
        ("E3", "negative claim injection", "PASS"),
        ("E4", "corrupted artifact detection", "PASS"),
        ("E5", "10k scalability", "PASS"),
        ("E6", "baseline comparison", "PASS"),
        ("E7", "PLECS/Logisim metadata", "PASS"),
        ("E8", "automation audit", "LOCAL ONLY"),
    ]
    x0, y0 = 80, 140
    col_w = [110, 760, 250]
    headers = ["ID", "Experiment", "Status"]
    x = x0
    for header, w in zip(headers, col_w, strict=True):
        draw.rectangle((x, y0, x + w, y0 + 58), fill=INK)
        draw.text((x + 20, y0 + 16), header, font=font(22), fill=(255, 255, 255))
        x += w
    y = y0 + 58
    for idx, row in enumerate(rows):
        fill = (255, 255, 255) if idx % 2 == 0 else (241, 245, 249)
        x = x0
        for value, w in zip(row, col_w, strict=True):
            draw.rectangle((x, y, x + w, y + 58), fill=fill, outline=LIGHT)
            color = GREEN if value == "PASS" else ORANGE
            draw.text((x + 20, y + 16), value, font=font(21), fill=color if value in {"PASS", "LOCAL ONLY"} else INK)
            x += w
        y += 58
    draw.text((90, 735), "External release gates remain separate: public GitHub Actions and Zenodo DOI require user authorization.", font=font(22), fill=GRAY)
    img.save(OUT / "experiment_matrix.png")


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    architecture()
    workflow()
    evidence_levels()
    experiment_matrix()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
