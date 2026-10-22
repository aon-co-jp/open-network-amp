import math
def plot(x0, y0, x1, y1, xmin, xmax, ymin, ymax, logx, title, xlabel, ylabel):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=(150, 160, 190), width=int(LW * .7), fill=(252, 252, 252))
    text(x0, y1 + 2.2, title, 1.3, INK, "la", True)

    def mx(v):
        t = (math.log10(v) - math.log10(xmin)) / (math.log10(xmax) - math.log10(xmin)) if logx else (v - xmin) / (xmax - xmin)
        return x0 + t * (x1 - x0)

    def my(v):
        return y0 + (v - ymin) / (ymax - ymin) * (y1 - y0)
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
                text(mx(10 ** e), y0 - 1.5, "%g" % (10 ** e), 0.95, GRY, "mm")
            e += 1
    text((x0 + x1) / 2, y0 - 3.6, xlabel, 1.0, GRY, "mm")
    text(x0 - 0.6, y1 + 0.6, ylabel, 0.95, GRY, "rb")
    return mx, my


def curve(mx, my, pts, col, dashed=False, w=None):
    seg = [(mx(x), my(y)) for (x, y) in pts]
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


