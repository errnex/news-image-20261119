#!/usr/bin/env python3
"""News image for Thursday 19 November 2026 — make.fun news-image-20261119.

Draws a 1024x1024 newspaper-style front page with the Python standard
library only: a hand-written 5x7 bitmap font, vector shapes, and a
struct+zlib PNG encoder. No network, no clock, no randomness with an
unfixed seed: two runs write byte-identical PNGs.

Stories (all reported on 19 November 2026, checked against wire reports):
  lead   GTA VI begins its global rollout; Vice City opens, 99 on Metacritic
  gulf   US-Iran clash widens: Iran hits Kuwait and Bahrain after a US
         strike on a missile site on Qeshm Island
  summit Trump, Xi and Putin hold trilateral talks in Shenzhen at APEC
  europe EU proposes a 45bn euro loan for Ukraine, to be repaid after
         Russia pays reparations
  court  The World Court (ICJ) delivers its judgment in the Myanmar
         genocide case (The Gambia v. Myanmar, Rohingya)
  space  Voyager 1 reaches one light-day from Earth; NASA confirms
         the milestone on 19 November
  also   Nvidia stops shipping H-series chips to mainland China;
         Fed minutes point to further rate hikes
"""

import os
import struct
import zlib

W, H = 1024, 1024

# --- palette ---
PAPER = (246, 241, 231)
INK = (22, 22, 22)
NAVY = (20, 33, 61)
NAVY_DARK = (11, 16, 38)
RED = (193, 18, 31)
GOLD = (216, 164, 32)
BLUE = (29, 78, 216)
TEAL = (15, 118, 110)
PURPLE = (107, 33, 168)
WHITE = (255, 255, 255)
SKY = (43, 45, 92)
DUSK = (74, 43, 107)
SUNSET = (198, 93, 59)
NIGHT = (20, 20, 43)
GREY = (74, 74, 74)
LIGHT = (190, 195, 210)
STEEL = (200, 200, 205)
ORANGE = (230, 120, 30)
EU_BLUE = (0, 51, 153)

# --- 5x7 bitmap font: '#' is ink, ' ' is blank. Text is rendered uppercase. ---
FONT = {
    "A": [" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "B": ["#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "],
    "C": [" ####", "#    ", "#    ", "#    ", "#    ", "#    ", " ####"],
    "D": ["#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "],
    "E": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"],
    "F": ["#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "],
    "G": [" ####", "#    ", "#    ", "# ###", "#   #", "#   #", " ### "],
    "H": ["#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"],
    "I": [" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "J": ["  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "],
    "K": ["#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"],
    "L": ["#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"],
    "M": ["#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"],
    "N": ["#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"],
    "O": [" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "P": ["#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "],
    "Q": [" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"],
    "R": ["#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"],
    "S": [" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "],
    "T": ["#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "],
    "U": ["#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "],
    "V": ["#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "],
    "W": ["#   #", "#   #", "#   #", "# # #", "# # #", "# # #", " # # "],
    "X": ["#   #", " # # ", "  #  ", "  #  ", "  #  ", " # # ", "#   #"],
    "Y": ["#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "Z": ["#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"],
    "0": [" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "],
    "1": ["  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "],
    "2": [" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"],
    "3": ["#### ", "    #", "    #", " ### ", "    #", "    #", "#### "],
    "4": ["   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "],
    "5": ["#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "],
    "6": [" ### ", "#    ", "#    ", "#### ", "#   #", "#   #", " ### "],
    "7": ["#####", "    #", "   # ", "  #  ", "  #  ", "  #  ", "  #  "],
    "8": [" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "],
    "9": [" ### ", "#   #", "#   #", " ####", "    #", "    #", " ### "],
    " ": ["     ", "     ", "     ", "     ", "     ", "     ", "     "],
    ".": ["     ", "     ", "     ", "     ", "     ", "     ", "  #  "],
    ",": ["     ", "     ", "     ", "     ", "     ", "  #  ", " #   "],
    ":": ["     ", "     ", "  #  ", "     ", "  #  ", "     ", "     "],
    ";": ["     ", "     ", "  #  ", "     ", "  #  ", "  #  ", " #   "],
    "'": ["  #  ", "  #  ", "     ", "     ", "     ", "     ", "     "],
    "-": ["     ", "     ", "     ", "#####", "     ", "     ", "     "],
    "(": ["   # ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "   # "],
    ")": [" #   ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " #   "],
    "%": ["#   #", "#  # ", "   # ", "  #  ", " #   ", "#  # ", "#   #"],
    "/": ["    #", "   # ", "   # ", "  #  ", " #   ", " #   ", "#    "],
    "!": ["  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "],
    "?": [" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "],
    "&": [" ### ", "#   #", "#   #", " ##  ", "# # #", "#  # ", " ## #"],
    "+": ["     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "],
    "=": ["     ", "     ", "#####", "     ", "#####", "     ", "     "],
    '"': [" # # ", " # # ", "     ", "     ", "     ", "     ", "     "],
}

# --- canvas (RGB, row-major) ---
buf = bytearray(W * H * 3)


def put(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i], buf[i + 1], buf[i + 2] = c


def fill(x, y, w, h, c):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    for yy in range(y0, y1):
        base = yy * W * 3 + x0 * 3
        for xx in range(x0, x1):
            i = base + (xx - x0) * 3
            buf[i], buf[i + 1], buf[i + 2] = c


def border(x, y, w, h, c, t=3):
    fill(x, y, w, t, c)
    fill(x, y + h - t, w, t, c)
    fill(x, y, t, h, c)
    fill(x + w - t, y, t, h, c)


def hline(x0, x1, y, c, t=1):
    for yy in range(y, y + t):
        for xx in range(x0, x1 + 1):
            put(xx, yy, c)


def vline(x, y0, y1, c, t=1):
    for xx in range(x, x + t):
        for yy in range(y0, y1 + 1):
            put(xx, yy, c)


def line(x0, y0, x1, y1, c):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        put(x0, y0, c)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x0 += sx
        if e2 <= dx:
            err += dx
            y0 += sy


def disc(cx, cy, r, c):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                put(xx, yy, c)


def tri(x0, y0, x1, y1, x2, y2, c):
    def sign(ax, ay, bx, by, cx, cy):
        return (ax - cx) * (by - cy) - (bx - cx) * (ay - cy)

    d = sign(x0, y0, x1, y1, x2, y2)
    if d == 0:
        return
    for yy in range(min(y0, y1, y2), max(y0, y1, y2) + 1):
        for xx in range(min(x0, x1, x2), max(x0, x1, x2) + 1):
            s1 = sign(xx, yy, x0, y0, x1, y1)
            s2 = sign(xx, yy, x1, y1, x2, y2)
            s3 = sign(xx, yy, x2, y2, x0, y0)
            if (d > 0 and s1 >= 0 and s2 >= 0 and s3 >= 0) or \
               (d < 0 and s1 <= 0 and s2 <= 0 and s3 <= 0):
                put(xx, yy, c)


def text_w(s, sc):
    return len(s) * 6 * sc - sc


def draw_text(x, y, s, sc, c):
    s = s.upper()
    cx = x
    for ch in s:
        g = FONT.get(ch)
        if g is None:
            cx += 6 * sc
            continue
        for row in range(7):
            bits = g[row]
            for col in range(5):
                if bits[col] == "#":
                    fill(cx + col * sc, y + row * sc, sc, sc, c)
        cx += 6 * sc


def draw_text_c(cx, y, s, sc, c):
    draw_text(cx - text_w(s, sc) // 2, y, s, sc, c)


# --- deterministic pseudo-random (fixed seed, for stars) ---
_seed = [12345]


def rnd():
    _seed[0] = (_seed[0] * 1103515245 + 12345) & 0x7FFFFFFF
    return _seed[0]


# --- icons (drawn in a 64x64 box at ox, oy) ---
def icon_rocket(ox, oy):
    tri(ox + 26, oy + 12, ox + 38, oy + 12, ox + 32, oy + 2, STEEL)
    fill(ox + 26, oy + 12, 12, 28, STEEL)
    disc(ox + 32, oy + 22, 4, BLUE)
    tri(ox + 26, oy + 32, ox + 18, oy + 44, ox + 26, oy + 40, RED)
    tri(ox + 38, oy + 32, ox + 46, oy + 44, ox + 38, oy + 40, RED)
    tri(ox + 28, oy + 40, ox + 36, oy + 40, ox + 32, oy + 54, ORANGE)
    tri(ox + 30, oy + 40, ox + 34, oy + 40, ox + 32, oy + 48, GOLD)
    hline(ox + 8, ox + 16, oy + 58, GREY, 2)
    hline(ox + 48, ox + 56, oy + 58, GREY, 2)


def icon_flags(ox, oy):
    for px, col in ((14, RED), (32, (200, 160, 30)), (50, WHITE)):
        vline(ox + px, oy + 10, oy + 54, INK, 2)
        fill(ox + px, oy + 10, 15, 12, col)
    fill(ox + 50, oy + 16, 15, 4, (0, 51, 153))
    fill(ox + 50, oy + 20, 15, 3, RED)
    hline(ox + 8, ox + 62, oy + 56, INK, 2)


def icon_eu(ox, oy):
    disc(ox + 32, oy + 32, 26, EU_BLUE)
    for dx, dy in ((18, 0), (13, 13), (0, 18), (-13, 13),
                   (-18, 0), (-13, -13), (0, -18), (13, -13)):
        disc(ox + 32 + dx, oy + 32 + dy, 2, GOLD)


def icon_scales(ox, oy):
    vline(ox + 32, oy + 8, oy + 52, INK, 3)
    hline(ox + 12, ox + 52, oy + 10, INK, 3)
    line(ox + 14, oy + 10, ox + 8, oy + 30, INK)
    line(ox + 14, oy + 10, ox + 20, oy + 30, INK)
    tri(ox + 6, oy + 30, ox + 22, oy + 30, ox + 14, oy + 40, GOLD)
    line(ox + 50, oy + 10, ox + 44, oy + 30, INK)
    line(ox + 50, oy + 10, ox + 56, oy + 30, INK)
    tri(ox + 42, oy + 30, ox + 58, oy + 30, ox + 50, oy + 40, GOLD)
    disc(ox + 32, oy + 10, 3, INK)
    hline(ox + 20, ox + 44, oy + 56, INK, 3)


# --- story panel ---
def panel(x, y, w, h, accent, tag, head, sub, icon=None):
    fill(x, y, w, h, WHITE)
    border(x, y, w, h, INK, 3)
    fill(x + 3, y + 3, w - 6, 10, accent)
    draw_text(x + 16, y + 24, tag, 2, accent)
    yy = y + 52
    for ln in head:
        draw_text(x + 16, yy, ln, 3, INK)
        yy += 28
    yy = y + 118
    for ln in sub:
        draw_text(x + 16, yy, ln, 2, GREY)
        yy += 20
    if icon is not None:
        icon(x + w - 80, y + 16)


# --- PNG encoder (truecolour RGB, filter 0, zlib level 9) ---
def png_bytes():
    def chunk(typ, data):
        out = struct.pack(">I", len(data)) + typ + data
        out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    raw = bytearray()
    for yy in range(H):
        raw.append(0)
        raw += buf[yy * W * 3:(yy + 1) * W * 3]
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    fill(0, 0, W, H, PAPER)

    # --- masthead ---
    fill(0, 0, W, 116, NAVY)
    draw_text_c(512, 16, "THE WORLD TODAY", 2, GOLD)
    draw_text_c(512, 42, "19 NOVEMBER 2026", 6, WHITE)
    draw_text_c(512, 92, "THURSDAY - WORLD NEWS IN ONE IMAGE", 2, LIGHT)

    # --- lead: GTA VI ---
    lx, ly, lw, lh = 16, 132, 992, 276
    fill(lx, ly, lw, lh, WHITE)
    border(lx, ly, lw, lh, INK, 3)
    ax, ay, aw, ah = lx + 3, ly + 3, 353, 270
    fill(ax, ay, aw, ah, SKY)
    fill(ax, ay + 158, aw, 22, SUNSET)
    fill(ax, ay + 180, aw, ah - 180, DUSK)
    disc(ax + 264, ay + 78, 36, GOLD)
    disc(ax + 264, ay + 78, 28, (232, 190, 60))
    # skyline silhouettes
    for bx, bw, bh in ((0, 40, 68), (40, 36, 98), (76, 44, 58), (120, 30, 88),
                       (150, 52, 48), (202, 34, 108), (236, 40, 63),
                       (276, 36, 93), (312, 41, 53)):
        fill(ax + bx, ay + ah - bh, bw, bh, NIGHT)
    for wx, wy in ((12, 200), (52, 180), (88, 220), (128, 190), (162, 210),
                   (214, 175), (248, 205), (288, 185), (324, 215)):
        fill(ax + wx, ay + wy, 4, 4, GOLD)
    draw_text(ax + 52, ay + 104, "VI", 8, (20, 20, 40))
    draw_text(ax + 48, ay + 100, "VI", 8, WHITE)
    # lead text
    tx = lx + 388
    draw_text(tx, ly + 20, "CULTURE - GAMING", 2, RED)
    fill(tx, ly + 40, 120, 4, RED)
    draw_text(tx, ly + 58, "GTA VI LAUNCHES", 4, INK)
    draw_text(tx, ly + 94, "WORLDWIDE", 4, INK)
    draw_text(tx, ly + 142, "VICE CITY OPENS AS THE GAME", 2, GREY)
    draw_text(tx, ly + 166, "ROLLS OUT GLOBALLY, 99 ON METACRITIC", 2, GREY)
    draw_text(tx, ly + 206, "LAUNCHES AT MIDNIGHT IN EACH", 2, INK)
    draw_text(tx, ly + 230, "TIME ZONE, STARTING IN", 2, INK)
    draw_text(tx, ly + 254, "AUSTRALIA AT 12AM LOCAL", 2, INK)

    # --- grid: four stories ---
    panel(16, 424, 488, 204, RED, "MIDDLE EAST",
          ["US-IRAN CLASH", "WIDENS IN GULF"],
          ["IRAN HITS KUWAIT AND BAHRAIN",
           "AFTER US STRIKE ON QESHM"], icon_rocket)
    panel(520, 424, 488, 204, BLUE, "DIPLOMACY",
          ["TRUMP, XI, PUTIN", "MEET IN SHENZHEN"],
          ["TRILATERAL TALKS AT APEC",
           "NUCLEAR ARMS AND IRAN"], icon_flags)
    panel(16, 644, 488, 204, TEAL, "EUROPE",
          ["EU PLANS 45BN", "UKRAINE LOAN"],
          ["TO BE REPAID AFTER RUSSIA",
           "PAYS REPARATIONS"], icon_eu)
    panel(520, 644, 488, 204, PURPLE, "JUSTICE",
          ["WORLD COURT", "RULES ON MYANMAR"],
          ["ROHINGYA GENOCIDE CASE",
           "JUDGMENT DELIVERED TODAY"], icon_scales)

    # --- bottom band: Voyager 1 + also today ---
    bx, by, bw, bh = 16, 864, 992, 144
    fill(bx, by, bw, bh, NAVY_DARK)
    for _ in range(60):
        sx = bx + 8 + rnd() % (bw - 16)
        sy = by + 8 + rnd() % (bh - 16)
        put(sx, sy, GOLD if rnd() % 5 == 0 else WHITE)
    # probe
    fill(44, 918, 26, 14, STEEL)
    tri(70, 916, 70, 934, 84, 925, GOLD)
    line(44, 925, 30, 925, STEEL)
    line(30, 925, 24, 918, STEEL)
    line(30, 925, 24, 932, STEEL)
    for dx in range(0, 84, 12):
        hline(96 + dx, 102 + dx, 916, LIGHT, 2)
    draw_text(200, by + 16, "SPACE", 2, GOLD)
    draw_text(200, by + 40, "VOYAGER 1 REACHES", 3, WHITE)
    draw_text(200, by + 66, "ONE LIGHT-DAY", 3, WHITE)
    draw_text(200, by + 96, "NASA TO CONFIRM THE MILESTONE", 2, LIGHT)
    draw_text(200, by + 114, "TODAY, AFTER ALMOST 50 YEARS", 2, LIGHT)
    vline(648, by + 16, by + bh - 16, (90, 95, 120), 2)
    draw_text(672, by + 16, "ALSO TODAY", 2, GOLD)
    draw_text(672, by + 40, "NVIDIA STOPS H-CHIP", 2, WHITE)
    draw_text(672, by + 58, "SHIPMENTS TO CHINA", 2, WHITE)
    draw_text(672, by + 86, "FED MINUTES POINT TO", 2, WHITE)
    draw_text(672, by + 104, "MORE RATE HIKES", 2, WHITE)

    # --- footer line ---
    draw_text_c(512, 1013, "ALL EVENTS AS REPORTED ON THURSDAY 19 NOVEMBER 2026",
                1, GREY)

    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "entry.png"), "wb") as f:
        f.write(png_bytes())


if __name__ == "__main__":
    main()
