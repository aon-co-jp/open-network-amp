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
