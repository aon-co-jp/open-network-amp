from PIL import Image, ImageDraw, ImageFont

W, H = 200, 150
S = 32
img = Image.new("RGB", (W * S, H * S), "white")
d = ImageDraw.Draw(img)
LW = int(S * 0.13)
INK = (20, 30, 60)
HOT = (190, 30, 30)
COLD = (30, 70, 180)
GRY = (110, 110, 110)
ORG = (170, 90, 10)


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


def circ(x, y, r, col, fill="white"):
    px, py = P(x, y)
    d.ellipse([px - S * r, py - S * r, px + S * r, py + S * r], outline=col, width=LW, fill=fill)


def res(x, y, label, val, col=INK, vertical=False):
    L, Wd = 8, 2.6
    if vertical:
        d.rectangle([*P(x - Wd / 2, y + L / 2), *P(x + Wd / 2, y - L / 2)], outline=col, width=LW)
        text(x + 2.2, y + 0.3, label, 1.5, col, "lm", True)
        text(x + 2.2, y - 1.4, val, 1.3, GRY, "lm")
    else:
        d.rectangle([*P(x - L / 2, y + Wd / 2), *P(x + L / 2, y - Wd / 2)], outline=col, width=LW)
        text(x, y + 3.6, label, 1.5, col, "mm", True)
        text(x, y + 1.9, val, 1.3, GRY, "mm")


def vcap(x, y, label, val, col=INK, left=False):
    g, h = 0.9, 2.6
    line([(x - h, y + g), (x + h, y + g)], col)
    line([(x - h, y - g), (x + h, y - g)], col)
    if left:
        text(x - 3.4, y + 0.3, label, 1.5, col, "rm", True)
        text(x - 3.4, y - 1.4, val, 1.3, GRY, "rm")
    else:
        text(x + 3.4, y + 0.3, label, 1.5, col, "lm", True)
        text(x + 3.4, y - 1.4, val, 1.3, GRY, "lm")


def gnd(x, y):
    line([(x, y), (x, y - 1.5)])
    line([(x - 1.8, y - 1.5), (x + 1.8, y - 1.5)])
    line([(x - 1.1, y - 2.3), (x + 1.1, y - 2.3)])
    line([(x - 0.4, y - 3.1), (x + 0.4, y - 3.1)])


def opamp(cx, cy, name, part, plus_top=False, w=11, h=13):
    x0, x1 = cx - w / 2, cx + w / 2
    pts = [P(x0, cy + h / 2), P(x0, cy - h / 2), P(x1, cy)]
    d.polygon(pts, outline=INK, fill=(250, 250, 235))
    d.line(pts + [pts[0]], fill=INK, width=LW)
    top, bot = cy + h / 4, cy - h / 4
    plus_y, minus_y = (top, bot) if plus_top else (bot, top)
    text(x0 + 1.0, plus_y, "+", 2.0, INK, "lm", True)
    text(x0 + 1.0, minus_y, "\u2212", 2.0, INK, "lm", True)
    text(cx - 1.2, cy + h / 2 + 1.2, name, 1.7, INK, "mm", True)
    text(cx - 1.2, cy - h / 2 - 1.6, part, 1.3, GRY, "mm")
    return (x0, plus_y), (x0, minus_y), (x1, cy)


def frame(x0, y0, x1, y1, title):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=(150, 160, 190), width=int(LW * 0.7))
    text(x0 + 1, y1 - 0.8, title, 1.9, (60, 80, 150), "la", True)


HY, CY = 100, 44

text(3, 147, "Mono Subwoofer Output for a Fully Balanced Integrated Amplifier  -  XLR + RCA", 3.0, INK, "la", True)
text(3, 143.4, "Reference schematic  |  tapped AFTER the volume control (sub level follows main volume)  |  "
     "L+R balanced summing -> phase -> 80/100/120 Hz low-pass -> buffered XLR + differential RCA", 1.6, GRY)
text(3, 141.0, "Reference design - verify by simulation and bench-test before production.", 1.3, GRY)
text(150, 141.0, "red = Hot (+)", 1.3, HOT, "la", True)
text(166, 141.0, "blue = Cold (\u2212)", 1.3, COLD, "la", True)
text(184, 141.0, "orange = switch", 1.3, ORG, "la", True)

frame(1, 23, 62, 139, "STAGE 1  Balanced L+R summing")
frame(64, 23, 83, 139, "STAGE 2")
frame(85, 23, 143, 139, "STAGE 3  2nd-order Butterworth low-pass (balanced)")
frame(145, 23, 199, 139, "STAGE 4  Output buffers / drivers")


# ---------------------------------------------------------------- stage 1
def sum_row(yc, col, lname, rname, rf_ref, r_refs, u_name, part):
    yl, yr = yc + 12, yc + 6
    text(2, yl, lname, 1.9, col, "lm", True)
    text(2, yr, rname, 1.9, col, "lm", True)
    plus, minus, out = opamp(46, yc, u_name, part, plus_top=False)
    xr = 20
    res(xr, yl, r_refs[0], "10k 0.1%", col)
    line([(13, yl), (xr - 4, yl)], col)
    res(xr, yr, r_refs[1], "10k 0.1%", col)
    line([(13, yr), (xr - 4, yr)], col)
    xb = 29
    line([(xr + 4, yl), (xb, yl), (xb, minus[1])], col)
    line([(xr + 4, yr), (xb, yr)], col)
    dot(xb, yr, col)
    line([(xb, minus[1]), minus], col)
    yf = yc + 19.5
    res(46, yf, rf_ref, "4.99k 0.1%", col)
    line([(xb, yl), (xb, yf), (42, yf)], col)
    xo = out[0] + 4.5
    line([(50, yf), (xo, yf), (xo, out[1])], col)
    line([out, (xo, out[1])], col)
    dot(xo, out[1], col)
    cfy = yf + 5.2
    line([(xb + 3, yf), (xb + 3, cfy), (36.8, cfy)], col)
    d.line([*P(36.8, cfy + 1.8), *P(36.8, cfy - 1.8)], fill=col, width=LW)
    d.line([*P(38.4, cfy + 1.8), *P(38.4, cfy - 1.8)], fill=col, width=LW)
    line([(38.4, cfy), (xo, cfy), (xo, yf)], col)
    dot(xb + 3, yf, col)
    dot(xo, yf, col)
    text(37.6, cfy + 3.0, "Cf 33p C0G", 1.3, GRY, "mm")
    line([plus, (plus[0] - 6, plus[1])], col)
    res(plus[0] - 6, plus[1] - 4.5, "Rb", "2.49k", col, vertical=True)
    line([(plus[0] - 6, plus[1] - 8.5), (plus[0] - 6, plus[1] - 9.5)], col)
    gnd(plus[0] - 6, plus[1] - 9.5)
    return (xo, out[1])


oH = sum_row(HY, HOT, "L +  (Hot)", "R +  (Hot)", "Rf1", ("R1", "R2"), "U1A", "OPA1612  ch.A")
oC = sum_row(CY, COLD, "L \u2212  (Cold)", "R \u2212  (Cold)", "Rf2", ("R3", "R4"), "U1B", "OPA1612  ch.B")
text(3, 133.6, "Balanced inputs from the volume stage (post-volume)", 1.25, GRY, "la")

d.rectangle([*P(3, 82), *P(35, 72)], outline=(200, 120, 20), width=int(LW * .7))
text(19, 80.0, "SW1  MONO / STEREO  (ganged to R2, R4)", 1.35, ORG, "mm", True)
text(19, 77.6, "MONO: L and R summed in one bus", 1.25, GRY, "mm")
text(19, 75.4, "STEREO: R side -> identical chain", 1.25, GRY, "mm")
text(19, 73.3, "-> SUB OUT 2 (second XLR/RCA)", 1.25, GRY, "mm")

text(3, 25.9, "Gain per input = Rf/R = 0.5 -> correlated bass (L=R) = 0 dB, i.e. (L+R)/2 (absorbs the +6 dB of a plain sum).", 1.2, GRY)
text(3, 24.2, "Stage polarity is inverting on both legs (SW2 sets the final polarity).", 1.2, GRY)

# ---------------------------------------------------------------- stage 2
d.rectangle([*P(66, 106), *P(81, 36)], outline=(200, 120, 20), width=int(LW * .7))
text(73.5, 104.2, "SW2", 1.8, ORG, "mm", True)
text(73.5, 101.8, "PHASE", 1.4, ORG, "mm", True)
text(73.5, 99.6, "0\u00b0 / 180\u00b0", 1.4, ORG, "mm", True)
line([oH, (69, oH[1]), (69, 76), (70, 76)], HOT)
line([oC, (69, oC[1]), (69, 66), (70, 66)], COLD)
line([(77, 76), (78, 76), (78, HY), (84, HY)], HOT)
line([(77, 66), (78, 66), (78, CY), (84, CY)], COLD)
G = (130, 130, 130)
d.line([*P(70, 76), *P(77, 76)], fill=G, width=LW)
d.line([*P(70, 66), *P(77, 66)], fill=G, width=LW)
d.line([*P(70, 76), *P(77, 66)], fill=G, width=LW)
d.line([*P(70, 66), *P(77, 76)], fill=G, width=LW)
for (x, y, c) in ((70, 76, HOT), (70, 66, COLD), (77, 76, HOT), (77, 66, COLD)):
    dot(x, y, c)
for i, t in enumerate(["DPDT: straight", "= 0\u00b0"]):
    text(73.5, 88.5 - 1.7 * i, t, 1.15, GRY, "mm")
for i, t in enumerate(["crossed", "= 180\u00b0"]):
    text(73.5, 62.5 - 1.7 * i, t, 1.15, GRY, "mm")
for i, t in enumerate(["relay or toggle", "(relay = silent", "switching)"]):
    text(73.5, 56.0 - 1.7 * i, t, 1.15, GRY, "mm")


# ---------------------------------------------------------------- stage 3
def lpf(yc, col, tag, ua, part):
    n = 1 if tag == "H" else 3
    y = yc
    line([(84, y), (88, y)], col)
    res(92, y, "R%d" % (n + 4), "10k 0.1%", col)
    line([(96, y), (99, y)], col)
    dot(99, y, col)
    res(103, y, "R%d" % (n + 5), "10k 0.1%", col)
    line([(107, y), (110, y)], col)
    dot(110, y, col)
    plus, minus, out = opamp(121, y, ua, part, plus_top=True)
    line([(110, y), (110, plus[1]), plus], col)
    line([(110, y), (110, y - 5.0)], col)
    vcap(110, y - 7.0, "C%d" % (2 if tag == "H" else 4), "150n/110n/100n", col=col, left=True)
    line([(110, y - 8.1), (110, y - 11.5)], col)
    gnd(110, y - 11.5)
    yfb = y + 12.0
    line([(99, y), (99, yfb), (104.6, yfb)], col)
    d.line([*P(104.6, yfb + 2.6), *P(104.6, yfb - 2.6)], fill=col, width=LW)
    d.line([*P(106.4, yfb + 2.6), *P(106.4, yfb - 2.6)], fill=col, width=LW)
    line([(106.4, yfb), (130, yfb), (130, y)], col)
    text(105.5, yfb + 3.2, "C%d" % (1 if tag == "H" else 3), 1.5, col, "mm", True)
    text(105.5, yfb + 4.9, "270n/220n/180n", 1.3, GRY, "mm")
    line([minus, (minus[0] - 2.5, minus[1]), (minus[0] - 2.5, y - 17.0), (130, y - 17.0), (130, y)], col)
    line([out, (130, y)], col)
    dot(130, y, col)
    line([(130, y), (146, y)], col)


lpf(HY, HOT, "H", "U2A", "OPA1612  ch.A")
lpf(CY, COLD, "C", "U2B", "OPA1612  ch.B")
d.rectangle([*P(87, 81.5), *P(141, 64)], outline=(200, 120, 20), width=int(LW * .7))
text(114, 79.3, "SW3  ROTARY  BYPASS / 80 / 100 / 120 Hz", 1.55, ORG, "mm", True)
for i, t in enumerate([
    "Switches C1..C4 as matched film pairs  (fc = 1/(2*pi*R*C), R = 10k, Q = 0.707)",
    "80 Hz: C1 270n / C2 150n    100 Hz: 220n / 110n    120 Hz: 180n / 100n",
    "BYPASS = full-range mono (use the sub's own crossover).  Caps: PPS / C0G film, 1%",
    "Hot and Cold legs use identical values so the balance (CMRR) is kept.",
    "12 dB/oct per section; add a second section for 24 dB/oct if desired.",
    "Switch bank: 2-pole 4-throw rotary or analog-switch IC.",
]):
    text(114, 76.8 - 2.1 * i, t, 1.2, GRY, "mm")


# ---------------------------------------------------------------- stage 4
def buf(yc, col, ua, part):
    plus, minus, out = opamp(155, yc, ua, part, plus_top=True, w=10, h=12)
    line([(146, yc), (150, yc), (150, plus[1]), plus], col)
    line([minus, (minus[0] - 2, minus[1]), (minus[0] - 2, yc - 10), (163, yc - 10), (163, yc)], col)
    line([out, (163, yc)], col)
    dot(163, yc, col)
    return (163, yc)


bH = buf(HY, HOT, "U4A", "OPA1612  ch.A")
bC = buf(CY, COLD, "U4B", "OPA1612  ch.B")
for (b, col, rn, pin, lab) in ((bH, HOT, "R9", 2, "Hot"), (bC, COLD, "R10", 3, "Cold")):
    line([b, (168, b[1])], col)
    res(172, b[1], rn, "47R", col)
    line([(176, b[1]), (188.8, b[1])], col)
    circ(190, b[1], 1.2, col)
    text(190, b[1], str(pin), 1.4, col, "mm", True)
    text(190, b[1] + (3.0 if pin == 2 else -3.0), "XLR %d %s" % (pin, lab), 1.25, col, "mm", True)
circ(190, 113, 1.2, INK)
text(190, 113, "1", 1.4, INK, "mm", True)
line([(188.8, 113), (184, 113)], INK)
res(180, 113, "R11", "10R || C5 10n", INK)
line([(176, 113), (172, 113)], INK)
gnd(172, 113)
text(198, 108.0, "SUB OUT (XLR, balanced mono)", 1.3, INK, "ra", True)

text(166, 73.8, "RCA output: balanced -> single-ended", 1.3, INK, "la", True)
d.rectangle([*P(168, 68), *P(181, 54)], outline=INK, width=LW, fill=(250, 250, 235))
text(174.5, 65.8, "U5", 1.6, INK, "mm", True)
text(174.5, 63.8, "THAT1240", 1.3, INK, "mm", True)
for i, t in enumerate(["diff. receiver", "(or OPA1612 +", "4x 10k 0.1%)"]):
    text(174.5, 62.0 - 1.6 * i, t, 1.15, GRY, "mm")
line([(163, HY), (163, 66), (168, 66)], HOT)
line([(163, CY), (163, 56), (168, 56)], COLD)
text(169, 66.0, "IN+", 1.1, HOT, "lm", True)
text(169, 56.0, "IN\u2212", 1.1, COLD, "lm", True)
line([(181, 61), (184, 61)], INK)
res(188, 61, "R12", "100R", INK)
line([(192, 61), (192.6, 61)], INK)
circ(194.2, 61, 1.6, INK)
text(196.4, 63.5, "RCA", 1.1, INK, "lm", True)
text(190, 55.0, "SUB OUT (RCA, tip)", 1.25, INK, "mm", True)
gnd(174.5, 54)

# ---------------------------------------------------------------- bottom panels
frame(1, 1, 98, 21, "POWER / BYPASS (every IC)")
pw = [
    ("+15 V / \u221215 V low-noise post-regulators (LT3045 / LT3094, or LM317/LM337 + RC)", INK),
    ("taken from the existing analog rails of the amplifier (or a small separate winding).", GRY),
    ("Each IC: 100 nF X7R at the pins + 10 \u00b5F per rail within 10 mm.", INK),
    ("Star-ground to the amplifier's analog ground at one point; XLR pin 1 -> chassis via R11 || C5.", INK),
    ("Optional: 4.7 \u00b5F film DC-block in each XLR leg (after R9/R10) and a mute relay.", GRY),
    ("R1-R8 as 0.1% 25 ppm thin-film arrays; all SMD, suited to automated assembly.", GRY),
]
for i, (t, c) in enumerate(pw):
    text(3, 16.2 - 2.45 * i, t, 1.3, c)

frame(100, 1, 199, 21, "BILL OF MATERIALS (summary)")
for i, t in enumerate([
    "U1, U2, U4   OPA1612 dual (or NJM4580 / LME49720 for cost)  x3",
    "U5           THAT1240 (laser-trimmed differential receiver)  x1",
    "R1-R8 10k 0.1% 25 ppm    Rf1, Rf2 4.99k 0.1%    Rb 2.49k 1%",
    "C1-C4 PPS/C0G film pairs (270n/220n/180n, 150n/110n/100n)",
    "R9, R10 47R   R11 10R   R12 100R   C5 10n   Cf 33p C0G",
    "SW1 MONO/STEREO   SW2 PHASE   SW3 LPF (BYPASS/80/100/120 Hz)",
    "J1 XLR-3 male   J2 RCA   (J3 = SUB OUT 2 for STEREO mode)",
]):
    text(102, 17.2 - 2.2 * i, t, 1.3, INK)

img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\mono_sub_out_schematic.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
