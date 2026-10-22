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
