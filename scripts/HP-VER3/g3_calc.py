import math, random
FINE = {0: (0, 0, 0), 1: (1, 0, 0), 2: (0, 1, 0), 3: (1, 1, 0), 4: (0, 1, 1), 5: (1, 1, 1)}   # relays of 1, 2, 2 dB
COARSE = {0: (0, 0), 1: (1, 0), 2: (0, 1), 3: (1, 1)}                                         # relays of 6 and 12 dB
def analog_state(g):
    return COARSE[g // 6] + FINE[g % 6]
def mixed_state(g):
    return COARSE[g // 6]
def toggles(state_fn, lo=0, hi=18):
    t = [sum(a != b for a, b in zip(state_fn(g), state_fn(g + 1))) for g in range(lo, hi)]
    return sum(t) / len(t), max(t)
def bits(gain_db, mode, width=32):
    if mode == "analog":
        return width
    if mode == "digital":
        return width - gain_db / 6.02
    return width - (gain_db % 6) / 6.02            # analog + digital: the digital part is only the fine 0-5 dB
def step_error_db(tol, n=2000, seed=1):
    """spread (std) of the gain error of the 1/2/2 dB fine ladder with resistors of the given tolerance."""
    rnd = random.Random(seed)
    errs = []
    for _ in range(n):
        e = 0.0
        for g in range(6):
            # each active relay stage has a gain set by a ratio of two resistors
            tot = 0.0
            for (on, w) in zip(FINE[g], (1.0, 2.0, 2.0)):
                if on:
                    r1, r2 = 1 + rnd.gauss(0, tol / 2), 1 + rnd.gauss(0, tol / 2)
                    ratio = 10 ** (w / 20.0)
                    tot += 20 * math.log10((ratio * r1) / r2 / ratio) if True else 0
            e = max(e, abs(tot))
        errs.append(e)
    errs.sort()
    return errs[int(0.95 * n)]
def relay_years(toggles_per_step, steps_per_day, ops=1e7):
    ops_day = toggles_per_step * steps_per_day
    return ops / max(ops_day, 1e-9) / 365.0
if __name__ == "__main__":
    print("toggles/step analog", toggles(analog_state), "mixed", toggles(mixed_state))
    for g in (0, 6, 12, 18):
        print(g, "bits digital", round(bits(g, "digital"), 2), "mixed", round(bits(g, "mixed"), 2))
    print("err 95% 0.1%", round(step_error_db(0.001), 4), "1%", round(step_error_db(0.01), 4))
    for n, st in (("analog", analog_state), ("mixed", mixed_state)):
        t, _ = toggles(st)
        print(n, "relay life at 1000 steps/day", round(relay_years(t, 1000), 1), "y")


# ---------------------------------------------------------------- volume (attenuation 0..-90 dB in 1 dB steps)
VCOARSE_W = (6, 12, 24, 48)                       # coarse attenuator relays (dB)
def vol_analog_state(a):
    c = (a // 6)
    coarse = tuple((c >> i) & 1 for i in range(4))
    return coarse + FINE[a % 6]
def vol_mixed_state(a):
    c = (a // 6)
    return tuple((c >> i) & 1 for i in range(4))
def vol_toggles(fn, hi=90):
    t = [sum(x != y for x, y in zip(fn(a), fn(a + 1))) for a in range(0, hi)]
    return sum(t) / len(t), max(t)
def vol_bits(att, mode, width=32):
    if mode == "analog":
        return width
    if mode == "digital":
        return width - att / 6.02
    return width - (att % 6) / 6.02
