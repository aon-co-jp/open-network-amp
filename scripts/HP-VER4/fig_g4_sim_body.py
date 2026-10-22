import math
SDIR = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
exec(open(SDIR + r"\plot_helpers.py", encoding="utf-8").read())
c = {}
exec(open(SDIR + r"\g4_calc.py", encoding="utf-8").read().replace('if __name__ == "__main__":', 'if False:'), c)
GR, BL, RD, PU, OR = (25, 115, 60), (30, 70, 180), (190, 30, 30), (120, 60, 160), (200, 120, 20)
text(3, 127, "低音・高音ゲイン TEST / DEBUG: シェルビング特性・係数の語長・リレー寿命  Low / high gain: shelf response, coefficient word length, relay life", 2.1, INK, "la", True)
text(3, 123.6, "Python による設計計算 (SPICE・実機測定ではありません)。仮定: サンプリング 384kHz、低音 100Hz・高音 8kHz のシェルビング、±10dB を 1dB 刻み。 Python calculations, not bench measurements.", 1.2, GRY)
mx, my = plot(8, 72, 62, 108, 20, 40000, -12, 12, True, "① 低音・高音ゲインの周波数特性 (dB)  Shelf responses", "周波数 (Hz)", "dB")
for g, col in ((10, RD), (5, OR), (-5, BL), (-10, PU)):
    curve(mx, my, [(f, c["mag_db"](c["shelf"]("low", 100.0, g), f) + c["mag_db"](c["shelf"]("high", 8000.0, g), f)) for f in [20 * 10 ** (i / 30.0) for i in range(0, 100)]], col)
legend(12, 106, [("低音・高音とも +10dB", RD, False), ("+5dB", OR, False), ("−5dB", BL, False), ("−10dB", PU, False)])
mx, my = plot(70, 72, 124, 108, 0, 5, 0, 1.0, False, "② 係数の語長と 20Hz のずれ (dB、+12dB 低音シェルビング・384kHz)  Coefficient word length", "", "dB")
for i, b in enumerate((20, 24, 28, 32, 48)):
    e = abs(c["coef_error"](b))
    d.rectangle([*P(mx(0.2 + i), my(min(e, 1.0))), *P(mx(0.9 + i), my(0))], fill=RD if e > 0.05 else GR)
    text(mx(0.55 + i), my(min(e, 1.0)) + 1.6, "%.3f" % e, 0.95, INK, "mm", True)
    text(mx(0.55 + i), my(0) - 1.8, "%dbit" % b, 0.95, GRY, "mm")
mx, my = plot(132, 72, 192, 108, 100, 5000, 1, 1000, True, "③ リレー寿命 (年) と 1 日のステップ数 (ゲイン)  Relay life", "1 日のステップ数", "年")
for fn, col in ((c["analog_state"], RD), (c["mixed_state"], BL)):
    t, _ = c["toggles"](fn)
    curve(mx, my, [(n, min(1000, c["relay_years"](t, n))) for n in (100, 200, 500, 1000, 2000, 5000)], col)
legend(138, 106, [("ANALOG", RD, False), ("ANALOG+DIGITAL", BL, False)])
text(6, 62, "結果 (全文は下の 8 言語の説明)  Results (full text in 8 languages below)", 1.5, INK, "la", True)
import textwrap
rows = ["TEST 1: 低音 (100Hz 以下) と高音 (8kHz 以上) のシェルビングを 1dB 刻み (±10dB) で動かすと、中域はほぼ動かない。2 つの合成も 1dB 刻みで足し算できる。",
        "TEST 2 [不具合]: デジタルの低音シェルビングを 384kHz で 24bit 係数にすると、20Hz で %.2fdB ずれて 1dB 刻みが壊れる → 修正: 32bit 以上 (倍精度) の係数 (ずれ %.3fdB)。" % (abs(c["coef_error"](24)), abs(c["coef_error"](32))),
        "TEST 3: 1 日 1000 ステップのゲイン操作でのリレー寿命は、ANALOG が約 %.0f 年、ANALOG+DIGITAL が約 %.0f 年 (境目で動くリレーは最大 %d 個)。" % (c["relay_years"](c["toggles"](c["analog_state"])[0], 1000), c["relay_years"](c["toggles"](c["mixed_state"])[0], 1000), c["toggles"](c["analog_state"])[1]),
        "TEST 4: 音量は HP-VER3 と同じ (DIGITAL だけで深く絞るとビット深度が減るため、音量は ANALOG か ANALOG+DIGITAL を推奨)。"]
y = 59.5
for r_ in rows:
    for ln in textwrap.wrap(r_, 90):
        text(6, y, ln, 1.05, INK, "la"); y -= 2.0
    y -= 0.4
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = SDIR + r"\amp_gain4_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300)); print(out, round(y, 1))
