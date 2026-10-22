import math, cmath
FS = 384000.0
def shelf(kind, f0, gain_db, fs=FS, S=1.0):
    """RBJ low / high shelf biquad (b0 b1 b2 a1 a2, a0 = 1)."""
    A = 10 ** (gain_db / 40.0)
    w0 = 2 * math.pi * f0 / fs
    cw, sw = math.cos(w0), math.sin(w0)
    alpha = sw / 2 * math.sqrt((A + 1 / A) * (1 / S - 1) + 2)
    sq = 2 * math.sqrt(A) * alpha
    if kind == "low":
        b0 = A * ((A + 1) - (A - 1) * cw + sq); b1 = 2 * A * ((A - 1) - (A + 1) * cw); b2 = A * ((A + 1) - (A - 1) * cw - sq)
        a0 = (A + 1) + (A - 1) * cw + sq; a1 = -2 * ((A - 1) + (A + 1) * cw); a2 = (A + 1) + (A - 1) * cw - sq
    else:
        b0 = A * ((A + 1) + (A - 1) * cw + sq); b1 = -2 * A * ((A - 1) + (A + 1) * cw); b2 = A * ((A + 1) + (A - 1) * cw - sq)
        a0 = (A + 1) - (A - 1) * cw + sq; a1 = 2 * ((A - 1) - (A + 1) * cw); a2 = (A + 1) - (A - 1) * cw - sq
    return [b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0]
def mag_db(c, f, fs=FS):
    z = cmath.exp(1j * 2 * math.pi * f / fs)
    num = c[0] + c[1] / z + c[2] / z ** 2
    den = 1 + c[3] / z + c[4] / z ** 2
    return 20 * math.log10(abs(num / den))
def quantize(c, frac_bits):
    q = 2.0 ** frac_bits
    return [round(x * q) / q for x in c]
def coef_error(bits, f_check=20.0, gain=12.0):
    c = shelf("low", 100.0, gain)
    # 2 integer bits for the coefficients, so the word length 'bits' leaves bits-3 fractional bits
    cq = quantize(c, bits - 3)
    return mag_db(cq, f_check) - mag_db(c, f_check)
# analog / mixed relay states for a bipolar +-10 dB, 1 dB step shelf: sign relay + coarse 6 dB relay + fine 1/2/2
FINE = {0: (0, 0, 0), 1: (1, 0, 0), 2: (0, 1, 0), 3: (1, 1, 0), 4: (0, 1, 1), 5: (1, 1, 1)}
def analog_state(g):
    a = abs(g)
    return ((1 if g < 0 else 0), (1 if a >= 6 else 0)) + FINE[a % 6]
def mixed_state(g):
    a = abs(g)
    return ((1 if g < 0 else 0), (1 if a >= 6 else 0))
def toggles(fn, lo=-10, hi=10):
    t = [sum(x != y for x, y in zip(fn(g), fn(g + 1))) for g in range(lo, hi)]
    return sum(t) / len(t), max(t)
def relay_years(tps, steps_per_day, ops=1e7):
    return ops / max(tps * steps_per_day, 1e-9) / 365.0
if __name__ == "__main__":
    for b in (24, 32, 48, 64):
        print(b, "bit coefficients: error at 20 Hz", round(coef_error(b), 3), "dB")
    print("toggles analog", toggles(analog_state), "mixed", toggles(mixed_state))
    print("life analog", round(relay_years(toggles(analog_state)[0], 1000), 1), "mixed", round(relay_years(toggles(mixed_state)[0], 1000), 1))
