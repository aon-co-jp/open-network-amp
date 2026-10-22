import math
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\plot_helpers.py", encoding="utf-8").read())
GR, BL, RD, PU, OR = (25, 115, 60), (30, 70, 180), (190, 30, 30), (120, 60, 160), (200, 120, 20)
text(3, 127, "VER6 TEST / DEBUG: 配線短縮・音量ノブの耐久  VER6: shorter wiring, volume-knob durability", 2.4, INK, "la", True)
text(3, 123.6, "世界各国語 (日・独・露・中・英) の検索で得た設計指針 + Python 計算。実機測定ではありません。 Design hints from multilingual searches + Python arithmetic, not bench measurements.", 1.3, GRY)
# 1) pick-up vs signal path length
mx, my = plot(8, 72, 62, 108, 20, 100, -60, 20, False, "① 信号経路の長さと誘導ノイズ (VER5 = 60mm を 0dB)  Pick-up vs path length", "経路長 (mm)", "dB")
ref = 60 * 10.0
f1 = lambda l, h: 20 * math.log10(l * h / ref)
curve(mx, my, [(l, f1(l, 10.0)) for l in range(20, 101, 2)], RD)
curve(mx, my, [(l, f1(l, 0.2)) for l in range(20, 101, 2)], GR)
legend(24, 106, [("戻り線が離れる(間隔10mm)", RD, False), ("直下にグランド面 (0.2mm)", GR, False)])
text(mx(45), my(f1(45, 0.2)) + 2.5, "45mm: %.0f dB" % f1(45, 0.2), 1.0, GR, "mm", True)
# 2) decoupling distance
mx, my = plot(70, 72, 124, 108, 0, 10, 0, 1.4, False, "② バイパスコンデンサの距離とインピーダンス (1nH/mm)  Decoupling distance", "ピンからの距離 (mm)", "Ω")
curve(mx, my, [(x / 10, 2 * math.pi * 10e6 * x / 10 * 1e-9) for x in range(0, 101)], BL)
curve(mx, my, [(x / 10, 2 * math.pi * 20e6 * x / 10 * 1e-9) for x in range(0, 101)], OR)
legend(76, 106, [("10 MHz", BL, False), ("20 MHz", OR, False)])
text(mx(2), my(2 * math.pi * 10e6 * 2e-9) + 2.3, "2mm: %.2f Ω" % (2 * math.pi * 10e6 * 2e-9), 1.0, GR, "mm", True)
# 3) knob wear life (years at 20 rev/day)
mx, my = plot(132, 72, 192, 108, 0, 4, 0, 20, False, "③ 音量ノブの寿命 (1日20回転・計算/仮定)  Knob life (years)", "", "年")
bars = [("可変抵抗\n50,000回転", 50000 / 20 / 365, RD), ("機械クリック\n30,000回", 30000 / 20 / 365, OR), ("VER6 触覚\n(軸受でL10)", 17.0, GR)]
for i, (lab, v, c) in enumerate(bars):
    xa = 0.3 + i * 1.2
    d.rectangle([*P(mx(xa), my(min(v, 20))), *P(mx(xa + 0.8), my(0))], fill=c)
    text(mx(xa + 0.4), my(min(v, 20)) + 1.6, "%.1f 年" % v, 1.0, INK, "mm", True)
    text(mx(xa + 0.4), my(0) - 1.8, lab.split("\n")[0], 0.85, GRY, "mm")
    text(mx(xa + 0.4), my(0) - 3.4, lab.split("\n")[1], 0.85, GRY, "mm")
rows = [
 ("TEST 7 (配線): 入力コンデンサ・抵抗をピンの直近に置き、信号を入力→出力へ一方向に並べ、電源・グランドの母線は最後に結ぶ (PS Audio・ADI の指針)。1チャンネルの経路は 60mm → 45mm、グランド面を直下に切れ目なく敷くとループ面積が約 1/50 になり、誘導ノイズは約 −36dB (計算)。",
  "TEST 7 (wiring): input parts sit right at the pins, the signal runs one way from input to output and the supply and ground buses are joined last. The path goes from 60 mm to 45 mm and an unbroken ground plane right beneath cuts the loop area to about 1/50, about 36 dB less pick-up (calculated).",
  "TEST 7 (Verdrahtung): Eingangsbauteile direkt an den Pins, Signal in einer Richtung vom Eingang zum Ausgang, Versorgungs- und Massebus zuletzt verbunden. Der Weg sinkt von 60 auf 45 mm; eine ununterbrochene Massefläche darunter verkleinert die Schleife auf etwa 1/50, etwa 36 dB weniger Einstreuung (berechnet).",
  "TEST 7 (разводка): входные детали у самых выводов, сигнал идёт в одну сторону от входа к выходу, шины питания и земли соединяются в конце. Путь сокращён с 60 до 45 мм; сплошной слой земли под ним уменьшает петлю примерно в 50 раз, наводка меньше примерно на 36 дБ (расчёт)."),
 ("TEST 8 (電源の近さ): バイパスコンデンサがピンから 2mm なら 10MHz で 0.13Ω、8mm だと 0.5Ω。→ 全チップの 100nF を 2mm 以内に置き、デジタル・アナログ・無線は別区画で 1 点だけ結ぶ (擬似スター)。",
  "TEST 8 (decoupling): a bypass capacitor 2 mm from the pin is 0.13 ohm at 10 MHz, but 0.5 ohm at 8 mm. Every 100 nF sits within 2 mm, and digital, analog and RF areas are separate and joined at one point (pseudo-star).",
  "TEST 8 (Entkopplung): Ein Kondensator 2 mm vom Pin hat bei 10 MHz 0,13 Ω, bei 8 mm 0,5 Ω. Jeder 100-nF-Kondensator sitzt innerhalb von 2 mm; Digital-, Analog- und HF-Bereich sind getrennt und an einem Punkt verbunden (Pseudo-Stern).",
  "TEST 8 (развязка): конденсатор в 2 мм от вывода даёт 0,13 Ом на 10 МГц, в 8 мм — 0,5 Ом. Все 100 нФ стоят в пределах 2 мм; цифровая, аналоговая и ВЧ-части разделены и соединены в одной точке (псевдозвезда)."),
 ("TEST 9 (音量ノブ VER6): 可変抵抗 (50,000 回転) は 1 日 20 回転で約 6.8 年、機械式クリックは約 4 年。非接触の磁気エンコーダを 2 個 (相互監視)、ボールベアリング 2 個で軸を支え (軸受の L10 寿命は横荷重 5N で桁違いに長く、実質はグリース劣化の約 17 年)、モーターは停止位置で通電を絞り (うなり・ノイズ防止、PWM 60kHz 以上)、クリックの強さはコギングを校正して均一にする。ラダーはラッチングリレー + 0.1% 薄膜抵抗。",
  "TEST 9 (volume knob VER6): a potentiometer (50,000 turns) lasts about 6.8 years at 20 turns a day and a mechanical click about 4 years. VER6 uses two non-contact magnetic encoders that watch each other, two ball bearings (the bearing L10 life is far longer at 5 N side load; grease ageing, about 17 years, is the real limit), lowers the motor current at rest (no whine; PWM at 60 kHz or higher) and calibrates the cogging so every click feels equal. The ladder is latching relays with 0.1% thin-film resistors.",
  "TEST 9 (Lautstärkeknopf VER6): Ein Potentiometer (50.000 Umdrehungen) hält bei 20 Umdrehungen am Tag etwa 6,8 Jahre, ein mechanisches Rasten etwa 4 Jahre. VER6 nutzt zwei berührungslose Magnetencoder, die sich gegenseitig überwachen, zwei Kugellager (die Lager-L10-Lebensdauer ist bei 5 N Seitenlast weit länger; Fettalterung, etwa 17 Jahre, ist die eigentliche Grenze), senkt den Motorstrom im Stillstand (kein Pfeifen; PWM ab 60 kHz) und kalibriert das Cogging, damit jede Raste gleich wirkt.",
  "TEST 9 (ручка громкости VER6): потенциометр (50 000 оборотов) служит около 6,8 года при 20 оборотах в день, механический фиксатор около 4 лет. В VER6 два бесконтактных магнитных энкодера, следящих друг за другом, два шарикоподшипника (ресурс L10 подшипника при боковой нагрузке 5 Н намного больше; реальный предел — старение смазки, около 17 лет), сниженный ток двигателя в покое (без свиста; ШИМ от 60 кГц) и калибровка зубцового момента, чтобы каждый щелчок ощущался одинаково."),
 ("未実施: 実機の測定 (雑音・位相・THD・触覚の感触)・過渡応答・基板の電磁界解析。数値は設計用の計算と仮定です。",
  "Not done: bench measurements (noise, phase, THD, feel), transient response and board field solving. The numbers are design calculations and assumptions.",
  "Nicht durchgeführt: Messungen am Gerät (Rauschen, Phase, THD, Haptik), Einschwingverhalten und Feldberechnung der Platine. Die Werte sind Entwurfsrechnungen und Annahmen.",
  "Не выполнено: измерения на устройстве (шум, фаза, КНИ, ощущение), переходные процессы и расчёт поля платы. Значения — проектные расчёты и допущения."),
]
y = 64
text(6, 66.5, "TEST / DEBUG の記録 (VER6)  Log", 1.6, INK, "la", True)
import textwrap
for blk in rows:
    for i, t in enumerate(blk):
        for ln in textwrap.wrap(t, 150 if i in (1, 2, 3) else 78):
            text(6, y, ln, 0.85, INK if i == 0 else GRY, "la")
            y -= 1.5
    y -= 0.8
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_ver6_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size, round(f1(45, 0.2), 1), round(y, 1))
