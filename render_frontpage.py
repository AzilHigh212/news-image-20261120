#!/usr/bin/env python3
"""Render the make.fun bounty "Sum up 20 November's world news in one
image" (news-image-20261120) as a one-page newspaper front page.

Draws a 1024x1024 front page with PIL from the verified news stories of
Friday 20 November 2026 and writes entry.png next to this file.
Deterministic: fixed layout, fixed fonts, no network, no clock, no
randomness — the same input always produces the same bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 230)
INK = (25, 25, 25)
ACCENT = (163, 22, 33)
MUTED = (90, 85, 75)
RULE = (25, 25, 25)
MARGIN = 44

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = f"{FONT_DIR}/DejaVuSerif-Bold.ttf"
SERIF = f"{FONT_DIR}/DejaVuSerif.ttf"
SANS = f"{FONT_DIR}/DejaVuSans.ttf"
SANS_B = f"{FONT_DIR}/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap using the font's real text widths."""
    lines, cur = [], ""
    for word in text.split():
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


def draw_story(draw, x, y, w, kicker, headline, body, head_size,
               body_size, kicker_size=17, max_head_lines=2, max_body_lines=3):
    """Draw one story block; return the y just below it."""
    kf = font(SANS_B, kicker_size)
    hf = font(SERIF_B, head_size)
    bf = font(SANS, body_size)
    draw.text((x, y), kicker, font=kf, fill=ACCENT)
    y += kicker_size + 7
    head_lines = wrap(draw, headline, hf, w)[:max_head_lines]
    for line in head_lines:
        draw.text((x, y), line, font=hf, fill=INK)
        y += head_size + 5
    y += 2
    body_lines = wrap(draw, body, bf, w)[:max_body_lines]
    for line in body_lines:
        draw.text((x, y), line, font=bf, fill=INK)
        y += body_size + 6
    return y


def rule(draw, y, weight=2):
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=weight)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead ----
    title_f = font(SERIF_B, 60)
    draw.text((W // 2, 34), "THE WORLD TODAY", font=title_f, fill=INK,
              anchor="ma")
    date_f = font(SANS_B, 23)
    draw.text((W // 2, 112), "FRIDAY, 20 NOVEMBER 2026", font=date_f,
              fill=INK, anchor="ma")
    tag_f = font(SANS, 18)
    draw.text((W // 2, 144), "Six stories that defined the day",
              font=tag_f, fill=MUTED, anchor="ma")
    rule(draw, 176, weight=4)

    # ---- Lead story: ICJ / Myanmar ----
    y = draw_story(
        draw, MARGIN, 196, W - 2 * MARGIN,
        "JUSTICE  ·  THE HAGUE",
        "World Court: Myanmar committed genocide",
        "The International Court of Justice ruled that Myanmar committed "
        "genocide against its Rohingya minority — the first such finding "
        "against a state by the world court.",
        head_size=38, body_size=19, kicker_size=19,
        max_head_lines=2, max_body_lines=3)
    rule(draw, y + 10)

    # ---- Row 2: Shenzhen summit + Anthropic debut ----
    col_w = (W - 2 * MARGIN - 32) // 2
    y2 = y + 22
    left = draw_story(
        draw, MARGIN, y2, col_w,
        "DIPLOMACY  ·  SHENZHEN",
        "Trump, Xi and Putin hold first three-way summit",
        "The leaders of the United States, China and Russia met for the "
        "first time as a trio and signed a four-point joint declaration "
        "toward peace.",
        head_size=26, body_size=16, max_head_lines=3, max_body_lines=4)
    right = draw_story(
        draw, MARGIN + col_w + 32, y2, col_w,
        "TECH  ·  NEW YORK",
        "Anthropic soars in Nasdaq debut",
        "Shares priced at $83 closed near $97, up 17% on the AI lab's "
        "first day of trading under the ticker ANT.",
        head_size=26, body_size=16, max_head_lines=3, max_body_lines=4)
    y = max(left, right)
    rule(draw, y + 10)

    # ---- Row 3: Riyadh tower + Kyiv strikes ----
    y3 = y + 22
    left = draw_story(
        draw, MARGIN, y3, col_w,
        "CONFLICT  ·  RIYADH",
        "Houthi missile hits Riyadh's tallest tower",
        "A missile damaged the Saudi sovereign wealth fund tower in the "
        "capital's financial district, the tallest building in Riyadh.",
        head_size=26, body_size=16, max_head_lines=3, max_body_lines=4)
    right = draw_story(
        draw, MARGIN + col_w + 32, y3, col_w,
        "WAR  ·  KYIV",
        "Russian strikes hit Kyiv's bridges",
        "Overnight missile attacks on the Ukrainian capital killed eight "
        "people and injured 28 across nine regions; Kyiv said it struck "
        "a chemical plant inside Russia.",
        head_size=26, body_size=16, max_head_lines=3, max_body_lines=4)
    y = max(left, right)
    rule(draw, y + 10)

    # ---- Bottom strip: markets sell-off ----
    y4 = y + 22
    y = draw_story(
        draw, MARGIN, y4, W - 2 * MARGIN,
        "MARKETS  ·  NEW YORK",
        "Stocks fall for a fifth straight day",
        "The S&P 500 lost about 2% and Japan's Nikkei slid 4.8% as doubts "
        "over AI valuations dragged global markets lower.",
        head_size=26, body_size=16, kicker_size=16,
        max_head_lines=1, max_body_lines=2)
    rule(draw, y + 10)

    # ---- In brief: three more stories from the day ----
    y5 = y + 20
    brief_f = font(SANS_B, 16)
    item_f = font(SANS, 16)
    draw.text((MARGIN, y5), "IN BRIEF", font=brief_f, fill=ACCENT)
    y5 += 16 + 8
    briefs = [
        "Kenya discharged its last Ebola patient, 37 days after its "
        "first case.",
        "COP31 draft drops the call to phase out fossil fuels.",
        "GTA 6 launch tops $2.3 billion in sales.",
    ]
    for item in briefs:
        for line in wrap(draw, "•  " + item, item_f, W - 2 * MARGIN):
            draw.text((MARGIN, y5), line, font=item_f, fill=INK)
            y5 += 16 + 6

    # ---- Footer ----
    foot_f = font(SANS, 14)
    draw.text((W // 2, H - 24),
              "Compiled from public reporting  ·  20 November 2026",
              font=foot_f, fill=MUTED, anchor="ma")

    img.save("entry.png")
    print("wrote entry.png")


if __name__ == "__main__":
    main()
