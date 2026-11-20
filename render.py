#!/usr/bin/env python3
"""Draw the 20 November 2026 world-news front page as a 1024x1024 PNG.

A single-page newspaper: a dark masthead naming the day, then six story
panels in a two-by-three grid, each with a small geometric pictogram, a
bold headline and a short factual summary. All artwork is drawn with
Pillow primitives; there are no photos and no outside assets.
"""

import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))

# Page and ink colours.
COLOURS = {
    "masthead": (13, 42, 74),
    "masthead_deep": (9, 30, 54),
    "gold": (232, 178, 74),
    "rule": (178, 52, 40),
    "paper": (247, 243, 236),
    "panel": (255, 255, 255),
    "panel_edge": (203, 196, 184),
    "headline": (24, 24, 24),
    "summary": (58, 58, 58),
    "credit": (112, 108, 100),
    "white": (255, 255, 255),
    "soft": (205, 214, 226),
    "divider": (216, 210, 200),
}

FONT_FILES = {
    "bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "regular": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
}

# The six verified stories of Friday 20 November 2026.
PANELS = [
    {
        "tag": "UKRAINE",
        "hue": (46, 111, 168),
        "glyph": "flame",
        "title": "KYIV HIT BY MISSILE DEBRIS",
        "body": ("Fire breaks out in a three-storey building in the "
                 "Obolonskyi district; the mayor says crews are on the "
                 "scene after early-morning blasts."),
    },
    {
        "tag": "CHINA",
        "hue": (168, 50, 50),
        "glyph": "bank",
        "title": "CHINA HOLDS RATES FOR 18TH MONTH",
        "body": ("The central bank keeps its loan prime rates at 3.0% "
                 "and 3.5%; the benchmark now matters less as the "
                 "overnight rate takes over."),
    },
    {
        "tag": "JAPAN",
        "hue": (72, 61, 139),
        "glyph": "chart",
        "title": "JAPAN INFLATION BEATS 2% TARGET",
        "body": ("Core prices rise 2.2% in October, the second month "
                 "above the Bank of Japan's target, cementing a "
                 "December rate-hike bet."),
    },
    {
        "tag": "CLIMATE",
        "hue": (14, 116, 144),
        "glyph": "globe",
        "title": "COP31 FACES FINAL DAY WITHOUT A DEAL",
        "body": ("The summit enters its closing day in Antalya with no "
                 "agreement yet; a slimmed-down draft drops every "
                 "mention of fossil fuels."),
    },
    {
        "tag": "BRUSSELS",
        "hue": (46, 125, 91),
        "glyph": "flags",
        "title": "UK AND EU MEET IN BRUSSELS",
        "body": ("The second EU-UK summit opens with Burnham, Costa "
                 "and von der Leyen; food, carbon and youth deals on "
                 "the table."),
    },
    {
        "tag": "GAMING",
        "hue": (107, 79, 161),
        "glyph": "pad",
        "title": "GTA VI SALES TOP $2.3 BILLION",
        "body": ("Estimates published Friday put first-day sales at "
                 "$2.36 billion and 24.6 million copies, a record for "
                 "the industry."),
    },
]

CREDIT_LINE = ("Sources: Reuters \u00b7 Business Today \u00b7 UN News "
               "\u00b7 European Council")


def load_font(weight, size):
    return ImageFont.truetype(FONT_FILES[weight], size)


def wrap_text(canvas, text, face, width):
    """Split text into lines that each fit inside width pixels."""
    words = text.split()
    out = []
    line = ""
    for word in words:
        candidate = word if line == "" else line + " " + word
        if canvas.textlength(candidate, font=face) <= width:
            line = candidate
        else:
            out.append(line)
            line = word
    if line:
        out.append(line)
    return out


def choose_face(canvas, text, sizes, width, limit, weight):
    """Return the biggest face (and its wrapped lines) fitting limit lines."""
    for size in sizes:
        face = load_font(weight, size)
        lines = wrap_text(canvas, text, face, width)
        if len(lines) <= limit:
            return face, lines
    face = load_font(weight, sizes[-1])
    return face, wrap_text(canvas, text, face, width)


def pale(rgb, amount=0.88):
    """Return rgb lightened toward white by amount (0..1)."""
    return tuple(round(c + (255 - c) * amount) for c in rgb)


def draw_glyph(canvas, kind, cx, cy, size, hue):
    """Draw one geometric pictogram of the given kind, centred on cx, cy."""
    half = size // 2
    if kind == "flame":
        # Teardrop flame with a pale inner tongue and three sparks.
        left, top = cx - size // 4, cy - half + 4
        right, bottom = cx + size // 4, cy + half - 4
        canvas.pieslice([left, top, right, bottom], 180, 360, fill=hue)
        canvas.polygon([(left, cy), (right, cy), (cx, bottom)], fill=hue)
        ix0, iy0 = cx - size // 8, cy + 2
        ix1, iy1 = cx + size // 8, cy + half - 8
        canvas.pieslice([ix0, iy0, ix1, iy1], 180, 360,
                        fill=COLOURS["white"])
        canvas.polygon([(ix0, cy + 8), (ix1, cy + 8), (cx, iy1)],
                       fill=COLOURS["white"])
        for sx, sy in ((cx - 12, cy - half + 2), (cx + 2, cy - half - 2),
                       (cx + 12, cy - half + 4)):
            canvas.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=hue)
    elif kind == "bank":
        # Pediment, three columns and a plinth.
        apex = cy - half + 4
        canvas.polygon([(cx - half + 4, apex + 12),
                        (cx + half - 4, apex + 12), (cx, apex)], fill=hue)
        canvas.rectangle([cx - half + 4, apex + 12,
                          cx + half - 4, apex + 16], fill=hue)
        for step in (-1, 0, 1):
            col = cx + step * (size // 4)
            canvas.rectangle([col - 4, apex + 20, col + 4,
                              cy + half - 14], fill=hue)
        canvas.rectangle([cx - half + 4, cy + half - 12,
                          cx + half - 4, cy + half - 6], fill=hue)
    elif kind == "chart":
        # Three rising bars under an upward arrow.
        floor = cy + half - 8
        for pos, tall in enumerate((12, 20, 28)):
            bx = cx - half + 8 + pos * (size // 3)
            canvas.rectangle([bx, floor - tall, bx + 12, floor], fill=hue)
        canvas.line([(cx - half + 6, cy - 2),
                     (cx + half - 8, cy - half + 8)], fill=hue, width=4)
        ax, ay = cx + half - 8, cy - half + 8
        canvas.polygon([(ax - 10, ay + 2), (ax, ay - 2), (ax - 2, ay + 10)],
                       fill=hue)
    elif kind == "globe":
        # Meridian globe with a small leaf at the lower right.
        r = half - 4
        canvas.ellipse([cx - r, cy - r, cx + r, cy + r],
                       outline=hue, width=4)
        canvas.ellipse([cx - r // 2, cy - r, cx + r // 2, cy + r],
                       outline=hue, width=3)
        canvas.line([(cx - r, cy), (cx + r, cy)], fill=hue, width=3)
        canvas.arc([cx - r, cy - r // 2, cx + r, cy + r // 2],
                   200, 340, fill=hue, width=3)
        lx, ly = cx + r - 2, cy + r - 6
        canvas.pieslice([lx - 10, ly - 12, lx + 6, ly + 4],
                        270, 90, fill=hue)
        canvas.line([(lx - 8, ly - 2), (lx + 4, ly - 10)],
                    fill=hue, width=2)
    elif kind == "flags":
        # Two poles with small pennants, a dot between them.
        for n, fx in enumerate((cx - size // 4, cx + size // 4)):
            ptop, pbot = cy - half + 4, cy + half - 4
            canvas.line([(fx, ptop), (fx, pbot)], fill=hue, width=3)
            if n == 0:
                canvas.polygon([(fx, ptop), (fx + 16, ptop + 4),
                                (fx, ptop + 12)], fill=hue)
            else:
                canvas.polygon([(fx, ptop), (fx - 16, ptop + 4),
                                (fx, ptop + 12)], fill=hue)
        sx, sy = cx, cy + size // 4
        canvas.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=hue)
    else:  # "pad": a game controller
        x0, y0 = cx - half + 3, cy - size // 4
        x1, y1 = cx + half - 3, cy + size // 4 + 4
        canvas.rounded_rectangle([x0, y0, x1, y1], radius=10,
                                 outline=hue, width=4)
        px, py = cx - size // 4, cy + 2
        canvas.line([(px - 9, py), (px + 9, py)], fill=hue, width=4)
        canvas.line([(px, py - 9), (px, py + 9)], fill=hue, width=4)
        for bx in (cx + size // 4 - 5, cx + size // 4 + 5):
            canvas.ellipse([bx - 4, py - 4, bx + 4, py + 4], fill=hue)
        canvas.line([(cx - size // 4, y0 - 5),
                     (cx - size // 4 + 8, y0 - 5)], fill=hue, width=3)
        canvas.line([(cx + size // 4 - 8, y0 - 5),
                     (cx + size // 4, y0 - 5)], fill=hue, width=3)


def draw_masthead(canvas, width):
    canvas.rectangle([0, 0, width, 150], fill=COLOURS["masthead"])
    canvas.rectangle([0, 150, width, 156], fill=COLOURS["rule"])
    canvas.text((24, 14), "THE WORLD IN ONE DAY",
                font=load_font("bold", 28), fill=COLOURS["gold"])
    canvas.text((22, 46), "WORLD NEWS",
                font=load_font("bold", 62), fill=COLOURS["white"])
    canvas.text((width - 24, 16), "FRIDAY",
                font=load_font("bold", 30), fill=COLOURS["white"],
                anchor="ra")
    canvas.text((width - 24, 50), "20 NOVEMBER 2026",
                font=load_font("bold", 40), fill=COLOURS["gold"],
                anchor="ra")
    canvas.text((width - 24, 104), "Six stories that shaped the day",
                font=load_font("regular", 20), fill=COLOURS["soft"],
                anchor="ra")


def draw_story(canvas, panel, x, y, w, h):
    canvas.rounded_rectangle([x, y, x + w, y + h], radius=10,
                             fill=COLOURS["panel"],
                             outline=COLOURS["panel_edge"], width=2)
    pad = 18
    tile = 62
    tx, ty = x + pad, y + pad
    canvas.rounded_rectangle([tx, ty, tx + tile, ty + tile], radius=8,
                             fill=pale(panel["hue"]))
    draw_glyph(canvas, panel["glyph"], tx + tile // 2, ty + tile // 2,
               tile - 14, panel["hue"])
    label_x = tx + tile + 14
    canvas.text((label_x, ty + 6), panel["tag"],
                font=load_font("bold", 24), fill=panel["hue"])
    canvas.line([(label_x, ty + 44), (x + w - pad, ty + 44)],
                fill=COLOURS["divider"], width=2)
    text_x = x + pad
    text_w = w - 2 * pad
    head_y = ty + tile + 12
    face, lines = choose_face(canvas, panel["title"], [30, 28, 26],
                              text_w, 2, "bold")
    cursor = head_y
    for line in lines:
        canvas.text((text_x, cursor), line, font=face,
                    fill=COLOURS["headline"])
        cursor += face.size + 4
    body_y = cursor + 6
    face, lines = choose_face(canvas, panel["body"], [19, 18, 17, 16],
                              text_w, 3, "regular")
    for line in lines:
        canvas.text((text_x, body_y), line, font=face,
                    fill=COLOURS["summary"])
        body_y += face.size + 5


def build():
    size = 1024
    page = Image.new("RGB", (size, size), COLOURS["paper"])
    canvas = ImageDraw.Draw(page)

    draw_masthead(canvas, size)

    margin, gutter = 24, 16
    top, bottom = 172, 956
    cell_w = (size - 2 * margin - gutter) // 2
    cell_h = (bottom - top - 2 * gutter) // 3
    for pos, panel in enumerate(PANELS):
        row, col = divmod(pos, 2)
        px = margin + col * (cell_w + gutter)
        py = top + row * (cell_h + gutter)
        draw_story(canvas, panel, px, py, cell_w, cell_h)

    canvas.text((size // 2, 970), CREDIT_LINE,
                font=load_font("regular", 17), fill=COLOURS["credit"],
                anchor="ma")

    target = os.path.join(BASE, "entry.png")
    page.save(target, "PNG")
    print("wrote", target, page.size, os.path.getsize(target), "bytes")


if __name__ == "__main__":
    build()
