"""Draw a one-page front-page infographic of 20 November 2026 world news.

Build-time only: reads the story lists defined below and writes entry.png
(1024 x 1024) next to this script. No network, no randomness, no clock, so
every run produces the same bytes.
"""

import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
MARGIN = 12
GAP = 6

CREAM = (244, 241, 232)
NAVY = (11, 31, 58)
NAVY_LIGHT = (23, 52, 88)
INK = (18, 18, 18)
MUTED = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (200, 196, 186)
GOLD = (212, 175, 55)
RED = (176, 42, 42)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 34)
F_DATE = font("DejaVuSans-Bold.ttf", 15)
F_STRAP = font("DejaVuSans.ttf", 12)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 16)
F_LEAD_BODY = font("DejaVuSans.ttf", 12)
F_HEAD = font("DejaVuSans-Bold.ttf", 13)
F_BODY = font("DejaVuSans.ttf", 11)
F_SRC = font("DejaVuSans-Bold.ttf", 9)
F_REGION = font("DejaVuSans-Bold.ttf", 12)
F_TIME = font("DejaVuSans-Bold.ttf", 11)
F_TIME_BODY = font("DejaVuSans.ttf", 11)
F_FOOT = font("DejaVuSans.ttf", 11)


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_lines(draw, text, fnt, max_w, max_lines):
    """Wrap text, keeping at most max_lines; ellipsize the last line."""
    lines = wrap(draw, text, fnt, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and draw.textlength(lines[-1] + "...", font=fnt) > max_w:
        lines[-1] = lines[-1][:-1]
    lines[-1] = lines[-1] + "..."
    return lines


def draw_src(draw, x, y, text, color):
    draw.text((x, y), text.upper(), font=F_SRC, fill=color)

# --- Stories: headline, one or two lines of plain fact, source tag. ---
# Every fact below comes from the verified briefing; nothing is invented.

LEADS = [
    ("CYCLONE AKVAN MAKES LANDFALL",
     "Severe storm crosses the north Andhra Pradesh and south Odisha "
     "coast near Gopalpur, winds 70-80 km/h gusting to 90. Third "
     "cyclone in under a month; 300,000+ evacuated, 423 teams deployed.",
     "Reuters / IMD"),
    ("KYIV HIT BY BALLISTIC MISSILES",
     "Overnight Russian missile and drone barrage damages three Dnipro "
     "bridges, kills 3 and injures about 15, and knocks out power in "
     "five districts. Hours after the Trump-Putin-Xi talks in Shenzhen.",
     "Reuters / CNN"),
    ("COP31 FINAL-DAY DEADLOCK",
     "UN climate talks in Antalya reach their final day with 21 issues "
     "unresolved. A new draft deal drops any mention of fossil fuels; "
     "adaptation finance of $120bn a year is sought. US absent again.",
     "UN News / AP"),
]

# (region label, accent colour, [(headline, fact, source), ...])
SECTIONS = [
    ("ASIA", (176, 42, 42), [
        ("Asia AI sell-off",
         "Nikkei -4.8%, SoftBank -16%+, Taiwan -2,200 pts on AI fears.",
         "BBC / Reuters"),
        ("Trump, Xi and Putin meet",
         "Three-way summit in Shenzhen; joint peace declaration.",
         "Reports, 19 Nov"),
        ("World Court: Myanmar genocide",
         "Myanmar committed genocide against the Rohingya, 9-6.",
         "ICJ, 19 Nov"),
        ("880,000 AI chips for China",
         "Nearly 880,000 advanced AI chips approved for China.",
         "US House"),
        ("California probes Nvidia",
         "California targets Nvidia in a probe of China AI-chip sales.",
         "California"),
    ]),
    ("EUROPE", (31, 97, 141), [
        ("UK pledges 1,000+ drones",
         "Over 1,000 drones for Ukraine in a 260-million-pound package.",
         "UK Government"),
        ("EU to summon Russian envoy",
         "EU to summon Russia's envoy over embassy damage in Kyiv.",
         "EU"),
        ("Poland probes mystery objects",
         "Unknown objects probed as an air-threat warning is lifted.",
         "Polish authorities"),
        ("UK-EU youth mobility deal",
         "UK and EU agree a youth-mobility scheme.",
         "BBC"),
        ("Genoa airport halts flights",
         "Flights suspended after unidentified drones detected.",
         "Italian authorities"),
    ]),
    ("MIDDLE EAST", (125, 102, 8), [
        ("Houthi missile hits Riyadh tower",
         "Missile damages the Saudi wealth fund tower in Riyadh.",
         "Reports"),
        ("Tanker burns after mine strike",
         "Tanker catches fire after hitting a mine east of Hormuz.",
         "Reports"),
        ("Saudi defences down two drones",
         "Saudi air defences destroy two Houthi drones.",
         "Saudi authorities"),
        ("Strike hits Hezbollah facility",
         "Israeli strike hits a Hezbollah missile facility, east Lebanon.",
         "Reports"),
    ]),
    ("NORTH AMERICA", (30, 132, 73), [
        ("GTA VI launch smashes records",
         "24.6m copies, $2.36bn in 24h; 125.47m hours watched live.",
         "Sensor Tower"),
        ("Senate rejects Iran war powers",
         "Senate rejects the Iran war-powers resolution, 51 to 48.",
         "US Senate"),
        ("Trump pardons Pete Rose",
         "Posthumous pardon for baseball's Pete Rose.",
         "White House"),
        ("US stocks fall a fifth day",
         "US stocks fall for a fifth straight day; S&P 500 down about "
         "2%.",
         "Markets"),
        ("Broadcom patches vCenter flaw",
         "Critical VMware vCenter flaw patched; update now.",
         "Broadcom"),
    ]),
    ("SOUTH AMERICA", (108, 52, 131), [
        ("Argentina backs disability law",
         "Disability framework approved unanimously, 71 senators.",
         "Argentina Senate"),
        ("Lula visits Chief Raoni",
         "Lula visits ailing Chief Raoni as land recognition advances.",
         "Brazil"),
        ("Bukele seeks third term",
         "Bukele to formally register for a third term in El Salvador.",
         "Reports"),
    ]),
    ("AFRICA", (183, 119, 14), [
        ("Malawi fuel crisis turns violent",
         "Fuel crisis triggers violence and economic strain.",
         "Reports"),
        ("Senegal boat capsizing kills 4",
         "Boat capsizing kills four as the migration surge continues.",
         "Reports"),
        ("Kenya discharges last Ebola patient",
         "Last Ebola patient discharged, 37 days after the first case.",
         "Kenya health authorities"),
    ]),
    ("OCEANIA · AND FINALLY", (20, 143, 119), [
        ("5.6 quake near New Caledonia",
         "A 5.6-magnitude earthquake strikes near New Caledonia.",
         "Reports"),
        ("Fiona the hippo dies",
         "Fiona dies after swallowing a hat at Cincinnati Zoo.",
         "Cincinnati Zoo"),
    ]),
]

# Timeline strip: day-part labels only, in UTC order. No clock times invented.
TIMELINE = [
    ("OVERNIGHT", "Kyiv barrage"),
    ("MORNING", "Akvan landfall"),
    ("MARKETS CLOSE", "Asia AI sell-off"),
    ("FINAL DAY", "COP31 deadlock"),
    ("LAUNCH DAY", "GTA VI records"),
]

TOTAL_STORIES = 3 + sum(len(s[2]) for s in SECTIONS)


def draw_masthead(draw, y, h):
    draw.rectangle([0, y, W, y + h], fill=NAVY)
    draw.rectangle([0, y + h - 4, W, y + h], fill=GOLD)
    draw.text((MARGIN, y + 8), "THE WORLD IN ONE PAGE",
              font=F_TITLE, fill=(255, 255, 255))
    date_txt = "FRIDAY 20 NOVEMBER 2026"
    dw = draw.textlength(date_txt, font=F_DATE)
    draw.rectangle([W - MARGIN - dw - 16, y + 10, W - MARGIN, y + 34],
                   outline=GOLD, width=2)
    draw.text((W - MARGIN - dw - 8, y + 13), date_txt,
              font=F_DATE, fill=GOLD)
    draw.text((MARGIN, y + h - 24),
              "30 stories  ·  6 continents  ·  every story reported on 20 November 2026",
              font=F_STRAP, fill=(200, 210, 225))


def draw_lead(draw, x, y, w, h, head, body, src, accent):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    draw.rectangle([x, y, x + w, y + 6], fill=accent)
    tx = x + 10
    tw = w - 20
    lines = fit_lines(draw, head, F_LEAD_HEAD, tw, 2)
    ly = y + 12
    for ln in lines:
        draw.text((tx, ly), ln, font=F_LEAD_HEAD, fill=INK)
        ly += 19
    blines = fit_lines(draw, body, F_LEAD_BODY, tw, 4)
    for ln in blines:
        draw.text((tx, ly), ln, font=F_LEAD_BODY, fill=(40, 40, 40))
        ly += 15
    draw.text((tx, y + h - 20), src.upper(), font=F_SRC, fill=accent)


def draw_card(draw, x, y, w, h, head, body, src, accent):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=LINE, width=1)
    draw.rectangle([x, y, x + 4, y + h], fill=accent)
    tx = x + 10
    tw = w - 16
    lines = fit_lines(draw, head, F_HEAD, tw, 2)
    ly = y + 5
    for ln in lines:
        draw.text((tx, ly), ln, font=F_HEAD, fill=INK)
        ly += 16
    blines = fit_lines(draw, body, F_BODY, tw, 2)
    for ln in blines:
        draw.text((tx, ly), ln, font=F_BODY, fill=(50, 50, 50))
        ly += 14
    draw.text((tx, y + h - 15), src.upper(), font=F_SRC, fill=accent)


def draw_region_header(draw, x, y, w, label, accent):
    draw.rectangle([x, y, x + w, y + 16], fill=accent)
    draw.text((x + 6, y + 1), label, font=F_REGION, fill=(255, 255, 255))


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Masthead
    draw_masthead(draw, 0, 64)

    # Lead band: the three biggest stories
    lead_y = 70
    lead_h = 148
    lead_accents = [RED, (31, 97, 141), (30, 132, 73)]
    lead_xs = [MARGIN, 347, 682]
    lead_ws = [329, 329, 330]
    for (head, body, src), x, w, accent in zip(
            LEADS, lead_xs, lead_ws, lead_accents):
        draw_lead(draw, x, lead_y, w, lead_h, head, body, src, accent)

    # Region grid: 5 columns of small cards under thin region headers
    col_xs = [MARGIN, 213, 414, 615, 816]
    col_ws = [195, 195, 195, 195, 196]
    card_h = 80
    y = lead_y + lead_h + GAP
    for label, accent, stories in SECTIONS:
        draw_region_header(draw, MARGIN, y, W - 2 * MARGIN, label, accent)
        y += 16 + 4
        for row_start in range(0, len(stories), 5):
            row = stories[row_start:row_start + 5]
            for (head, body, src), x, w in zip(row, col_xs, col_ws):
                draw_card(draw, x, y, w, card_h, head, body, src, accent)
            y += card_h + GAP
    # y already carries the row gap, so the next header starts here.

    # UTC timeline strip (day-parts only, in UTC order)
    tl_y = y + 2
    draw.rectangle([0, tl_y, W, tl_y + 34], fill=NAVY)
    slot_w = (W - 2 * MARGIN) // len(TIMELINE)
    for i, (part, label) in enumerate(TIMELINE):
        text = part + "  " + label
        tw = draw.textlength(text, font=F_TIME_BODY)
        cx = MARGIN + i * slot_w + slot_w // 2
        tx = cx - tw // 2
        draw.text((tx, tl_y + 10), part + "  ",
                  font=F_TIME, fill=GOLD)
        pw = draw.textlength(part + "  ", font=F_TIME)
        draw.text((tx + pw, tl_y + 10), label,
                  font=F_TIME_BODY, fill=(255, 255, 255))
        if i < len(TIMELINE) - 1:
            ax = MARGIN + (i + 1) * slot_w
            draw.text((ax - 5, tl_y + 9), ">", font=F_TIME, fill=GOLD)

    # Footer line
    foot = ("%d stories  ·  All stories reported on Friday 20 November 2026  ·  "
            "Sources tagged on every card" % TOTAL_STORIES)
    fw = draw.textlength(foot, font=F_FOOT)
    draw.text(((W - fw) // 2, tl_y + 40), foot, font=F_FOOT, fill=MUTED)

    img.save(OUT, format="PNG", optimize=True)
    print("wrote %s (%dx%d)" % (OUT, W, H))


if __name__ == "__main__":
    main()
