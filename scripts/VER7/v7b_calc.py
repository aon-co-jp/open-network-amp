import math
VT = 0.026
# ---------------------------------------------------------------- 1) output stage: gain error across the load current
RE_SIDE = 0.22 / 2          # 0.22 ohm emitter resistors, two devices in parallel per side


def side_g(ie):
    return 1.0 / (RE_SIDE + VT / max(ie, 1e-6))


def rout_ol(il, ib_side):
    ip = (il + math.sqrt(il * il + 4 * ib_side ** 2)) / 2.0     # class AB: Ip * In = Ib^2
    inn = ib_side ** 2 / ip
    return 1.0 / (side_g(ip) + side_g(inn))


def gain(il, ib_side, rl=8.0):
    return rl / (rl + rout_ol(il, ib_side))


def gm_doubling(ib_side):
    """peak-to-peak variation of the open-loop stage gain between idle and a load current of 4 A peak."""
    g0 = gain(0.0, ib_side)
    gs = [gain(i / 10.0, ib_side) for i in range(0, 41)]
    return (max(gs) - min(gs)) / g0


# ---------------------------------------------------------------- 2) loop gain and phase margin of the amplifier
def loop(re_deg, f, cdom=68e-12, gain_cl=23.0, ic=1e-3, p2=6e6, p3=12e6):
    gm = 1.0 / (2 * (VT / ic + re_deg))
    gbw = gm / (2 * math.pi * cdom)
    t = gbw / f / gain_cl
    xover = gbw / gain_cl
    pm = 90 - math.degrees(math.atan(xover / p2)) - math.degrees(math.atan(xover / p3))
    return t, xover, pm


# ---------------------------------------------------------------- 3) valve stage (12AU7 half, three-halves power law)
MU, K = 17.0, 0.68e-3


def ia_of(vgk, vak):
    x = vgk + vak / MU
    return K * x ** 1.5 if x > 0 else 0.0


def stage(vg_peak, rk, rl_ac, ia_q, vb=250.0, n=256, drop_dc=0.0):
    """quiet point from the cathode resistor / current, then a sine of the grid. Returns (gain, h2 %, h3 %)."""
    # quiescent: find vgk at ia_q
    x = (ia_q / K) ** (1 / 1.5)
    vak_q = vb - drop_dc - ia_q * rk
    vgk_q = x - vak_q / MU
    vk_q = ia_q * rk
    outs = []
    for k in range(n):
        vg = vg_peak * math.sin(2 * math.pi * k / n)
        lo, hi = 0.0, 0.03
        for _ in range(60):
            ia = 0.5 * (lo + hi)
            vk = ia * rk
            vak = vak_q + vk_q - (ia - ia_q) * rl_ac - vk
            if ia_of(vg - vk, vak) > ia:
                lo = ia
            else:
                hi = ia
        outs.append(-(ia - ia_q) * rl_ac)
    def harm(m):
        a = sum(o * math.cos(2 * math.pi * m * i / n) for i, o in enumerate(outs)) * 2 / n
        b = sum(o * math.sin(2 * math.pi * m * i / n) for i, o in enumerate(outs)) * 2 / n
        return math.hypot(a, b)
    h1 = harm(1)
    return h1 / vg_peak, 100 * harm(2) / h1, 100 * harm(3) / h1, vgk_q


# ---------------------------------------------------------------- 4) class D loop gain
def class_d_t(f, rfb, cint):
    return 1.0 / (2 * math.pi * f * rfb * cint)


if __name__ == "__main__":
    for ib in (0.05, 0.75, 1.5):
        print("bias per side", ib, "Rout idle", round(rout_ol(0, ib), 3), "Rout 4A", round(rout_ol(4, ib), 3), "gm-doubling %", round(100 * gm_doubling(ib), 2))
    for rd in (0, 22):
        t, xo, pm = loop(rd, 20e3)
        print("deg", rd, "T(20k) dB", round(20 * math.log10(t), 1), "xover MHz", round(xo / 1e6, 2), "PM", round(pm, 1))
    old = stage(0.4, 1000.0, 42.7e3, 3e-3)
    # old: 47k resistor load (quiescent drop 47k*3mA but keep the original bias 3 mA for a fair comparison)
    new_bad = stage(0.4, 1000.0, 320e3, 3e-3)
    new = stage(0.4, 3300.0, 320e3, 3e-3)
    print("old", old, "new R4=1k", new_bad, "new R4=3.3k", new)
    for rfb, c in ((22e3, 220e-12), (22e3, 10e-12)):
        print("Rfb", rfb, "C", c, "T(20k) dB", round(20 * math.log10(class_d_t(20e3, rfb, c)), 1), "T(500k)", round(class_d_t(500e3, rfb, c), 2))


def quiescent(rk, rdc, vb=250.0):
    lo, hi = 0.0, 0.03
    for _ in range(60):
        ia = 0.5 * (lo + hi)
        if ia_of(-ia * rk, vb - ia * (rdc + rk)) > ia:
            lo = ia
        else:
            hi = ia
    return ia


def valve_cases():
    ia_old = quiescent(1000.0, 51.7e3)
    g0, _, _, _ = stage(0.05, 1000.0, 42.7e3, ia_old, drop_dc=ia_old * 51.7e3)
    old = stage(1.0 / g0, 1000.0, 42.7e3, ia_old, drop_dc=ia_old * 51.7e3)
    drop = 4.7e3 * 3e-3 + 15.0
    bad_vgk = -3.0
    rk_new = 3900.0
    g1, _, _, _ = stage(0.05, rk_new, 320e3, 3e-3, drop_dc=drop)
    new = stage(1.0 / g1, rk_new, 320e3, 3e-3, drop_dc=drop)
    return ia_old, old, new, rk_new, bad_vgk


if __name__ == "__main__":
    ia_old, old, new, rk_new, bad = valve_cases()
    print("OLD ia", round(ia_old * 1000, 2), "mA gain %.1f H2 %.4f%% H3 %.6f%%" % old[:3], "Vgk %.1f" % old[3])
    print("NEW R4 %.0f gain %.1f H2 %.4f%% H3 %.6f%% Vgk %.1f" % ((rk_new,) + new))
