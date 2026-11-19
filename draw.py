#!/usr/bin/env python3
"""
THE DAILY SUM — one image that sums up the world news of Thursday 19 November 2026.

Drawn with PIL at 2x and downscaled to 1024x1024 for clean edges.
Layout: masthead, a big red date band, one lead story (Shenzhen summit),
a row of three story cards, a row of three horizontal cards, and an
"also today" footer strip.

News selection (all reported on 19 Nov 2026, cross-checked across
Reuters/USA Today/The Times/BBC/NDTV/Just Security roundups of the day):
  LEAD  Trump, Xi & Putin hold their first-ever three-way summit in Shenzhen
        (APEC sidelines); 90-minute talks, joint "peace declaration" —
        UN reform, nuclear-risk reduction, more oil supply; Ukraine not named.
  1     ICJ rules Myanmar committed genocide against the Rohingya —
        first ruling of its kind by the UN's highest court (Gambia v. Myanmar).
  2     Ukraine strikes the Crimean (Kerch) Bridge for the third time this
        week; traffic halted; Putin vows a "much more painful" response.
  3     Houthi rocket debris damages the PIF Tower in Riyadh; Iran trades
        strikes with Gulf states after US strikes on Qeshm Island.
  4     Anthropic's stock-market debut raises a record $81bn, valuing the
        AI company at about $1.5 trillion — the biggest IPO in history.
  5     COP31 in Antalya: ministers in a final push to unblock a climate deal.
  6     US midterms: Democrats take the House and Senate; Hakeem Jeffries set
        to be the first Black House Speaker; Musk breaks: "I'm not MAGA."
  ALSO  Van Gogh sells for a record $190.4m; measles returns to the US,
        ending 26 years of elimination; Bangladesh unrest — Yunus home torched.
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

S = 2                      # supersample factor
W = 1024 * S
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------- palette ----------
PAPER   = (247, 243, 234)
CARD    = (255, 253, 247)
INK     = (20, 24, 38)
RED     = (178, 34, 40)
GOLD    = (242, 193, 78)
WHITE   = (255, 255, 255)

F = "/usr/share/fonts/truetype/"
def font(path, size):
    return ImageFont.truetype(F + path, size * S)

SERIF_B   = lambda s: font("liberation/LiberationSerif-Bold.ttf", s)
BLACK     = lambda s: font("noto/NotoSansDisplay-Black.ttf", s)
XBOLD     = lambda s: font("noto/NotoSans-ExtraBold.ttf", s)
BOLD      = lambda s: font("noto/NotoSans-Bold.ttf", s)
REG       = lambda s: font("noto/NotoSans-Regular.ttf", s)

img = Image.new("RGB", (W, W), PAPER)
d = ImageDraw.Draw(img)

def X(v):
    return v * S

def rect(x, y, w, h, fill=None, outline=None, width=1):
    d.rectangle([X(x), X(y), X(x + w), X(y + h)], fill=fill, outline=outline, width=width * S)

def line(points, fill=INK, width=2):
    d.line([(X(a), X(b)) for a, b in points], fill=fill, width=width * S)

def text(x, y, s, fnt, fill=INK, anchor="la"):
    d.text((X(x), X(y)), s, font=fnt, fill=fill, anchor=anchor)

def textw(s, fnt):
    return d.textlength(s, font=fnt) / S

def wrap(s, fnt, maxw):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if textw(t, fnt) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

def block(x, y, s, fnt, maxw, lh, fill=INK):
    """Draw wrapped text; return the y just below it."""
    for i, l in enumerate(wrap(s, fnt, maxw)):
        text(x, y + i * lh, l, fnt, fill)
    return y + len(wrap(s, fnt, maxw)) * lh

# ================= masthead =================
text(28, 16, "THE DAILY SUM", SERIF_B(52))
text(996, 30, "ONE IMAGE · THE WHOLE DAY'S NEWS", BOLD(16), anchor="ra")
text(996, 56, "WORLD EDITION — No. 19", REG(15), fill=(90, 90, 90), anchor="ra")
rect(28, 84, 968, 3, fill=INK)

# ================= date band =================
rect(28, 96, 968, 58, fill=RED)
text(512, 106, "THURSDAY · 19 NOVEMBER 2026", BLACK(41), fill=WHITE, anchor="ma")

# ================= lead story =================
LY, LH = 166, 288
rect(28, LY, 968, LH, fill=CARD, outline=INK, width=2)

IX, IW = 28, 392
for i, c in enumerate([(38, 74, 116), (47, 88, 132), (58, 103, 150), (72, 120, 168)]):
    rect(IX, LY + i * 52, IW, 52, fill=c)
d.ellipse([X(IX + 300), X(LY + 24), X(IX + 352), X(LY + 76)], fill=(250, 214, 120))
sil = (16, 34, 56)
for bx, bw, bh in [(0, 46, 96), (52, 34, 140), (92, 52, 78), (150, 30, 168),
                   (186, 58, 104), (250, 36, 128), (292, 48, 84), (346, 46, 118)]:
    rect(IX + bx, LY + LH - 64 - bh, bw, bh + 64, fill=sil)
for wx in range(IX + 8, IX + IW - 8, 17):
    for wy in range(LY + LH - 190, LY + LH - 78, 21):
        if (wx * 7 + wy * 13) % 5 == 0:
            rect(wx, wy, 5, 7, fill=(250, 220, 130))
rect(IX, LY + LH - 64, IW, 64, fill=(10, 22, 38))

def flag(x, y, w, h, kind):
    line([(x, y - 6), (x, y + 112)], fill=(230, 230, 230), width=3)
    if kind == "us":
        for i in range(7):
            rect(x + 2, y + i * (h // 7), w, h // 7 + 1,
                 fill=(178, 34, 52) if i % 2 == 0 else WHITE)
        rect(x + 2, y, w * 0.45, (h // 7) * 4, fill=(38, 54, 120))
        for r_ in range(3):
            for c_ in range(4):
                d.ellipse([X(x + 6 + c_ * 9), X(y + 4 + r_ * 8),
                           X(x + 9 + c_ * 9), X(y + 7 + r_ * 8)], fill=WHITE)
    elif kind == "cn":
        rect(x + 2, y, w, h, fill=(222, 41, 16))
        def star(cx, cy, r_):
            pts = []
            for i in range(10):
                ang = -math.pi / 2 + i * math.pi / 5
                rr = r_ if i % 2 == 0 else r_ * 0.42
                pts.append((X(cx + rr * math.cos(ang)), X(cy + rr * math.sin(ang))))
            d.polygon(pts, fill=(255, 222, 0))
        star(x + 15, y + 13, 8); star(x + 30, y + 7, 3.4)
        star(x + 33, y + 14, 3.4); star(x + 33, y + 22, 3.4); star(x + 30, y + 29, 3.4)
    else:
        rect(x + 2, y, w, h // 3 + 1, fill=WHITE)
        rect(x + 2, y + h // 3, w, h // 3 + 1, fill=(30, 70, 160))
        rect(x + 2, y + 2 * h // 3, w, h // 3 + 1, fill=(205, 40, 45))

fx = IX + 58
for i, k in enumerate(["us", "cn", "ru"]):
    flag(fx + i * 104, LY + 92, 62, 40, k)
rect(IX + 46, LY + 230, 300, 10, fill=(240, 236, 226))
for i in range(3):
    cx = IX + 96 + i * 100
    d.ellipse([X(cx - 13), X(LY + 188), X(cx + 13), X(LY + 214)], fill=(240, 205, 170))
    d.polygon([(X(cx - 24), X(LY + 232)), (X(cx + 24), X(LY + 232)),
               (X(cx + 13), X(LY + 212)), (X(cx - 13), X(LY + 212))], fill=(24, 28, 40))
    rect(cx - 3, LY + 214, 6, 12, fill=(178, 34, 40) if i != 1 else (30, 70, 160))

TX = 448
text(TX, LY + 16, "SHENZHEN, CHINA — APEC SUMMIT", BOLD(16), fill=RED)
block(TX, LY + 44, "TRUMP, XI & PUTIN HOLD FIRST-EVER THREE-WAY SUMMIT",
      BLACK(40), 520, 47)
rect(TX, LY + 192, 520, 2, fill=(200, 195, 180))
block(TX, LY + 204,
      "90 minutes of talks end in a joint “peace declaration”: reform the UN, "
      "cut nuclear risks, supply more oil. Ukraine was not mentioned.",
      REG(20), 520, 27)

# ================= icons =================
def icon_scales(cx, cy):
    line([(cx, cy - 30), (cx, cy + 26)], fill=GOLD, width=4)
    line([(cx - 30, cy - 22), (cx + 30, cy - 22)], fill=GOLD, width=4)
    d.ellipse([X(cx - 5), X(cy - 36), X(cx + 5), X(cy - 26)], fill=GOLD)
    for sgn in (-1, 1):
        px = cx + sgn * 30
        line([(px, cy - 22), (px - 11, cy + 6)], fill=GOLD, width=2)
        line([(px, cy - 22), (px + 11, cy + 6)], fill=GOLD, width=2)
        d.pieslice([X(px - 15), X(cy - 2), X(px + 15), X(cy + 16)], 0, 180, fill=GOLD)
    line([(cx - 16, cy + 30), (cx + 16, cy + 30)], fill=GOLD, width=4)

def icon_bridge(cx, cy):
    deck = (232, 228, 216)
    for px in (cx - 52, cx + 44):
        rect(px, cy - 30, 7, 52, fill=deck)
    line([(cx - 78, cy + 22), (cx - 14, cy + 22)], fill=deck, width=5)
    line([(cx + 30, cy + 22), (cx + 78, cy + 22)], fill=deck, width=5)
    d.polygon([(X(cx - 12), X(cy + 22)), (X(cx + 28), X(cy + 22)), (X(cx + 18), X(cy + 40))],
              fill=deck, outline=(240, 150, 60), width=2 * S)
    for a in range(5):
        ang = -math.pi * (0.15 + 0.175 * a)
        line([(cx + 8 + 6 * math.cos(ang), cy + 16 + 6 * math.sin(ang)),
              (cx + 8 + 13 * math.cos(ang), cy + 16 + 13 * math.sin(ang))],
             fill=(240, 150, 60), width=2)
    for px, sgn in ((cx - 49, 1), (cx + 47, -1)):
        for t in (0.3, 0.55, 0.8):
            line([(px + 3, cy - 28), (px + 3 + sgn * 62 * t, cy + 20)], fill=deck, width=1)
    for i in range(4):
        d.arc([X(cx - 66 + i * 34), X(cy + 30), X(cx - 42 + i * 34), X(cy + 44)], 180, 360,
              fill=(150, 200, 235), width=2 * S)

def icon_tower(cx, cy):
    sand = (232, 220, 195)
    d.polygon([(X(cx - 16), X(cy + 32)), (X(cx - 9), X(cy - 30)), (X(cx), X(cy - 38)),
               (X(cx + 9), X(cy - 30)), (X(cx + 16), X(cy + 32))], fill=sand)
    rect(cx - 30, cy + 32, 60, 4, fill=sand)
    for t in [i / 14 for i in range(15)]:
        px = cx + 62 - 74 * t
        py = cy - 34 + 58 * t * t
        if int(t * 14) % 2 == 0:
            d.ellipse([X(px - 2), X(py - 2), X(px + 2), X(py + 2)], fill=WHITE)
    for a in range(8):
        ang = a * math.pi / 4
        line([(cx + 10 * math.cos(ang), cy - 26 + 10 * math.sin(ang)),
              (cx + 17 * math.cos(ang), cy - 26 + 17 * math.sin(ang))], fill=GOLD, width=2)

def icon_ipo(cx, cy):
    for i, bh in enumerate((14, 24, 36)):
        rect(cx - 38 + i * 24, cy + 26 - bh, 15, bh, fill=(120, 200, 250))
    pts = [(cx - 40, cy + 6), (cx - 16, cy - 8), (cx + 6, cy - 3), (cx + 36, cy - 26)]
    line(pts, fill=GOLD, width=4)
    d.polygon([(X(cx + 36), X(cy - 26)), (X(cx + 23), X(cy - 25)), (X(cx + 35), X(cy - 13))],
              fill=GOLD)
    text(cx + 18, cy + 8, "$", BLACK(24), fill=WHITE)

def icon_globe(cx, cy):
    d.ellipse([X(cx - 26), X(cy - 26), X(cx + 26), X(cy + 26)], outline=(190, 240, 200), width=3 * S)
    d.ellipse([X(cx - 10), X(cy - 26), X(cx + 10), X(cy + 26)], outline=(190, 240, 200), width=2 * S)
    line([(cx - 26, cy), (cx + 26, cy)], fill=(190, 240, 200), width=2)
    d.pieslice([X(cx + 2), X(cy - 40), X(cx + 38), X(cy - 6)], 180, 270, fill=(110, 220, 130))
    line([(cx + 6, cy - 8), (cx + 30, cy - 32)], fill=(110, 220, 130), width=2)

def icon_capitol(cx, cy):
    w_ = WHITE
    rect(cx - 44, cy + 22, 88, 6, fill=w_)
    for i in range(6):
        rect(cx - 40 + i * 14, cy + 4, 5, 18, fill=w_)
    rect(cx - 46, cy - 2, 92, 6, fill=w_)
    d.pieslice([X(cx - 24), X(cy - 34), X(cx + 24), X(cy + 14)], 180, 360, fill=w_)
    rect(cx - 2, cy - 42, 4, 10, fill=w_)
    d.ellipse([X(cx - 3), X(cy - 46), X(cx + 3), X(cy - 40)], fill=w_)

# ================= story cards (icon strip on top) =================
def card_v(x, y, w, h, icon_bg, icon_fn, kicker, head, sub):
    rect(x, y, w, h, fill=CARD, outline=INK, width=2)
    rect(x, y, w, 86, fill=icon_bg)
    icon_fn(x + w // 2, y + 43)
    text(x + 14, y + 95, kicker, BOLD(13), fill=RED)
    end = block(x + 14, y + 113, head, BLACK(23), w - 28, 28)
    block(x + 14, end + 7, sub, REG(17), w - 28, 22)

RY, RH, CW = 468, 258, 309
card_v(28, RY, CW, RH, (31, 58, 95), icon_scales,
       "THE HAGUE — UN COURT",
       "MYANMAR COMMITTED GENOCIDE, ICJ RULES",
       "First ruling of its kind — the Rohingya case brought by Gambia.")
card_v(357, RY, CW, RH, (63, 84, 104), icon_bridge,
       "UKRAINE WAR",
       "CRIMEAN BRIDGE HIT — 3RD TIME THIS WEEK",
       "Kerch Strait traffic halted. Putin vows a “much more painful” response.")
card_v(686, RY, CW, RH, (109, 26, 26), icon_tower,
       "MIDDLE EAST",
       "MISSILES OVER THE GULF",
       "Houthi rocket debris damages a Riyadh tower; Iran trades strikes with Gulf states.")

# ================= story cards (icon panel on the left) =================
def card_h(x, y, w, h, icon_bg, icon_fn, kicker, head, sub):
    rect(x, y, w, h, fill=CARD, outline=INK, width=2)
    rect(x, y, 92, h, fill=icon_bg)
    icon_fn(x + 46, y + h // 2)
    text(x + 106, y + 13, kicker, BOLD(12), fill=RED)
    end = block(x + 106, y + 31, head, BLACK(21), w - 120, 25)
    block(x + 106, end + 6, sub, REG(16), w - 120, 21)

R3, R3H = 740, 206
card_h(28, R3, CW, R3H, (55, 48, 163), icon_ipo,
       "TECH — MARKETS",
       "ANTHROPIC'S RECORD $81BN IPO",
       "Biggest debut in history — the AI firm is valued at $1.5 trillion.")
card_h(357, R3, CW, R3H, (22, 101, 52), icon_globe,
       "CLIMATE — ANTALYA",
       "COP31 GOES DOWN TO THE WIRE",
       "Ministers race to unblock a final climate deal in Antalya, Turkey.")
card_h(686, R3, CW, R3H, (30, 58, 138), icon_capitol,
       "WASHINGTON",
       "DEMOCRATS TAKE BOTH HOUSES",
       "Jeffries set to be first Black Speaker. Musk: “I'm not MAGA.”")

# ================= footer =================
rect(28, 960, 968, 44, fill=INK)
text(42, 972, "ALSO TODAY", XBOLD(17), fill=GOLD)
foot = ("Van Gogh: record $190.4m · Measles returns to US after 26 years "
        "· Bangladesh: Yunus home torched")
text(192, 973, foot, REG(16), fill=WHITE)

img = img.resize((1024, 1024), Image.LANCZOS)
img.save(OUT)
print("saved", OUT, os.path.getsize(OUT), "bytes; footer width:", textw(foot, REG(16)))
