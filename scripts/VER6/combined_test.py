from PIL import Image, ImageDraw, ImageFont

W, H = 200, 130
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
    name = "meiryob.ttc" if bold else "meiryo.ttc"
    return ImageFont.truetype("C:/Windows/Fonts/" + name, int(size * S * 0.92))


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



import math
DIG = (30, 70, 180)
ANA = (25, 115, 60)
PWR = (190, 100, 20)
CTL = (110, 110, 110)
HOT = (190, 30, 30)
COLD = (30, 70, 180)
ORG = (170, 90, 10)
OFFY = 0


def P(x, y):
    return (x * S, (H - y - OFFY) * S)


def L(t, sz=1.15, b=False, c=None):
    return (t, sz, b, c)


def box(x0, y0, x1, y1, lines, col=INK, fill=(250, 250, 240)):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=col, width=LW, fill=fill)
    n = len(lines)
    cy = (y0 + y1) / 2
    top = cy + (n - 1) * 1.05
    for i, (t, sz, b, c) in enumerate(lines):
        text((x0 + x1) / 2, top - 2.1 * i, t, sz, c or INK, "mm", b)


def head(x1, y1, x0, y0, col=INK, size=1.8):
    a = math.atan2(y1 - y0, x1 - x0)
    pts = [(x1, y1), (x1 - size * math.cos(a - 0.4), y1 - size * math.sin(a - 0.4)), (x1 - size * math.cos(a + 0.4), y1 - size * math.sin(a + 0.4))]
    d.polygon([P(*p) for p in pts], fill=col)


def arrow(pts, col=INK):
    line(pts, col)
    head(pts[-1][0], pts[-1][1], pts[-2][0], pts[-2][1], col)


def rail(x, y, label, col=PWR, up=True):
    ly = y + (3.0 if up else -3.0)
    line([(x, y), (x, ly)], col)
    text(x, ly + (1.4 if up else -1.4), label, 1.4, col, "mm", True)


def bjt(x, y, kind="npn", name="", val="", col=INK):
    circ(x, y, 4.6, col, fill=(252, 252, 245))
    line([(x - 6.5, y), (x - 1.8, y)], col)
    line([(x - 1.8, y + 2.6), (x - 1.8, y - 2.6)], col)
    line([(x - 1.8, y + 1.3), (x + 2.6, y + 4.0), (x + 2.6, y + 7)], col)
    line([(x - 1.8, y - 1.3), (x + 2.6, y - 4.0), (x + 2.6, y - 7)], col)
    if kind == "npn":
        head(x + 2.6, y - 4.0, x - 1.0, y - 1.7, col, 1.5)
        pins = {"B": (x - 6.5, y), "C": (x + 2.6, y + 7), "E": (x + 2.6, y - 7)}
    else:
        head(x - 1.0, y + 1.7, x + 2.6, y + 4.0, col, 1.5)
        pins = {"B": (x - 6.5, y), "E": (x + 2.6, y + 7), "C": (x + 2.6, y - 7)}
    if name:
        text(x + 5.4, y + 1.0, name, 1.4, col, "lm", True)
        text(x + 5.4, y - 1.0, val, 1.1, GRY, "lm")
    return pins


def mos(x, y, kind="n", name="", val="", col=INK):
    line([(x - 6.5, y), (x - 3, y)], col)
    line([(x - 3, y + 3.4), (x - 3, y - 3.4)], col)
    for a, b in ((3.4, 1.9), (0.9, -0.9), (-1.9, -3.4)):
        line([(x - 1.6, y + a), (x - 1.6, y + b)], col)
    line([(x - 1.6, y + 2.7), (x + 2.6, y + 2.7), (x + 2.6, y + 7)], col)
    line([(x - 1.6, y - 2.7), (x + 2.6, y - 2.7), (x + 2.6, y - 7)], col)
    if kind == "n":
        head(x - 1.6, y - 2.7, x + 0.4, y - 2.7, col, 1.4)
        pins = {"G": (x - 6.5, y), "D": (x + 2.6, y + 7), "S": (x + 2.6, y - 7)}
    else:
        head(x + 0.4, y - 2.7, x - 1.6, y - 2.7, col, 1.4)
        pins = {"G": (x - 6.5, y), "S": (x + 2.6, y + 7), "D": (x + 2.6, y - 7)}
    if name:
        text(x + 5.4, y + 1.0, name, 1.4, col, "lm", True)
        text(x + 5.4, y - 1.0, val, 1.1, GRY, "lm")
    return pins


def triode(x, y, name="", val="", col=INK):
    circ(x, y, 5.4, col, fill=(252, 252, 245))
    line([(x - 2.8, y + 2.8), (x + 2.8, y + 2.8)], col)
    line([(x, y + 2.8), (x, y + 8)], col)
    line([(x - 2.8, y - 2.8), (x + 2.8, y - 2.8)], col)
    line([(x, y - 2.8), (x, y - 8)], col)
    for k in range(3):
        xa = x - 3.6 + k * 2.6
        line([(xa, y), (xa + 1.4, y)], col)
    line([(x - 8, y), (x - 3.6, y)], col)
    if name:
        text(x + 6.4, y + 1.0, name, 1.4, col, "lm", True)
        text(x + 6.4, y - 1.0, val, 1.1, GRY, "lm")
    return {"G": (x - 8, y), "P": (x, y + 8), "K": (x, y - 8)}


def diode(p0, p1, name="", col=INK, zener=False, label_side=1):
    (x0, y0), (x1, y1) = p0, p1
    L_ = math.hypot(x1 - x0, y1 - y0)
    ux, uy = (x1 - x0) / L_, (y1 - y0) / L_
    nx, ny = -uy, ux
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    a = (mx - ux * 1.6, my - uy * 1.6)
    b = (mx + ux * 1.6, my + uy * 1.6)
    line([p0, a], col)
    line([b, p1], col)
    tri = [(a[0] + nx * 1.7, a[1] + ny * 1.7), (a[0] - nx * 1.7, a[1] - ny * 1.7), b]
    d.polygon([P(*p) for p in tri], outline=col, fill=(250, 250, 235))
    bar = [(b[0] + nx * 1.9, b[1] + ny * 1.9), (b[0] - nx * 1.9, b[1] - ny * 1.9)]
    if zener:
        bar = [(b[0] + nx * 1.9 - ux * 0.9, b[1] + ny * 1.9 - uy * 0.9), (b[0] + nx * 1.9, b[1] + ny * 1.9),
               (b[0] - nx * 1.9, b[1] - ny * 1.9), (b[0] - nx * 1.9 + ux * 0.9, b[1] - ny * 1.9 + uy * 0.9)]
    line(bar, col)
    if name:
        text(mx + nx * 3.8 * label_side, my + ny * 3.8 * label_side, name, 1.3, col, "mm", True)


def hcap(x, y, label="", val="", col=INK):
    line([(x - 0.9, y + 2.6), (x - 0.9, y - 2.6)], col)
    line([(x + 0.9, y + 2.6), (x + 0.9, y - 2.6)], col)
    if label:
        text(x, y + 4.4, label, 1.4, col, "mm", True)
        text(x, y - 4.2, val, 1.1, GRY, "mm")


def isrc(x, y, label="", col=INK):
    circ(x, y, 2.8, col)
    line([(x, y - 1.6), (x, y + 1.6)], col)
    head(x, y + 1.7, x, y - 0.5, col, 1.3)
    if label:
        text(x + 3.8, y, label, 1.2, GRY, "lm")


def out_net(xo, yo, col=ANA):
    """Zobel, L||R, relay K1, bi-wire terminals. OUT node at (xo, yo)."""
    line([(xo, yo), (xo + 8, yo)], col)
    dot(xo + 6, yo, col)
    line([(xo + 6, yo), (xo + 6, yo - 6)], col)
    res(xo + 6, yo - 10, "Rz", "10R", col, vertical=True)
    line([(xo + 6, yo - 14), (xo + 6, yo - 16.9)], col)
    d.line([*P(xo + 3.4, yo - 16.9), *P(xo + 8.6, yo - 16.9)], fill=col, width=LW)
    d.line([*P(xo + 3.4, yo - 18.7), *P(xo + 8.6, yo - 18.7)], fill=col, width=LW)
    text(xo + 10.4, yo - 17.8, "Cz 100n", 1.2, GRY, "lm")
    line([(xo + 6, yo - 18.7), (xo + 6, yo - 21)], col)
    gnd(xo + 6, yo - 21)
    line([(xo + 8, yo), (xo + 11, yo)], col)
    d.rectangle([*P(xo + 11, yo + 1.6), *P(xo + 20, yo - 1.6)], outline=col, width=LW, fill=(250, 250, 235))
    text(xo + 15.5, yo, "L1 1µH", 1.1, col, "mm", True)
    line([(xo + 11, yo), (xo + 11, yo + 5), (xo + 12.5, yo + 5)], col)
    res(xo + 15.5, yo + 5, "R", "10Ω", col)
    line([(xo + 18.5, yo + 5), (xo + 20, yo + 5), (xo + 20, yo)], col)
    line([(xo + 20, yo), (xo + 22, yo)], col)
    d.rectangle([*P(xo + 22, yo + 3), *P(xo + 30, yo - 3)], outline=col, width=LW, fill=(250, 250, 235))
    text(xo + 26, yo + 0.9, "K1", 1.4, col, "mm", True)
    text(xo + 26, yo - 1.0, "DC保護", 0.95, GRY, "mm")
    line([(xo + 30, yo), (xo + 34, yo)], col)
    xb = xo + 34
    line([(xb, yo + 4), (xb, yo - 4)], HOT)
    dot(xb, yo, HOT)
    for (y, t) in ((yo + 4, "HF+"), (yo - 4, "LF+")):
        line([(xb, y), (xb + 6.8, y)], HOT)
        circ(xb + 8, y, 1.2, HOT)
        text(xb + 10.2, y, t, 1.3, HOT, "lm", True)
    yr = yo - 14
    line([(xb, yr + 4), (xb, yr - 4)], COLD)
    for (y, t) in ((yr + 4, "HF−"), (yr - 4, "LF−")):
        line([(xb, y), (xb + 6.8, y)], COLD)
        circ(xb + 8, y, 1.2, COLD)
        text(xb + 10.2, y, t, 1.3, COLD, "lm", True)
    line([(xb, yr), (xb - 3, yr)], COLD)
    gnd(xb - 3, yr)
    G = (130, 130, 130)
    d.line([*P(xb + 13.8, yo + 4), *P(xb + 15.5, yo + 4), *P(xb + 15.5, yo - 4), *P(xb + 13.8, yo - 4)], fill=G, width=LW)
    d.line([*P(xb + 13.8, yr + 4), *P(xb + 15.5, yr + 4), *P(xb + 15.5, yr - 4), *P(xb + 13.8, yr - 4)], fill=G, width=LW)
    text(xb + 6, yr - 8.5, "バイワイヤ対応 bi-wire (灰=ジャンパー)", 1.1, GRY, "mm")

import io, contextlib, math
_ns = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\sim.py", encoding="utf-8").read().replace('with open("sim_results.json"', 'with open("sim_results_tmp.json"'), _ns)
sk, lc, db, logspace = _ns["sk"], _ns["lc"], _ns["db"], _ns["logspace"]

text(3, 127, "シミュレーション (TEST / DEBUG) の結果  Simulation (test and debug) results", 2.4, INK, "la", True)
text(3, 123.6, "Python による計算 (交流応答・直流動作点・真空管モデル・設計計算)。実機測定ではありません。過渡応答・歪み・安定性の SPICE 解析は未実施。", 1.45, GRY)
text(3, 121.2, "Calculated in Python (AC response, DC operating points, tube model, design arithmetic). Not bench measurements. Transient / THD / stability SPICE runs were not done.", 1.2, GRY)


def plot(x0, y0, x1, y1, xmin, xmax, ymin, ymax, logx, title, xlabel, ylabel):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=(150, 160, 190), width=int(LW * .7), fill=(252, 252, 252))
    text(x0, y1 + 2.2, title, 1.3, INK, "la", True)

    def mx(v):
        t = (math.log10(v) - math.log10(xmin)) / (math.log10(xmax) - math.log10(xmin)) if logx else (v - xmin) / (xmax - xmin)
        return x0 + t * (x1 - x0)

    def my(v):
        return y0 + (v - ymin) / (ymax - ymin) * (y1 - y0)
    # grid
    yv = ymin
    step = (ymax - ymin) / 6
    for k in range(7):
        v = ymin + k * step
        line([(x0, my(v)), (x1, my(v))], (225, 225, 230), int(LW * .5))
        text(x0 - 0.6, my(v), "%g" % round(v, 1), 0.95, GRY, "rm")
    if logx:
        e = math.floor(math.log10(xmin))
        while 10 ** e <= xmax:
            if 10 ** e >= xmin:
                line([(mx(10 ** e), y0), (mx(10 ** e), y1)], (225, 225, 230), int(LW * .5))
                lab = ("%gk" % (10 ** e / 1e3)) if 10 ** e >= 1e3 else ("%g" % 10 ** e)
                text(mx(10 ** e), y0 - 1.5, lab, 0.95, GRY, "mm")
            e += 1
    text((x0 + x1) / 2, y0 - 3.6, xlabel, 1.0, GRY, "mm")
    text(x0 - 0.6, y1 + 0.6, ylabel, 0.95, GRY, "rb")
    return mx, my


def curve(mx, my, pts, col, dashed=False, w=None):
    seg = []
    for i, (x, y) in enumerate(pts):
        seg.append((mx(x), my(y)))
    if dashed:
        for i in range(0, len(seg) - 1, 2):
            line([seg[i], seg[i + 1]], col, w or int(LW * .9))
    else:
        line(seg, col, w or LW)


def legend(x, y, items):
    for i, (t, col, dashed) in enumerate(items):
        yy = y - i * 2.0
        line([(x, yy), (x + 4, yy)], col, int(LW * .9))
        text(x + 5, yy, t, 0.95, INK, "lm")


# ---- panel 1: Sallen-Key
mx, my = plot(8, 70, 62, 108, 10, 1000, -30, 3, True, "① サブウーファー LPF (2次バターワース)  Sub-woofer LPF", "Hz", "dB")
fs = logspace(10, 1000, 160)
cols = {"80Hz": (30, 70, 180), "100Hz": (25, 115, 60), "120Hz": (190, 30, 30)}
for name, c1, c2 in (("80Hz", 270e-9, 150e-9), ("100Hz", 220e-9, 110e-9), ("120Hz", 180e-9, 100e-9)):
    H, f0, q = sk(10e3, 10e3, c1, c2)
    curve(mx, my, [(f, max(-30, db(H(f)))) for f in fs], cols[name], dashed=True)
for name, rr in (("80Hz", 12.7e3), ("100Hz", 10.2e3), ("120Hz", 8.45e3)):
    H, f0, q = sk(rr, rr, 220e-9, 110e-9)
    curve(mx, my, [(f, max(-30, db(H(f)))) for f in fs], cols[name])
legend(36, 105, [("修正後 (実線) / after", INK, False), ("修正前 (破線) / before", INK, True)])

# ---- panel 2: Class D
mx, my = plot(70, 70, 124, 108, 1e3, 1e6, -50, 10, True, "② Class D 出力フィルタ (BTL 8Ω, 片側 4Ω)  Class D output filter", "Hz", "dB")
fs = logspace(1e3, 1e6, 200)
Ho = lc(10e-6, 1e-6, 4); Hn = lc(22e-6, 0.47e-6, 4)
curve(mx, my, [(f, max(-50, db(Ho(f)))) for f in fs], (190, 30, 30), dashed=True)
curve(mx, my, [(f, max(-50, db(Hn(f)))) for f in fs], (25, 115, 60))
legend(95, 105, [("22µH/0.47µF (修正後)", (25, 115, 60), False), ("10µH/1µF (修正前)", (190, 30, 30), True)])

# ---- panel 3: Class A idle current
mx, my = plot(132, 70, 192, 108, 3.0, 5.5, 0, 4.5, False, "③ Class A アイドル電流  Class A idle current", "Vgs (V)", "A")
pts = [(v, max(0.0, (5.6 - v) / 0.62)) for v in [3.0 + 0.05 * k for k in range(51)]]
curve(mx, my, pts, (190, 30, 30), dashed=True)
curve(mx, my, [(3.0, 2.306), (5.5, 2.306)], (25, 115, 60))
legend(150, 105, [("電流サーボ (修正後) 2.31A", (25, 115, 60), False), ("ツェナー固定 (修正前)", (190, 30, 30), True)])

# ---- result table
rows = [
 ("① LPF: -3dB が 74.7 / 100 / 112 Hz → 抵抗切替で 80.6 / 100.3 / 121.2 Hz (Q = 0.707)",
  "① LPF: the -3 dB points were 74.7 / 100 / 112 Hz; resistor switching now gives 80.6 / 100.3 / 121.2 Hz (Q = 0.707)."),
 ("② Class D: 10µH/1µF は BTL 8Ω で +2.8dB のピーク (Q 1.27) → 22µH/0.47µF で Q 0.58・20kHz −0.7dB。4Ω は −4.2dB (帰還が補正)",
  "② Class D: 10 µH / 1 µF peaked +2.8 dB at BTL 8 ohm; 22 µH / 0.47 µF gives Q 0.58 and -0.7 dB at 20 kHz (4 ohm: -4.2 dB, corrected by feedback)."),
 ("③ Class A: ツェナー固定は Vgs 3〜5.5V で 0.2〜4.2A とばらつく → 電流サーボ (Vset ÷ R7) で 2.31A (R7 ±1% で 2.28A)",
  "③ Class A: a fixed zener bias swung from 0.2 to 4.2 A over Vgs 3-5.5 V; a current servo (Vset / R7) holds 2.31 A (2.28 A with R7 +1%)."),
 ("④ 真空管: 12AX7 は利得 56倍 (35dB) で高すぎ → 12AU7 の片側 (利得 10.9倍 = 20.7dB、入力 3.9Vrms まで余裕)。V2 カソードフォロワの出力 ≈ 1.44kΩ",
  "④ Tube: the 12AX7 stage had 56x (35 dB) gain, too high; a 12AU7 half now gives 10.9x (20.7 dB) with room for 3.9 Vrms input. V2 output impedance is about 1.44 kohm."),
 ("⑤ 外付け電源: 二次 2×18V/2×32V/2×42V では整流後電圧が足りない (±45V 用は最低 38.6V < 48V) → 2×24V / 2×40V / 2×52V (最低 28.4 / 48.8 / 64.0V)",
  "⑤ External supply: the old secondaries (2x18 / 2x32 / 2x42 V) left too little raw voltage (38.6 V minimum for +-45 V, below 48 V); now 2x24 / 2x40 / 2x52 V (28.4 / 48.8 / 64.0 V minimum)."),
 ("問題なし: 加算 (L=R) −0.02dB、I/V LPF 141kHz (バランス) / 133kHz、Class AB バイアス比 R1/R2 = 3、LTP+VAS 帰還帯域 ≈ 0.83MHz (利得 23)。",
  "No problem found: mono sum -0.02 dB, I/V low-pass 141 kHz (balanced) / 133 kHz, Class AB bias ratio R1/R2 = 3, LTP + VAS loop bandwidth about 0.83 MHz (gain 23)."),
 ("未実施: 過渡応答・歪み (THD)・位相余裕 (Class AB / D)・デッドタイム・熱。実機または SPICE での確認が必要です。",
  "Not done: transient response, THD, phase margin (Class AB / D), dead time and thermal checks. Bench or SPICE verification is still required."),
]
y = 60
text(6, 63.5, "見つかった問題と修正 / 確認結果  Problems found, fixes and checks", 1.6, INK, "la", True)
for ja, en in rows:
    text(6, y, ja, 1.15, INK, "la")
    text(6, y - 2.0, en, 1.05, GRY, "la")
    y -= 5.6

img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_test.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
