
# ================= VER3 additional circuits (drawn below the main schematic) =================
SIGC = globals().get("SIGC", (25, 115, 60))
frame(1, -46, 199, -1, "VER5 追加回路 (SW4 で挿入)  VER5 added circuits  [片側のみ図示 / one leg shown]")
# ---- (a) all-pass phase control
A = -24
text(6, -6.5, "位相 連続可変 (1次オールパス)  Variable phase", 1.3, INK, "la", True)
text(6, -9.2, "VR2 を回すと 0〜−165° (60Hz)。SW2 の 180° 反転と併用で 0〜345°", 1.0, GRY, "la")
text(6, A + 1.2, "IN", 1.2, SIGC, "rm", True)
line([(7, A), (10, A)], SIGC)
dot(8, A, SIGC)
res(14, A, "R15", "10k", SIGC)
line([(18, A), (22, A), (22, A + 3.25), (42.5, A + 3.25)], SIGC)
dot(22, A + 3.25, SIGC)
plus, minus, out = opamp(48, A, "U4", "OPA1612", plus_top=False)
line([(22, A + 3.25), (22, A + 8), (32, A + 8)], SIGC)
res(36, A + 8, "R16", "10k", SIGC)
line([(40, A + 8), (57, A + 8), (57, A)], SIGC)
line([out, (57, A)], SIGC)
dot(57, A, SIGC)
line([(8, A), (8, A - 6), (10, A - 6)], SIGC)
res(14, A - 6, "VR2", "0-220k", SIGC)
line([(18, A - 6), (30, A - 6), (30, A - 3.25), (42.5, A - 3.25)], SIGC)
dot(30, A - 6, SIGC)
line([(30, A - 6), (30, A - 8.1)], SIGC)
d.line([*P(27.4, A - 8.1), *P(32.6, A - 8.1)], fill=SIGC, width=LW)
d.line([*P(27.4, A - 9.9), *P(32.6, A - 9.9)], fill=SIGC, width=LW)
text(34.5, A - 9.0, "C7 100n PPS", 1.1, GRY, "lm")
line([(30, A - 9.9), (30, A - 12)], SIGC)
gnd(30, A - 12)
line([(57, A), (64, A)], SIGC)
text(65, A, "→ 次段", 1.1, SIGC, "lm", True)

# ---- (b) second LPF stage for LR4 (24 dB/oct)
r = -26
text(76, -6.5, "2段目 LPF (LR4 24dB/oct)  2nd LPF stage", 1.3, INK, "la", True)
text(76, -9.2, "SW4 で挿入。R は SW3 と連動 (6.34k / 5.11k / 4.22k)", 1.0, GRY, "la")
text(75, r + 1.2, "IN", 1.2, SIGC, "rm", True)
line([(76, r), (76.5, r)], SIGC)
res(80, r, "R5'", "6.34k..", SIGC)
line([(84, r), (88, r)], SIGC)
dot(86, r, SIGC)
res(92, r, "R6'", "6.34k..", SIGC)
line([(96, r), (98, r), (98, r + 3.25), (102.5, r + 3.25)], SIGC)
dot(98, r, SIGC)
plus2, minus2, out2 = opamp(108, r, "U3", "OPA1612", plus_top=True)
line([(98, r), (98, r - 5.2)], SIGC)
d.line([*P(95.4, r - 5.2), *P(100.6, r - 5.2)], fill=SIGC, width=LW)
d.line([*P(95.4, r - 7.0), *P(100.6, r - 7.0)], fill=SIGC, width=LW)
text(94, r - 6.1, "C2' 220n", 1.0, GRY, "rm")
line([(98, r - 7.0), (98, r - 10)], SIGC)
gnd(98, r - 10)
line([(86, r), (86, r + 9), (88.6, r + 9)], SIGC)
d.line([*P(88.6, r + 11.6), *P(88.6, r + 6.4)], fill=SIGC, width=LW)
d.line([*P(90.4, r + 11.6), *P(90.4, r + 6.4)], fill=SIGC, width=LW)
text(89.5, r + 14.0, "C1' 440n", 1.0, GRY, "mm")
line([(90.4, r + 9), (116, r + 9), (116, r)], SIGC)
line([minus2, (100.5, minus2[1]), (100.5, r - 13), (116, r - 13), (116, r)], SIGC)
line([out2, (116, r)], SIGC)
dot(116, r, SIGC)
line([(116, r), (122, r)], SIGC)
text(123, r, "→ 出力へ", 1.1, SIGC, "lm", True)

# ---- (c) notes
d.rectangle([*P(138, -3), *P(197, -44)], outline=(150, 160, 190), width=int(LW * .7), fill=(252, 252, 247))
text(168, -6.0, "VER5 の変更点 (TEST/DEBUG 3 回)", 1.35, INK, "mm", True)
for i, t in enumerate([
    "① 雑音 0.40 → 0.29 µV (-2.9 dB): SK の R を半分に・C を 2 倍に、",
    "   HPF を 10k + 2.2µF、加算段 3.32k/1.65k (プリアウト負荷 -0.12dB)",
    "② GND リフト SW9 (XLR 1番ピン): ハムを避ける (R11||C5 ⇄ 開放)",
    "③ 出力ミュートリレー K2: 電源 ON/OFF 時のポップ音を防ぐ",
    "④ LR4 (SW4)・位相連続可変 (VR2)・サブソニック HPF は継続",
    "Noise -2.9 dB; ground lift SW9; mute relay K2; LR4, phase and HPF kept."]):
    text(139, -9.6 - 3.8 * i, t, 1.05, INK if i < 5 else GRY, "la")
