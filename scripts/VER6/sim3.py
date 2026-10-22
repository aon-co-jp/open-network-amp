import math, json, cmath

R = {}
kB, T = 1.380649e-23, 300.0


def db(x):
    return 20 * math.log10(abs(x)) if abs(x) > 0 else -400


def logspace(a, b, n):
    return [a * (b / a) ** (i / (n - 1)) for i in range(n)]


# ---- 1) clock jitter budget: SNR limit for a full-scale 20 kHz sine
jit = {}
for tj in (10e-15, 50e-15, 100e-15, 500e-15, 1e-12, 10e-12):
    jit["%g fs" % (tj * 1e15)] = -20 * math.log10(2 * math.pi * 20e3 * tj)
R["jitter_SNR_dB"] = jit

# ---- 2) digital volume: effective bits lost vs attenuation
dv = {}
for att in (0, 6, 12, 20, 30, 40, 50, 60):
    dv["-%ddB" % att] = {"bits_lost": att / 6.02, "eff_bits_from_24": 24 - att / 6.02, "eff_bits_from_32": 32 - att / 6.02}
R["digital_volume"] = dv

# ---- 3) Class AB: loop crossover and phase margin vs Cdom (assumed output-stage poles 3 MHz / 6 MHz)
cab = {}
gm = 1 / (2 * (26 + 100))
for c in (33e-12, 47e-12, 68e-12, 100e-12):
    fu = gm / (2 * math.pi * c)
    fc = fu / 23
    pm = 90 - math.degrees(math.atan(fc / 3e6)) - math.degrees(math.atan(fc / 6e6))
    cab["%dpF" % (c * 1e12)] = {"open_loop_unity_MHz": fu / 1e6, "loop_crossover_MHz (gain 23)": fc / 1e6, "phase_margin_deg (assumed poles 3/6 MHz)": pm}
R["class_ab_cdom"] = cab

# ---- 4) subwoofer summer noise (7-120 Hz band, thermal + OPA1612 en/in)
def summer_noise(Rin, Rf, bw=(7.0, 120.0), en=1.1e-9, inn=1.7e-12):
    rp = 1 / (1 / Rin + 1 / Rin)          # two inputs in parallel
    ng = 1 + Rf / rp
    # input-referred contributions at output
    v_en = en * ng
    v_in = inn * (Rf + rp * 0)             # inverting input current noise through Rf
    v_rf = math.sqrt(4 * kB * T * Rf)
    v_rs = math.sqrt(4 * kB * T * rp) * (Rf / rp)     # source resistors (inputs grounded through source ~ 0, summer resistors)
    v_rin = math.sqrt(2 * 4 * kB * T * Rin) * (Rf / Rin)
    tot2 = v_en ** 2 + v_in ** 2 + v_rf ** 2 + v_rin ** 2
    # plus non-inverting bias resistor Rb (matched) thermal noise gain ng
    rb = 1 / (1 / Rin + 1 / Rin + 1 / Rf)
    tot2 += (math.sqrt(4 * kB * T * rb) * ng) ** 2
    dens = math.sqrt(tot2)
    return dens * math.sqrt(bw[1] - bw[0])


sn = {}
for name, rin, rf in (("VER2 10k/4.99k", 10e3, 4.99e3), ("VER3 4.99k/2.49k", 4.99e3, 2.49e3), ("2.49k/1.24k", 2.49e3, 1.24e3)):
    v = summer_noise(rin, rf)
    sn[name] = {"noise_uVrms_7-120Hz": v * 1e6, "dBV": db(v), "dB_re_1Vrms": db(v)}
R["sub_summer_noise"] = sn
R["sub_noise_note"] = "to be checked: lower resistor values cut thermal noise; the source (pre-out) must drive 4.99 kohm per input (47 ohm source: -0.08 dB)"
R["sub_loading_dB_47ohm_4k99"] = db(4.99e3 / (4.99e3 + 47))

# ---- 5) crossover: sub LPF (BW2 or LR4) + main HPF (same order), magnitude of the acoustic sum for polarity cases
fc = 80.0


def bw2_lp(f):
    s = 1j * f / fc
    return 1 / (s * s + math.sqrt(2) * s + 1)


def bw2_hp(f):
    s = 1j * f / fc
    return (s * s) / (s * s + math.sqrt(2) * s + 1)


def lr4_lp(f):
    return bw2_lp(f) ** 2


def lr4_hp(f):
    return bw2_hp(f) ** 2


xo = {}
for f in (40, 60, 70, 80, 90, 100, 120, 160):
    xo[str(f)] = {"BW2 sum in-phase dB": db(bw2_lp(f) + bw2_hp(f)), "BW2 sum inverted-sub dB": db(-bw2_lp(f) + bw2_hp(f)),
                  "LR4 sum in-phase dB": db(lr4_lp(f) + lr4_hp(f)), "LR4 sum inverted dB": db(-lr4_lp(f) + lr4_hp(f))}
R["crossover_sum"] = xo

# ---- 6) all-pass phase (0.1 uF, VR2 0..220k)
ap = {}
for rv in (0, 22e3, 47e3, 100e3, 220e3):
    row = {}
    for f in (40, 60, 80, 120):
        w = 2 * math.pi * f
        row["%dHz" % f] = -2 * math.degrees(math.atan(w * rv * 0.1e-6))
    ap["%gk" % (rv / 1e3)] = row
R["allpass_phase_deg"] = ap

json.dump(R, open("sim3_results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def show(k, v, ind=0):
    if isinstance(v, dict):
        print(" " * ind + k + ":")
        for a, b in v.items():
            show(a, b, ind + 2)
    else:
        print(" " * ind + k + ": " + (("%.4g" % v) if isinstance(v, (int, float)) else str(v)))


for k, v in R.items():
    show(k, v)
