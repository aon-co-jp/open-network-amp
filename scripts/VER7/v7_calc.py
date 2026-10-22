import math
S, DIST, STEREO, R = 87.0, 3.0, 3.0, 8.0              # speaker 87 dB/W/m, 3 m, two speakers, 8 ohm
VAB, VA = 45.0, 24.0
spl = lambda p: S + STEREO + 10 * math.log10(p) - 20 * math.log10(DIST)
need = lambda s: 10 ** ((s - S - STEREO + 20 * math.log10(DIST)) / 10.0)
IB_A, IB_H = 1.5, 0.75
P_A = IB_A ** 2 * R / 2                                # single-ended class A with a current source
P_H = 2 * IB_H ** 2 * R                                # push-pull with bias per device (class A up to 2*Ib)
heat_A = 2 * VA * IB_A                                 # per channel idle
heat_H = 2 * VAB * IB_H


def ps_ab(po, v=VAB, bias=0.05):
    ipk = math.sqrt(2 * po / R)
    return 2 * v / math.pi * ipk + 2 * v * bias


def pd_A(po):
    return heat_A if po <= P_A else None


def pd_H(po):
    ps = max(heat_H, ps_ab(po, VAB, 0.0))
    return ps - po


def pd_AB(po):
    return ps_ab(po) - po


def pd_D(po):
    return po * (1 / 0.9 - 1) + 1.5


# average listening: music averages about 15 dB below the peak
avg_w = lambda peak_w: peak_w / 10 ** 1.5
kwh = lambda w_total, hrs=4: w_total * hrs * 365 / 1000.0
if __name__ == "__main__":
    for s in (75, 80, 85, 90, 95, 100):
        print(s, "dB peak needs", round(need(s), 2), "W")
    print("P_A", round(P_A, 1), "SPL at P_A", round(spl(P_A), 1), "P_H", round(P_H, 1))
    print("heat idle A", heat_A, "H", heat_H, "stereo", 2 * heat_A, 2 * heat_H)
    print("AB idle", 2 * VAB * 0.05, "D idle", 1.5)
    pk = need(100)
    print("100 dB peak needs", round(pk), "W; avg", round(avg_w(pk), 2), "W")
    for n, f in (("A", lambda: 2 * heat_A), ("H", lambda: 2 * pd_H(avg_w(need(90))) + 0), ("AB", lambda: 2 * pd_AB(avg_w(need(90)))), ("D", lambda: 2 * pd_D(avg_w(need(90))))):
        print(n, "avg heat W (stereo, 90 dB peak)", round(f(), 1), "kWh/yr", round(kwh(f()), 0))
