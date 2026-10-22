from PIL import Image, ImageDraw, ImageFont

W, H = 200, 135          # drawing units
S = 32                    # px per unit while drawing (downsampled 2x at the end)
img = Image.new("RGB", (W * S, H * S), "white")
d = ImageDraw.Draw(img)
LW = int(S * 0.13)
INK = (20, 30, 60)
HOT = (190, 30, 30)
COLD = (30, 70, 180)
GRY = (110, 110, 110)


def F(size, bold=False):
    name = "arialbd.ttf" if bold else "arial.ttf"
    return ImageFont.truetype("C:/Windows/Fonts/" + name, int(size * S))


def P(x, y):
    return (x * S, (H - y) * S)


def line(pts, col=INK, w=LW):
    pp = [P(*p) for p in pts]
    d.line(pp, fill=col, width=w, joint="curve")
    for p in (pp[0], pp[-1]):
        d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=col)


def dot(x, y, col=INK):
    px, py = P(x, y)
    r = S * 0.32
    d.ellipse([px - r, py - r, px + r, py + r], fill=col)


def text(x, y, s, size=1.6, col=INK, anchor="la", bold=False):
    d.text(P(x, y), s, fill=col, font=F(size, bold), anchor=anchor)


def res(x, y, label, val, col=INK, vertical=False, lab_above=True):
    """box resistor centred at x,y; 8 long"""
    L, Wd = 8, 2.6
    if vertical:
        d.rectangle([*P(x - Wd / 2, y + L / 2), *P(x + Wd / 2, y - L / 2)], outline=col, width=LW)
        text(x + 2.2, y + 0.3, label, 1.5, col, "lm", True)
        text(x + 2.2, y - 1.4, val, 1.3, GRY, "lm")
    else:
        d.rectangle([*P(x - L / 2, y + Wd / 2), *P(x + L / 2, y - Wd / 2)], outline=col, width=LW)
        ty = y + 2.0 if lab_above else y - 5.2
        text(x, ty + 1.6, label, 1.5, col, "mm", True)
        text(x, ty - 0.1, val, 1.3, GRY, "mm")


def cap(x, y, label, val, vertical=False, col=INK):
    g, h = 0.9, 2.6
    if vertical:
        line([(x - h, y + g), (x + h, y + g)], col)
        line([(x - h, y - g), (x + h, y - g)], col)
        text(x + 3.4, y + 0.3, label, 1.5, col, "lm", True)
        text(x + 3.4, y - 1.4, val, 1.3, GRY, "lm")
    else:
        line([(x - g, y + h), (x - g, y - h)], col)
        line([(x + g, y + h), (x + g, y - h)], col)
        text(x, y + 3.2, label, 1.5, col, "mm", True)
        text(x, y + 4.8, val, 1.3, GRY, "mm")


def gnd(x, y):
    line([(x, y), (x, y - 1.5)])
    line([(x - 1.8, y - 1.5), (x + 1.8, y - 1.5)])
    line([(x - 1.1, y - 2.3), (x + 1.1, y - 2.3)])
    line([(x - 0.4, y - 3.1), (x + 0.4, y - 3.1)])


def opamp(cx, cy, name, part, plus_top=False, w=11, h=13):
    """triangle pointing right; returns (inA, inB, out) coordinates; inputs at +-h/4"""
    x0, x1 = cx - w / 2, cx + w / 2
    pts = [P(x0, cy + h / 2), P(x0, cy - h / 2), P(x1, cy)]
    d.polygon(pts, outline=INK, fill=(250, 250, 235))
    d.line(pts + [pts[0]], fill=INK, width=LW)
    top, bot = (cy + h / 4, cy - h / 4)
    plus_y, minus_y = (top, bot) if plus_top else (bot, top)
    text(x0 + 1.0, plus_y, "+", 2.0, INK, "lm", True)
    text(x0 + 1.0, minus_y, "\u2212", 2.0, INK, "lm", True)
    text(cx - 1.2, cy + h / 2 + 1.2, name, 1.7, INK, "mm", True)
    text(cx - 1.2, cy - h / 2 - 1.6, part, 1.3, GRY, "mm")
    return (x0, plus_y), (x0, minus_y), (x1, cy)


# ---------------------------------------------------------------- title
text(3, 132, "Mono Subwoofer Output for a Fully Balanced Integrated Amplifier  -  XLR + RCA", 3.0, INK, "la", True)
text(3, 128.2, "Reference schematic  |  tapped AFTER the volume control (sub level follows main volume)  |  "
     "L+R balanced summing -> phase -> 80/100/120 Hz low-pass -> buffered XLR + differential RCA", 1.6, GRY)

# ---------------------------------------------------------------- stage frames
def frame(x0, y0, x1, y1, title):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=(150, 160, 190), width=int(LW * 0.7))
    text(x0 + 1, y1 - 0.8, title, 1.9, (60, 80, 150), "la", True)


frame(1, 28, 62, 124, "STAGE 1  Balanced L+R summing")
frame(64, 28, 83, 124, "STAGE 2")
frame(85, 28, 143, 124, "STAGE 3  2nd-order Butterworth low-pass (balanced)")
frame(145, 28, 199, 124, "STAGE 4  Output buffers / drivers")

# ================================================================ STAGE 1
def sum_row(yc, tag, col, lname, rname, rf_ref, r_refs, u_name, pin_note):
    # yc: row centre
    yl, yr = yc + 12, yc + 6          # L and R input rows
    xin = 2
    text(xin, yl + 1.2, lname, 1.9, col, "la", True)
    text(xin, yr + 1.2, rname, 1.9, col, "la", True)
    a = opamp(46, yc, u_name, "OPA1612 (dual)", plus_top=False)
    plus, minus, out = a
    # input resistors
    xr = 17
    res(xr, yl, r_refs[0], "10k 0.1%", col, lab_above=True)
    line([(xin + 6.5, yl), (xr - 4, yl)], col)
    res(xr, yr, r_refs[1], "10k 0.1%", col, lab_above=True)
    # SW1 contact (right channel mono/stereo)
    line([(xin + 6.5, yr), (xr - 4, yr)], col)
    # summing bus
    xb = 29
    line([(xr + 4, yl), (xb, yl), (xb, minus[1])], col)
    line([(xr + 4, yr), (xb, yr)], col)
    dot(xb, yr, col)
    line([(xb, minus[1]), minus], col)
    # feedback
    yf = yc + 19.5
    res(46, yf, rf_ref, "4.99k 0.1%", col, lab_above=True)
    line([(xb, yl), (xb, yf), (46 - 4, yf)], col)
    line([(46 + 4, yf), (out[0] + 4.5, yf), (out[0] + 4.5, out[1])], col)
    line([out, (out[0] + 4.5, out[1])], col)
    dot(out[0] + 4.5, out[1], col)
    # Cf 33pF in parallel with Rf
    cfy = yf + 5.2
    line([(xb + 3, yf), (xb + 3, cfy), (36.8, cfy)], col)
    d.line([*P(36.8, cfy + 1.8), *P(36.8, cfy - 1.8)], fill=col, width=LW)
    d.line([*P(38.4, cfy + 1.8), *P(38.4, cfy - 1.8)], fill=col, width=LW)
    line([(38.4, cfy), (out[0] + 4.5, cfy), (out[0] + 4.5, yf)], col)
    dot(xb + 3, yf, col)
    text(37.6, cfy + 3.0, "Cf 33p C0G", 1.3, GRY, "mm")
    # + input bias resistor (R_in || R_in || Rf)
    line([plus, (plus[0] - 6, plus[1])], col)
    res(plus[0] - 6, plus[1] - 4.5, "Rb", "2.49k", col, vertical=True)
    line([(plus[0] - 6, plus[1]), (plus[0] - 6, plus[1] - 0.5)], col)
    line([(plus[0] - 6, plus[1] - 8.5), (plus[0] - 6, plus[1] - 9.5)], col)
    gnd(plus[0] - 6, plus[1] - 9.5)
    text(out[0] + 6.0, out[1] - 1.0, pin_note, 1.4, col, "la", True)
    return out


outH = sum_row(88, "H", HOT, "L +  (Hot)", "R +  (Hot)", "Rf1", ("R1", "R2"), "U1A", "")
outC = sum_row(43, "C", COLD, "L \u2212  (Cold)", "R \u2212  (Cold)", "Rf2", ("R3", "R4"), "U1B", "")
text(2, 121.6, "Balanced inputs from the volume\nstage (post-volume)", 1.3, GRY, "la")

# SW1 mono/stereo note
d.rectangle([*P(3, 74.5), *P(33, 66.5)], outline=(200, 120, 20), width=int(LW * .7))
text(18, 72.6, "SW1  MONO / STEREO  (ganged to R1..R4 nodes)", 1.3, (170, 90, 10), "mm", True)
text(18, 70.4, "MONO: L and R summed in one bus.", 1.25, GRY, "mm")
text(18, 68.3, "STEREO: R-side goes to an identical chain -> SUB OUT 2", 1.25, GRY, "mm")

# gain annotation
text(31.5, 31.0, "Gain per input = Rf/R = 0.5  ->  correlated bass (L=R) = 0 dB, i.e. (L+R)/2.", 1.25, GRY)
text(31.5, 29.2, "Using 10k/0.1% and Rf 4.99k absorbs the +6 dB of a plain sum. Stage polarity is inverting (both legs).", 1.25, GRY)

# ================================================================ STAGE 2 : phase switch
d.rectangle([*P(67, 112), *P(80, 40)], outline=(200, 120, 20), width=int(LW * .7))
text(73.5, 110.0, "SW2", 1.8, (170, 90, 10), "mm", True)
text(73.5, 107.6, "PHASE", 1.5, (170, 90, 10), "mm", True)
text(73.5, 105.4, "0\u00b0 / 180\u00b0", 1.5, (170, 90, 10), "mm", True)
xl, xr2 = 67, 80
line([(outH[0] + 4.5, outH[1]), (xl, outH[1])], HOT)
line([(outC[0] + 4.5, outC[1]), (xl, outC[1])], COLD)
# DPDT : straight (0 deg) and crossed (180 deg)
line([(xl, outH[1]), (xr2, outH[1])], HOT)
line([(xl, outC[1]), (xr2, outC[1])], COLD)
d.line([*P(xl + 3, outH[1]), *P(xr2 - 3, outC[1])], fill=(130, 130, 130), width=LW)
d.line([*P(xl + 3, outC[1]), *P(xr2 - 3, outH[1])], fill=(130, 130, 130), width=LW)
text(73.5, 66.0, "0\u00b0: straight", 1.2, GRY, "mm")
text(73.5, 64.3, "180\u00b0: Hot/Cold", 1.2, GRY, "mm")
text(73.5, 62.6, "crossed (DPDT)", 1.2, GRY, "mm")
text(73.5, 59.4, "relay or toggle,", 1.2, GRY, "mm")
text(73.5, 57.7, "DC-blocked path", 1.2, GRY, "mm")
text(73.5, 56.0, "keeps it silent", 1.2, GRY, "mm")

# ================================================================ STAGE 3 : LPF
def lpf(yc, col, tag, ua):
    xin = 80
    y = yc
    line([(xin, y), (88, y)], col)
    res(92, y, "R5" if tag == "H" else "R7", "10k 0.1%", col)
    line([(96, y), (99, y)], col)
    dot(99, y, col)
    res(103, y, "R6" if tag == "H" else "R8", "10k 0.1%", col)
    line([(107, y), (110, y)], col)
    dot(110, y, col)
    plus, minus, out = opamp(121, y, ua, "OPA1612 (dual)", plus_top=True)
    line([(110, y), (110, plus[1]), plus], col)
    # C2 to ground (switched value)
    line([(110, y), (110, y - 5.0)], col)
    cap(110, y - 7.0, "C2" if tag == "H" else "C4", "150n/110n/100n", vertical=True, col=col)
    line([(110, y - 8.1), (110, y - 11.5)], col)
    gnd(110, y - 11.5)
    # C1 feedback from mid node to output
    yfb = y + 12.0
    line([(99, y), (99, yfb), (102, yfb)], col)
    cap(105.5, yfb, "", "", col=col)
    line([(109.5, yfb), (130, yfb), (130, out[1])], col)
    text(105.5, yfb + 3.2, "C1" if tag == "H" else "C3", 1.5, col, "mm", True)
    text(105.5, yfb + 4.9, "270n/220n/180n", 1.3, GRY, "mm")
    # unity-gain feedback
    line([minus, (minus[0] - 2.5, minus[1]), (minus[0] - 2.5, y - 8.0), (130, y - 8.0), (130, out[1])], col)
    line([out, (130, out[1])], col)
    dot(130, out[1], col)
    dot(130, yfb - 0.0, col) if False else None
    return (130, out[1])


lpH = lpf(outH[1], HOT, "H", "U2A")
lpC = lpf(outC[1], COLD, "C", "U2B")
# SW3 note
d.rectangle([*P(87, 66), *P(141, 50.5)], outline=(200, 120, 20), width=int(LW * .7))
text(114, 64.0, "SW3  ROTARY  BYPASS / 80 / 100 / 120 Hz", 1.55, (170, 90, 10), "mm", True)
text(114, 61.5, "Switches C1..C4 as matched film pairs  (fc = 1/(2*pi*R*C), R = 10k, Q = 0.707)", 1.25, GRY, "mm")
text(114, 59.4, "80 Hz: C1 270n / C2 150n    100 Hz: 220n / 110n    120 Hz: 180n / 100n", 1.25, GRY, "mm")
text(114, 57.3, "BYPASS = full-range mono (use the sub's own crossover).  Caps: PPS / C0G film, 1%", 1.25, GRY, "mm")
text(114, 55.2, "Both legs use identical C values so the balance (CMRR) is kept.", 1.25, GRY, "mm")
text(114, 52.4, "Slope: 12 dB/oct per section; add 2nd section for 24 dB/oct if desired.", 1.25, GRY, "mm")

# ================================================================ STAGE 4 : buffers / outputs
def buf(yc, col, ua, rname, pin):
    xin = 146
    line([(lpH[0] if col == HOT else lpC[0], yc), (xin, yc)], col)
    plus, minus, out = opamp(157, yc, ua, "OPA1612 (dual)", plus_top=True, w=10, h=12)
    line([(xin, yc), plus], col)
    # follower
    line([minus, (minus[0] - 2, minus[1]), (minus[0] - 2, yc - 8), (out[0] + 3, yc - 8), (out[0] + 3, yc)], col)
    line([out, (out[0] + 3, yc)], col)
    dot(out[0] + 3, yc, col)
    return (out[0] + 3, yc)


bH = buf(outH[1], HOT, "U4A", "R9", 2)
bC = buf(outC[1], COLD, "U4B", "R10", 3)
# series output resistors + XLR
for (b, col, rn, pin, lab) in ((bH, HOT, "R9", 2, "Hot"), (bC, COLD, "R10", 3, "Cold")):
    line([b, (b[0] + 3.5, b[1])], col)
    res(b[0] + 7.5, b[1], rn, "47R", col)
    line([(b[0] + 11.5, b[1]), (188, b[1])], col)
    # XLR contact
    px, py = P(190, b[1])
    d.ellipse([px - S * 1.2, py - S * 1.2, px + S * 1.2, py + S * 1.2], outline=col, width=LW, fill="white")
    text(190, b[1], str(pin), 1.4, col, "mm", True)
    text(190, b[1] + 3.0, "XLR " + str(pin) + " " + lab, 1.2, col, "mm", True)
# XLR body and shield pin 1
xm = (bH[1] + bC[1]) / 2
d.ellipse([*P(184, xm + 17), *P(196, xm - 17)], outline=INK, width=int(LW * .8))
px, py = P(190, xm)
d.ellipse([px - S * 1.2, py - S * 1.2, px + S * 1.2, py + S * 1.2], outline=INK, width=LW, fill="white")
text(190, xm, "1", 1.4, INK, "mm", True)
line([(190, xm - 1.4), (190, xm - 5.0)], INK)
res(190, xm - 8.0, "", "", INK, vertical=True)
text(192.4, xm - 8.5, "R11 10R", 1.2, INK, "lm", True)
text(192.4, xm - 10.2, "|| C5 10n", 1.2, GRY, "lm")
line([(190, xm - 11.0), (190, xm - 13.0)], INK)
gnd(190, xm - 13.0)
text(190, bH[1] + 8.8, "SUB OUT  (XLR, balanced, mono)", 1.5, INK, "mm", True)

# --- RCA differential receiver (THAT1240 style) fed from buffer outputs
ry = 51.5
text(147, 44.5, "RCA output  (balanced -> single-ended)", 1.5, INK, "la", True)
line([(bH[0], bH[1]), (bH[0], 32 + 0)], HOT) if False else None
# tap points
dot(bH[0], bH[1], HOT)
dot(bC[0], bC[1], COLD)
d.rectangle([*P(160, 44), *P(175, 31)], outline=INK, width=LW, fill=(250, 250, 235))
text(167.5, 41.4, "U5", 1.7, INK, "mm", True)
text(167.5, 39.4, "THAT1240", 1.4, INK, "mm", True)
text(167.5, 37.5, "or OPA1612 +", 1.2, GRY, "mm")
text(167.5, 36.0, "4x 10k 0.1%", 1.2, GRY, "mm")
text(167.5, 34.2, "(diff. receiver)", 1.2, GRY, "mm")
# tap wires
line([(bH[0], bH[1] - 0), (bH[0], 42), (160, 42)], HOT)
line([(bC[0], bC[1]), (bC[0], 33), (160, 33)], COLD)
text(158.2, 43.3, "IN+", 1.2, HOT, "rm", True)
text(158.2, 34.3, "IN\u2212", 1.2, COLD, "rm", True)
line([(175, 37.5), (178, 37.5)], INK)
res(182.2, 37.5, "R12", "100R", INK)
line([(186.2, 37.5), (190, 37.5)], INK)
px, py = P(191, 37.5)
d.ellipse([px - S * 1.6, py - S * 1.6, px + S * 1.6, py + S * 1.6], outline=INK, width=LW, fill="white")
text(194.2, 37.5, "RCA", 1.3, INK, "lm", True)
text(194.2, 35.7, "(tip)", 1.2, GRY, "lm")
text(185, 31.0, "SUB OUT (RCA)", 1.4, INK, "mm", True)
# ground ref for U5
gnd(167.5, 31.0)

# ---------------------------------------------------------------- power + BOM
frame(1, 1, 98, 26, "POWER / BYPASS (every IC)")
text(3, 20.0, "+15 V / \u221215 V low-noise post-regulators (LT3045 / LT3094, or LM317/LM337 + RC)", 1.4, INK)
text(3, 17.9, "taken from the existing analog rails of the amplifier (or a small separate winding).", 1.4, GRY)
text(3, 15.4, "Each IC:  100 nF X7R (ceramic, at the pins)  +  10 \u00b5F  (per rail, within 10 mm)", 1.4, INK)
text(3, 12.9, "Star-ground to the amplifier's analog ground at one point.  XLR pin 1 -> chassis via R11 || C5.", 1.4, INK)
text(3, 10.4, "Optional: output DC-blocking 4.7 \u00b5F film in series with each XLR leg (after R9/R10) and mute relay.", 1.4, GRY)
text(3, 7.9, "No unsafe/unusual parts: all SMD, 0.1% 25 ppm thin-film resistor arrays recommended for R1-R8.", 1.4, GRY)
text(3, 5.4, "Switches: SW1 / SW2 as small DPDT slide/relay, SW3 as 2-pole 4-throw rotary or analog switch bank.", 1.4, GRY)

frame(100, 1, 199, 26, "BILL OF MATERIALS (summary)")
bom = [
    "U1, U2, U4   OPA1612 dual (or NJM4580 / LME49720 for cost)  x3",
    "U5           THAT1240 (laser-trimmed diff. receiver)  x1",
    "R1-R8        10 k  0.1%  25 ppm thin-film (arrays)",
    "Rf1, Rf2     4.99 k 0.1%     Rb  2.49 k 1%",
    "C1-C4        PPS/C0G film pairs (270n/220n/180n, 150n/110n/100n)",
    "R9, R10 47R   R11 10R   R12 100R   C5 10n   Cf 33p C0G",
    "SW1 MONO/STEREO  SW2 PHASE  SW3 LPF (BYPASS/80/100/120 Hz)",
    "J1 XLR-3 (Neutrik NC3FAH)   J2 RCA   (J3 = SUB OUT 2 for STEREO mode)",
]
for i, s in enumerate(bom):
    text(102, 22.0 - 2.35 * i, s, 1.35, INK)

# legend
text(3, 3.6, "Legend:", 1.3, INK, "la", True)
text(11, 3.6, "red = Hot (+)", 1.3, HOT, "la", True)
text(26, 3.6, "blue = Cold (\u2212)", 1.3, COLD, "la", True)
text(46, 3.6, "orange box = user switch", 1.3, (170, 90, 10), "la", True)
text(80, 3.0, "Reference design - verify by simulation and bench-test before production.", 1.2, GRY, "la")

img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\mono_sub_out_schematic.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
