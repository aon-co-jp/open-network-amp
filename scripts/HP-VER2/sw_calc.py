import math
ROUT = 0.04                       # amplifier output impedance (ohm), assumed
def df(rl, rc): return rl / (ROUT + rc)
def level_db(rl, rc): return 20 * math.log10(rl / (rl + rc))
KINDS = [("安価なトグル (30mΩ→経年で増加)", 0.03, 0.010, 5e4, (190, 30, 30)), ("本設計のリレー (5mΩ)", 0.005, 0.0002, 1e7, (25, 115, 60))]
def rc_after(kind, years): return kind[1] + kind[2] * years
def life_years(ops, ops_per_day): return ops / ops_per_day / 365.0
if __name__ == "__main__":
    for n, r0, dr, ops, col in KINDS:
        print(n, "DF new", round(df(8, r0)), "DF after 10 y", round(df(8, r0 + dr * 10)), "level dB", round(level_db(8, r0), 4), "life at 20/day", round(life_years(ops, 20), 1), "y; at 100/day", round(life_years(ops, 100), 1))
    print("sub line level 10k load, 5 mohm:", round(level_db(10000, 0.005), 7), "dB")
