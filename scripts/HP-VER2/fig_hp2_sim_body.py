import math
SDIR = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
exec(open(SDIR + r"\plot_helpers.py", encoding="utf-8").read())
c = {}
exec(open(SDIR + r"\hp2_calc.py", encoding="utf-8").read().replace('if __name__ == "__main__":', 'if False:'), c)
GR, BL, RD, PU, OR = (25, 115, 60), (30, 70, 180), (190, 30, 30), (120, 60, 160), (200, 120, 20)
text(3, 127, "HP-VER2 TEST / DEBUG: ヘッドホンアンプ (3.5・4.4・6.35mm・XLR)・ゲイン  Headphone amplifier: power, gain and hiss", 2.3, INK, "la", True)
text(3, 123.6, "Python による設計計算 (SPICE・実機測定ではありません)。仮定: ±15V レール (振幅 13V)、電流バッファ 1A、出力ノイズ 4µVrms (0dB)。 Python design calculations with assumed rails and noise.", 1.2, GRY)
mx, my = plot(8, 72, 62, 108, 16, 600, 0.05, 12, True, "① 最大出力 (W) と負荷抵抗  Max power vs load", "ヘッドホンの抵抗 (Ω)", "W")
curve(mx, my, [(r, min(12, c["p_max"](r, False))) for r in (16, 20, 25, 32, 40, 50, 64, 80, 100, 150, 200, 300, 400, 600)], RD)
curve(mx, my, [(r, min(12, c["p_max"](r, True))) for r in (16, 20, 25, 32, 40, 50, 64, 80, 100, 150, 200, 300, 400, 600)], GR)
legend(12, 106, [("アンバランス (3.5・6.35mm)", RD, False), ("バランス (4.4・XLR・3.5mm TRRS): 電圧 2 倍 → 約 4 倍", GR, False)])
mx, my = plot(70, 72, 124, 108, 0, 18, -10, 55, False, "② ゲインとヒス音 (dB SPL)  Hiss level vs gain", "ゲイン (dB)", "dB SPL")
for (n, s, r), col in zip(c["CASES"], (RD, OR, GR, BL)):
    curve(mx, my, [(g, c["hiss_spl"](g, s, r)) for g in range(0, 19)], col)
line([(mx(0), my(30)), (mx(18), my(30)), ], (150, 150, 150), int(LW * .6))
text(mx(17.8), my(30) + 1.8, "30dB 目安", 1.0, GRY, "rm")
legend(76, 106, [(n, col, False) for (n, s, r), col in zip(c["CASES"], (RD, OR, GR, BL))])
mx, my = plot(132, 72, 192, 108, 0, 5, 0, 1.2, False, "③ 100dB SPL に必要な電圧 (Vrms)  Voltage needed for 100 dB SPL", "", "Vrms")
for i, (n, s, r) in enumerate(c["CASES"]):
    v = c["v_for_spl"](100, s, r)
    d.rectangle([*P(mx(0.2 + i * 1.2), my(v)), *P(mx(1.0 + i * 1.2), my(0))], fill=(RD, OR, GR, BL)[i])
    text(mx(0.6 + i * 1.2), my(v) + 1.6, "%.2f" % v, 1.0, INK, "mm", True)
    text(mx(0.6 + i * 1.2), my(0) - 1.8, n.split(" ")[0], 0.9, GRY, "mm")
text(6, 62, "結果 (全文は下の 8 言語の説明)  Results (full text in 8 languages below)", 1.5, INK, "la", True)
rows = ["TEST 1: 32Ω では アンバランス 約 2.6W、バランス 約 10.6W。300Ω でも バランス 約 1.1W。→ 高インピーダンスの機種はバランス (4.4mm・XLR) が有利。",
        "TEST 2 [不具合]: +18dB 固定だと 高感度イヤホン (16Ω・120dB/mW) のヒスが 約 48dB SPL で聞こえる (0dB では約 30dB)。→ 抵抗検出で 0dB 側を推奨するゲイン自動推奨を追加。",
        "TEST 3: 100dB SPL に必要な電圧は 16Ω イヤホンで 約 0.01V、600Ω で 約 1V → ゲインは 0 / +6 / +12 / +18dB の 4 段で足りる。",
        "TEST 4 [注意]: 4.4mm / XLR / 3.5mm TRRS のピン配置は 規格により異なる。バランスのジャックに アンバランスのプラグを挿しても Cold を GND に落とさないよう、ジャック検出で Cold を切り離す。"]
y = 59.5
for r_ in rows:
    text(6, y, r_, 1.05, INK, "la"); y -= 2.3
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = SDIR + r"\amp_hp2_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, round(y, 1))
