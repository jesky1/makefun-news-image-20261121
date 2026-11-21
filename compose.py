#!/usr/bin/env python3
"""Typeset a one-page newspaper front page — The World in One Day."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
HERO_PATH = HERE / "hero.webp"
OUT_PATH = HERE / "entry.png"

W, H = 1024, 1024
MARGIN = 40
LIVE_W = W - 2 * MARGIN  # 944

PAPER = (250, 247, 238)
INK = (22, 20, 18)
FADED = (96, 90, 82)
ACCENT = (122, 28, 28)
HAIRLINE = (60, 56, 50)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def load(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"


def wrap_words(draw, text, font, max_width):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, y, text, font, fill, line_h):
    lines = wrap_words(draw, text, font, LIVE_W)
    for ln in lines:
        tw = draw.textlength(ln, font=font)
        draw.text((MARGIN + (LIVE_W - tw) / 2, y), ln, font=font, fill=fill)
        y += line_h
    return y


def draw_wrapped_at(draw, x, y, text, font, fill, max_width, line_h):
    for ln in wrap_words(draw, text, font, max_width):
        draw.text((x, y), ln, font=font, fill=fill)
        y += line_h
    return y


def hline(draw, y, thickness=1):
    draw.rectangle([MARGIN, y, MARGIN + LIVE_W, y + thickness - 1], fill=HAIRLINE)
    return y + thickness


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    y = 22

    # --- Masthead ---
    y = hline(draw, y, 1)
    y += 6

    # Fitted title
    title = "THE WORLD IN ONE DAY"
    size = 54
    while size > 20:
        f = load(SERIF_BOLD, size)
        if draw.textlength(title, font=f) <= LIVE_W:
            break
        size -= 2
    title_font = load(SERIF_BOLD, size)
    tw = draw.textlength(title, font=title_font)
    draw.text((MARGIN + (LIVE_W - tw) / 2, y), title, font=title_font, fill=INK)
    y += size + 2

    date_font = load(SANS_BOLD, 16)
    date_text = "SATURDAY · 21 NOVEMBER 2026"
    dw = draw.textlength(date_text, font=date_font)
    draw.text((MARGIN + (LIVE_W - dw) / 2, y), date_text, font=date_font, fill=FADED)
    y += 20

    y = hline(draw, y, 4)
    y += 3
    y = hline(draw, y, 1)
    y += 8

    # --- Hero photo: centre-crop into 944x330 ---
    hero = Image.open(HERO_PATH).convert("RGB")
    target_w, target_h = LIVE_W, 330
    scale = max(target_w / hero.width, target_h / hero.height)
    nw, nh = int(hero.width * scale + 0.5), int(hero.height * scale + 0.5)
    hero_r = hero.resize((nw, nh), Image.LANCZOS)
    left = (nw - target_w) // 2
    top = (nh - target_h) // 2
    hero_c = hero_r.crop((left, top, left + target_w, top + target_h))
    img.paste(hero_c, (MARGIN, y))
    # redraw draw after paste
    draw = ImageDraw.Draw(img)
    y += target_h + 4

    caption_font = load(SANS, 13)
    caption = "Air defenses over Kyiv at dawn, as the heaviest Russian barrage in weeks lit up the sky over the Dnipro."
    y = draw_centered(draw, y, caption, caption_font, FADED, 16)
    y += 5

    # --- Lead story ---
    kicker_font = load(SANS_BOLD, 13)
    kicker = "KYIV · WARSAW"
    kw = draw.textlength(kicker, font=kicker_font)
    draw.text((MARGIN + (LIVE_W - kw) / 2, y), kicker, font=kicker_font, fill=ACCENT)
    y += 17

    lead_head_font = load(SERIF_BOLD, 34)
    lead_head = "Russian Missiles Fall in Poland as Massive Barrage Pounds Ukraine"
    y = draw_centered(draw, y, lead_head, lead_head_font, INK, 38)
    y += 2

    lead_body_font = load(SERIF, 16)
    lead_body = (
        "Russia fired more than 400 drones and 110 missiles at Ukraine overnight, killing at least eight people "
        "in Kyiv and damaging bridges and railway stations. Two missiles and a suspected drone came down in "
        "southeastern Poland, and Prime Minister Donald Tusk called the incursion a deliberate provocation. "
        "A later strike on Kryvyi Rih wounded about 20 people."
    )
    y = draw_wrapped_at(draw, MARGIN, y, lead_body, lead_body_font, INK, LIVE_W, 20)
    y += 4
    y = hline(draw, y, 1)
    y += 7

    # --- Two columns ---
    gutter = 30
    col_w = (LIVE_W - gutter) // 2  # 457
    col_x = [MARGIN, MARGIN + col_w + gutter]
    col_head_font = load(SANS_BOLD, 18)
    col_body_font = load(SANS, 13)

    left_stories = [
        ("NEW YORK", "AI Sell-Off Pushes S&P 500 Into Correction",
         "US stocks fell 3.7% on Friday as a rout in AI and chip shares deepened, pushing the S&P 500 and the Dow into correction territory and wiping out the Nasdaq's gains for the year."),
        ("LONDON", "Cancer Pill Erases Tumours in Trial",
         "A trial of the pill daraxonrasib found pancreatic cancer became undetectable on scans in one in 12 patients \u2014 a rare breakthrough against one of the deadliest cancers."),
    ]
    right_stories = [
        ("BRUSSELS", "UK and EU Sign Biggest Post-Brexit Agreements",
         "Prime Minister Andy Burnham and EU leaders signed three agreements covering food exports, carbon markets and youth mobility \u2014 the biggest step in UK-EU relations since Brexit."),
        ("ANTALYA", "COP31 Talks Run Past Deadline in Fossil-Fuel Deadlock",
         "The UN climate summit in Antalya, Turkey, ran into overtime as nearly 200 nations failed to agree on language over fossil fuels."),
    ]

    def render_column(x, stories, start_y):
        cy = start_y
        for dateline, headline, body in stories:
            full_head = f"{dateline} \u2014 {headline}"
            cy = draw_wrapped_at(draw, x, cy, full_head, col_head_font, INK, col_w, 21)
            cy += 1
            cy = draw_wrapped_at(draw, x, cy, body, col_body_font, INK, col_w, 16)
            cy += 6
        return cy

    left_bottom = render_column(col_x[0], left_stories, y)
    right_bottom = render_column(col_x[1], right_stories, y)
    y = max(left_bottom, right_bottom)

    # --- ALSO TODAY band ---
    y = hline(draw, y, 1)
    y += 6
    label_font = load(SANS_BOLD, 14)
    draw.text((MARGIN, y), "ALSO TODAY", font=label_font, fill=ACCENT)
    y += 18

    brief_font = load(SANS, 12)
    briefs = [
        "FBI criminal database reportedly hacked as cyberattacks and outages continue across the US",
        "Iran says it downed a US MQ-9 drone over the Strait of Hormuz",
        "US judge validates Bayer's $7.25 billion settlement of Roundup claims",
        "Magnitude 6.9 earthquake shakes the Peruvian Andes",
        "Man convicted of starting Los Angeles' deadly Palisades fire",
        "Swimmer Lewis Pugh crosses the Strait of Hormuz to spotlight the war's toll on wildlife",
    ]
    for b in briefs:
        y = draw_wrapped_at(draw, MARGIN, y, "\u2022  " + b, brief_font, INK, LIVE_W, 15)

    y += 6
    # --- Footer ---
    y = hline(draw, y, 1)
    y += 6
    footer_font = load(SANS, 11)
    footer = "Compiled from news reporting of Saturday 21 November 2026 \u2014 wire services and international outlets."
    fw = draw.textlength(footer, font=footer_font)
    draw.text((MARGIN + (LIVE_W - fw) / 2, y), footer, font=footer_font, fill=FADED)
    y += 14

    assert y <= 1024, f"Content overflow: end y={y} > 1024"
    img.save(OUT_PATH, "PNG")
    print(f"end y: {y}")
    print(f"output: {OUT_PATH}")


if __name__ == "__main__":
    main()
