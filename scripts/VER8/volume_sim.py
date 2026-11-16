# -*- coding: utf-8 -*-
"""Sound-quality emulator for the hybrid volume (relay ladder + 32-bit trim). Python calculation, not a bench measurement.
Models: T-pad sections switched by latching relays (contact resistance), resistor tolerance (Monte Carlo),
source/load termination, Johnson noise of the network (4kT Re(Zout)), 32-bit digital trim quantisation."""
import math, random, sys
KB, TEMP, BW = 1.380649e-23, 300.0, 20000.0
def tpad(att_db, z0):
    k = 10 ** (att_db / 20); return z0 * (k - 1) / (k + 1), 2 * z0 * k / (k * k - 1)
def mm(a, b): return [[a[0][0]*b[0][0]+a[0][1]*b[1][0], a[0][0]*b[0][1]+a[0][1]*b[1][1]],
                      [a[1][0]*b[0][0]+a[1][1]*b[1][0], a[1][0]*b[0][1]+a[1][1]*b[1][1]]]
def ser(r): return [[1, r], [0, 1]]
def shu(r): return [[1, 0], [1 / r, 1]]
class Ladder:
    def __init__(s, kind, z0, tol, rc, rng):
        s.kind, s.z0, s.rc = kind, z0, rc
        if kind == "binary8": s.cells = [0.5 * 2 ** i for i in range(8)]
        else: s.cells = [0.5, 1, 2, 4, 8] + [16] * 5           # 5 fine binary + 5 coarse (thermometer)
        s.cellr = []
        for a in s.cells:
            r1, r2 = tpad(a, z0)
            s.cellr.append((r1 * (1 + tol * rng.uniform(-1, 1)), r2 * (1 + tol * rng.uniform(-1, 1)), r1 * (1 + tol * rng.uniform(-1, 1))))
    def code_to_state(s, n):
        if s.kind == "binary8": return [(n >> i) & 1 for i in range(8)]
        q, r = divmod(n, 32); return [(r >> i) & 1 for i in range(5)] + [1 if i < q else 0 for i in range(5)]
    def abcd(s, n):
        m = [[1, 0], [0, 1]]
        for on, (a, b, c) in zip(s.code_to_state(n), s.cellr):
            m = mm(m, ser(s.rc))                              # relay contact in the signal path
            if on: m = mm(mm(mm(m, ser(a)), shu(b)), ser(c))
        return m
    def gain_db_zout(s, n, zs, zl):
        (A, B), (C, D) = s.abcd(n)
        g = zl / (A * zl + B + zs * (C * zl + D)); zo = (D * zs + B) / (C * zs + A)
        return 20 * math.log10(abs(g)), zo.real if isinstance(zo, complex) else zo
def run(kind, z0, tol, rc, trials, zs, zl, calibrate=False, seed=1):
    rng = random.Random(seed); worst_err = worst_dnl = 0.0; nonmono = 0; noise_lo = 0.0
    errs_all = []
    for _ in range(trials):
        L = Ladder(kind, z0, tol, rc, rng)
        g0, _z = L.gain_db_zout(0, zs, zl); prev = 0.0; errs = []
        for n in range(181):
            g, zo = L.gain_db_zout(n, zs, zl); att = g0 - g; e = att - 0.5 * n
            if calibrate: e = e - round(e / 0.01) * 0.01   # residual after storing the measured error in a table with 0.01 dB resolution
            errs.append(e)
            if n and att - prev < 0: nonmono += 1
            prev = att
        worst_err = max(worst_err, max(abs(x) for x in errs)); worst_dnl = max(worst_dnl, max(abs(errs[i+1]-errs[i]) for i in range(180)))
        _g, zo = L.gain_db_zout(180, zs, zl); noise_lo = max(noise_lo, zo)
    vn = math.sqrt(4 * KB * TEMP * noise_lo * BW)
    return worst_err, worst_dnl, nonmono, vn
if __name__ == "__main__":
    print("== ladder emulation: worst case of 200 random 0.1%% resistor sets, contact resistance 0.05 ohm ==")
    print("kind     Z0     Zs/ZL(ohm)   max err(dB)  max step err(dB)  nonmono  noise(uV,20kHz)  SNR@-60dB(2Vrms in)")
    for kind in ("binary8", "fine5+16dBx5"):
        for z0 in (200, 600, 1000, 10000):
            for (zs, zl, lab) in ((z0, z0, "matched"),):
                try: e, d, nm, vn = run(kind, z0, 0.001, 0.05, 200, zs, zl)
                except ZeroDivisionError: print(kind, z0, "div0"); continue
                snr = 20 * math.log10(2 * 10 ** (-60 / 20) / 2 / vn)
                print("%-12s %6d  %-9s   %8.3f   %10.3f        %5d   %8.3f        %6.1f" % (kind, z0, lab, e, d, nm, vn * 1e6, snr))
    print("== termination mismatch (fine5+16dBx5, Z0=600, no tolerance): source 50 ohm / load 100 kohm ==")
    e, d, nm, vn = run("fine5+16dBx5", 600, 0.0, 0.0, 1, 50, 100e3); print("max err %.3f dB, max step err %.3f dB" % (e, d))
    print("== with a stored error table (0.01 dB resolution), fine5+16dBx5, Z0=600, 0.1%% ==")
    e, d, nm, vn = run("fine5+16dBx5", 600, 0.001, 0.05, 200, 600, 600, calibrate=True); print("residual max err %.4f dB, step %.4f dB" % (e, d))
    print("== 32-bit digital trim, 24-bit full-scale sine in a 32-bit word, -0.17 dB ==")
    n = 20000; g = 10 ** (-0.17 / 20); se = sx = 0.0
    for t in range(n):
        x = round(math.sin(2 * math.pi * 997 * t / 48000) * (2**23 - 1)) * 256
        e = round(x * g) - x * g; se += e * e; sx += x * x
    print("trim quantisation noise: %.1f dB below the signal (24-bit source quantisation is about 146 dB below full scale)" % (10 * math.log10(sx / (se))))
