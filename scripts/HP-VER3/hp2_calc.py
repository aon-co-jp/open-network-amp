import math
VPK_SE, IPK = 13.0, 1.0          # +-15 V rails, 2 buffers of 0.5 A per leg
def p_max(r, balanced):
    v = VPK_SE * (2 if balanced else 1)
    return min(v * v / (2 * r), IPK * IPK * r / 2) * 1.0
def v_for_spl(spl, sens_db_mw, r):
    p_mw = 10 ** ((spl - sens_db_mw) / 10.0)
    return math.sqrt(p_mw * 1e-3 * r)
def hiss_spl(gain_db, sens_db_mw, r, noise0=4e-6):
    vn = noise0 * 10 ** (gain_db / 20.0)
    p_mw = vn * vn / r * 1e3
    return sens_db_mw + 10 * math.log10(p_mw)
CASES = [("IEM 16Ω 120dB/mW", 120.0, 16.0), ("32Ω 100dB/mW", 100.0, 32.0), ("300Ω 100dB/mW", 100.0, 300.0), ("600Ω 98dB/mW", 98.0, 600.0)]
if __name__ == "__main__":
    for n, s, r in CASES:
        print(n, "need Vrms for 100dB SPL", round(v_for_spl(100, s, r), 3), "Pmax SE", round(p_max(r, False), 2), "bal", round(p_max(r, True), 2),
              "hiss 0/+18", round(hiss_spl(0, s, r), 1), round(hiss_spl(18, s, r), 1))
