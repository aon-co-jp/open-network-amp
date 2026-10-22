import math
SDIR = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
exec(open(SDIR + r"\plot_helpers.py", encoding="utf-8").read())
c = {}
exec(open(SDIR + r"\sw_calc.py", encoding="utf-8").read().replace('if __name__ == "__main__":', 'if False:'), c)
GR, BL, RD, PU, OR = (25, 115, 60), (30, 70, 180), (190, 30, 30), (120, 60, 160), (200, 120, 20)
text(3, 127, "ON/OFF スイッチ TEST / DEBUG: 接触抵抗・寿命・経年変化  Switch contact resistance, life and ageing", 2.3, INK, "la", True)
text(3, 123.6, "Python による設計計算 (SPICE・実機測定ではありません)。仮定: アンプ出力抵抗 0.04Ω、負荷 8Ω、トグル 5 万回・リレー 1000 万回 (ゼロ電流開閉)。 Python calculations with assumed contact data.", 1.2, GRY)
mx, my = plot(8, 72, 62, 108, 0, 100, 0, 200, False, "① 接触抵抗とダンピングファクター (8Ω)  Damping factor vs contact resistance", "接触抵抗 (mΩ)", "DF")
curve(mx, my, [(r, c["df"](8, r / 1000.0)) for r in range(0, 101, 2)], PU)
text(mx(5), my(c["df"](8, 0.005)) - 3.0, "5mΩ: DF %.0f" % c["df"](8, 0.005), 1.0, GR, "lm", True)
text(mx(100), my(c["df"](8, 0.1)) + 2.6, "100mΩ: DF %.0f" % c["df"](8, 0.1), 1.0, RD, "rm", True)
mx, my = plot(70, 72, 124, 108, 1, 200, 0.5, 5000, True, "② 寿命 (年) と 1 日の操作回数  Life vs operations per day", "1 日の操作回数", "年")
for kind in c["KINDS"]:
    curve(mx, my, [(o, min(5000, c["life_years"](kind[3], o))) for o in (1, 2, 5, 10, 20, 50, 100, 200)], kind[4])
legend(76, 106, [(k[0], k[4], False) for k in c["KINDS"]])
mx, my = plot(132, 72, 192, 108, 0, 10, 0, 200, False, "③ 経年のダンピングファクター  Damping factor over the years", "経過年数", "DF")
for kind in c["KINDS"]:
    curve(mx, my, [(y, c["df"](8, c["rc_after"](kind, y))) for y in range(0, 11)], kind[4])
legend(138, 106, [(k[0], k[4], False) for k in c["KINDS"]])
text(6, 62, "結果 (全文は下の 8 言語の説明)  Results (full text in 8 languages below)", 1.5, INK, "la", True)
rows = ["TEST 1: 接触抵抗 5mΩ (リレー) ならダンピングファクター %.0f、レベル変化 %.3fdB。100mΩ (劣化したトグル) だと DF %.0f・%.2fdB。" % (c["df"](8, 0.005), c["level_db"](8, 0.005), c["df"](8, 0.1), c["level_db"](8, 0.1)),
        "TEST 2: 寿命は 1 日 20 回の操作で、トグル(5 万回)が 約 %.1f 年、リレー(1000 万回、ゼロ電流開閉)が 約 %.0f 年。" % (c["life_years"](5e4, 20), c["life_years"](1e7, 20)),
        "TEST 3 [不具合]: 信号を通すトグルは 10 年後に DF が %.0f → %.0f (経年の接触抵抗増加を仮定)。→ 修正: ユーザーが触るのは非接触スイッチ、信号は密閉リレーだけを通す。" % (c["df"](8, c["rc_after"](c["KINDS"][0], 0)), c["df"](8, c["rc_after"](c["KINDS"][0], 10))),
        "TEST 4: サブウーファー出力 (ライン、10kΩ 負荷) の 5mΩ は レベル変化 約 %.0e dB で無視できる。" % abs(c["level_db"](10000, 0.005))]
y = 59.5
for r_ in rows:
    text(6, y, r_, 1.05, INK, "la"); y -= 2.3
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = SDIR + r"\amp_sw_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300)); print(out, round(y, 1))
