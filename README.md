# Integrated amplifier — VER5 (design files)
Fully balanced and unbalanced integrated amplifiers with a haptic hybrid volume knob, DDC + DAC, headphone amplifier and dedicated mono subwoofer terminals (RCA + XLR).
Reference designs only (Python calculations, not bench measurements). See https://audiocafe.tokyo/ for the figures, PDF and JPG files.
Languages: [日本語](#ja) · [English](#en) · [Deutsch](#de) · [Русский](#ru)

<a id="ja"></a>
## 日本語

### 説明書 (取扱・設計メモ)  VER5 — 完全バランス / アンバランス プリメインアンプ

#### 1. 概要
- ハイテク音量ボリューム (触覚ハイブリッド VER2)、DDC + DAC (AK4191 + BD34302、MQA フルデコーダ別搭載)、ヘッドホンアンプ、モノラルのサブウーファー専用端子 (RCA と XLR) を備えたプリメインアンプです。完全バランス版とアンバランス版の 2 種類があり、どちらにもサブウーファー端子が付きます。
- アナログ版 (外付けリニア電源・Class A / AB / D・半導体 / 真空管プリ) も同じ考え方で設計しています。

#### 2. スイッチ (本体)
- SW1: DDC と DAC の I2S 接続 ON / OFF (OFF で I2S OUT から外部 DAC へ)。SW2: DAC の電源 + I2S ON / OFF。SW3: 無線 (Wi-Fi / Bluetooth) の電源 ON / OFF。
- SW5: デジタルのボリューム / EQ をバイパス (ビットパーフェクト)。SW6: 音量ノブのクリック感 ON / OFF。SW7: ゲイン調整のモード ANALOG / DIGITAL。SW8: ヘッドホン挿入時のスピーカー自動ミュート ON / OFF。

#### 3. スイッチ (サブウーファー回路)
- SW1: MONO / STEREO。SW2: 位相 0° / 180°。SW3: LPF BYPASS / 80 / 100 / 120 Hz。SW4: 12 dB/oct / 24 dB/oct (LR4)。VR2: 位相の連続可変。SW9: XLR 1番ピンの GND リフト。K2: 出力ミュートリレー (自動)。

#### 4. 端子
- 入力: RCA / XLR (アナログ)、USB-C、I2S、LAN / Wi-Fi、Bluetooth。出力: スピーカー (バイワイヤ対応 HF / LF)、PRE OUT (RCA + XLR)、SUB OUT (モノラル RCA + XLR)、ヘッドホン 3.5mm (バランス / アンバランス兼用)・4.4mm (バランス)・6.35mm (アンバランス)、HDMI / USB-C 映像出力。

#### 5. 使い方
- 音量: ノブを回します。SW6 が ON ならクリック 1 回 = 1 dB のクリック感、OFF なら滑らかです。ゲイン調整は SW7 で ANALOG (ビットパーフェクトを保つ) か DIGITAL (FPGA のデジタルゲイン) を選びます。どちらも、スピーカーとヘッドホンに同時に効きます。
- ヘッドホン: 3 つのジャックのどれかに挿します (3.5mm は TRRS = バランス、TRS = アンバランスを自動検出)。ゲインは 0 / +6 / +12 / +18 dB。
- サブウーファー: SUB OUT をサブウーファーの入力へつなぎ、SW3 でカットオフを、SW4 と SW2 / VR2 でメインスピーカーとの合成が平坦になるよう位相を合わせます。メインが 24 dB/oct (LR4) なら SW4 を 24 dB にします。

#### 6. 注意
- 参考設計です。部品値は机上計算で、シミュレーションは Python の計算までです。過渡応答・歪み (THD)・実機の雑音と位相・触覚の感触は未実施で、安全規格・認証の確認が必要です。
- 電源トランスはトロイダルを左右独立の 2 台にして、静電シールド・ミューメタル缶・商用 DC ブロッカを併用します。
- 耐久性: 大容量の電解コンデンサは外付け電源に置き (45°C 以下)、Class AB の出力素子は 2 並列、Class A は温度制御ファンつきです。リレー式ボリュームは 1 日 500 回で約 55 年、真空管は約 10,000 時間です。ヘッドホンジャックは交換できるサブ基板に付けます。
- 外付けリニア電源 (アナログ版) には高電圧 (B+ 250V) と大電流があります。取り扱いに注意してください。

<a id="en"></a>
## English

### Manual (operation and design notes)  VER5 — fully balanced / unbalanced integrated amplifiers

#### 1. Overview
- An integrated amplifier with a high-tech volume knob (haptic hybrid VER2), DDC + DAC (AK4191 + BD34302, with a separate MQA full decoder), a headphone amplifier and dedicated mono subwoofer terminals (RCA and XLR). There are two versions, fully balanced and unbalanced, and both have the subwoofer terminals.
- The analog versions (external linear supply, Class A / AB / D, solid-state / tube preamp) follow the same ideas.

#### 2. Switches (main unit)
- SW1: DDC-to-DAC I2S link ON / OFF (OFF sends the I2S out to an external DAC). SW2: DAC power + I2S ON / OFF. SW3: wireless (Wi-Fi / Bluetooth) power ON / OFF.
- SW5: bypass the digital volume / EQ (bit-perfect). SW6: knob click feel ON / OFF. SW7: gain mode ANALOG / DIGITAL. SW8: automatic speaker mute when headphones are plugged in, ON / OFF.

#### 3. Switches (subwoofer circuit)
- SW1: MONO / STEREO. SW2: phase 0 / 180 degrees. SW3: LPF BYPASS / 80 / 100 / 120 Hz. SW4: 12 dB/oct or 24 dB/oct (LR4). VR2: continuous phase. SW9: ground lift of XLR pin 1. K2: output mute relay (automatic).

#### 4. Terminals
- Inputs: RCA / XLR (analog), USB-C, I2S, LAN / Wi-Fi, Bluetooth. Outputs: speakers (bi-wire HF / LF), PRE OUT (RCA + XLR), SUB OUT (mono RCA + XLR), headphones 3.5 mm (balanced and unbalanced), 4.4 mm (balanced), 6.35 mm (unbalanced), and HDMI / USB-C video output.

#### 5. How to use
- Volume: turn the knob. With SW6 ON each click is 1 dB with a click feel; OFF is smooth. SW7 selects the gain mode, ANALOG (keeps bit-perfect) or DIGITAL (digital gain in the FPGA). Both act on the speakers and the headphones at the same time.
- Headphones: plug into any of the three jacks (the 3.5 mm jack detects TRRS = balanced and TRS = unbalanced automatically). Gain steps are 0 / +6 / +12 / +18 dB.
- Subwoofer: connect SUB OUT to the subwoofer input, set the cutoff with SW3, and use SW4 and SW2 / VR2 to make the sum with the main speakers flat. If the main speaker is 24 dB/oct (LR4), set SW4 to 24 dB.

#### 6. Notes
- Reference designs. The component values are on paper and the simulation is Python calculation only. Transient response, THD, real noise and phase, and the haptic feel have not been checked, and safety standards and certification must be checked.
- The power transformers are two independent toroids (one per channel) with an electrostatic shield, a mu-metal can and a mains DC blocker.
- Durability: the large electrolytic capacitors sit in the external supply (45 C or below), the Class AB output devices are doubled in parallel and Class A has a temperature-controlled fan. The relay volume lasts about 55 years at 500 operations a day and a tube about 10,000 hours. The headphone jacks sit on a replaceable sub-board.
- The external linear supply of the analog versions carries high voltage (B+ 250 V) and high current. Handle it with care.

<a id="de"></a>
## Deutsch

### Anleitung (Bedienung und Entwurfsnotizen)  VER5 — voll symmetrische / unsymmetrische Vollverstärker

#### 1. Überblick
- Ein Vollverstärker mit High-Tech-Lautstärkeknopf (haptischer Hybrid VER2), DDC + DAC (AK4191 + BD34302, mit separatem MQA-Volldecoder), Kopfhörerverstärker und eigenen Mono-Subwoofer-Anschlüssen (RCA und XLR). Es gibt zwei Versionen, voll symmetrisch und unsymmetrisch; beide haben die Subwoofer-Anschlüsse.
- Die Analogversionen (externes lineares Netzteil, Klasse A / AB / D, Halbleiter- / Röhren-Vorstufe) folgen denselben Ideen.

#### 2. Schalter (Hauptgerät)
- SW1: I2S-Verbindung DDC–DAC EIN / AUS (AUS leitet das I2S an einen externen DAC aus). SW2: DAC-Spannung + I2S EIN / AUS. SW3: Funk (Wi-Fi / Bluetooth) EIN / AUS.
- SW5: digitale Lautstärke / EQ umgehen (Bit-perfekt). SW6: Rastgefühl des Knopfes EIN / AUS. SW7: Verstärkungsmodus ANALOG / DIGITAL. SW8: automatische Lautsprecher-Stummschaltung beim Einstecken von Kopfhörern EIN / AUS.

#### 3. Schalter (Subwoofer-Schaltung)
- SW1: MONO / STEREO. SW2: Phase 0 / 180°. SW3: Tiefpass BYPASS / 80 / 100 / 120 Hz. SW4: 12 dB/Okt oder 24 dB/Okt (LR4). VR2: stufenlose Phase. SW9: Ground-Lift von XLR-Pin 1. K2: Ausgangs-Stummschaltrelais (automatisch).

#### 4. Anschlüsse
- Eingänge: RCA / XLR (analog), USB-C, I2S, LAN / Wi-Fi, Bluetooth. Ausgänge: Lautsprecher (Bi-Wiring HF / LF), PRE OUT (RCA + XLR), SUB OUT (Mono-RCA + XLR), Kopfhörer 3,5 mm (symmetrisch und unsymmetrisch), 4,4 mm (symmetrisch), 6,35 mm (unsymmetrisch) sowie HDMI- / USB-C-Videoausgang.

#### 5. Bedienung
- Lautstärke: Knopf drehen. Mit SW6 EIN hat jede Raste 1 dB mit Rastgefühl, AUS läuft der Knopf sanft. SW7 wählt ANALOG (bleibt Bit-perfekt) oder DIGITAL (digitale Verstärkung im FPGA). Beides wirkt gleichzeitig auf Lautsprecher und Kopfhörer.
- Kopfhörer: in eine der drei Buchsen stecken (die 3,5-mm-Buchse erkennt TRRS = symmetrisch und TRS = unsymmetrisch automatisch). Verstärkungsstufen: 0 / +6 / +12 / +18 dB.
- Subwoofer: SUB OUT mit dem Subwoofer-Eingang verbinden, mit SW3 die Trennfrequenz wählen und mit SW4 sowie SW2 / VR2 die Summe mit den Hauptlautsprechern glätten. Ist der Hauptlautsprecher 24 dB/Okt (LR4), SW4 auf 24 dB stellen.

#### 6. Hinweise
- Referenzentwürfe. Die Bauteilwerte sind rechnerisch, die Simulation besteht nur aus Python-Berechnungen. Einschwingverhalten, Klirrfaktor (THD), echtes Rauschen und Phase sowie das haptische Gefühl wurden nicht geprüft; Sicherheitsnormen und Zertifizierung müssen geprüft werden.
- Die Netztransformatoren sind zwei unabhängige Ringkerne (je Kanal) mit elektrostatischer Schirmung, Mu-Metall-Becher und Netz-Gleichstromblocker.
- Haltbarkeit: Die großen Elektrolytkondensatoren sitzen im externen Netzteil (45 °C oder weniger), die Klasse-AB-Endtransistoren sind doppelt parallel geschaltet, und Klasse A hat einen temperaturgeregelten Lüfter. Der Relais-Lautstärkeregler hält bei 500 Bedienungen pro Tag etwa 55 Jahre, eine Röhre etwa 10.000 Stunden. Die Kopfhörerbuchsen sitzen auf einer austauschbaren Unterplatine.
- Das externe lineare Netzteil der Analogversionen führt Hochspannung (B+ 250 V) und hohe Ströme. Mit Vorsicht behandeln.

<a id="ru"></a>
## Русский

### Руководство (эксплуатация и заметки по проекту)  VER5 — полностью балансные / несимметричные интегральные усилители

#### 1. Обзор
- Интегральный усилитель с высокотехнологичной ручкой громкости (тактильный гибрид VER2), DDC + ЦАП (AK4191 + BD34302, с отдельным полным декодером MQA), усилителем для наушников и отдельными моно-выходами для сабвуфера (RCA и XLR). Есть две версии, полностью балансная и несимметричная; в обеих есть выходы для сабвуфера.
- Аналоговые версии (внешний линейный блок питания, классы A / AB / D, полупроводниковый / ламповый предусилитель) построены по тем же принципам.

#### 2. Переключатели (основной блок)
- SW1: связь I2S между DDC и ЦАП ВКЛ / ВЫКЛ (ВЫКЛ выводит I2S на внешний ЦАП). SW2: питание ЦАП + I2S ВКЛ / ВЫКЛ. SW3: питание беспроводной связи (Wi-Fi / Bluetooth) ВКЛ / ВЫКЛ.
- SW5: обход цифровой громкости / эквалайзера (бит-в-бит). SW6: ощущение щелчков ручки ВКЛ / ВЫКЛ. SW7: режим усиления АНАЛОГОВЫЙ / ЦИФРОВОЙ. SW8: автоматическое отключение звука колонок при подключении наушников ВКЛ / ВЫКЛ.

#### 3. Переключатели (схема сабвуфера)
- SW1: МОНО / СТЕРЕО. SW2: фаза 0 / 180°. SW3: ФНЧ BYPASS / 80 / 100 / 120 Гц. SW4: 12 дБ/окт или 24 дБ/окт (LR4). VR2: плавная фаза. SW9: разрыв земли контакта 1 XLR. K2: реле отключения звука на выходе (автоматическое).

#### 4. Разъёмы
- Входы: RCA / XLR (аналоговые), USB-C, I2S, LAN / Wi-Fi, Bluetooth. Выходы: колонки (bi-wiring HF / LF), PRE OUT (RCA + XLR), SUB OUT (моно RCA + XLR), наушники 3,5 мм (балансный и несимметричный), 4,4 мм (балансный), 6,35 мм (несимметричный), а также видеовыход HDMI / USB-C.

#### 5. Использование
- Громкость: вращайте ручку. При SW6 ВКЛ каждый щелчок равен 1 дБ, при ВЫКЛ ход плавный. SW7 выбирает АНАЛОГОВЫЙ режим (сохраняет бит-в-бит) или ЦИФРОВОЙ (цифровое усиление в FPGA). Оба действуют на колонки и наушники одновременно.
- Наушники: подключите к любому из трёх разъёмов (разъём 3,5 мм сам определяет TRRS = балансный и TRS = несимметричный). Ступени усиления: 0 / +6 / +12 / +18 дБ.
- Сабвуфер: соедините SUB OUT со входом сабвуфера, задайте частоту среза переключателем SW3 и с помощью SW4 и SW2 / VR2 добейтесь ровной суммы с основными колонками. Если основная колонка работает с 24 дБ/окт (LR4), поставьте SW4 на 24 дБ.

#### 6. Примечания
- Это справочные проекты. Номиналы деталей расчётные, моделирование ограничено расчётами на Python. Переходные процессы, искажения (THD), реальный шум и фаза, а также тактильные ощущения не проверялись; необходимо проверить стандарты безопасности и сертификацию.
- Сетевые трансформаторы — два независимых тороидальных (по одному на канал) с электростатическим экраном, экраном из мю-металла и блокиратором постоянного тока.
- Долговечность: крупные электролитические конденсаторы стоят во внешнем блоке питания (45 °C или ниже), выходные транзисторы класса AB удвоены параллельно, а у класса A есть вентилятор с температурным управлением. Релейный регулятор громкости служит около 55 лет при 500 операциях в день, лампа около 10 000 часов. Разъёмы наушников стоят на сменной подплате.
- Внешний линейный блок питания аналоговых версий содержит высокое напряжение (B+ 250 В) и большие токи. Обращайтесь осторожно.

## Files

- `streaming-amp/`, `analog-amp/`, `mono-sub-out/`, `manual/`: JPG and PDF (Japanese / English / German / Russian explanations inside).

---

## Versions / バージョン / Versionen / Версии
- [VER1](VER1) — first network streaming / analog / subwoofer schematics
- [VER2](VER2) — shorter wiring, virtual simulation, subwoofer VER2
- [VER3](VER3) — sound-quality review, haptic hybrid volume, LR4 subwoofer
- [VER4](VER4) — headphone amplifier (3.5 / 4.4 / 6.35 mm), ANALOG/DIGITAL gain
- [VER5](VER5) — latest (toroidal dual-mono transformers): 4-language (JA/EN/DE/RU) text in the figures, durability review, manual (`VER5/manual`)

Each VER folder contains `streaming-amp`, `analog-amp` and `mono-sub-out` (JPG + PDF).
Home page: https://audiocafe.tokyo/
