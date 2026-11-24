> Latest translations / 翻訳の最新版: [0-LATEST-TRANSLATIONS.md](0-LATEST-TRANSLATIONS.md)

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
- 音量: ノブを回します。SW6 が ON ならクリック 1 回 = 0.5 dB のクリック感、OFF なら 0.01 dB 刻みの滑らかさです(詳細は [VOLUME-STEP-SPEC.md](VOLUME-STEP-SPEC.md))。ゲイン調整は SW7 で ANALOG (ビットパーフェクトを保つ) か DIGITAL (FPGA のデジタルゲイン) を選びます。どちらも、スピーカーとヘッドホンに同時に効きます。
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
- Volume: turn the knob. With SW6 ON each click is 0.5 dB with a click feel; OFF is smooth in 0.01 dB steps (see [VOLUME-STEP-SPEC.md](VOLUME-STEP-SPEC.md)). SW7 selects the gain mode, ANALOG (keeps bit-perfect) or DIGITAL (digital gain in the FPGA). Both act on the speakers and the headphones at the same time.
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
- Lautstärke: Knopf drehen. Mit SW6 EIN hat jede Raste 0,5 dB mit Rastgefühl, AUS läuft der Knopf sanft in 0,01-dB-Schritten (siehe [VOLUME-STEP-SPEC.md](VOLUME-STEP-SPEC.md)). SW7 wählt ANALOG (bleibt Bit-perfekt) oder DIGITAL (digitale Verstärkung im FPGA). Beides wirkt gleichzeitig auf Lautsprecher und Kopfhörer.
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
- Громкость: вращайте ручку. При SW6 ВКЛ каждый щелчок равен 0,5 дБ, при ВЫКЛ ход плавный с шагом 0,01 дБ (см. [VOLUME-STEP-SPEC.md](VOLUME-STEP-SPEC.md)). SW7 выбирает АНАЛОГОВЫЙ режим (сохраняет бит-в-бит) или ЦИФРОВОЙ (цифровое усиление в FPGA). Оба действуют на колонки и наушники одновременно.
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
- [VER6](VER6) — shorter wiring (45 mm path, ground plane, 2 mm decoupling) and a more durable hybrid volume knob (VER5 + delta)
- Surround AV amplifier: see the new repository [open-av-amp](https://github.com/aon-co-jp/open-av-amp)
- [VER8](VER8) — VER7 plus the power input: 100-240 V auto-ranging, 50/60 Hz, device recognition over the power line at connection time only, 120 Hz only when both sides support it, optional 20 A connector (design proposal, 8-language explanation)
- [VER7](VER7) — quiet-to-practical volume for a 12-tatami room: Class A (9 W) and tube versions, Class A + AB version (automatic), improved analog Class D; manual in 8 languages (JA, EN-US, EN-UK, RU, UK, DE, IT, FR)
- [headphone/HP-VER2](headphone/HP-VER2) — headphone amplifier on the front panel of every integrated amplifier and the AV amplifier: 3.5 / 4.4 / 6.35 mm and XLR (stereo 4-pin plus two mono 3-pin), with gain adjustment; 8-language explanation in each figure
- [headphone/HP-VER3](headphone/HP-VER3) — gain control in 1 dB steps with three modes (ANALOG / DIGITAL / ANALOG + DIGITAL) and two independent controls, one for the speaker output and one for the headphone output; 8-language explanation in each figure
- [headphone/HP-VER4](headphone/HP-VER4) — volume plus two gains (low-frequency and high-frequency shelves) on both the speaker and the headphone outputs, each in 1 dB steps with three modes (ANALOG / DIGITAL / ANALOG + DIGITAL); 8-language explanation in each figure
- [classd-analog/CD-VER2](classd-analog/CD-VER2) — analog-input Class D amplifier with external linear DC supply, reviewed for durability, sound and shorter wiring (CD-VER1 = VER6 Class D figure)

Each VER folder contains `streaming-amp`, `analog-amp` and `mono-sub-out` (JPG + PDF).
Home page: https://audiocafe.tokyo/

## API 方針: REST 全廃・gRPC / Connect へ (2026-11-04)

### 日本語
- **REST は全廃する。新しい API は REST で作らない。** ブラウザや `curl` から呼ぶ API は **Connect の単純呼び出し**(`POST /<パッケージ>.<Service>/<Method>`、`content-type: application/json`、本文は JSON)、サービス間は **gRPC / gRPC-web**(RPoem の管理API `open_runo.admin.v1.Admin` と同じ流儀)。ストリーミングは、必要になってから。
- **既存の REST は、触るときに順に移す。** 移したら旧 REST の経路は消す。移行が終わるまで残るが、**新規には追加しない**。
- **JSON は RS-JSON に統一**する(読み込みは `from_str_secure` / `parse_secure` でサイズ・深さ・重複キーの上限つき、書き出しは `rust_json::fast`)。ブラウザの WASM に `prost` は入れない(サイズが増えるため)。
- **例外(自分たちの API ではなく、相手の規格が決めているもの)**: ACME、OAuth/OIDC のコールバック、第三者(GitHub など)からの Webhook、ヘルスチェック、静的ファイル配信、OTLP など。これらは規格どおりの HTTP を受ける。
- 参考実装: `RPoem`(`open_runo.admin.v1.Admin`)、`open-easy-web`(`server/src/connect.rs`、`proto/open_easy_web/admin/v1/admin.proto`)。
- ※ このリポジトリのコードが既に方針どおりかどうかは、各リポジトリの現状による。この節は方針の記録であり、コードの変更を意味しない。

### English
- **REST is being abolished. New APIs are not built as REST.** APIs called from browsers or `curl` use **Connect unary calls** (`POST /<package>.<Service>/<Method>`, `content-type: application/json`, JSON body); service-to-service calls use **gRPC / gRPC-web** (the same style as RPoem's admin API `open_runo.admin.v1.Admin`). Streaming only when it is actually needed.
- **Existing REST endpoints are migrated one by one, when they are touched.** The old REST route is removed once migrated. Until migration is finished they remain, but **no new ones are added**.
- **JSON is unified on RS-JSON**: reading with `from_str_secure` / `parse_secure` (size, depth and duplicate-key limits), writing with `rust_json::fast`. `prost` is not put into browser WASM (it would grow the binary).
- **Exceptions (shapes dictated by someone else's standard, not our own API)**: ACME, OAuth/OIDC callbacks, webhooks from third parties (e.g. GitHub), health checks, static file serving, OTLP, and so on. These accept plain HTTP as the standard requires.
- Reference implementations: `RPoem` (`open_runo.admin.v1.Admin`) and `open-easy-web` (`server/src/connect.rs`, `proto/open_easy_web/admin/v1/admin.proto`).
- Note: whether the code in a given repository already follows this policy depends on that repository. This section records the policy; it does not mean the code has been changed.

### Deutsch (KI-Übersetzung, redaktionell überarbeitet; noch nicht von Muttersprachlern geprüft)
- **REST wird vollständig abgeschafft; neue APIs entstehen nicht mehr als REST.** APIs, die aus dem Browser oder per `curl` aufgerufen werden, verwenden **unäre Connect-Aufrufe** (`POST /<Paket>.<Service>/<Methode>`, `content-type: application/json`, JSON-Body). Zwischen Diensten kommen **gRPC bzw. gRPC-web** zum Einsatz, im selben Stil wie die Admin-API von RPoem (`open_runo.admin.v1.Admin`). Streaming wird erst ergänzt, wenn es tatsächlich gebraucht wird.
- **Bestehende REST-Endpunkte werden schrittweise umgestellt, und zwar immer dann, wenn man ohnehin an ihnen arbeitet.** Sobald ein Endpunkt umgestellt ist, wird die alte REST-Route entfernt. Bis zum Abschluss der Migration bleiben die übrigen bestehen, es werden aber **keine neuen mehr hinzugefügt**.
- **JSON wird einheitlich über RS-JSON verarbeitet**: Gelesen wird mit `from_str_secure` bzw. `parse_secure` (mit Obergrenzen für Größe, Verschachtelungstiefe und doppelte Schlüssel), geschrieben mit `rust_json::fast`. `prost` wird nicht in das Browser-WASM aufgenommen, da es die Datei vergrößern würde.
- **Ausnahmen (Schnittstellen, deren Form ein fremder Standard vorgibt und die nicht zu unserer eigenen API gehören)**: ACME, OAuth/OIDC-Callbacks, Webhooks von Drittanbietern (z. B. GitHub), Health-Checks, die Auslieferung statischer Dateien, OTLP und Ähnliches. Diese nehmen, wie vom jeweiligen Standard verlangt, gewöhnliches HTTP entgegen.
- Referenzimplementierungen: `RPoem` (`open_runo.admin.v1.Admin`) und `open-easy-web` (`server/src/connect.rs`, `proto/open_easy_web/admin/v1/admin.proto`).
- Hinweis: Ob der Code eines einzelnen Repositorys diese Richtlinie bereits erfüllt, hängt vom jeweiligen Repository ab. Dieser Abschnitt dokumentiert lediglich die Richtlinie; er besagt nicht, dass der Code schon angepasst wurde.

### Русский (перевод выполнен с помощью ИИ и отредактирован; носителями языка пока не проверен)
- **От REST мы полностью отказываемся; новые API больше не создаются в стиле REST.** API, к которым обращаются из браузера или через `curl`, используют **унарные вызовы Connect** (`POST /<пакет>.<Service>/<Method>`, `content-type: application/json`, тело запроса — JSON). Для взаимодействия между сервисами применяются **gRPC и gRPC-web** — в том же стиле, что и административный API RPoem (`open_runo.admin.v1.Admin`). Потоковая передача данных добавляется лишь тогда, когда в ней действительно возникает необходимость.
- **Существующие REST-эндпоинты переводятся поэтапно — по мере того, как с ними приходится работать.** После перевода старый REST-маршрут удаляется. Пока миграция не завершена, оставшиеся эндпоинты сохраняются, но **новые не добавляются**.
- **Работа с JSON унифицирована на основе RS-JSON**: чтение — через `from_str_secure` или `parse_secure` (с ограничениями на размер, глубину вложенности и повторяющиеся ключи), запись — через `rust_json::fast`. `prost` в браузерный WASM не включается, поскольку это увеличило бы размер файла.
- **Исключения (интерфейсы, форму которых определяет чужой стандарт, а не наш собственный API)**: ACME, обратные вызовы OAuth/OIDC, вебхуки сторонних сервисов (например, GitHub), проверки работоспособности, раздача статических файлов, OTLP и тому подобное. Такие интерфейсы принимают обычный HTTP, как того требует соответствующий стандарт.
- Эталонные реализации: `RPoem` (`open_runo.admin.v1.Admin`) и `open-easy-web` (`server/src/connect.rs`, `proto/open_easy_web/admin/v1/admin.proto`).
- Примечание: соответствует ли код конкретного репозитория этой политике, зависит от самого репозитория. Данный раздел лишь фиксирует политику и не означает, что код уже изменён.

## API 方針の補足: 用語の整理と使い分け (2026-11-04)

### 日本語
**1つに統一するものではなく、別の層の話です。** 「REST の代わり」になるのは Connect・gRPC・GraphQL だけで、WASM は画面を作る技術です。

| 用語 | 何か | REST の代わりか |
|---|---|---|
| REST | URL と HTTP メソッドで操作を表す API の作り方 | 全廃する側 |
| **Connect** | `POST /サービス名/メソッド名` に JSON を送る形式。`curl` でもブラウザの `fetch` でも呼べる | はい(**採用**) |
| **gRPC** | 同じ「サービス/メソッド」の考え方を、バイナリ(protobuf)と HTTP/2 で行う形式。速く、ストリーミングも得意 | はい(**サービス同士に採用**) |
| gRPC-web | gRPC のブラウザ向けの変形版 | はい(必要なら) |
| GraphQL | 欲しい項目を問い合わせる形式 | 一部だけ(**問い合わせ(読み取り)専用**) |
| WASM | Rust をブラウザの中で動かす仕組み | いいえ(画面を作る技術) |

- **ブラウザの画面や `curl` から呼ぶ API は Connect**(POST、JSON を RS-JSON で読み書き)。ブラウザの WASM は素の gRPC を話せず、Connect なら `fetch` のままで、`prost` を足さずに済む(画面のサイズも増えない)。
- **サービス同士の通信(サーバー間、重い処理、ストリーミング)は gRPC。** 多くは Connect で足りるので、ストリーミングが必要になった所だけ gRPC に上げる。
- **GraphQL は、まとめて問い合わせたいときの読み取り専用。** 書き込み(操作)には使わない。
- **WASM は画面を作る技術として、そのまま使う。** 画面から呼ぶ API が Connect になっただけ。
- 外部の規格が形を決めるもの(ACME、OAuth のコールバック、第三者の Webhook、ヘルスチェック、静的ファイル、OTLP)は、規格どおりの HTTP のまま。
- **迷ったら Connect。**

### English
**These are not alternatives to unify; they sit at different layers.** Only Connect, gRPC and GraphQL can replace REST; WASM is a way to build the UI.

| Term | What it is | Replaces REST? |
|---|---|---|
| REST | API style that expresses operations through URLs and HTTP methods | The thing being abolished |
| **Connect** | `POST /Service/Method` with a JSON body; callable from `curl` and from a browser `fetch` | Yes (**adopted**) |
| **gRPC** | The same service/method idea over binary (protobuf) and HTTP/2; fast, good at streaming | Yes (**for service-to-service**) |
| gRPC-web | A browser-friendly variant of gRPC | Yes (if needed) |
| GraphQL | A query language: ask for exactly the fields you want | Partly (**read-only queries**) |
| WASM | Runs Rust inside the browser | No (a UI technology) |

- **APIs called from browser screens or `curl` use Connect** (POST, JSON read and written with RS-JSON). Browser WASM cannot speak plain gRPC; with Connect it stays a `fetch`, and `prost` is not needed (the binary does not grow).
- **Service-to-service calls (server to server, heavy work, streaming) use gRPC.** Connect is enough in most places; move a call to gRPC only where streaming is actually needed.
- **GraphQL is read-only**, for queries that gather several pieces of data. It is not used for writes (operations).
- **WASM stays as the way to build the UI.** The API it calls simply became Connect.
- Interfaces whose shape an outside standard dictates (ACME, OAuth callbacks, third-party webhooks, health checks, static files, OTLP) stay plain HTTP.
- **When in doubt, use Connect.**

### Deutsch (KI-Übersetzung, sprachlich überarbeitet; noch nicht von Muttersprachlern geprüft)
**Es geht nicht darum, eine einzige Technik auszuwählen – die Begriffe liegen auf unterschiedlichen Ebenen.** Als Ersatz für REST kommen nur Connect, gRPC und GraphQL in Frage; WASM dagegen ist eine Technik, mit der die Benutzeroberfläche gebaut wird.

| Begriff | Was ist das? | Ersatz für REST? |
|---|---|---|
| REST | Ein API-Stil, bei dem Operationen über URLs und HTTP-Methoden ausgedrückt werden | wird abgeschafft |
| **Connect** | `POST /Dienst/Methode` mit JSON im Body; aufrufbar mit `curl` ebenso wie mit `fetch` im Browser | ja (**gewählt**) |
| **gRPC** | Dasselbe Prinzip aus Dienst und Methode, aber über binäres protobuf und HTTP/2; schnell und gut für Streaming geeignet | ja (**zwischen Diensten**) |
| gRPC-web | Eine für den Browser angepasste Variante von gRPC | ja (bei Bedarf) |
| GraphQL | Abfragesprache, mit der man genau die benötigten Felder anfordert | teilweise (**nur für lesende Abfragen**) |
| WASM | Führt Rust-Code direkt im Browser aus | nein (Technik für die Oberfläche) |

- **APIs, die von Browseroberflächen oder per `curl` aufgerufen werden, verwenden Connect** (POST; JSON wird mit RS-JSON gelesen und geschrieben). WASM im Browser kann kein reines gRPC sprechen. Mit Connect bleibt es bei einem gewöhnlichen `fetch`, und `prost` ist nicht nötig – die WASM-Datei wird dadurch nicht größer.
- **Für die Kommunikation zwischen Diensten (Server zu Server, rechenintensive Aufgaben, Streaming) wird gRPC eingesetzt.** In den meisten Fällen reicht Connect aus; auf gRPC wird nur dort umgestellt, wo Streaming tatsächlich gebraucht wird.
- **GraphQL dient ausschließlich lesenden Abfragen**, wenn mehrere Informationen gebündelt abgefragt werden sollen. Für Schreibzugriffe (Operationen) wird es nicht verwendet.
- **WASM bleibt die Technik für die Oberfläche.** Geändert hat sich lediglich, dass die aufgerufene API nun auf Connect beruht.
- Schnittstellen, deren Form durch einen externen Standard festgelegt ist (ACME, OAuth-Callbacks, Webhooks von Drittanbietern, Health-Checks, statische Dateien, OTLP), bleiben gewöhnliches HTTP.
- **Im Zweifel: Connect.**

### Русский (перевод выполнен с помощью ИИ и литературно отредактирован; носителями языка пока не проверен)
**Это не варианты, из которых нужно выбрать один, а технологии разных уровней.** Заменить REST могут только Connect, gRPC и GraphQL; WASM же — это способ создания пользовательского интерфейса.

| Термин | Что это | Заменяет REST? |
|---|---|---|
| REST | Стиль построения API, при котором операции выражаются через URL и HTTP-методы | отменяется |
| **Connect** | `POST /Сервис/Метод` с телом в формате JSON; вызывается как из `curl`, так и из браузерного `fetch` | да (**выбран**) |
| **gRPC** | Тот же принцип «сервис — метод», но поверх двоичного формата protobuf и HTTP/2; работает быстро и хорошо подходит для потоковой передачи | да (**для связи между сервисами**) |
| gRPC-web | Адаптированный для браузера вариант gRPC | да (при необходимости) |
| GraphQL | Язык запросов: клиент запрашивает ровно те поля, которые ему нужны | частично (**только запросы на чтение**) |
| WASM | Позволяет выполнять код на Rust прямо в браузере | нет (технология для интерфейса) |

- **API, которые вызываются из браузерных интерфейсов или через `curl`, строятся на Connect** (POST; JSON читается и записывается через RS-JSON). Браузерный WASM не умеет работать с «чистым» gRPC. С Connect достаточно обычного `fetch`, а `prost` не требуется — размер WASM-файла не увеличивается.
- **Для обмена между сервисами (сервер — сервер, ресурсоёмкие задачи, потоковая передача) применяется gRPC.** В большинстве случаев достаточно Connect; на gRPC переходят только там, где потоковая передача действительно необходима.
- **GraphQL используется только для чтения**, когда нужно получить сразу несколько связанных данных. Для записи (операций) он не применяется.
- **WASM по-прежнему остаётся технологией для интерфейса.** Изменилось лишь то, что вызываемый им API теперь построен на Connect.
- Интерфейсы, форма которых задана внешним стандартом (ACME, обратные вызовы OAuth, вебхуки сторонних сервисов, проверки работоспособности, статические файлы, OTLP), остаются обычным HTTP.
- **Если есть сомнения — выбирайте Connect.**
