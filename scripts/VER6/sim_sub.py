import io, contextlib, math, json
ns = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open("sim.py", encoding="utf-8").read().replace('with open("sim_results.json"', 'with open("sim_results_tmp.json"').replace('with open("sim_results_tmp.json", "w"', 'with open("sim_results_tmp.json", "w"'), ns)
sk, db, logspace, f3db = ns["sk"], ns["db"], ns["logspace"], ns["f3db"]
res = {}
hp = lambda f: (2j * math.pi * f * 22e3 * 1e-6) / (1 + 2j * math.pi * f * 22e3 * 1e-6)   # C 1uF + R 10k
chain = {}
for name, rr in (("80Hz", 12.7e3), ("100Hz", 10.2e3), ("120Hz", 8.45e3)):
    H, f0, q = sk(rr, rr, 220e-9, 110e-9)
    tot = lambda f, H=H: H(f) * hp(f)
    fs = logspace(1, 1000, 3000)
    ref = max(abs(tot(f)) for f in fs)
    lo = next(f for f in fs if abs(tot(f)) >= ref * 10 ** (-3 / 20))
    hi = next(f for f in fs if f > lo * 1.5 and abs(tot(f)) < ref * 10 ** (-3 / 20))
    chain[name] = {"band_-3dB_Hz": (lo, hi), "gain_5Hz_dB": db(tot(5)), "gain_10Hz_dB": db(tot(10)), "gain_20Hz_dB": db(tot(20)), "gain_30Hz_dB": db(tot(30)),
                   "peak_dB": db(ref), "HPF_only_fc_Hz": 1 / (2 * math.pi * 22e3 * 1e-6)}
res["chain_VER2"] = chain
# VER1 (without HPF, old caps)
old = {}
for name, c1, c2 in (("80Hz", 270e-9, 150e-9), ("100Hz", 220e-9, 110e-9), ("120Hz", 180e-9, 100e-9)):
    H, f0, q = sk(10e3, 10e3, c1, c2)
    old[name] = {"f3dB_Hz": f3db(H, 1, 1e4), "gain_5Hz_dB": db(H(5))}
res["chain_VER1"] = old
# summer
Rf, Cf, R = 4.99e3, 33e-12, 10e3
res["summer"] = {"gain_per_input": Rf / R, "correlated_gain_dB": db(2 * Rf / R), "anti_phase_gain_dB": "-inf (L=-R cancels)",
                 "Rf_Cf_pole_kHz": 1 / (2 * math.pi * Rf * Cf) / 1e3, "noise_gain": 1 + Rf / (R / 2), "GBW_limit_MHz": 40 / (1 + Rf / (R / 2)),
                 "bias_match_ohm": 1 / (1 / R + 1 / R + 1 / Rf), "Rb_ohm": 2490, "offset_mV_per_10nA": 10e-9 * abs(1 / (1 / R + 1 / R + 1 / Rf) - 2490) * 1e3}
# source loading: pre-out sees R1 = 10k per input
res["loading"] = {"Zin_per_input_ohm": R, "to_preout_dB_loss_if_Zsrc_47ohm": db(R / (R + 47))}
# output filter THAT1646 / 47R + cable 10nF
res["output"] = {"R9_47ohm_with_cable_10nF_pole_kHz": 1 / (2 * math.pi * 47 * 10e-9) / 1e3}
json.dump(res, open("sim_sub_results.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
def show(k, v, ind=0):
    if isinstance(v, dict):
        print(" " * ind + k + ":")
        for a, b in v.items():
            show(a, b, ind + 2)
    else:
        print(" " * ind + k + ": " + (("%.4g" % v) if isinstance(v, (int, float)) else str(v)))
for k, v in res.items():
    show(k, v)
