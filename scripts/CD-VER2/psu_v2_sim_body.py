import math, textwrap
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\plot_helpers.py", encoding="utf-8").read())
GR, BL, RD, PU, OR = (25, 115, 60), (30, 70, 180), (190, 30, 30), (120, 60, 160), (200, 120, 20)
RHO = 0.0172                                   # ohm mm2 / m, copper
cable_drop = lambda l, a, i: RHO * 2 * l / a * i
I_SUS, I_PK = 4.5, 13.6                        # sustained 1/3 power and full-power peak per rail pair (A)
spike = lambda mm, didt=50.0: 1.0 * mm * 1e-9 * didt * 1e6   # 1 nH/mm loop, di/dt in A/us -> V
life = lambda tamb, dt: 10000 * 2 ** ((105 - (tamb + dt)) / 10.0) / 8760
text(3, 127, "PSU-VER2 外付けリニア DC 電源 TEST / DEBUG (5 回)  External linear DC supply: durability, sound, wiring", 2.3, INK, "la", True)
text(3, 123.6, "Python による設計計算 (SPICE・実機測定ではありません)。仮定: 銅 0.0172Ω·mm²/m、ループ 1nH/mm、整流の di/dt 50A/µs、電解 105°C 10,000h 品。", 1.3, GRY)
mx, my = plot(8, 72, 62, 108, 0.3, 2.0, 0, 0.35, False, "① DC ケーブルの電圧降下 (V、ピーク 13.6A)  Cable drop", "ケーブル長 (m)", "V")
curve(mx, my, [(l / 100.0, cable_drop(l / 100.0, 2.5, I_PK)) for l in range(30, 201, 5)], RD)
curve(mx, my, [(l / 100.0, cable_drop(l / 100.0, 6.0, I_PK)) for l in range(30, 201, 5)], GR)
legend(12, 106, [("2.5mm²: 1.5m で %.0f mV" % (1000 * cable_drop(1.5, 2.5, I_PK)), RD, False), ("6mm²: 0.8m で %.0f mV" % (1000 * cable_drop(0.8, 6.0, I_PK)), GR, False)])
mx, my = plot(70, 72, 124, 108, 5, 100, 0, 6, False, "② 整流 → コンデンサのループ長とスパイク (V)  Loop length vs spike", "配線長 (mm)", "V")
curve(mx, my, [(l, spike(l)) for l in range(5, 101, 2)], PU)
text(mx(20), my(spike(20)) + 2.4, "20mm: %.1f V" % spike(20), 1.0, GR, "mm", True)
text(mx(80), my(spike(80)) - 2.4, "80mm: %.1f V" % spike(80), 1.0, RD, "mm", True)
mx, my = plot(132, 72, 192, 108, 25, 85, 0, 100, False, "③ 電解コンデンサの寿命 (年)  Capacitor life", "周囲温度 (°C)", "年")
curve(mx, my, [(t, min(100, life(t, 20))) for t in range(25, 86)], RD)
curve(mx, my, [(t, min(100, life(t, 5))) for t in range(25, 86)], GR)
legend(138, 106, [("リップル発熱 +20K", RD, False), ("低 ESR・リップル電流に余裕 +5K", GR, False)])
text(mx(45), my(life(45, 5)) + 2.4, "45°C: %.0f 年" % min(100, life(45, 5)), 1.0, GR, "mm", True)
d_old, d_new = cable_drop(1.5, 2.5, I_PK), cable_drop(0.8, 6.0, I_PK)
chain = [("ブリッジ整流後 (88mF、映画の平均)", 100e3), ("+ CRC (または容量倍増) 約 40dB (仮定)", 1e3), ("+ LT3045 / LT3094 PSRR 約 80dB (仮定)", 0.1)]
rows = [
    ("ROUND 1 (配線): VER1 は 2.5mm² で 1.5m のケーブルを想定。ピーク 13.6A で %.0f mV (パワー段のレールが 動的に 垂れる)。→ 問題あり。対策: 6mm² で 0.8m に短縮し %.0f mV (%.0f 分の 1)、アナログ側は センス線で補償。" % (1000 * d_old, 1000 * d_new, d_old / d_new),
     "ROUND 1 (wiring): VER1 assumed a 1.5 m cable of 2.5 mm2, which drops %.0f mV at the 13.6 A peak (the power rails sag dynamically). Problem. Fix: 6 mm2 at 0.8 m gives %.0f mV (1/%.0f); the analog side is compensated with sense wires." % (1000 * d_old, 1000 * d_new, d_old / d_new),
     "RUNDE 1 (Verdrahtung): VER1 nahm 1,5 m Kabel mit 2,5 mm² an, das bei 13,6 A Spitze %.0f mV abfallen lässt (die Endstufenschienen sacken dynamisch ein). Problem. Abhilfe: 6 mm² bei 0,8 m ergeben %.0f mV (1/%.0f); die Analogseite wird mit Fühlerleitungen kompensiert." % (1000 * d_old, 1000 * d_new, d_old / d_new),
     "РАУНД 1 (разводка): в VER1 предполагался кабель 1,5 м сечением 2,5 мм², падение %.0f мВ при пике 13,6 А (силовые шины динамически просаживаются). Проблема. Решение: 6 мм² при 0,8 м дают %.0f мВ (1/%.0f); аналоговая часть компенсируется измерительными проводами." % (1000 * d_old, 1000 * d_new, d_old / d_new)),
    ("ROUND 2 (整流ループ): 整流ダイオードとコンデンサの配線が 80mm だとスパイク %.1fV、20mm なら %.1fV (di/dt 50A/µs、1nH/mm)。→ 対策: ブリッジをコンデンサ端子に直付けし (ループ 20mm 以下)、ソフトリカバリ ダイオード + RC スナバ、太い銅バスバー、グランドはコンデンサ中点の 1 点スター。" % (spike(80), spike(20)),
     "ROUND 2 (rectifier loop): an 80 mm wire between the rectifier and the capacitor gives a %.1f V spike, 20 mm gives %.1f V (di/dt 50 A/us, 1 nH/mm). Fix: mount the bridge directly on the capacitor terminals (loop 20 mm or less), soft-recovery diodes with an RC snubber, thick copper bus bars and a single-point star ground at the capacitor midpoint." % (spike(80), spike(20)),
     "RUNDE 2 (Gleichrichterschleife): Eine 80 mm lange Leitung zwischen Gleichrichter und Kondensator ergibt %.1f V Spitze, 20 mm ergeben %.1f V (di/dt 50 A/µs, 1 nH/mm). Abhilfe: Brücke direkt an den Kondensatorklemmen (Schleife höchstens 20 mm), Soft-Recovery-Dioden mit RC-Snubber, dicke Kupfer-Sammelschienen, Sternpunkt-Masse am Kondensator-Mittelpunkt." % (spike(80), spike(20)),
     "РАУНД 2 (петля выпрямителя): провод 80 мм между выпрямителем и конденсатором даёт выброс %.1f В, 20 мм — %.1f В (di/dt 50 А/мкс, 1 нГн/мм). Решение: мост прямо на выводах конденсатора (петля не более 20 мм), диоды с мягким восстановлением и RC-демпфер, толстые медные шины, звезда земли в средней точке конденсаторов." % (spike(80), spike(20))),
    ("ROUND 3 (耐久: 電解コンデンサ): リップル電流で +20K 自己発熱すると 45°C で %.0f 年、低 ESR・リップル電流に余裕 (+5K) なら %.0f 年 (100 年で頭打ち表示)。→ 対策: 定格電圧は レール電圧の 1.4 倍 (63V、45V レール)、リップル電流は定格の 50%% 以下、フィルムコンデンサを並列、別筐体で 45°C 以下。" % (life(45, 20), min(100, life(45, 5))),
     "ROUND 3 (durability, electrolytic capacitors): with +20 K self-heating from ripple current the life is %.0f years at 45 C, and %.0f years with low ESR and ripple-current margin (+5 K; the chart caps at 100). Fix: voltage rating 1.4 times the rail (63 V on 45 V rails), ripple current at 50%% of the rating or less, film capacitors in parallel, and a separate case at 45 C or below." % (life(45, 20), min(100, life(45, 5))),
     "RUNDE 3 (Haltbarkeit, Elektrolytkondensatoren): Bei +20 K Eigenerwärmung durch Rippelstrom beträgt die Lebensdauer bei 45 °C %.0f Jahre, mit niedrigem ESR und Rippelstromreserve (+5 K) %.0f Jahre (Diagramm bei 100 gekappt). Abhilfe: Spannungsfestigkeit das 1,4-fache der Schiene (63 V bei 45-V-Schienen), Rippelstrom höchstens 50 %% der Nennwerte, Folienkondensatoren parallel, getrenntes Gehäuse bei höchstens 45 °C." % (life(45, 20), min(100, life(45, 5))),
     "РАУНД 3 (долговечность, электролиты): при самонагреве +20 К от пульсирующего тока срок службы при 45 °C — %.0f лет, при низком ESR и запасе по току (+5 К) — %.0f лет (график ограничен 100). Решение: номинальное напряжение в 1,4 раза выше шины (63 В при шинах 45 В), пульсирующий ток не более 50 %% от номинала, плёночные конденсаторы параллельно, отдельный корпус при 45 °C или ниже." % (life(45, 20), min(100, life(45, 5)))),
    ("ROUND 4 (音質: リップルの連鎖): 整流後のリップル 0.10V (SV-VER4 の計算) → 容量倍増で 約 %.0fmV → LT3045 / LT3094 で 約 %.1fµV (アナログ ±15V、100Hz、段ごとの減衰は仮定)。クロックと DAC は専用のレギュレータを 別に持ち、ほかの負荷と共用しない。" % (chain[1][1] / 1e3 * 1, chain[2][1] / 1.0),
     "ROUND 4 (sound, the ripple chain): the 0.10 V ripple after rectification (SV-VER4 calculation) drops to about %.0f mV with a capacitance multiplier and to about %.1f uV with LT3045 / LT3094 regulators (analog +-15 V, 100 Hz; the attenuation per stage is assumed). The clock and the DAC each have their own regulator and share it with nothing else." % (chain[1][1] / 1e3, chain[2][1]),
     "RUNDE 4 (Klang, Rippelkette): Die 0,10 V Rippel nach der Gleichrichtung (Rechnung aus SV-VER4) sinken mit Kapazitätsvervielfacher auf etwa %.0f mV und mit LT3045 / LT3094 auf etwa %.1f µV (analog ±15 V, 100 Hz; Dämpfung je Stufe angenommen). Takt und DAC haben je einen eigenen Regler und teilen ihn mit nichts anderem." % (chain[1][1] / 1e3, chain[2][1]),
     "РАУНД 4 (звук, цепочка пульсаций): пульсации 0,10 В после выпрямления (расчёт SV-VER4) падают до около %.0f мВ с умножителем ёмкости и до около %.1f мкВ с LT3045 / LT3094 (аналоговые ±15 В, 100 Гц; ослабление каскадов принято). У такта и ЦАП отдельные стабилизаторы, не общие ни с чем другим." % (chain[1][1] / 1e3, chain[2][1])),
    ("ROUND 5 (投入と保護): 1.0kVA の R コアと 88mF の投入では、NTC 10Ω + リレーで突入電流を約 14A に抑え (制限なしは数百 A)、1 秒後にリレーで短絡。DC ブロッカで 偏磁を防ぎ、MOV・ヒューズ・過電圧・過電流・温度・DC 出力の保護を持つ。未実施: 実機測定・過渡・EMI・安全規格試験。",
     "ROUND 5 (switch-on and protection): with a 1.0 kVA R-core and 88 mF, an NTC of 10 ohm plus a relay holds the inrush to about 14 A (hundreds of amps without limiting) and the relay shorts it after one second. A DC blocker prevents core saturation, and there are MOV, fuse, over-voltage, over-current, temperature and DC-output protection. Not done: bench measurements, transients, EMI, safety-standard testing.",
     "RUNDE 5 (Einschalten und Schutz): Bei einem 1,0-kVA-R-Kern und 88 mF hält ein NTC von 10 Ω plus Relais den Einschaltstrom bei etwa 14 A (ohne Begrenzung Hunderte A); das Relais überbrückt nach einer Sekunde. Ein Gleichstromblocker verhindert Kernsättigung; vorhanden sind MOV, Sicherung, Überspannungs-, Überstrom-, Temperatur- und Gleichspannungs-Ausgangsschutz. Nicht durchgeführt: Messungen, Transienten, EMV, Sicherheitsprüfung.",
     "РАУНД 5 (включение и защита): при R-сердечнике 1,0 кВА и 88 мФ NTC 10 Ом с реле ограничивает пусковой ток около 14 А (без ограничения сотни ампер), реле шунтирует его через секунду. Блокиратор постоянного тока предотвращает насыщение сердечника; есть MOV, предохранитель, защита от перенапряжения, перегрузки, перегрева и постоянной составляющей на выходе. Не выполнено: измерения, переходные процессы, ЭМС, испытания по стандартам безопасности."),
]
y = 64
text(6, 66.5, "TEST / DEBUG の記録 (5 回)  Log", 1.6, INK, "la", True)
for blk in rows:
    for i, t in enumerate(blk):
        for ln in textwrap.wrap(t, 190 if i else 100):
            text(6, y, ln, 0.8, INK if i == 0 else GRY, "la")
            y -= 1.22
    y -= 0.5
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\psu_v2_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, round(1000 * d_old), round(1000 * d_new), round(spike(80), 1), round(spike(20), 1), round(life(45, 20)), round(life(45, 5)), round(y, 1))
