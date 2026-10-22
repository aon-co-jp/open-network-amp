import re, subprocess, os
SD = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
COMMON = {
    "ja": "VER6 音質改善: 入力・帰還の抵抗は 0.1% 薄膜、結合・積分コンデンサはフィルム (C0G)、0.1µF のバイパスは各チップの 2mm 以内、信号は入力→出力へ一方向、グランド面を直下に敷く (経路 約 40mm)、電源は外付けリニア DC。",
    "en": "VER6 sound improvements: 0.1% thin-film resistors in the input and feedback, film (C0G) coupling and integrator capacitors, 0.1 uF bypass capacitors within 2 mm of each device, one-way signal flow from input to output, a ground plane beneath (path about 40 mm) and the external linear DC supply.",
    "de": "VER6 Klangverbesserung: 0,1-%-Dünnschichtwiderstände in Eingang und Gegenkopplung, Folien-Kondensatoren (C0G) für Kopplung und Integrator, 0,1-µF-Abblockkondensatoren höchstens 2 mm vom Bauteil, Signal einseitig vom Eingang zum Ausgang, Massefläche darunter (Weg etwa 40 mm), externes lineares Gleichspannungsnetzteil.",
    "ru": "VER6, улучшение звука: плёночные резисторы 0,1 % на входе и в цепи обратной связи, плёночные (C0G) конденсаторы связи и интегратора, блокировочные 0,1 мкФ в пределах 2 мм от компонента, сигнал в одну сторону от входа к выходу, слой земли под ним (путь около 40 мм), внешний линейный блок питания постоянного тока.",
}
SPEC = {
    "a": {"ja": "Class A: Q1 のゲートとドレインに近接したゲート抵抗 (発振防止)、定電流源は温度補償、アイドル電流は高温で自動低減、ヒートシンク ≤0.3°C/W + 温度制御ファン。",
          "en": "Class A: gate stopper resistors right at the gate and drain of Q1 (anti-oscillation), a temperature-compensated current source, idle current reduced automatically when hot and a heatsink of 0.3 C/W or better with a temperature-controlled fan.",
          "de": "Klasse A: Gate-Stopper-Widerstände direkt an Gate und Drain von Q1 (gegen Schwingen), temperaturkompensierte Stromquelle, bei Hitze automatisch geringerer Ruhestrom, Kühlkörper 0,3 °C/W oder besser mit temperaturgeregeltem Lüfter.",
          "ru": "Класс A: затворные резисторы у затвора и стока Q1 (против самовозбуждения), температурно-компенсированный источник тока, автоматическое снижение тока покоя при нагреве, радиатор не хуже 0,3 °C/Вт и вентилятор с термоуправлением."},
    "b": {"ja": "Class AB: 出力素子 2 並列 (4Ω でも約 91°C)、エミッタ抵抗 0.33Ω は無誘導、Cdom 68pF は C0G、Vbe 倍率のトランジスタは出力素子と同じヒートシンクに熱結合 (バイアス安定)。",
          "en": "Class AB: two output devices in parallel (about 91 C even at 4 ohm), non-inductive 0.33 ohm emitter resistors, a C0G Cdom of 68 pF and the Vbe multiplier thermally coupled to the output heatsink for a stable bias.",
          "de": "Klasse AB: zwei Endtransistoren parallel (selbst an 4 Ω etwa 91 °C), induktionsarme 0,33-Ω-Emitterwiderstände, Cdom 68 pF als C0G, Vbe-Multiplikator thermisch mit dem Endstufenkühlkörper gekoppelt (stabiler Ruhestrom).",
          "ru": "Класс AB: два выходных транзистора параллельно (даже на 4 Ом около 91 °C), безындуктивные эмиттерные резисторы 0,33 Ом, Cdom 68 пФ типа C0G, умножитель Vbe термически связан с радиатором выходных транзисторов (стабильный ток покоя)."},
    "d": {"ja": "真空管: ヒーターは 6.3V の DC (ソフトスタート)、B+ は容量倍増 + CRC で遅延投入、管はシールドとダンパーで振動 (マイクロフォニック) を抑える、カソード抵抗は無誘導の金属皮膜、管ソケットは金めっき。",
          "en": "Tube: a 6.3 V DC heater with soft start, B+ through a capacitance multiplier and CRC with delayed switch-on, a shield and damper on the tube against microphonics, a non-inductive metal-film cathode resistor and gold-plated tube sockets.",
          "de": "Röhre: 6,3-V-Gleichstromheizung mit Sanftanlauf, B+ über Kapazitätsvervielfacher und CRC mit verzögertem Einschalten, Abschirmung und Dämpfer gegen Mikrofonie, induktionsarmer Metallschicht-Kathodenwiderstand, vergoldete Röhrenfassungen.",
          "ru": "Лампа: накал 6,3 В постоянным током с мягким пуском, B+ через умножитель ёмкости и CRC с задержкой включения, экран и демпфер против микрофонного эффекта, безындуктивный металлоплёночный катодный резистор, позолоченные ламповые панели."},
}
JOBS = [("a", "fig_a_body.py", "amp_classA.jpg", "amp_ver6_classA.jpg", 130),
        ("b", "fig_b_body.py", "amp_classAB.jpg", "amp_ver6_classAB.jpg", 130),
        ("d", "fig_d_body.py", "amp_tube_pre.jpg", "amp_ver6_tube.jpg", 130)]
for key, src, oldjpg, newjpg, H in JOBS:
    s = open(os.path.join(SD, src), encoding="utf-8").read()
    s = s.replace(oldjpg, newjpg)
    s = re.sub(r'(text\(3, 127, ")', r'\1VER6  ', s, count=1)
    add = "\n"
    y = 8.0
    for lang in ("ja", "en", "de", "ru"):
        for t in (COMMON[lang], SPEC[key][lang]):
            add += "import textwrap as _tw\n"
        # one wrapped block per language
    add = "import textwrap as _tw\n_y = 30.0\n"
    for lang in ("ja", "en", "de", "ru"):
        add += "for _l in _tw.wrap(%r, 100 if %r != 'ja' else 48):\n    text(104, _y, _l, 0.8, INK if %r == 'ja' else GRY, 'la'); _y -= 1.15\n" % (COMMON[lang] + " " + SPEC[key][lang], lang, lang)
    s = s.replace("img = img.resize", add + "img = img.resize", 1)
    out = os.path.join(SD, "v6_" + src)
    open(out, "w", encoding="utf-8").write(s)
    r = subprocess.run(["python", os.path.join(SD, "run_fig.py"), "v6_" + src, str(H)], capture_output=True, text=True, encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"), cwd=SD)
    print(key, r.stdout.strip()[-120:], r.stderr.strip()[-200:])
