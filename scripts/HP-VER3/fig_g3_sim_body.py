import math
SDIR = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
exec(open(SDIR + r"\plot_helpers.py", encoding="utf-8").read())
c = {}
exec(open(SDIR + r"\g3_calc.py", encoding="utf-8").read().replace('if __name__ == "__main__":', 'if False:'), c)
GR, BL, RD, PU, OR = (25, 115, 60), (30, 70, 180), (190, 30, 30), (120, 60, 160), (200, 120, 20)
text(3, 127, "ゲイン調整 TEST / DEBUG: ビット深度・リレー動作・精度  Gain control: bit depth, relay operations, accuracy", 2.3, INK, "la", True)
text(3, 123.6, "Python による設計計算 (SPICE・実機測定ではありません)。仮定: デジタル 32bit、リレー 1000 万回、1 日 1000 ステップの操作。 Python calculations with assumed 32-bit path and 10-million-operation relays.", 1.2, GRY)
mx, my = plot(8, 72, 62, 108, 0, 18, 28, 33, False, "① ゲインとビット深度 (bit)  Effective bits vs gain", "ゲイン (dB、1dB 刻み)", "bit")
curve(mx, my, [(g, c["bits"](g, "analog")) for g in range(0, 19)], GR)
curve(mx, my, [(g, c["bits"](g, "digital")) for g in range(0, 19)], RD)
curve(mx, my, [(g, c["bits"](g, "mixed")) for g in range(0, 19)], BL)
legend(12, 106, [("ANALOG: 32bit のまま", GR, False), ("DIGITAL: 18dB で %.1fbit" % c["bits"](18, "digital"), RD, False), ("ANALOG+DIGITAL: 最小 %.1fbit" % c["bits"](5, "mixed"), BL, False)])
mx, my = plot(70, 72, 124, 108, 0, 18, 0, 6, False, "② 1 ステップで動くリレーの数  Relays toggled per step", "ゲイン (dB)", "個")
for g in range(18):
    ta = sum(a != b for a, b in zip(c["analog_state"](g), c["analog_state"](g + 1)))
    tm = sum(a != b for a, b in zip(c["mixed_state"](g), c["mixed_state"](g + 1)))
    d.rectangle([*P(mx(g + 0.1), my(ta)), *P(mx(g + 0.5), my(0))], fill=RD)
    d.rectangle([*P(mx(g + 0.5), my(tm)), *P(mx(g + 0.9), my(0))], fill=BL)
legend(76, 106, [("ANALOG (最大 5 個が同時に動く)", RD, False), ("ANALOG+DIGITAL (最大 2 個)", BL, False)])
mx, my = plot(132, 72, 192, 108, 100, 5000, 1, 1000, True, "③ リレー寿命 (年) と 1 日の操作ステップ数  Relay life vs steps per day", "1 日のステップ数", "年")
for st, col in ((c["analog_state"], RD), (c["mixed_state"], BL)):
    t, _ = c["toggles"](st)
    curve(mx, my, [(n, min(1000, c["relay_years"](t, n))) for n in (100, 200, 500, 1000, 2000, 5000)], col)
legend(138, 106, [("ANALOG", RD, False), ("ANALOG+DIGITAL", BL, False)])
text(6, 62, "結果 (全文は下の 8 言語の説明)  Results (full text in 8 languages below)", 1.5, INK, "la", True)
ta, tmax = c["toggles"](c["analog_state"]); tm, tmmax = c["toggles"](c["mixed_state"])
rows = ["TEST 1: DIGITAL モードでは 18dB で 32bit のうち %.1fbit が残る (24bit 音源には十分)。ANALOG+DIGITAL は最小でも %.1fbit。" % (c["bits"](18, "digital"), c["bits"](5, "mixed")),
        "TEST 2 [不具合]: ANALOG モードの 1dB 刻みは、境目 (例: 11→12dB) で最大 %d 個のリレーが同時に動き、ゲインが一瞬飛ぶ → 修正: メイク・ビフォア・ブレイク + 3ms ミュート。" % tmax,
        "TEST 3: 1 日 1000 ステップの操作で、リレー寿命は ANALOG が 約 %.0f 年、ANALOG+DIGITAL は 約 %.0f 年 (動作が 1/9 以下)。" % (c["relay_years"](ta, 1000), c["relay_years"](tm, 1000)),
        "TEST 4: 微調整の精度は 0.1%% 抵抗で 約 %.2fdB、1%% 抵抗だと 約 %.2fdB → 0.1%% 薄膜を採用。" % (c["step_error_db"](0.001), c["step_error_db"](0.01))]
y = 59.5
for r_ in rows:
    text(6, y, r_, 1.05, INK, "la"); y -= 2.3
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = SDIR + r"\amp_gain3_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300)); print(out, round(y, 1))
