import math
SDIR = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
exec(open(SDIR + r"\plot_helpers.py", encoding="utf-8").read())
g = {}
exec(open(SDIR + r"\v7_calc.py", encoding="utf-8").read().replace('if __name__ == "__main__":', 'if False:'), g)
GR, BL, RD, PU, OR = (25, 115, 60), (30, 70, 180), (190, 30, 30), (120, 60, 160), (200, 120, 20)
text(3, 127, "VER7 TEST / DEBUG: 12 畳以上・小音量から少し大きな音量まで  A級 / A級+AB級 / クラスD  Required power, heat and electricity", 2.2, INK, "la", True)
text(3, 123.6, "Python による設計計算 (SPICE・実機測定ではありません)。想定: 87dB/W/m ×2 (+3dB)、聴取距離 3m、平均はピークより 約 15dB 低い、8Ω。 Python design calculations, not bench measurements.", 1.2, GRY)
# 1) required power vs peak SPL
mx, my = plot(8, 72, 62, 108, 70, 105, 0.1, 150, False, "① 必要な出力 (W) とピーク音圧  Power needed vs peak SPL", "ピーク音圧 (dB、3m)", "W")
for sens, col in ((84, RD), (87, GR), (90, BL)):
    curve(mx, my, [(s, min(150, 10 ** ((s - sens - 3 + 20 * math.log10(3.0)) / 10.0))) for s in range(70, 106)], col)
legend(12, 106, [("スピーカー 84dB", RD, False), ("87dB (想定)", GR, False), ("90dB", BL, False)])
line([(mx(70), my(g["P_A"])), (mx(105), my(g["P_A"]))], OR, int(LW * .6))
text(mx(104), my(g["P_A"]) + 2.0, "A級 %.0fW" % g["P_A"], 1.0, OR, "rm", True)
text(mx(88), my(100) - 2.0, "AB級 100W", 1.0, RD, "mm", True)
line([(mx(70), my(100)), (mx(105), my(100))], RD, int(LW * .6))
# 2) heat per channel vs output power
mx, my = plot(70, 72, 124, 108, 0, 100, 0, 80, False, "② 1ch の発熱 (W) と出力  Heat per channel vs output", "出力 (W、8Ω)", "W")
curve(mx, my, [(p / 2.0, g["heat_A"]) for p in range(1, 19)], RD)
curve(mx, my, [(p, g["pd_H"](p)) for p in range(1, 101)], OR)
curve(mx, my, [(p, g["pd_AB"](p)) for p in range(1, 101)], PU)
curve(mx, my, [(p, g["pd_D"](p)) for p in range(1, 101)], GR)
legend(76, 106, [("A級 (最大 9W)", RD, False), ("A級+AB級 (9W から自動で AB)", OR, False), ("AB級 (低バイアス)", PU, False), ("クラス D", GR, False)])
# 3) annual electricity
mx, my = plot(132, 72, 192, 108, 0, 5, 0, 250, False, "③ 年間の電力量 (kWh、1日 4 時間・平均 約 85dB)  Electricity per year", "方式", "kWh")
pk = g["need"](100)
bars = [("A級", g["kwh"](2 * g["heat_A"]), RD), ("A+AB", g["kwh"](2 * g["pd_H"](g["avg_w"](pk))), OR), ("AB", g["kwh"](2 * g["pd_AB"](g["avg_w"](pk))), PU), ("D", g["kwh"](2 * g["pd_D"](g["avg_w"](pk))), GR)]
for i, (lab, v, c) in enumerate(bars):
    xa = 0.2 + i * 1.2
    d.rectangle([*P(mx(xa), my(min(v, 250))), *P(mx(xa + 0.9), my(0))], fill=c)
    text(mx(xa + 0.45), my(min(v, 250)) + 1.8, "%.0f" % v, 1.0, INK, "mm", True)
    text(mx(xa + 0.45), my(0) - 1.8, lab, 0.95, GRY, "mm")
rows = [
    "ROUND 1 (必要な出力): ピーク 90dB は 9W、95dB は 28W、100dB (平均 約 85dB の少し大きな音量) は 90W。A級は 9W までなので、少し大きな音量には足りない → A級 + AB級が必要。",
    "ROUND 2 (A級の発熱): 1ch 1.5A バイアスで 72W (ステレオ 144W)。12 畳の部屋では小さな暖房器具程度で、ヒートシンク ≤0.3°C/W/ch + 温度制御ファン + 換気があれば許容。BIAS ECO (0.75A) で半分に。",
    "ROUND 3 (A級 + AB級): 1 素子 0.75A の高バイアスで 9W まで A級、超えると自動で AB級、最大 100W。アイドル発熱は 67.5W/ch。出力素子 2 並列でも接合部は余裕。",
    "ROUND 4 (クラスD): アイドル 1.5W/ch、平均 約 85dB でもステレオ 約 3.6W、年 約 5kWh (A級は 約 210kWh)。ゾベルで 16Ω のピークを 7.6dB → 0.7dB。",
    "ROUND 5 (全版共通): 配線は入力→出力へ一方向 約 40mm、グランド面、2mm 以内のバイパス、0.1% 薄膜、フィルム/C0G、外付けリニア DC 電源 (R コア、6mm² 0.8m)、電解は 63V・別筐体で約 52 年。未実施: 実機測定・聴感評価。",
    "Round 1-5 (EN): 9 W gives a 90 dB peak, 28 W gives 95 dB and 90 W gives 100 dB, so Class A (9 W) covers quiet to practical levels and the Class A + AB version covers the louder levels. Class A idles at 72 W per channel; Class D at 1.5 W. Full text in 8 languages is in the README and the manual image.",
]
y = 62
text(6, 64.5, "TEST / DEBUG の記録 (5 回)  Log  (全文は 8 言語の README と説明書の画像へ)", 1.5, INK, "la", True)
import textwrap
for r_ in rows:
    for ln in textwrap.wrap(r_, 70 if not r_.startswith("Round") else 150):
        text(6, y, ln, 1.0, INK if not r_.startswith("Round") else GRY, "la")
        y -= 1.7
    y -= 0.8
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = SDIR + r"\amp_ver7_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, round(y, 1), [round(b[1]) for b in bars])
