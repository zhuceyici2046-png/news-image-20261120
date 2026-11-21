#!/usr/bin/env python3
"""Build entry.png: one front page summing up Friday 20 November 2026.

34 stories, all checked against the day's reporting (One Turn's
20 November digest and the Just Security Early Edition of 20 Nov):
  LEADS
  - Kyiv's bridges hit in overnight strikes, 8 killed; Poland says
    two missiles and a drone crossed its airspace.
  - Merz rejects a great-power deal over Europe's head; EU-UK summit
    in Brussels; Kushner floats a NATO-style guarantee for Ukraine
    if Kyiv cedes territory.
  SPOTLIGHT
  - Anthropic closes near $97, 17% above its $83 IPO price, while
    tech shares still slide (S&P 500 down a fifth straight day).
  - GTA 6 sales top $2.3bn on industry estimates, the biggest
    entertainment launch ever.
  - The US Senate passes its energy permitting overhaul, 62-33.
  ASIA & PACIFIC (6) / EUROPE (5) / MIDDLE EAST (5) / AMERICAS (5) /
  TECH & MARKETS (4) / CLIMATE & MORE (4), plus a markets strip
  (Nikkei -4.8%, S&P 500 -2.0%, Brent $90.05, Gold -4.2%).
"""
from PIL import Image, ImageDraw, ImageFont

PAGE = 1024
EDGE = 24
GAP = 12

PAL = {
    "paper": (246, 241, 231),
    "card": (255, 255, 255),
    "white": (253, 251, 246),
    "ink": (22, 35, 58),
    "navy": (18, 30, 54),
    "crimson": (178, 39, 30),
    "brass": (212, 172, 60),
    "steel": (46, 94, 140),
    "teal": (31, 122, 109),
    "violet": (90, 60, 140),
    "leaf": (56, 118, 70),
    "muted": (74, 80, 96),
    "edge": (200, 192, 175),
    "hair": (220, 214, 200),
    "slate": (60, 60, 66),
    "sand": (214, 196, 140),
}

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def typeface(kind, size):
    return ImageFont.truetype(f"{FONT_DIR}/{kind}", size)


def serif_bold(size):
    return typeface("DejaVuSerif-Bold.ttf", size)


def sans_bold(size):
    return typeface("DejaVuSans-Bold.ttf", size)


def sans_plain(size):
    return typeface("DejaVuSans.ttf", size)


def fit_words(pen, text, face, limit):
    """Split text into lines that fit `limit` pixels wide."""
    out, running = [], ""
    for piece in text.split():
        trial = f"{running} {piece}".strip()
        if pen.textlength(trial, font=face) <= limit:
            running = trial
        else:
            if running:
                out.append(running)
            running = piece
    if running:
        out.append(running)
    return out


def paint_lines(pen, x, top, rows, face, colour, step=None):
    step = step if step is not None else int(face.size * 1.18)
    for row in rows:
        pen.text((x, top), row, font=face, fill=colour)
        top += step
    return top


def centred(pen, x0, x1, y, text, face, colour):
    w = pen.textlength(text, font=face)
    pen.text(((x0 + x1 - w) / 2, y), text, font=face, fill=colour)


def paint_globe(pen, cx, cy, rad, colour):
    pen.ellipse([cx - rad, cy - rad, cx + rad, cy + rad],
                outline=colour, width=5)
    pen.ellipse([cx - rad // 2, cy - rad, cx + rad // 2, cy + rad],
                outline=colour, width=3)
    pen.line([cx - rad, cy, cx + rad, cy], fill=colour, width=3)
    pen.arc([cx - rad, cy - rad // 2, cx + rad, cy + rad // 2],
            0, 360, fill=colour, width=3)


def paint_balance(pen, x, top, span, colour):
    mid = x + span // 2
    pen.line([mid, top, mid, top + int(span * 0.75)], fill=colour, width=5)
    pen.line([x, top + int(span * 0.15), x + span, top + int(span * 0.15)],
             fill=colour, width=5)
    for px in (x + span // 7, x + span * 6 // 7):
        pen.line([px, top + int(span * 0.15), px, top + int(span * 0.4)],
                 fill=colour, width=3)
        pen.polygon([(px - span // 7, top + int(span * 0.4)),
                     (px + span // 7, top + int(span * 0.4)),
                     (px, top + int(span * 0.65))], outline=colour, width=3)
    pen.line([x + span // 5, top + int(span * 0.88),
              x + span * 4 // 5, top + int(span * 0.88)],
             fill=colour, width=5)


LEADS = [
    {
        "flag": "TOP STORY  ·  KYIV, UKRAINE",
        "accent": "crimson",
        "lines": ["KYIV BRIDGES HIT,", "8 KILLED"],
        "deck": "Overnight strikes hit bridges; Poland says missiles "
                "crossed its airspace",
        "mark": "globe",
        "tint": "steel",
    },
    {
        "flag": "AFTER SHENZHEN",
        "accent": "navy",
        "lines": ["EUROPE SAYS NO", "TO A NEW YALTA"],
        "deck": "Merz: no deal over Europe's head; Kushner floats "
                "NATO-for-land",
        "mark": "balance",
        "tint": "teal",
    },
]

SPOTLIGHT = [
    {
        "head": ["ANTHROPIC", "CLOSES +17%"],
        "deck": "IPO ends day one near $97 — but tech shares still slide",
        "accent": "steel",
    },
    {
        "head": ["GTA 6 SALES", "TOP $2.3BN"],
        "deck": "Biggest entertainment launch ever, industry estimates say",
        "accent": "violet",
    },
    {
        "head": ["SENATE PASSES", "ENERGY BILL"],
        "deck": "Permitting overhaul clears 62–33; the House is next",
        "accent": "crimson",
    },
]

GROUPS = [
    {"name": "ASIA & PACIFIC", "accent": "crimson", "items": [
        "Takaichi gets cool reception at APEC in Shenzhen",
        "Japan core inflation hits year's high; BOJ hike on track",
        "Philippines and Chile sign free trade deal at APEC",
        "IAEA: North Korea expanding uranium enrichment",
        "Mongolia's president resigns; acting president named",
        "South Korea court orders retrial of ex-PM Han",
    ]},
    {"name": "EUROPE", "accent": "navy", "items": [
        "Estonia to shut Russia border for six months",
        "Denmark ratifies Greenland security deal with US",
        "Youth strike in 25+ countries over costs and rearmament",
        "Sánchez admits mistakes in TV debate before Spain vote",
        "UK–EU summit: youth mobility scheme on the table",
    ]},
    {"name": "MIDDLE EAST", "accent": "teal", "items": [
        "Iraqi forces move into Kataib Hezbollah stronghold",
        "Israeli troops cross Gaza ceasefire line — first since truce",
        "Iran war has cost US $48.3bn, Pentagon tells lawmakers",
        "Mosque torched in northern Israel; 8 hurt in car-ramming",
        "Riyadh vows no tolerance after Houthi tower strike",
    ]},
    {"name": "AMERICAS", "accent": "steel", "items": [
        "US and Venezuela sign military cooperation deal",
        "White House fires cyber chief after week of outages",
        "Texas executes 70-year-old; Florida sets execution record",
        "Bukele registers for third term in El Salvador",
        "Colombia protests tax plans; national strike called",
    ]},
    {"name": "TECH & MARKETS", "accent": "violet", "items": [
        "SoftBank −16% as Asian tech slides; Korea halts trading",
        "AMD −7% after short-seller report on China exposure",
        "Brazil central bank sells $1bn as real slides 18% in a month",
        "IMF: global public debt to near 100% of GDP",
    ]},
    {"name": "CLIMATE & MORE", "accent": "leaf", "items": [
        "COP31 enters final day; fossil fuels still out of draft",
        "Fiji declares disaster as El Niño drought worsens",
        "El Niño storm threatens LA with floods and mudslides",
        "Voyager 1 reaches one light-day from Earth",
    ]},
]

TICKER = [
    ("Nikkei", "−4.8%"),
    ("S&P 500", "−2.0%"),
    ("Brent crude", "$90.05"),
    ("Gold", "−4.2%"),
]


def group_height(pen, group, face, width):
    """Pixel height of one section: title bar plus its headlines."""
    total = 30
    for head in group["items"]:
        total += len(fit_words(pen, head, face, width)) * 18 + 9
    return total


def paint_group(pen, x, top, width, group, face):
    pen.rectangle([x, top, x + width, top + 24], fill=PAL[group["accent"]])
    pen.text((x + 8, top + 3), group["name"], font=sans_bold(15),
             fill=PAL["white"])
    top += 30
    for head in group["items"]:
        rows = fit_words(pen, head, face, width)
        top = paint_lines(pen, x, top, rows, face, PAL["ink"], step=18)
        top += 3
        pen.line([x, top, x + width, top], fill=PAL["hair"], width=1)
        top += 6
    return top


def render():
    sheet = Image.new("RGB", (PAGE, PAGE), PAL["paper"])
    pen = ImageDraw.Draw(sheet)
    total = (len(LEADS) + len(SPOTLIGHT)
             + sum(len(g["items"]) for g in GROUPS))

    # masthead
    pen.rectangle([0, 0, PAGE, 112], fill=PAL["navy"])
    pen.rectangle([0, 112, PAGE, 116], fill=PAL["brass"])
    centred(pen, 0, PAGE, 8, "THE WORLD IN ONE DAY", sans_bold(19),
            PAL["brass"])
    centred(pen, 0, PAGE, 30, "20 NOVEMBER 2026", serif_bold(58),
            PAL["white"])
    centred(pen, 0, PAGE, 90,
            f"FRIDAY  ·  {total} STORIES  ·  ASIA  ·  EUROPE  ·  "
            "MIDDLE EAST  ·  AMERICAS  ·  TECH  ·  CLIMATE",
            sans_plain(17), PAL["sand"])

    # leads: two wide cards
    lead_w = (PAGE - 2 * EDGE - 16) // 2
    lead_top, lead_bot = 124, 274
    for i, lead in enumerate(LEADS):
        x0 = EDGE + i * (lead_w + 16)
        pen.rectangle([x0, lead_top, x0 + lead_w, lead_bot],
                      fill=PAL["card"], outline=PAL["edge"], width=2)
        pen.rectangle([x0, lead_top, x0 + lead_w, lead_top + 6],
                      fill=PAL[lead["accent"]])
        if lead["mark"] == "globe":
            paint_globe(pen, x0 + 76, lead_top + 78, 52, PAL[lead["tint"]])
        else:
            paint_balance(pen, x0 + 18, lead_top + 62, 58, PAL[lead["tint"]])
        tx = x0 + 140
        tw = x0 + lead_w - 14 - tx
        pen.text((tx, lead_top + 12), lead["flag"], font=sans_bold(16),
                 fill=PAL[lead["accent"]])
        y = paint_lines(pen, tx, lead_top + 34, lead["lines"],
                        sans_bold(30), PAL["ink"], step=34)
        deck_rows = fit_words(pen, lead["deck"], sans_plain(17), tw)
        paint_lines(pen, tx, y + 4, deck_rows, sans_plain(17),
                    PAL["muted"], step=21)

    # spotlight: three cards
    spot_w = (PAGE - 2 * EDGE - 2 * GAP) // 3
    spot_top, spot_bot = 284, 408
    for i, card in enumerate(SPOTLIGHT):
        x0 = EDGE + i * (spot_w + GAP)
        pen.rectangle([x0, spot_top, x0 + spot_w, spot_bot],
                      fill=PAL["card"], outline=PAL["edge"], width=2)
        pen.rectangle([x0, spot_top, x0 + spot_w, spot_top + 6],
                      fill=PAL[card["accent"]])
        tx = x0 + 14
        tw = x0 + spot_w - 14 - tx
        y = paint_lines(pen, tx, spot_top + 16, card["head"],
                        sans_bold(23), PAL["ink"], step=26)
        deck_rows = fit_words(pen, card["deck"], sans_plain(16), tw)
        paint_lines(pen, tx, y + 8, deck_rows, sans_plain(16),
                    PAL["muted"], step=19)

    # sections: three columns, two groups each
    col_w = (PAGE - 2 * EDGE - 2 * GAP) // 3
    area_top, area_bot = 420, 990
    room = area_bot - area_top
    columns = [GROUPS[0:2], GROUPS[2:4], GROUPS[4:6]]
    size = 18
    while size > 14:
        face = sans_bold(size)
        fits = True
        for ci, pair in enumerate(columns):
            need = sum(group_height(pen, g, face, col_w) for g in pair) + 12
            if ci == 2:
                need += 24 + 4 + 4 * 26
            if need > room:
                fits = False
        if fits:
            break
        size -= 1
    face = sans_bold(size)
    for ci, pair in enumerate(columns):
        x0 = EDGE + ci * (col_w + GAP)
        y = area_top
        for group in pair:
            y = paint_group(pen, x0, y, col_w, group, face)
            y += 12
        if ci == 2:
            pen.rectangle([x0, y, x0 + col_w, y + 24], fill=PAL["slate"])
            pen.text((x0 + 8, y + 3), "MARKETS", font=sans_bold(15),
                     fill=PAL["white"])
            y += 28
            for label, value in TICKER:
                pen.text((x0, y), label, font=sans_plain(16),
                         fill=PAL["muted"])
                vw = pen.textlength(value, font=sans_bold(16))
                pen.text((x0 + col_w - vw, y), value, font=sans_bold(16),
                         fill=PAL["ink"])
                y += 22
                pen.line([x0, y, x0 + col_w, y], fill=PAL["hair"], width=1)
                y += 4

    # footer
    centred(pen, 0, PAGE, 998,
            "Drawn from the day's reporting  ·  20 November 2026",
            sans_plain(18), PAL["muted"])

    sheet.save("entry.png", optimize=True)
    print(f"saved entry.png, {total} stories, headline size {size}")


if __name__ == "__main__":
    render()
