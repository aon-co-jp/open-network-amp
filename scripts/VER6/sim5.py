import math, json
kB, T = 1.380649e-23, 300.0
R = {}
BW = (7.0, 120.0)
nb = BW[1] - BW[0]


def en_r(r):
    return math.sqrt(4 * kB * T * r)


def sk_noise(Rk, en=1.1e-9):
    # two equal input resistors + op-amp, unity gain
    return math.sqrt(2 * en_r(Rk) ** 2 + en ** 2)


def hpf_noise(Rsh):
    return en_r(Rsh)


def summer(Rin, Rf, en=1.1e-9, inn=1.7e-12):
    rp = Rin / 2
    ng = 1 + Rf / rp
    rb = 1 / (1 / Rin + 1 / Rin + 1 / Rf)
    t2 = (en * ng) ** 2 + (inn * Rf) ** 2 + en_r(Rf) ** 2 + (en_r(rp) * Rf / rp) ** 2 + (en_r(rb) * ng) ** 2
    return math.sqrt(t2)


# ---------- iteration 1 : VER4 baseline (summer 4.99k/2.49k, SK R 12.7k, HPF 22k, LR4 = two SK stages)
it = {}
v4 = {"summer": summer(4.99e3, 2.49e3), "SK1": sk_noise(12.7e3), "SK2 (LR4)": sk_noise(12.7e3), "HPF R": hpf_noise(22e3)}
tot4 = math.sqrt(sum(v ** 2 for v in v4.values()))
it["iter1_VER4_nV_per_rtHz"] = {k: v * 1e9 for k, v in v4.items()}
it["iter1_total_nV_per_rtHz"] = tot4 * 1e9
it["iter1_total_uV_7-120Hz"] = tot4 * math.sqrt(nb) * 1e6
# ---------- iteration 2 : lower the SK resistors (C1 440n / C2 220n, R 6.34k) and HPF R 10k with 2.2 uF
v5a = {"summer": summer(4.99e3, 2.49e3), "SK1": sk_noise(6.34e3), "SK2 (LR4)": sk_noise(6.34e3), "HPF R": hpf_noise(10e3)}
tot5a = math.sqrt(sum(v ** 2 for v in v5a.values()))
it["iter2_nV_per_rtHz"] = {k: v * 1e9 for k, v in v5a.items()}
it["iter2_total_uV_7-120Hz"] = tot5a * math.sqrt(nb) * 1e6
# ---------- iteration 3 : also summer 2.49k/1.24k (source 47 ohm load check)
v5 = {"summer": summer(2.49e3, 1.24e3), "SK1": sk_noise(6.34e3), "SK2 (LR4)": sk_noise(6.34e3), "HPF R": hpf_noise(10e3)}
tot5 = math.sqrt(sum(v ** 2 for v in v5.values()))
it["iter3_nV_per_rtHz"] = {k: v * 1e9 for k, v in v5.items()}
it["iter3_total_uV_7-120Hz"] = tot5 * math.sqrt(nb) * 1e6
it["iter3_dB_vs_VER4"] = 20 * math.log10(tot5 / tot4)
it["iter3_load_on_47ohm_preout_dB"] = 20 * math.log10(2.49e3 / (2.49e3 + 47))
R["sub_noise"] = it


# ---------- SK values check
def sk(R1, R2, C1, C2):
    def H(f):
        s = 2j * math.pi * f
        return 1 / (1 + s * C2 * (R1 + R2) + s * s * R1 * R2 * C1 * C2)
    return H, math.sqrt(R1 * R2 * C1 * C2) / (C2 * (R1 + R2)), 1 / (2 * math.pi * math.sqrt(R1 * R2 * C1 * C2))


skn = {}
for nm, rr in (("80Hz", 6.34e3), ("100Hz", 5.11e3), ("120Hz", 4.22e3)):
    H, q, f0 = sk(rr, rr, 440e-9, 220e-9)
    fs = [1 * (1e4) ** (i / 4000) for i in range(4001)]
    ref = abs(H(1))
    f3 = next(f for f in fs if abs(H(f)) < ref * 10 ** (-3 / 20))
    skn[nm] = {"Q": q, "f0": f0, "f3dB": f3}
R["sk_values_v5"] = skn
# HPF 2.2uF + 10k
R["hpf_v5_fc"] = 1 / (2 * math.pi * 10e3 * 2.2e-6)

# ---------- volume ladder (series-shunt, 10 kohm input), accuracy and noise vs attenuation
vol = {}
for att in (0, -6, -12, -20, -30, -40, -60):
    a = 10 ** (att / 20)
    rin = 10e3
    rser = rin * (1 - a)
    rsh = rin * a
    zout = (rser * rsh) / (rser + rsh) if att != 0 else 0.0
    n = en_r(max(zout, 1e-3)) * math.sqrt(19980)
    # 0.1 % resistors -> worst-case attenuation error
    err = 20 * math.log10((1 + 0.001) / (1 - 0.001)) / 2 if att != 0 else 0
    vol[str(att)] = {"Zout_ohm": zout, "thermal_noise_uV_20Hz-20kHz": n * 1e6, "dBV": 20 * math.log10(max(n, 1e-12)), "max_error_dB_0.1pct": err}
R["volume_ladder"] = vol
# durability: latching relay 1e7 operations, 500 steps/day
R["durability"] = {"relay_ops_per_year_at_500_steps_per_day": 500 * 365, "years_for_1e7": 1e7 / (500 * 365), "encoder_wear": "contactless (magnetic), no wear", "motor": "brushless, ball bearings"}
# wiring: inductance ~1 nH/mm, loop area ratio
R["wiring"] = {"VER2_mm": 95, "VER5_mm": 60, "inductance_nH_VER2": 95, "inductance_nH_VER5": 60, "pickup_ratio_dB": 20 * math.log10(60 / 95)}
json.dump(R, open("sim5_results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def show(k, v, ind=0):
    if isinstance(v, dict):
        print(" " * ind + k + ":")
        for a, b in v.items():
            show(a, b, ind + 2)
    else:
        print(" " * ind + k + ": " + (("%.4g" % v) if isinstance(v, (int, float)) else str(v)))


for k, v in R.items():
    show(k, v)
