import math
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\plot_helpers.py", encoding="utf-8").read())
GR, BL, RD, PU, OR = (25, 115, 60), (30, 70, 180), (190, 30, 30), (120, 60, 160), (200, 120, 20)
text(3, 127, "VER5 追加 TEST / DEBUG (4〜6 回目): 耐久性と音質  VER5 extra rounds 4-6: durability and sound", 2.4, INK, "la", True)
text(3, 123.6, "Python による計算 (寿命・温度・リップルの設計計算)。実機測定ではありません。仮定は各項目に記載。", 1.45, GRY)
text(3, 121.2, "Calculated in Python (design arithmetic for life, temperature and ripple). Not bench measurements. Assumptions are listed per item.", 1.2, GRY)

# 1) electrolytic capacitor life (10,000 h at 105 C, life doubles per 10 C)
mx, my = plot(8, 70, 62, 108, 30, 95, 1, 400, True and False, "① 電解コンデンサの寿命 (105°C 10,000h 品)  Capacitor life", "周囲温度 (°C)", "年")
life = lambda t: 10000 * 2 ** ((105 - t) / 10) / 8760
curve(mx, my, [(t, min(400, life(t))) for t in range(30, 96)], BL)
for t, col in ((45, GR), (60, OR), (85, RD)):
    text(mx(t), my(min(400, life(t))) + 2.4, "%d°C: %.1f 年" % (t, life(t)), 1.0, col, "mm", True)
# 2) junction temperature vs load for the Class AB output stage
mx, my = plot(70, 70, 124, 108, 4, 16, 60, 170, False, "② Class AB 出力素子の接合部温度 (最悪 = 最大出力の 1/3 付近)  Junction temperature", "負荷 (Ω)", "°C")


def tj(rl, pairs):
    p = 2 * 45.0 ** 2 / (math.pi ** 2 * rl)         # worst-case total dissipation per channel
    per = p / (2 * pairs)
    return 40 + per * (0.7 + 0.3 + 1.0)


curve(mx, my, [(r / 2, tj(r / 2, 1)) for r in range(8, 33)], RD)
curve(mx, my, [(r / 2, tj(r / 2, 2)) for r in range(8, 33)], GR)
line([(mx(4), my(125)), (mx(16), my(125))], (150, 150, 150), int(LW * .6))
text(97, 95.0, "125°C (目標上限)", 0.95, GRY, "mm")
legend(78, 105, [("出力素子 1 組 (4Ω で 143°C)", RD, False), ("2 並列 (VER5): 4Ω でも 91°C", GR, False)])
# 3) supply ripple at the rails
mx, my = plot(132, 70, 192, 108, 0, 4, 0, 800, False, "③ レールのリップル (100Hz、3A)  Rail ripple", "段階", "µVpp")
rip = [("整流後", 750000), ("定電圧 PSRR 60dB", 750), ("+容量倍増 +20dB", 75)]
for i, (lab, v) in enumerate(rip):
    xa = 0.4 + i * 1.2
    h = (my(min(v, 800)) - my(0))
    d.rectangle([*P(mx(xa), my(min(v, 800))), *P(mx(xa + 0.8), my(0))], fill=[RD, OR, GR][i])
    text(mx(xa + 0.4), my(min(v, 800)) + 1.6, "%g µV" % v if v < 1000 else "750 mV", 1.0, INK, "mm", True)
    text(mx(xa + 0.4), my(0) - 1.8, lab, 0.9, GRY, "mm")
rows = [
    ("TEST 4 (耐久: コンデンサ): 105°C 10,000h 品の寿命は、周囲 45°C で約 73 年、60°C で約 26 年だが、ヒートシンクのそば (85°C) だと約 4.6 年。→ 問題あり。対策: 大容量コンデンサは外付け電源に置き (筐体外・45°C 以下)、本体の信号経路はフィルム/ポリマー品にし、ヒートシンクから離す。",
     "TEST 4 (durability, capacitors): a 105 C / 10,000 h part lasts about 73 years at 45 C and about 26 years at 60 C but only about 4.6 years next to a heatsink (85 C). Fix: the large capacitors sit in the external supply, the signal path uses film or polymer parts, and everything is kept away from heatsinks."),
    ("TEST 5 (耐久: 熱): Class AB 出力素子 (±45V) の接合部温度は、8Ω で約 92°C だが 4Ω では約 143°C (目標 125°C 超)。→ 問題あり。対策: 出力素子を 2 並列にして 4Ω でも約 91°C、ヒートシンク 90°C で温度保護、Class A は θ ≤ 0.3°C/W/ch + 温度制御ファン + 高温時にアイドル電流を下げる。",
     "TEST 5 (durability, heat): the Class AB junction temperature (+-45 V) is about 92 C at 8 ohm but about 142 C at 4 ohm, above the 125 C target. Fix: two output pairs in parallel give about 91 C even at 4 ohm, over-temperature protection at 90 C on the heatsink, and for Class A a heatsink of 0.3 C/W or better per channel, a temperature-controlled fan and a lower idle current when hot."),
    ("TEST 6 (音質: 電源リップル): 整流後のリップル 0.75Vpp (4×10,000µF、3A) を、定電圧回路 (PSRR 60dB と仮定) で 750µVpp、容量倍増でさらに 20dB (仮定) 下げて 75µVpp にする。目標 100µVpp 未満。",
     "TEST 6 (sound, supply ripple): the 0.75 Vpp ripple after rectification (4 x 10,000 uF, 3 A) becomes 750 uVpp through a regulator (PSRR assumed 60 dB) and 75 uVpp with a capacitance multiplier (another 20 dB, assumed). The target is below 100 uVpp."),
    ("そのほか: 真空管 (12AU7) は約 10,000 時間 = 1 日 4 時間で約 6.8 年、ヒーターのソフトスタートと B+ の遅延投入で寿命を延ばす。リレー式ボリュームは 1 日 500 回で約 55 年。ヘッドホンジャックは基板ごと交換できるサブ基板に (嵌合 約 5,000 回 = 1 日 5 回で約 2.7 年)。電源は NTC + リレーの突入電流制限・MOV・DC 検出・過電流・温度の保護。",
     "Others: a tube (12AU7) lasts about 10,000 hours, which is about 6.8 years at 4 hours a day, and the heater soft start and delayed B+ extend it. The relay volume lasts about 55 years at 500 operations a day. The headphone jacks sit on a replaceable sub-board (about 5,000 mating cycles, about 2.7 years at 5 per day). The supply has NTC + relay inrush limiting, MOV, DC detection and over-current and temperature protection."),
    ("未実施: 実機の温度・寿命の測定、過渡応答、歪み (THD)、実機の雑音と位相。数値は設計用の計算と仮定です。",
     "Not done: real temperature and life measurements, transient response, THD, and real noise and phase. The numbers are design calculations and assumptions."),
]
y = 60
text(6, 63.5, "TEST / DEBUG の記録 (耐久性と音質)  Log (durability and sound)", 1.6, INK, "la", True)
for ja, en in rows:
    text(6, y, ja, 1.05, INK, "la")
    text(6, y - 2.0, en, 0.95, GRY, "la")
    y -= 5.8
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_ver5b_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size, round(life(45), 1), round(life(60), 1), round(life(85), 1), round(tj(4, 1)), round(tj(8, 1)), round(tj(4, 2)))
