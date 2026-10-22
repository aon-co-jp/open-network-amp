# VER6 — shorter wiring, durable hybrid volume knob (差分 / delta / Unterschied / отличия from VER5)

VER6 is VER5 plus the changes below. The VER5 schematics remain valid; the figure `amp_ver6_sim.jpg` / `.pdf` holds the VER6 test log in Japanese, English, German and Russian.
Design hints came from web searches in Japanese, German, Russian, Chinese and English (PS Audio, Analog Devices, mikrocontroller.net forum, MPS). They are design guidance, not proof. All numbers are Python calculations, not bench measurements.

## 日本語
- 配線: 入力部品をピン直近に置く / 信号は入力→出力へ一方向 / 電源・グランドの母線は最後に結ぶ / 1チャンネルの経路 60mm→45mm / グランド面を直下に切れ目なく敷く (誘導ノイズ約 −36dB、計算) / バイパスコンデンサは 2mm 以内 (10MHz で 0.13Ω) / デジタル・アナログ・無線は別区画で 1 点接続 (擬似スター)。
- 音量ノブ: 非接触の磁気エンコーダ 2 個 (相互監視)、ボールベアリング 2 個、停止位置でモーター電流を絞る (PWM 60kHz 以上でうなり防止)、コギング校正でクリック感を均一に、ラッチングリレー + 0.1% 薄膜抵抗。寿命は可変抵抗 約 6.8 年 / 機械クリック 約 4.1 年に対し約 17 年 (1日 20 回転、グリース劣化が限界、仮定)。

## English
- Wiring: input parts at the pins; one-way signal flow; supply/ground buses joined last; channel path 60→45 mm; unbroken ground plane beneath (about 36 dB less pick-up, calculated); bypass capacitors within 2 mm (0.13 ohm at 10 MHz); digital, analog and RF areas separate, joined at one point (pseudo-star).
- Volume knob: two non-contact magnetic encoders watching each other, two ball bearings, reduced motor current at rest (PWM at 60 kHz or higher), cogging calibration for equal clicks, latching relays with 0.1% thin-film resistors. Life about 17 years versus about 6.8 (potentiometer) and 4.1 (mechanical click) at 20 turns a day (grease ageing limits it; assumption).

## Deutsch
- Verdrahtung: Eingangsbauteile an den Pins; Signal in einer Richtung; Versorgungs- und Massebus zuletzt verbunden; Kanalweg 60→45 mm; ununterbrochene Massefläche darunter (etwa 36 dB weniger Einstreuung, berechnet); Entkopplung innerhalb 2 mm; Digital-, Analog- und HF-Bereiche getrennt, an einem Punkt verbunden (Pseudo-Stern).
- Lautstärkeknopf: zwei berührungslose Magnetencoder mit gegenseitiger Überwachung, zwei Kugellager, reduzierter Motorstrom im Stillstand (PWM ab 60 kHz), Cogging-Kalibrierung, Latching-Relais mit 0,1-%-Dünnschichtwiderständen. Lebensdauer etwa 17 Jahre gegenüber 6,8 (Potentiometer) und 4,1 Jahren (mechanische Rastung) bei 20 Umdrehungen am Tag (Annahme).

## Русский
- Разводка: входные детали у выводов; сигнал в одну сторону; шины питания и земли соединяются в конце; путь канала 60→45 мм; сплошной слой земли под ним (наводка примерно на 36 дБ меньше, расчёт); развязка в пределах 2 мм; цифровая, аналоговая и ВЧ-части разделены и соединены в одной точке (псевдозвезда).
- Ручка громкости: два бесконтактных магнитных энкодера, следящих друг за другом, два шарикоподшипника, сниженный ток двигателя в покое (ШИМ от 60 кГц), калибровка зубцового момента, реле с защёлкой и тонкоплёночные резисторы 0,1 %. Ресурс около 17 лет против 6,8 (потенциометр) и 4,1 года (механический фиксатор) при 20 оборотах в день (допущение).

---
## Added to VER6: analog-input Class D power stage / クラス D アナログ版 / Klasse D mit Analogeingang / Класс D с аналоговым входом
Figure: `amp_ver6_classD.jpg` (both PDF pages in `amp_ver6_all.pdf`). Eigentakt-type self-oscillating Class D with feedback, fully balanced and unbalanced versions, selectable for the solid-state, tube and network versions. Always with the external linear DC supply (R-core; power rails as unregulated large capacitor banks, analog and clock low-noise linear). Python calculations, not SPICE or bench measurements.

- 日本語: アナログ入力のまま増幅するクラス D (Eigentakt 型、自己発振約 500kHz + 負帰還)。外付けリニア DC 電源 (R コア、パワー段は非安定の大容量コンデンサ、アナログとクロックは低雑音リニア)。発熱は 8Ω 最大出力で 1ch あたり約 14W (Class AB は約 51W)。出力 LC フィルタ (22µH / 0.47µF、共振約 49kHz) は 16Ω で高域が 7.6dB 持ち上がるため、RC ダンピング (ゾベル) で約 0.7dB に抑える。クラス D が必ず音がよいとは限らず、フィルタ・電源・配線次第。未実施: 実機測定、過渡応答。
- English: analog-input Class D (Eigentakt type, self-oscillating at about 500 kHz with feedback), with the external linear DC supply (R-core; power rails unregulated large capacitor banks; analog and clock low-noise linear). Heat is about 14 W per channel at full power into 8 ohm (Class AB about 51 W). The output LC filter (22 uH / 0.47 uF, resonance about 49 kHz) lifts the treble by 7.6 dB into 16 ohm, so an RC damper (Zobel) holds it to about 0.7 dB. Class D is not automatically better sounding. Not done: bench measurements, transient response.
- Deutsch: Klasse D mit Analogeingang (Eigentakt-Typ, selbstschwingend bei etwa 500 kHz mit Gegenkopplung) mit externem linearem Gleichspannungsnetzteil (R-Kern; Endstufenschienen ungeregelte große Kondensatorbänke; Analog und Takt rauscharm linear). Wärme etwa 14 W je Kanal bei Vollaussteuerung an 8 Ω (Klasse AB etwa 51 W). Der LC-Ausgangsfilter (22 µH / 0,47 µF, Resonanz etwa 49 kHz) hebt die Höhen an 16 Ω um 7,6 dB an; ein RC-Dämpfungsglied (Zobel) hält es bei etwa 0,7 dB. Klasse D klingt nicht automatisch besser. Nicht durchgeführt: Messungen, Einschwingverhalten.
- Русский: класс D с аналоговым входом (тип Eigentakt, самовозбуждение около 500 кГц с обратной связью) с внешним линейным блоком питания постоянного тока (R-сердечник; шины силового каскада — нестабилизированные батареи больших конденсаторов; аналоговая часть и такт — малошумящая линейная стабилизация). Нагрев около 14 Вт на канал при полной мощности на 8 Ом (класс AB около 51 Вт). Выходной LC-фильтр (22 мкГн / 0,47 мкФ, резонанс около 49 кГц) поднимает верха на 16 Ом на 7,6 дБ; RC-демпфер (цепь Цобеля) удерживает около 0,7 дБ. Класс D не всегда звучит лучше сам по себе. Не выполнено: измерения, переходные процессы.
