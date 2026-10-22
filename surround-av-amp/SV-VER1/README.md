# SV-VER1 — Surround AV amplifier / サラウンド AV アンプ / Surround-AV-Verstärker / AV-ресивер объёмного звука

Reference design (not a product). Python calculations, not SPICE or bench measurements. Figures: `surround_balanced.jpg` (fully balanced), `surround_unbalanced.jpg`, `surround_sim.jpg` (5 test/debug rounds); all in `surround-av-amp.pdf`.
IMAX Enhanced, Dolby and DTS certification need licences and were not done. 4DX is a cinema system without a home standard; this design offers tactile (bass-shaker) outputs and a control port for a similar feel.

## 日本語
- 構成: HDMI 2.1 入力 6 系統 (eARC)、Dolby Atmos・DTS:X (IMAX Enhanced 対応を想定) の 11.2.4 処理、DAC 12ch (AK4191 + BD34302 を 6 組)、触覚ハイブリッド音量 VER6、パワーアンプ 11ch (7.1.4)。
- 完全バランス版 (全 12ch を差動のまま処理) とアンバランス版 (DAC 直後に差動→単相) の 2 種類。どちらも、モノラルのサブウーファー端子 (RCA + XLR) を 2 系統 (低雑音 0.28µV の改良版)、触覚 (4DX 風) 出力 2ch、ヘッドホン、PRE OUT を持ちます。
- 配線: チャンネルごとに DAC→ボリューム→パワーを一直線 (約 40mm)、グランド面を直下に敷き、隣の経路と 25mm あける (集中配置の 180mm 比で誘導・クロストーク 約 −21dB、計算)。
- 発熱: 全 11ch を Class AB にすると 4Ω で約 1128W。フロント L/C/R だけ Class AB、他 8ch をクラス D にすると約 533W (映画の平均は約 138W) → 温度制御ファンで処理。
- 音質・耐久: ジッタ 0.3ps で SNR 約 148dB、電解コンデンサは別筐体 45°C 以下 (約 73 年)、ラッチングリレー、非接触磁気エンコーダ 2 重の音量ノブ (約 17 年)。
- 未実施: 実機測定、HDMI 認証、各社の認証、過渡応答、THD。

## English
- Layout: six HDMI 2.1 inputs (eARC), Dolby Atmos and DTS:X (aimed at IMAX Enhanced) 11.2.4 processing, a 12-channel DAC (six AK4191 + BD34302 pairs), the VER6 haptic hybrid volume, an 11-channel power amplifier (7.1.4).
- Two versions: fully balanced (all 12 channels stay differential) and unbalanced (differential to single-ended right after the DAC). Both have two mono subwoofer outputs (RCA + XLR, the low-noise 0.28 uV version), two tactile (4DX-style) channels, headphones and PRE OUT.
- Wiring: one straight line per channel, DAC to volume to power stage (about 40 mm), a ground plane beneath and 25 mm to the neighbour (about 21 dB less pick-up and crosstalk than a 180 mm central layout, calculated).
- Heat: all 11 channels in Class AB dissipate about 1128 W at 4 ohm; with only front L/C/R in Class AB and 8 channels in Class D it is about 533 W (about 138 W for the film average), handled by a temperature-controlled fan.
- Sound and durability: 0.3 ps jitter gives about 148 dB SNR, the electrolytic capacitors sit in a separate case at 45 C or below (about 73 years), latching relays, and the volume knob with two non-contact magnetic encoders (about 17 years).
- Not done: bench measurements, HDMI compliance, vendor certifications, transient response, THD.

## Deutsch
- Aufbau: sechs HDMI-2.1-Eingänge (eARC), Dolby Atmos und DTS:X (auf IMAX Enhanced ausgelegt) 11.2.4, 12-Kanal-DAC (sechs Paare AK4191 + BD34302), haptischer Hybrid-Lautstärkeregler VER6, 11-Kanal-Endstufe (7.1.4).
- Zwei Versionen: voll symmetrisch (alle 12 Kanäle bleiben differenziell) und unsymmetrisch. Beide haben zwei Mono-Subwoofer-Ausgänge (RCA + XLR, rauscharme Version 0,28 µV), zwei Haptikkanäle (4DX-artig), Kopfhörer und PRE OUT.
- Verdrahtung: je Kanal eine gerade Linie DAC, Lautstärke, Endstufe (etwa 40 mm), Massefläche darunter, 25 mm zum Nachbarn (etwa 21 dB weniger Einstreuung und Übersprechen als bei 180 mm zentralem Aufbau, berechnet).
- Wärme: Alle 11 Kanäle in Klasse AB ergeben etwa 1128 W an 4 Ω; nur Front L/C/R in Klasse AB und 8 Kanäle in Klasse D: etwa 533 W (Filmdurchschnitt etwa 138 W), mit temperaturgeregeltem Lüfter.
- Klang und Haltbarkeit: 0,3 ps Jitter ergeben etwa 148 dB SNR, Elektrolytkondensatoren im getrennten Gehäuse bei höchstens 45 °C (etwa 73 Jahre), Latching-Relais, Lautstärkeknopf mit zwei berührungslosen Magnetencodern (etwa 17 Jahre).
- Nicht durchgeführt: Messungen, HDMI-Konformität, Zertifizierungen, Einschwingverhalten, THD.

## Русский
- Состав: шесть входов HDMI 2.1 (eARC), обработка Dolby Atmos и DTS:X (в расчёте на IMAX Enhanced) 11.2.4, 12-канальный ЦАП (шесть пар AK4191 + BD34302), тактильный гибридный регулятор громкости VER6, 11-канальный усилитель (7.1.4).
- Две версии: полностью сбалансированная (все 12 каналов остаются дифференциальными) и несбалансированная. В обеих два моно-выхода сабвуфера (RCA + XLR, малошумящая версия 0,28 мкВ), два тактильных канала (в духе 4DX), наушники и PRE OUT.
- Разводка: для каждого канала одна прямая линия ЦАП, регулятор громкости, усилитель (около 40 мм), слой земли под ней, 25 мм до соседа (наводка и перекрёстные помехи примерно на 21 дБ меньше, чем при центральной компоновке 180 мм, расчёт).
- Нагрев: все 11 каналов в классе AB — около 1128 Вт на 4 Ом; только фронтальные L/C/R в классе AB и 8 каналов в классе D — около 533 Вт (среднее для фильма около 138 Вт), вентилятор с термоуправлением.
- Звук и долговечность: джиттер 0,3 пс даёт SNR около 148 дБ, электролитические конденсаторы в отдельном корпусе при 45 °C или ниже (около 73 лет), реле с защёлкой, ручка громкости с двумя бесконтактными магнитными энкодерами (около 17 лет).
- Не выполнено: измерения, проверка HDMI, сертификации, переходные процессы, КНИ.
