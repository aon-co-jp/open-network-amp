import math, textwrap
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\plot_helpers.py", encoding="utf-8").read())
GR, BL, RD, PU, OR = (25, 115, 60), (30, 70, 180), (190, 30, 30), (120, 60, 160), (200, 120, 20)
V = 45.0


def pd_ab(rl, frac=None):
    if frac is None:
        return 2 * V * V / (math.pi ** 2 * rl)
    po = frac * V * V / (2 * rl)
    vo = math.sqrt(2 * po * rl)
    return 2 * V * vo / (math.pi * rl) - vo * vo / (2 * rl)


def pd_d(rl, frac=None):
    po = (V * V / (2 * rl)) * (1 if frac is None else frac)
    return po * (1 / 0.9 - 1)


def mixed(rl, frac=None):
    return 3 * pd_ab(rl, frac) + 8 * pd_d(rl, frac)


allab4, allab8, mix4 = 11 * pd_ab(4), 11 * pd_ab(8), mixed(4)
film_ab, film_mix = 11 * pd_ab(8, 1 / 8), mixed(8, 1 / 8)
x0 = 20 * math.log10(40 / 180.0) + 20 * math.log10(10 / 25.0)
snr = lambda tj: -20 * math.log10(2 * math.pi * 20e3 * tj * 1e-12)
rip = 3.0 / (2 * 100 * 0.044)

text(3, 127, "SV-VER1 TEST / DEBUG (5 回): 発熱・配線・クロストーク・ジッタ  Surround AV: heat, wiring, crosstalk, jitter", 2.3, INK, "la", True)
text(3, 123.6, "Python による設計計算 (SPICE・実機測定ではありません)。仮定: レール ±45V、各ch 100W/8Ω、D 級効率 90%、映画の平均 = 最大出力の 1/8。", 1.3, GRY)
mx, my = plot(8, 72, 62, 108, 3, 9, 0, 1200, False, "① 11ch の最悪発熱 (W)  Worst-case heat", "負荷 (Ω)", "W")
curve(mx, my, [(r / 2, 11 * pd_ab(r / 2)) for r in range(8, 19)], RD)
curve(mx, my, [(r / 2, mixed(r / 2)) for r in range(8, 19)], GR)
legend(12, 106, [("全 11ch Class AB: 4Ωで %.0fW" % allab4, RD, False), ("混成 (L/C/R=AB, 他=D): %.0fW" % mix4, GR, False)])
mx, my = plot(70, 72, 124, 108, 20, 200, -60, 0, False, "② 信号経路とクロストーク (180mm を 0dB)  Path / crosstalk", "経路 (mm)", "dB")
curve(mx, my, [(l, 20 * math.log10(l / 180.0)) for l in range(20, 201, 4)], BL)
curve(mx, my, [(l, 20 * math.log10(l / 180.0) + 20 * math.log10(10.0 / 25.0)) for l in range(20, 201, 4)], GR)
legend(76, 106, [("隣との間隔 10mm", BL, False), ("間隔 25mm (本設計)", GR, False)])
text(mx(60), my(x0) - 3.0, "40mm・25mm: %.0f dB" % x0, 1.0, GR, "mm", True)
mx, my = plot(132, 72, 192, 108, 0.1, 2.0, 100, 160, False, "③ クロックジッタ限界の SNR (20kHz)  Jitter-limited SNR", "ジッタ (ps rms)", "dB")
curve(mx, my, [(t / 100, snr(t / 100)) for t in range(10, 201, 2)], PU)
text(mx(0.45), my(snr(0.3)) + 2.4, "0.3ps: %.0f dB" % snr(0.3), 1.0, GR, "mm", True)
text(mx(1.2), my(snr(1.0)) + 2.4, "1ps: %.0f dB" % snr(1.0), 1.0, RD, "mm", True)

rows = [
    ("ROUND 1 (発熱): 全 11ch を Class AB にすると、4Ω の最悪時に %.0fW、8Ω でも %.0fW の発熱。→ 問題あり: 筐体で処理できない (目安 300〜400W)。" % (allab4, allab8),
     "ROUND 1 (heat): all 11 channels in Class AB dissipate %.0f W worst case at 4 ohm and %.0f W at 8 ohm. Problem: the chassis cannot remove that (a rule of thumb is 300-400 W)." % (allab4, allab8),
     "RUNDE 1 (Wärme): Alle 11 Kanäle in Klasse AB geben im ungünstigsten Fall %.0f W an 4 Ω und %.0f W an 8 Ω ab. Problem: Das Gehäuse kann das nicht abführen (Richtwert 300-400 W)." % (allab4, allab8),
     "РАУНД 1 (нагрев): все 11 каналов в классе AB рассеивают в худшем случае %.0f Вт на 4 Ом и %.0f Вт на 8 Ом. Проблема: корпус не отведёт столько (ориентир 300-400 Вт)." % (allab4, allab8)),
    ("ROUND 2 (対策): フロント L/C/R の 3ch だけ Class AB (2 並列)、他 8ch はクラス D。最悪 %.0fW (4Ω)、映画の平均 (1/8 出力) は %.0fW (全 AB は %.0fW)。→ 温度制御ファンで処理可能。" % (mix4, film_mix, film_ab),
     "ROUND 2 (fix): only the front L/C/R are Class AB (two pairs in parallel); the other 8 channels are Class D. Worst case %.0f W at 4 ohm; the film average (1/8 power) is %.0f W (all-AB: %.0f W). A temperature-controlled fan can handle it." % (mix4, film_mix, film_ab),
     "RUNDE 2 (Abhilfe): Nur Front L/C/R in Klasse AB (zwei Paare parallel), die anderen 8 Kanäle in Klasse D. Ungünstigster Fall %.0f W an 4 Ω; Filmdurchschnitt (1/8 Leistung) %.0f W (alle AB: %.0f W). Ein temperaturgeregelter Lüfter genügt." % (mix4, film_mix, film_ab),
     "РАУНД 2 (решение): только фронтальные L/C/R в классе AB (две пары параллельно), остальные 8 каналов — класс D. Худший случай %.0f Вт на 4 Ом; среднее для фильма (1/8 мощности) %.0f Вт (все AB: %.0f Вт). Достаточно вентилятора с термоуправлением." % (mix4, film_mix, film_ab)),
    ("ROUND 3 (配線): DAC・ボリューム・パワーを 1 か所にまとめると経路 180mm。チャンネルごとの縦一列にして 40mm にし、隣との間隔 25mm を確保すると、誘導・クロストークは約 %.0f dB 減る (計算。経路長と間隔に比例するとの仮定)。" % abs(x0),
     "ROUND 3 (wiring): putting DAC, volume and power stage in one place gives a 180 mm path. One vertical line per channel shortens it to 40 mm and keeping 25 mm to the neighbour cuts pick-up and crosstalk by about %.0f dB (calculated, assuming it scales with length and spacing)." % abs(x0),
     "RUNDE 3 (Verdrahtung): DAC, Lautstärke und Endstufe an einer Stelle ergeben 180 mm Weg. Eine senkrechte Linie je Kanal verkürzt auf 40 mm; mit 25 mm Abstand zum Nachbarn sinken Einstreuung und Übersprechen um etwa %.0f dB (berechnet, Skalierung mit Länge und Abstand angenommen)." % abs(x0),
     "РАУНД 3 (разводка): если ЦАП, регулятор громкости и усилитель мощности собраны в одном месте, путь 180 мм. Одна вертикальная линия на канал сокращает его до 40 мм, а зазор 25 мм до соседа уменьшает наводку и перекрёстные помехи примерно на %.0f дБ (расчёт, масштабирование по длине и зазору принято)." % abs(x0)),
    ("ROUND 4 (音質): ジッタ 1ps だと 20kHz で SNR %.0fdB、0.3ps (低ジッタ クロックを各 DAC 組の隣に置く) なら %.0fdB。12ch 分のクロックは 1 つの発振器から等長で分配。レールのリップルは 4 万 4 千 µF・3A で %.2fV → 定電圧回路で 60dB 低減 (仮定)。" % (snr(1.0), snr(0.3), rip),
     "ROUND 4 (sound): 1 ps of jitter limits the SNR at 20 kHz to %.0f dB; 0.3 ps (low-jitter clock placed next to each DAC pair) gives %.0f dB. The 12-channel clock comes from one oscillator over equal-length lines. Rail ripple with 44,000 uF at 3 A is %.2f V, reduced by 60 dB with a regulator (assumed)." % (snr(1.0), snr(0.3), rip),
     "RUNDE 4 (Klang): 1 ps Jitter begrenzen den SNR bei 20 kHz auf %.0f dB, 0,3 ps (rauscharmer Takt neben jedem DAC-Paar) ergeben %.0f dB. Der 12-Kanal-Takt kommt von einem Oszillator über gleich lange Leitungen. Die Restwelligkeit mit 44.000 µF bei 3 A beträgt %.2f V, mit Regler 60 dB weniger (angenommen)." % (snr(1.0), snr(0.3), rip),
     "РАУНД 4 (звук): джиттер 1 пс ограничивает SNR на 20 кГц до %.0f дБ, 0,3 пс (малошумящий такт рядом с каждой парой ЦАП) даёт %.0f дБ. Такт 12 каналов идёт от одного генератора линиями равной длины. Пульсации шины при 44 000 мкФ и 3 А — %.2f В, регулятор снижает их на 60 дБ (допущение)." % (snr(1.0), snr(0.3), rip)),
    ("ROUND 5 (耐久・まとめ): 電解コンデンサは別筐体 45°C 以下 (約 73 年)、リレーはラッチング、音量ノブは VER6 (約 17 年)、出力素子は温度保護、触覚 2ch は DC 検出つき。合格: 発熱・配線・ジッタ。未実施: 実機の測定、HDMI の認証試験、IMAX Enhanced / Dolby / DTS の認証、過渡応答、THD。",
     "ROUND 5 (durability, summary): electrolytic capacitors in a separate case at 45 C or below (about 73 years), latching relays, the VER6 volume knob (about 17 years), temperature-protected output devices, DC detection on the 2 tactile channels. Passed: heat, wiring, jitter. Not done: bench measurements, HDMI compliance, IMAX Enhanced / Dolby / DTS certification, transient response, THD.",
     "RUNDE 5 (Haltbarkeit, Fazit): Elektrolytkondensatoren in einem getrennten Gehäuse bei höchstens 45 °C (etwa 73 Jahre), Latching-Relais, Lautstärkeknopf von VER6 (etwa 17 Jahre), temperaturgeschützte Endtransistoren, DC-Erkennung an den 2 Haptikkanälen. Bestanden: Wärme, Verdrahtung, Jitter. Nicht durchgeführt: Messungen, HDMI-Konformität, IMAX-Enhanced-/Dolby-/DTS-Zertifizierung, Einschwingverhalten, THD.",
     "РАУНД 5 (долговечность, итог): электролитические конденсаторы в отдельном корпусе при 45 °C или ниже (около 73 лет), реле с защёлкой, ручка громкости VER6 (около 17 лет), температурная защита выходных транзисторов, контроль постоянной составляющей на 2 тактильных каналах. Пройдено: нагрев, разводка, джиттер. Не выполнено: измерения, проверка HDMI, сертификация IMAX Enhanced / Dolby / DTS, переходные процессы, КНИ."),
]
y = 64
text(6, 66.5, "TEST / DEBUG の記録 (5 回)  Log", 1.6, INK, "la", True)
for blk in rows:
    for i, t in enumerate(blk):
        for ln in textwrap.wrap(t, 175 if i else 90):
            text(6, y, ln, 0.8, INK if i == 0 else GRY, "la")
            y -= 1.3
    y -= 0.5
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\surround_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, round(allab4), round(allab8), round(mix4), round(film_ab), round(film_mix), round(x0), round(snr(1)), round(snr(.3)), round(rip, 2), round(y, 1))
