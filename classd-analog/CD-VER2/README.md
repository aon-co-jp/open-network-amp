# CD-VER2 — analog-input Class D amplifier with external linear DC supply / クラスD アナログ版 + 外付けリニアDC電源 / Klasse D mit Analogeingang und externem Netzteil / Класс D с внешним линейным блоком питания

CD-VER2 reviews the whole design for durability, sound and shorter wiring (CD-VER1 = `VER6/amp_ver6_classD.jpg`). Figures: `cd_v2_block.jpg` (block diagram + changes), `psu_v2_sim.jpg` (5 virtual test/debug rounds in 4 languages), both in `classd-analog-cd-ver2.pdf`. Python calculations, not SPICE or bench measurements.

## 日本語
- 配線: DC ケーブルを 6mm² 0.8m に短縮 (ピーク 13.6A で 62mV、VER1 の 2.5mm² 1.5m は 281mV)。整流 → コンデンサのループを 20mm 以下 (スパイク 4.0V → 1.0V)、ソフトリカバリ ダイオード + RC スナバ、銅バスバー、グランドは 1 点スター。パワーモジュールはスピーカー端子の隣に置き、DAC・ボリュームとシールド板で仕切る。各チャンネルは入力から出力へ約 40mm の一直線。
- 耐久: 電解コンデンサは 63V (レール 45V の 1.4 倍)・リップル電流 50% 以下・フィルム並列。45°C で約 52 年 (リップル発熱 +5K)、旧設計 (+20K) は約 18 年。NTC 10Ω + リレーで突入電流を約 14A に、DC ブロッカで偏磁を防ぎ、MOV・過電圧・過電流・温度・DC 出力の保護。
- 音質: リップル 0.10V → 容量倍増で約 1mV → LT3045 / LT3094 で約 0.1µV (段ごとの減衰は仮定)。クロックと DAC は専用レギュレータ。16Ω での出力フィルタのピーク 7.6dB をゾベルで 0.7dB に。クラス D が必ず音がよいとは限らず、実機測定が必要。
- 未実施: 実機測定、過渡応答、EMI、安全規格試験。

## English
- Wiring: the DC cable shortens to 6 mm2 at 0.8 m (62 mV at the 13.6 A peak versus 281 mV for 2.5 mm2 at 1.5 m). The rectifier-to-capacitor loop is 20 mm or less (spike 4.0 V to 1.0 V) with soft-recovery diodes, an RC snubber, copper bus bars and a single-point star ground. The power modules sit next to the speaker terminals behind a shield plate from the DAC and volume; each channel runs about 40 mm in a straight line.
- Durability: electrolytic capacitors rated 63 V (1.4 times the 45 V rail), ripple current at 50% of the rating or less, film capacitors in parallel. About 52 years at 45 C (+5 K self-heating) against about 18 years for the old +20 K design. NTC 10 ohm plus relay limits the inrush to about 14 A, a DC blocker prevents core saturation, plus MOV, over-voltage, over-current, temperature and DC-output protection.
- Sound: 0.10 V ripple falls to about 1 mV with a capacitance multiplier and about 0.1 uV with LT3045 / LT3094 (attenuation per stage assumed). Clock and DAC have their own regulators. A Zobel cuts the 7.6 dB output-filter peak into 16 ohm to 0.7 dB. Class D is not automatically better sounding; bench measurements are needed.
- Not done: bench measurements, transient response, EMI, safety-standard testing.

## Deutsch
- Verdrahtung: Das DC-Kabel wird auf 6 mm² bei 0,8 m verkürzt (62 mV bei 13,6 A Spitze statt 281 mV bei 2,5 mm² und 1,5 m). Die Schleife Gleichrichter–Kondensator beträgt höchstens 20 mm (Spitze 4,0 V auf 1,0 V), mit Soft-Recovery-Dioden, RC-Snubber, Kupfer-Sammelschienen und Sternpunkt-Masse. Die Endstufenmodule sitzen neben den Lautsprecherklemmen hinter einer Schirmwand zu DAC und Lautstärkeregler; jeder Kanal verläuft etwa 40 mm geradlinig.
- Haltbarkeit: Elektrolytkondensatoren für 63 V (1,4-faches der 45-V-Schiene), Rippelstrom höchstens 50 % der Nennwerte, Folienkondensatoren parallel. Etwa 52 Jahre bei 45 °C (+5 K Eigenerwärmung) gegenüber etwa 18 Jahren beim alten Entwurf (+20 K). NTC 10 Ω plus Relais begrenzt den Einschaltstrom auf etwa 14 A, ein Gleichstromblocker verhindert Kernsättigung, dazu MOV-, Überspannungs-, Überstrom-, Temperatur- und Gleichspannungs-Ausgangsschutz.
- Klang: 0,10 V Rippel sinken mit Kapazitätsvervielfacher auf etwa 1 mV und mit LT3045 / LT3094 auf etwa 0,1 µV (Dämpfung je Stufe angenommen). Takt und DAC haben eigene Regler. Ein Zobel senkt die Spitze des Ausgangsfilters an 16 Ω von 7,6 dB auf 0,7 dB. Klasse D klingt nicht automatisch besser; Messungen sind nötig.
- Nicht durchgeführt: Messungen, Einschwingverhalten, EMV, Sicherheitsprüfung.

## Русский
- Разводка: кабель постоянного тока укорочен до 6 мм² при 0,8 м (62 мВ при пике 13,6 А против 281 мВ для 2,5 мм² и 1,5 м). Петля выпрямитель–конденсатор не более 20 мм (выброс 4,0 В → 1,0 В), диоды с мягким восстановлением, RC-демпфер, медные шины, звезда земли. Силовые модули рядом с клеммами акустики за экраном от ЦАП и регулятора громкости; каждый канал — прямая линия около 40 мм.
- Долговечность: электролиты на 63 В (в 1,4 раза выше шины 45 В), пульсирующий ток не более 50 % от номинала, плёночные конденсаторы параллельно. Около 52 лет при 45 °C (самонагрев +5 К) против около 18 лет в старом варианте (+20 К). NTC 10 Ом с реле ограничивает пусковой ток около 14 А, блокиратор постоянного тока предотвращает насыщение, есть защита MOV, от перенапряжения, перегрузки, перегрева и постоянной составляющей на выходе.
- Звук: пульсации 0,10 В падают до около 1 мВ с умножителем ёмкости и до около 0,1 мкВ с LT3045 / LT3094 (ослабление каскадов принято). У такта и ЦАП отдельные стабилизаторы. Цепь Цобеля снижает пик выходного фильтра на 16 Ом с 7,6 дБ до 0,7 дБ. Класс D не всегда звучит лучше сам по себе; нужны измерения.
- Не выполнено: измерения, переходные процессы, ЭМС, испытания по стандартам безопасности.
