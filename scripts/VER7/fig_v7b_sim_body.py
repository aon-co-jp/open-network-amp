import math
SDIR = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
exec(open(SDIR + r"\plot_helpers.py", encoding="utf-8").read())
c = {}
exec(open(SDIR + r"\v7b_calc.py", encoding="utf-8").read().replace('if __name__ == "__main__":', 'if False:'), c)
GR, BL, RD, PU, OR = (25, 115, 60), (30, 70, 180), (190, 30, 30), (120, 60, 160), (200, 120, 20)
text(3, 127, "VER7 追加 TEST / DEBUG (6〜10 回): 描き直した回路の再検証  Re-verification of the redrawn circuits", 2.3, INK, "la", True)
text(3, 123.6, "Python による設計計算 (SPICE・実機測定ではありません)。見つかった不具合 (TEST 7・9・10) は回路図と文書を修正済み。 Python design calculations; the bugs found (tests 7, 9, 10) were fixed in the schematics and texts.", 1.2, GRY)
mx, my = plot(8, 72, 62, 108, 0, 4, 95, 100, False, "① 出力段のゲイン (8Ω、%) と負荷電流  Output-stage gain vs load current", "負荷電流 (A)", "%")
for ib, col, lab in ((0.05, RD, "片側 50mA (AB級): 変動 %.2f%%"), (0.75, GR, "片側 0.75A (A級+AB級): %.2f%%"), (1.5, BL, "片側 1.5A: %.2f%%")):
    curve(mx, my, [(i / 20.0, 100 * c["gain"](i / 20.0, ib)) for i in range(0, 81)], col)
legend(12, 106, [(lab % (100 * c["gm_doubling"](ib)), col, False) for ib, col, lab in ((0.05, RD, "片側 50mA (AB級): 変動 %.2f%%"), (0.75, GR, "片側 0.75A (A級+AB級): %.2f%%"), (1.5, BL, "片側 1.5A: %.2f%%"))])
mx, my = plot(70, 72, 124, 108, 0, 100, 40, 100, False, "② 入力差動対のエミッタ抵抗と位相余裕 (°)  Phase margin vs degeneration", "エミッタ抵抗 (Ω)", "°")
curve(mx, my, [(r, c["loop"](r, 20e3)[2]) for r in range(0, 101, 2)], PU)
text(mx(22), my(c["loop"](22, 20e3)[2]) + 2.6, "22Ω: %.0f°" % c["loop"](22, 20e3)[2], 1.0, GR, "mm", True)
text(mx(2), my(c["loop"](0, 20e3)[2]) + 2.6, "0Ω: %.0f°" % c["loop"](0, 20e3)[2], 1.0, RD, "lm", True)
mx, my = plot(132, 72, 192, 108, 1, 1000, -20, 80, True, "③ クラスD の積分ループのゲイン (dB) と周波数 (kHz)  Class D loop gain", "周波数 (kHz)", "dB")
curve(mx, my, [(f / 1000.0, 20 * math.log10(c["class_d_t"](f, 22e3, 220e-12))) for f in range(1000, 1000001, 5000)], RD)
curve(mx, my, [(f / 1000.0, 20 * math.log10(c["class_d_t"](f, 22e3, 10e-12))) for f in range(1000, 1000001, 5000)], GR)
legend(138, 106, [("Cint 220p (20kHz で 4.3dB: 不足)", RD, False), ("Cint 10p C0G (20kHz で 31dB)", GR, False)])
line([(mx(1), my(0)), (mx(1000), my(0))], (150, 150, 150), int(LW * .6))
text(6, 62, "TEST 6〜10 の結果 (全文は下の 8 言語の説明)  Results of tests 6-10 (full text in 8 languages below)", 1.5, INK, "la", True)
rows = ["TEST 6: 出力段のゲイン変動 片側 50mA %.2f%% → 0.75A %.2f%%。" % (100 * c["gm_doubling"](0.05), 100 * c["gm_doubling"](0.75)),
        "TEST 7 [不具合]: 「1 素子 0.75A」は 2 並列だと片側 1.5A → A級 36W・発熱 135W/ch。→ 0.75A は『出力の片側の合計』に修正 (9W・67.5W/ch)。",
        "TEST 8: 入力対に 22Ω → 位相余裕 %.0f° → %.0f°。" % (c["loop"](0, 20e3)[2], c["loop"](22, 20e3)[2]),
        "TEST 9 [不具合]: CCS 3mA の V1 に R4 1k は不整合 (Vgk −3V、必要 約 −9.7V)。→ R4 3.3k。利得 10.2 → 14.0 倍。",
        "TEST 10 [不具合]: クラスD のゲイン 2.2 倍では定格に届かない → 前段 U0 ×7 で 15 倍。Cint 220p → 10p で 20kHz のループゲイン 4.3 → 31dB。"]
y = 59.5
for r_ in rows:
    text(6, y, r_, 1.05, INK, "la"); y -= 2.3
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = SDIR + r"\amp_ver7b_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, round(y, 1))
