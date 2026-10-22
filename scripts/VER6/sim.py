import cmath, math, json

R = {}   # results


def db(x):
    return 20 * math.log10(abs(x)) if abs(x) > 0 else -400


def logspace(a, b, n):
    return [a * (b / a) ** (i / (n - 1)) for i in range(n)]


def f3db(H, fmin=1, fmax=1e7):
    """first -3 dB frequency (relative to |H| at fmin)"""
    ref = abs(H(fmin))
    for f in logspace(fmin, fmax, 4000):
        if abs(H(f)) < ref * 10 ** (-3 / 20):
            return f
    return None


# ---------------------------------------------------------------- A) Sallen-Key LPF (unity gain)
def sk(R1, R2, C1, C2):
    # C1: feedback cap (to output), C2: to ground
    def H(f):
        s = 2j * math.pi * f
        return 1 / (1 + s * C2 * (R1 + R2) + s * s * R1 * R2 * C1 * C2)
    q = math.sqrt(R1 * R2 * C1 * C2) / (C2 * (R1 + R2))
    f0 = 1 / (2 * math.pi * math.sqrt(R1 * R2 * C1 * C2))
    return H, f0, q


sk_res = {}
for name, c1, c2 in (("80Hz", 270e-9, 150e-9), ("100Hz", 220e-9, 110e-9), ("120Hz", 180e-9, 100e-9)):
    H, f0, q = sk(10e3, 10e3, c1, c2)
    f3 = f3db(H, 1, 1e4)
    pk = max(db(H(f)) for f in logspace(10, 1000, 2000))
    sk_res[name] = {"f0": f0, "Q": q, "f3dB": f3, "peak_dB": pk, "att_2f_dB": db(H(2 * float(name[:-2])))}
R["sallen_key"] = sk_res

# ---------------------------------------------------------------- B) mono sum
R["mono_sum"] = {"gain_per_input": 4.99 / 10, "correlated_gain_dB": db(2 * 4.99 / 10), "note": "L=R -> (L+R)*0.499 = 0.998 (≈0 dB)"}

# ---------------------------------------------------------------- C) I/V + diff LPF
Hd = lambda f: 1 / (1 + 2j * math.pi * f * 2 * 1.2e3 * 470e-12)
Hs = lambda f: 1 / (1 + 2j * math.pi * f * 1.2e3 * 1e-9)
R["lpf_diff"] = {"fc_balanced_Hz": f3db(Hd, 10, 1e8), "fc_single_Hz": f3db(Hs, 10, 1e8)}

# ---------------------------------------------------------------- D) Class D output LC filter
def lc(L, C, Rl, Rz=None, Cz=None, Rs=0.0):
    def H(f):
        s = 2j * math.pi * f
        ZC = 1 / (s * C)
        Zload = Rl
        Y = 1 / Zload + s * C
        if Rz is not None:
            Y += 1 / (Rz + 1 / (s * Cz))
        Zp = 1 / Y
        return Zp / (Zp + s * L + Rs)
    return H


cd = {}
for name, L, C in (("10uH/1uF", 10e-6, 1e-6), ("22uH/0.47uF", 22e-6, 0.47e-6), ("15uH/0.68uF", 15e-6, 0.68e-6)):
    for rl in (8, 4):
        H = lc(L, C, rl)
        fs = logspace(1e3, 5e6, 3000)
        pk = max(db(H(f)) for f in fs)
        fpk = max(fs, key=lambda f: abs(H(f)))
        cd[name + " @%dohm" % rl] = {"peak_dB": pk, "f_peak_kHz": fpk / 1e3, "f3dB_kHz": f3db(H, 1e3, 5e6) / 1e3, "att_500kHz_dB": db(H(5e5)),
                                      "gain_20kHz_dB": db(H(20e3)), "Q": rl * math.sqrt(C / L)}
R["class_d_filter"] = cd

# ---------------------------------------------------------------- E) Tube stage (Koren model)
def koren(mu, ex, kg1, kp, kvb):
    def Ip(vpk, vgk):
        if vpk <= 0:
            return 0.0
        e1 = vpk / kp * math.log(1 + math.exp(kp * (1 / mu + vgk / math.sqrt(kvb + vpk * vpk))))
        return (max(e1, 0) ** ex) / kg1 * 2 if e1 > 0 else 0.0   # (1+sgn(E1)) = 2
    return Ip


ax7 = koren(100, 1.4, 1060, 600, 300)
au7 = koren(21.5, 1.3, 1180, 84, 300)


def solve_v1(bplus=250.0, rd=4.7e3, rp=100e3, rk=1.5e3):
    lo, hi = 0.0, 5e-3
    for _ in range(80):
        ia = (lo + hi) / 2
        vk = ia * rk
        vp = bplus - ia * (rd + rp)
        i_model = ax7(vp - vk, -vk)
        if i_model > ia:
            lo = ia
        else:
            hi = ia
    return ia, bplus - ia * (rd + rp), ia * rk


ia1, vp1, vk1 = solve_v1()
vpk1 = vp1 - vk1
d = 1e-3
gm1 = (ax7(vpk1, -vk1 + d) - ax7(vpk1, -vk1 - d)) / (2 * d)
gp1 = (ax7(vpk1 + 1, -vk1) - ax7(vpk1 - 1, -vk1)) / 2
rp1 = 1 / gp1
rl1 = 1 / (1 / 100e3 + 1 / 470e3)
av1 = gm1 * rp1 * rl1 / (rp1 + rl1)


def solve_v2(bplus=250.0, rk=10e3, vg=None):
    # V2 grid DC = V1 plate DC (direct coupling not used; C1 blocks) -> grid at 0V via R5 to gnd
    lo, hi = 0.0, 20e-3
    for _ in range(80):
        ia = (lo + hi) / 2
        vk = ia * rk
        i_model = au7(bplus - vk, -vk)
        if i_model > ia:
            lo = ia
        else:
            hi = ia
    return ia, bplus, ia * rk


ia2, vp2, vk2 = solve_v2()
gm2 = (au7(vp2 - vk2, -vk2 + d) - au7(vp2 - vk2, -vk2 - d)) / (2 * d)
gp2 = (au7(vp2 - vk2 + 1, -vk2) - au7(vp2 - vk2 - 1, -vk2)) / 2
rp2 = 1 / gp2
zout = 1 / (gm2 + gp2 + 1 / 10e3)
R["tube"] = {"V1": {"Ia_mA": ia1 * 1e3, "Vplate_V": vp1, "Vcathode_V": vk1, "gm_mS": gm1 * 1e3, "rp_kohm": rp1 / 1e3, "gain_x": av1, "gain_dB": db(av1), "B+_after_Rd_V": 250 - ia1 * 4.7e3},
             "V2_CF": {"Ia_mA": ia2 * 1e3, "Vcathode_V": vk2, "Vgk_V": -vk2, "gm_mS": gm2 * 1e3, "Zout_ohm": zout, "Pdiss_W": ia2 * (vp2 - vk2)}}

# ---------------------------------------------------------------- F) Class A bias sensitivity
ca = {}
for vgs in (3.0, 3.5, 4.0, 4.5, 5.0, 5.5):
    ca["Vsg=%.1fV" % vgs] = (5.6 - vgs) / 0.62
R["class_a_bias_A"] = ca
R["class_a_note"] = {"peak_current_20W_8ohm_A": math.sqrt(2 * 20 / 8) / 1.0 * 1.0 / math.sqrt(8) * math.sqrt(8) / 1,
                     "Vpk_V": math.sqrt(2 * 20 * 8), "Ipk_A": math.sqrt(2 * 20 * 8) / 8, "diss_W": 48 * 2.5}

# ---------------------------------------------------------------- G) PSU transformer sizing
def psu(vout, iout, rect_drop=1.4, dropout=3.0, line=0.9, ripple_pp=1.5, freq=100.0):
    vraw_min = vout + dropout
    vpk = (vraw_min + ripple_pp / 2 + rect_drop) / line
    vac = vpk / math.sqrt(2)
    c = iout / (2 * freq * ripple_pp) if False else iout / (freq * ripple_pp)
    return {"Vout": vout, "Iout": iout, "Vsec_pk_needed": vpk, "Vac_rms_needed": vac, "C_for_ripple_uF": c * 1e6,
            "Vsec_pk_with_old": None}


R["psu"] = {"ClassA_24V_6A": psu(24, 6), "ClassAB_45V_3A": psu(45, 3), "ClassD_60V_4A": psu(60, 4)}
R["psu_old_check"] = {k: {"old_Vac": v, "Vraw_min_V (low line -10%)": (v * math.sqrt(2) * 0.9 - 1.4 - 0.75)} for k, v in (("ClassA", 18), ("ClassAB", 32), ("ClassD", 42))}
# 4x10000uF at 3 A, 100 Hz ripple
R["psu_ripple_4x10000uF_3A_100Hz_Vpp"] = 3.0 / (100 * 0.04)

# ---------------------------------------------------------------- H) Class AB hand checks
vbe = 0.65
need = 4 * vbe
R["class_ab"] = {"need_bias_V": need, "R1_over_R2": need / vbe - 1, "idle_Vre_mV_at_50mA": 50e-3 * 0.33 * 1e3,
                 "ltp_gm_mS_deg100": 1e3 / (2 * (26 + 100)), "unity_gain_MHz_Cdom33p": (1 / (2 * (26 + 100))) / (2 * math.pi * 33e-12) / 1e6}
R["class_ab"]["closed_loop_BW_MHz_gain23"] = R["class_ab"]["unity_gain_MHz_Cdom33p"] / 23

with open("sim_results.json", "w", encoding="utf-8") as fh:
    json.dump(R, fh, ensure_ascii=False, indent=1)


def show(k, v, ind=0):
    if isinstance(v, dict):
        print(" " * ind + k + ":")
        for a, b in v.items():
            show(a, b, ind + 2)
    else:
        print(" " * ind + k + ": " + (("%.4g" % v) if isinstance(v, (int, float)) else str(v)))


for k, v in R.items():
    show(k, v)


# ================================================================ AFTER (redesign) ================================================================
A = {}
# SK with resistor switching: C1=220n, C2=110n
ska = {}
for name, rr in (("80Hz", 12.7e3), ("100Hz", 10.2e3), ("120Hz", 8.45e3)):
    H, f0, q = sk(rr, rr, 220e-9, 110e-9)
    ska[name] = {"R_k": rr / 1e3, "f0": f0, "Q": q, "f3dB": f3db(H, 1, 1e4), "peak_dB": max(db(H(f)) for f in logspace(10, 1000, 2000))}
A["sallen_key_new"] = ska
# Class D 22uH / 0.47uF, BTL: per-leg load = Rspk/2
cdn = {}
for rs in (4, 8, 16):
    H = lc(22e-6, 0.47e-6, rs / 2)
    fs = logspace(1e3, 5e6, 3000)
    cdn["22uH/0.47uF speaker %dohm (per-leg %dohm)" % (rs, rs // 2)] = {"peak_dB": max(db(H(f)) for f in fs), "f3dB_kHz": f3db(H, 1e3, 5e6) / 1e3,
                                                                       "gain_20kHz_dB": db(H(20e3)), "att_500kHz_dB": db(H(5e5)), "Q": (rs / 2) * math.sqrt(0.47e-6 / 22e-6)}
cdo = {}
for rs in (4, 8, 16):
    H = lc(10e-6, 1e-6, rs / 2)
    fs = logspace(1e3, 5e6, 3000)
    cdo["10uH/1uF speaker %dohm (per-leg %dohm)" % (rs, rs // 2)] = {"peak_dB": max(db(H(f)) for f in fs), "f3dB_kHz": f3db(H, 1e3, 5e6) / 1e3, "gain_20kHz_dB": db(H(20e3)), "Q": (rs / 2) * math.sqrt(1e-6 / 10e-6)}
A["class_d_old_btl"] = cdo
A["class_d_new_btl"] = cdn
# Tube: V1 = 12AU7 half, Rp 47k, Rk 1k (unbypassed), Rd 4.7k, B+ 250; V2 = other half CF Rk 10k
def solve_au7(bplus, rd, rp, rk):
    lo, hi = 0.0, 20e-3
    for _ in range(80):
        ia = (lo + hi) / 2
        vk = ia * rk
        vp = bplus - ia * (rd + rp)
        if au7(vp - vk, -vk) > ia:
            lo = ia
        else:
            hi = ia
    return ia, bplus - ia * (rd + rp), ia * rk


ia, vp, vk = solve_au7(250, 4.7e3, 47e3, 1e3)
gm = (au7(vp - vk, -vk + d) - au7(vp - vk, -vk - d)) / (2 * d)
gpv = (au7(vp - vk + 1, -vk) - au7(vp - vk - 1, -vk)) / 2
rpv = 1 / gpv
mu = gm * rpv
rl = 1 / (1 / 47e3 + 1 / 470e3)
av = mu * rl / (rpv + rl + (mu + 1) * 1e3)
A["tube_new"] = {"V1_12AU7": {"Ia_mA": ia * 1e3, "Vplate_V": vp, "Vcathode_V": vk, "gm_mS": gm * 1e3, "rp_kohm": rpv / 1e3, "mu": mu, "gain_x": av, "gain_dB": db(av),
                              "max_input_Vrms_for_plate_swing_60Vpk": 60 / 1.414 / av},
                 "V2_12AU7_CF": {"Zout_ohm": zout, "gain_x": gm2 * (1 / (1 / 10e3 + 1 / 47e3)) / (1 + gm2 * (1 / (1 / 10e3 + 1 / 47e3)))}}
# Class A current servo
A["class_a_servo"] = {"I_set_A_at_Vset_1.43V": 1.43 / 0.62, "I_at_R7_+1pct": 1.43 / (0.62 * 1.01), "I_at_Vset_+-5mV": (1.43 + 0.005) / 0.62,
                      "note": "電流は Vset / R7 で決まり、MOSFETのVgs(3〜5.5Vで0.2〜4.2A変動)に依存しない"}
# PSU new
A["psu_new"] = {k: {"new_Vac": v, "Vraw_min_V (-10% mains)": v * math.sqrt(2) * 0.9 - 1.4 - 0.75} for k, v in (("ClassA(24V)", 24), ("ClassAB(45V)", 40), ("ClassD(60V)", 52))}
R["after"] = A
with open("sim_results.json", "w", encoding="utf-8") as fh:
    json.dump(R, fh, ensure_ascii=False, indent=1)
print("=== AFTER ===")
for k, v in A.items():
    show(k, v)
