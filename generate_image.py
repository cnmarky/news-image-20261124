#!/usr/bin/env python3
"""Build the entry image for make.fun news-image-20261124.

Draws a one-page newspaper front page summarising the world news of
Tuesday 24 November 2026, using only researched facts (see SOURCES in
README.md). Run:  python3 generate_image.py  ->  writes entry.png
(1024x1024, PNG, under 1 MiB). The submitted program (main.py) only
copies entry.png to /output, so the graded run needs no fonts and no
network; this builder runs here on the build machine only.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (247, 243, 236)
INK = (18, 24, 34)
NAVY = (15, 36, 64)
NAVY2 = (24, 54, 96)
MUTED = (90, 96, 108)
RULE = (203, 196, 184)
CARD = (255, 255, 255)
WHITE = (255, 255, 255)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning list of lines fitting `width` px."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_wrapped(draw, x, y, text, fnt, width, fill, leading=None):
    lines = wrap(draw, text, fnt, width)
    lh = leading or int(fnt.size * 1.28)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


STORIES = [
    {
        "tag": "WAR SPREADS",
        "color": (178, 34, 34),
        "headline": "Ukraine sinks Russian warship off Libya",
        "body": "Sea drones sank the Russian corvette Merkury off Benghazi, President Zelenskyy said \u2014 a new front far from the Black Sea.",
    },
    {
        "tag": "EUROPE",
        "color": (31, 93, 168),
        "headline": "NATO sends AWACS jets to Poland",
        "body": "After three Russian missiles landed in Poland, NATO will send AWACS aircraft. A Russian drone also briefly entered Polish airspace.",
    },
    {
        "tag": "ASIA",
        "color": (178, 106, 0),
        "headline": "Russian jets trigger alert in South Korea",
        "body": "Seoul issued an evacuation warning for Ulleung Island on Tuesday after Russian aircraft entered its air defence zone without notice.",
    },
    {
        "tag": "BUSINESS",
        "color": (20, 120, 90),
        "headline": "Nvidia brings back Jensen Huang",
        "body": "Eleven days after he resigned, the board unanimously reinstated Huang as CEO, after President Trump pressed for his return.",
    },
    {
        "tag": "CLIMATE",
        "color": (46, 125, 50),
        "headline": "COP31 climate talks collapse",
        "body": "UN climate talks in Antalya ended with no fossil-fuel deal after about 90 nations rejected the draft. Pacific nations voice despair.",
    },
    {
        "tag": "AMERICAS",
        "color": (123, 63, 160),
        "headline": "Mexico captures \u2018El Chapo Isidro\u2019",
        "body": "Troops seized cartel boss Fausto Isidro Meza Flores; 16 suspected cartel members were killed in the raid. He will be tried in Mexico.",
    },
]

ALSO = [
    ("GAZA", "Israeli strikes kill three, including an UNRWA worker."),
    ("VANUATU", "Magnitude 6.5 quake; no tsunami threat."),
    ("SPAIN", "Polls: right on course to oust S\u00e1nchez on 29 Nov."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 150], fill=NAVY)
    d.rectangle([0, 150, W, 156], fill=(198, 162, 74))
    f_kick = font(BOLD, 23)
    f_date = font(BOLD, 56)
    f_sub = font(REG, 22)
    kick = "T H E   W O R L D   I N   O N E   D A Y"
    d.text((36, 14), kick, font=f_kick, fill=(198, 162, 74))
    d.text((36, 46), "Tuesday 24 November 2026", font=f_date, fill=WHITE)
    d.text((36, 116), "Six stories that defined the day \u2014 as reported on 24 November 2026",
           font=f_sub, fill=(205, 214, 228))

    # ---- Story cards: 2 cols x 3 rows ----
    margin, gap = 28, 20
    cw = (W - 2 * margin - gap) // 2
    ch = 210
    top = 172
    f_tag = font(BOLD, 19)
    f_head = font(BOLD, 27)
    f_body = font(REG, 18)

    for i, s in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = margin + col * (cw + gap)
        y = top + row * (ch + gap)
        d.rounded_rectangle([x, y, x + cw, y + ch], radius=10, fill=CARD,
                            outline=RULE, width=1)
        d.rectangle([x, y + 10, x + 8, y + ch - 10], fill=s["color"])
        tx = x + 24
        # tag chip
        tw = d.textlength(s["tag"], font=f_tag) + 18
        d.rounded_rectangle([tx, y + 16, tx + tw, y + 46], radius=6,
                            fill=s["color"])
        d.text((tx + 9, y + 21), s["tag"], font=f_tag, fill=WHITE)
        hy = draw_wrapped(d, tx, y + 58, s["headline"], f_head, cw - 44, INK,
                          leading=33)
        draw_wrapped(d, tx, hy + 6, s["body"], f_body, cw - 44, (52, 58, 70),
                     leading=24)

    # ---- Also today strip ----
    ay = top + 3 * ch + 2 * gap + 14
    ah = 120
    d.rounded_rectangle([margin, ay, W - margin, ay + ah], radius=10,
                        fill=NAVY2)
    f_also = font(BOLD, 20)
    d.text((margin + 20, ay + 12), "ALSO TODAY", font=f_also,
           fill=(198, 162, 74))
    colw = (W - 2 * margin - 40) // 3
    f_item = font(REG, 18)
    for j, (tag, text) in enumerate(ALSO):
        cx = margin + 20 + j * colw
        d.text((cx, ay + 44), tag + " \u2014", font=font(BOLD, 18),
               fill=(198, 162, 74))
        draw_wrapped(d, cx, ay + 66, text, f_item, colw - 16, WHITE, leading=22)

    # ---- Footer ----
    f_foot = font(REG, 16)
    d.text((margin, H - 34),
           "Sources: Reuters, CNN, WSJ, AP, CNBC. Events of Tuesday 24 November 2026.",
           font=f_foot, fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
