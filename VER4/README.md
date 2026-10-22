# VER4 — 説明 / Explanation

> 注 / Note: この版の図 (JPG/PDF) は当時の記録のままで、旧表記の「平衡」(現在は「バランス」) を含むことがあります。最新は VER5・VER6 です。 / The figures of this version are kept as originally made and may contain the old wording 平衡 (now written バランス). The newest are VER5 and VER6.

## ストリーミング / Streaming amplifier (`streaming-amp`)

## 日本語

### 最新ネットワーク対応プリメインアンプ(完全バランス版とアンバランス版)
Wi-Fi 8 (802.11bn) とLAN端子で音楽が聞け、最新のBluetoothにも対応し、ブラウザ対応でHDMIとUSB-Cで画像出力端子内蔵でU-NEXT・YouTube・Qobuzまで再生でき、USB-C / I2S入力でPCM最大32bit/1536kHz、DSD最大DSD1024に対応し、MQAにも対応する、最新のプリメインアンプを2種類設計しました。回路図は日本語と英語の併記で、PDFとJPGで掲載します。

### 共通の仕様
- ネットワーク: Wi-Fi 6E と有線LAN (GbE) 端子。ネットワーク・ストリーマで U-NEXT・YouTube・Qobuz・Roon・AirPlay・UPnP を再生します。
- デジタル入力: USB-C (UAC2) と I2S。PCM 最大 32bit/1536kHz、DSD 最大 DSD1024。
- DAC: AKM の AK4191 (デジタルフィルタ + ΔΣ変調器、PCM 最大 1536kHz・DSD 最大 DSD1024) と ROHM の BD34302 (32bit DAC、多ビットΔΣ入力) の組み合わせです。FPGA が I2C で BD34302 を設定し、1536kHz の PCM も DSD1024 も変換せずに扱います。この組み合わせの測定例 (参考ブログ) では THD 0.001% 未満、SNR ≈ 116dB (A 特性) 以上と報告されています。
- 無線 (最新規格): Wi-Fi 8 (IEEE 802.11bn) と Bluetooth 6.x (LE Audio / Auracast、LC3、LDAC、aptX Adaptive / aptX Lossless) に対応します。Bluetooth 入力は専用のモジュールで受け、I2S で FPGA に渡します。
- 音質改善回路・機能: (1) SW3 で Wi-Fi / Bluetooth の電源を遮断できます (無線を使わないときの RF ノイズ対策)。(2) 無線モジュールは金属シールドと専用の低ノイズ LDO で分離し、デジタルアイソレータで DAC 側と GND を分けます。(3) FPGA で再クロック (FIFO + 超低ジッタクロック) して、入力側のジッタを DAC に伝えません。(4) アンテナを分離し、Wi-Fi と Bluetooth の干渉を避けます。
- ボリューム (触覚ハイブリッド): 音量ノブは、LUXMAN L-570 や 真空管プリ L1000 のような「カチッ」というクリック感のある操作感と、クリック感のない滑らかな操作感を、SW6 のスイッチで好みに切り替えられます。ノブの軸に触覚モーターと磁気エンコーダ (MT6701 14bit) を付け、MCU (STM32G4) が位置に応じたトルクを 5kHz で出します。音声は電子ボリューム (MUSES72323 等) またはリレー式アッテネータで調整し、デジタル信号は通しません。すべてのプリメインアンプ (ネットワーク版・アナログ版・真空管プリ版) に搭載します (図7)。
- 音質改善 (VER3): デジタルのボリューム / EQ は SW5 でバイパスできます (ビットパーフェクト)。クロックは目標ジッタ 100fs 以下。Class AB は Cdom 68pF にして位相余裕を約 78.5° にしました (図8、いずれも計算)。
- ヘッドホンアンプ (VER4): 3.5mm (バランス・アンバランス兼用の4極ジャック、TRRS = バランス / TRS = アンバランスを自動検出)、4.4mm バランス、6.35mm アンバランスの3種類の出力を搭載します。スピーカーと同時に鳴らせ (スピーカーの自動ミュートは SW8 で ON / OFF)、通常の音楽をスピーカーで聞いても、イヤホン・ヘッドホンで聞いても同じ調整が両方に同時に効きます。ゲイン調整は2種類で、SW7 で ANALOG (ゲイン段・アッテネータ、ビットパーフェクト維持) と DIGITAL (FPGA のデジタルゲイン) を切り替えます。ヘッドホンアンプは OPA1612 のゲイン段 (0 / +6 / +12 / +18 dB) と LME49600 の電流バッファ (±0.5A/脚) で、出力インピーダンスは帰還後 約 0.1Ω、専用の LDO ±15V から動作します (図9)。
- 音質改善 (VER4): 出力インピーダンスを下げて周波数特性のずれを ±0.02dB にし (10Ω だと約 2dB)、ヘッドホンアンプの入力を 47kΩ にしてバスへの負荷を -0.01dB 以下にしました。最大出力はバランスで 32Ω に 4W、アンバランスで 2.3W (いずれも計算、図10)。
- 配線短縮 (再設計): 左右完全分離 (デュアルモノ) で、DAC を中央に置き、I/V → ボリューム → バッファ → パワーアンプ → 出力リレー → スピーカー端子 を左右へ一直線に並べます。1ch の信号経路は約 95mm (設計目標。従来の一般的な配置の約 1/3)。基板どうしはコネクタで直結して信号ケーブルをなくし、スピーカー端子はパワーアンプ基板の背面端に直付けします。各段の横に LDO と局所コンデンサを置き (ポイント・オブ・ロード)、デジタル・無線はシールドして遠ざけ、GND は 1 点で接続します。
- シミュレーション (TEST): Python による交流応答・直流動作点・設計計算で検証し、LPF の定数、Class D の出力フィルタ、Class A のバイアス、真空管の利得、外付け電源のトランス電圧の誤りを見つけて修正しました (図6)。実機測定と、SPICE での過渡応答・歪み・安定性の確認は未実施です。
- 映像出力: HDMI 出力と USB-C 出力 (DisplayPort Alt Mode) の画像出力端子を内蔵し、ブラウザ対応のストリーマ (Android 系 SoC) の画面をテレビやモニターに表示できます。USB-C 映像出力は、オーディオ入力用の USB-C とは別の端子です。
- USB-C: MUSICIAN Pisces III を参考にした DDC 回路 (USB→I2S 変換。STM32F446 + FPGA + 低ジッタの独自発振器) を内蔵しています。I2S の出力は RJ45 (I2S) と HDMI (I2S LVDS) の2系統で、ピン配列は複数の設定から切り替えられます (Pisces III では8種)。外部クロック (45.1584 / 49.152 MHz) の入力も備えます。DDC と内蔵 DAC は内部で I2S 接続されており (FPGA 経由)、この DDC + DAC の接続を SW1 で ON / OFF できます。ON: DDC の I2S を内部の FPGA を通して内蔵 DAC へ接続します。OFF: DDC を内蔵 DAC から切り離し、DDC の I2S を I2S OUT 端子から外部 DAC へ出力します (DDC として使用)。I2S 入力端子は、DDC が OFF のときや他の入力を選んだときに使えます。
- 動作モード (SW1 = DDC の ON/OFF、SW2 = DAC の ON/OFF): ① DDC ON + DAC ON (USB-C → DDC → DAC)。② DDC OFF + DAC ON (DAC だけ使う: I2S 入力や他のデジタル入力 → DAC)。③ DDC ON + DAC OFF (DDC だけ使う: I2S OUT から外部 DAC へ)。④ DDC OFF + DAC OFF (DDC も DAC も使わない: アナログ入力 XLR / RCA だけを使い、デジタル回路の電源を止めてデジタルノイズを避ける)。
- MQA: すべての版が MQA に対応します。AK4191 と BD34302 のチップ単体に MQA 機能があるという資料は見つからなかったため、MQA フルデコーダ (XMOS XU316 + MQA ファームウェア。同じ DAC を使う市販品も XU316 に MQA ファームウェアを載せた構成) を、DAC とは別に搭載します。MQA を検出すると、このデコーダで展開とレンダリングを行い、PCM を FPGA 経由で AK4191 + BD34302 に渡します。MQA 以外の信号と DSD はデコーダを通りません。DAC は1系統です。
- 出力: PRE OUT (RCA と XLR)、SUB OUT (モノラル、RCA と XLR)、バイワイヤリング対応のスピーカー端子 (L/R チャンネル各 HF・LF の2組、ジャンパー板つき)。
- 電源: アナログ・デジタル・ストリーマ・パワーアンプを別系統の低ノイズ電源にして、ノイズを分離します。

### 完全バランス版 (図1・図2)
- DAC を L 用・R 用に1個ずつモノ・モードで使い、Hot / Cold の電流出力をそれぞれ I/V 変換します。
- 差動 LPF、バランス電子ボリューム、バランスのラインバッファを通し、XLR (2=Hot, 3=Cold) に直接出力します。RCA は差動レシーバ (THAT1240) でシングルエンドに変換します。
- パワーアンプはバランス入力の Class-D (Eigentakt 型) です。最後までバランスのまま処理するので、ハム・ノイズ・グランドループに強い構成です。

### アンバランス版 (図3・図4)
- DAC は1個をステレオ・モードで使い、I/V 変換のあと、減算回路 (U2) で差動をシングルエンドにします。
- シングルエンドの LPF、ボリューム、バッファを通し、RCA に直接出力します。XLR が必要なときだけ THAT1646 でバランス化します (任意)。
- パワーアンプはシングルエンド入力です。部品が少なく安価ですが、バランス版よりハム・グランドループに弱いので、1点アースに注意が必要です。

### 注意
- BD34302 の資料は NDA 下で配布され、参考ブログでも「資料の記述に誤りがあり、回避策が必要だった」と報告されています。最初は動作しにくい可能性があるため、実機で信号と I2C 設定の確認が必要です。USB での 1536kHz / DSD1024 は専用の UAC2 ファームウェアと再生側の対応が必要です。
- MQA の利用には MQA 技術のライセンス (Lenbrook) と、MQA ファームウェアの供給元との契約が必要です。配信サービス (U-NEXT・YouTube・Qobuz) の音は、サービス側の仕様 (多くはロッシー、または 24bit/192kHz まで) に従います。
- Wi-Fi 8 (802.11bn) は規格策定中で、対応チップ・認証は製品化の時点で要確認です (Wi-Fi 7 / 6E との互換で選定します)。Bluetooth の LDAC・aptX は各ライセンスが必要です。
- U-NEXT・YouTube・Qobuz の再生には、各社の認証・契約 (Widevine、Google 認証、Qobuz Connect など) が必要です。配信の音質は各サービスの仕様に従い、ビットパーフェクトで出力できない場合があります。
- 2つとも参考設計です。部品値は机上で求めたもので、シミュレーションも実機測定も行っていません。製品化の前に、実機測定と各種認証・安全規格の確認が必要です。

## English

### Latest network-capable integrated amplifier (fully balanced and unbalanced versions)
I designed two versions of a latest integrated amplifier that plays music over Wi-Fi 8 (802.11bn) and a LAN port, also supports the latest Bluetooth, supports a web browser with built-in HDMI and USB-C video output terminals, can stream U-NEXT, YouTube and Qobuz, and accepts PCM up to 32 bit / 1536 kHz and DSD up to DSD1024 on its USB-C and I2S inputs, and also supports MQA. The circuit diagrams are in Japanese and English together and are published as PDF and JPG.

### Common specifications
- Network: Wi-Fi 6E and a wired LAN (GbE) port. A network streamer plays U-NEXT, YouTube, Qobuz, Roon, AirPlay and UPnP.
- Digital inputs: USB-C (UAC2) and I2S. PCM up to 32 bit / 1536 kHz and DSD up to DSD1024.
- DAC: the combination of AKM's AK4191 (digital filter and delta-sigma modulator, PCM up to 1536 kHz and DSD up to DSD1024) and ROHM's BD34302 (32-bit DAC with multi-bit delta-sigma input). An FPGA sets up the BD34302 over I2C, and both 1536 kHz PCM and DSD1024 are handled without conversion. A reference blog reports measurements of this combination with THD below 0.001% and A-weighted SNR of about 116 dB or more.
- Wireless (latest standards): Wi-Fi 8 (IEEE 802.11bn) and Bluetooth 6.x (LE Audio / Auracast, LC3, LDAC, aptX Adaptive / aptX Lossless) are supported. Bluetooth input is received by a dedicated module and passed to the FPGA over I2S.
- Sound-quality circuits and functions: (1) SW3 can cut the power of Wi-Fi and Bluetooth (RF noise countermeasure when wireless is not used). (2) The wireless modules are separated by a metal shield and a dedicated low-noise LDO, and a digital isolator separates the ground from the DAC side. (3) The FPGA reclocks the signal (FIFO + ultra-low-jitter clock) so input-side jitter does not reach the DAC. (4) The antennas are kept apart to avoid interference between Wi-Fi and Bluetooth.
- Volume (haptic hybrid): the volume knob can be switched with SW6 between a clicky feel, like the LUXMAN L-570 and the L1000 tube preamp, and a smooth feel with no clicks. A haptic motor and a magnetic encoder (MT6701, 14 bit) sit on the knob shaft, and an MCU (STM32G4) outputs a position-dependent torque at 5 kHz. The audio is adjusted by an electronic volume (MUSES72323 or similar) or a relay attenuator, so no digital signal passes through it. It is fitted to all integrated amplifiers (network, analog and tube-preamp versions) (Figure 7).
- Sound-quality improvements (VER3): the digital volume / EQ can be bypassed with SW5 (bit-perfect). The clock jitter target is 100 fs or less. The Class AB Cdom was changed to 68 pF, giving a phase margin of about 78.5 degrees (Figure 8, all calculated).
- Headphone amplifier (VER4): three outputs are fitted: 3.5 mm (a 4-pole jack for both balanced and unbalanced use, with TRRS = balanced and TRS = unbalanced detected automatically), 4.4 mm balanced and 6.35 mm unbalanced. It plays at the same time as the speakers (automatic speaker mute can be switched with SW8), so the same adjustments affect both the speakers and the headphones or earphones at once. There are two kinds of gain adjustment: SW7 switches between ANALOG (gain stage and attenuator, bit-perfect kept) and DIGITAL (digital gain in the FPGA). The amplifier uses an OPA1612 gain stage (0 / +6 / +12 / +18 dB) and LME49600 current buffers (+-0.5 A per leg), with an output impedance of about 0.1 ohm after feedback, and runs from dedicated +-15 V LDOs (Figure 9).
- Sound-quality improvements (VER4): the lower output impedance keeps the frequency response within +-0.02 dB (about 2 dB with 10 ohm), and the 47 kohm input of the headphone amplifier loads the bus by only -0.01 dB or less. The maximum power is 4 W into 32 ohm balanced and 2.3 W unbalanced (both calculated, Figure 10).
- Shorter wiring (redesign): the layout is fully left/right separated (dual mono), with the DAC in the centre and the I/V stage, volume, buffer, power amplifier, output relay and speaker terminals lined up straight to each side. The signal path of one channel is about 95 mm (a design target, roughly one third of a typical layout). Boards are joined directly by connectors so there are no signal cables, and the speaker terminals are mounted right at the rear edge of the power amplifier board. An LDO and a local capacitor sit next to each stage (point-of-load), the digital and wireless parts are shielded and kept away, and the grounds meet at a single point.
- Simulation (test): AC response, DC operating points and design arithmetic were checked in Python, and errors in the LPF values, the Class D output filter, the Class A bias, the tube gain and the external supply transformer voltages were found and fixed (Figure 6). Bench measurement and SPICE checks of transient response, distortion and stability have not been done.
- Video output: HDMI and USB-C (DisplayPort Alt Mode) video output terminals are built in, so the screen of the browser-capable streamer (Android-based SoC) can be shown on a TV or monitor. The USB-C video output is a separate port from the USB-C used for audio input.
- USB-C: A DDC circuit modeled on the MUSICIAN Pisces III (USB-to-I2S conversion with an STM32F446, an FPGA and low-jitter custom oscillators) is built in. The I2S output is available over RJ45 (I2S) and HDMI (I2S LVDS), and the pin assignment can be switched among several settings (eight on the Pisces III). An external clock input (45.1584 / 49.152 MHz) is provided too. The DDC and the built-in DAC are connected internally by I2S (through the FPGA), and this DDC + DAC link can be switched ON and OFF with SW1. ON: the I2S of the DDC is connected through the internal FPGA to the built-in DAC. OFF: the DDC is cut off from the built-in DAC and its I2S is sent from the I2S OUT terminal to an external DAC (used as a DDC). The I2S input terminal can be used while the DDC is OFF or when another input is selected.
- Operating modes (SW1 = DDC ON/OFF, SW2 = DAC ON/OFF): (1) DDC ON + DAC ON (USB-C to DDC to DAC). (2) DDC OFF + DAC ON (use only the DAC: I2S input or other digital inputs to the DAC). (3) DDC ON + DAC OFF (use only the DDC: from I2S OUT to an external DAC). (4) DDC OFF + DAC OFF (use neither the DDC nor the DAC: only the analog inputs XLR / RCA are used and the digital circuits are powered down to avoid digital noise).
- MQA: all versions support MQA. No document says that the AK4191 and BD34302 chips themselves have an MQA function, so a separate MQA full decoder (XMOS XU316 with MQA firmware; commercial products that use the same DAC are likewise built around an XU316 with MQA firmware) is fitted apart from the DAC. When MQA is detected, this decoder unfolds and renders it and passes the PCM through the FPGA to the AK4191 + BD34302. Non-MQA signals and DSD bypass the decoder. There is only one DAC.
- Outputs: PRE OUT (RCA and XLR), SUB OUT (mono, RCA and XLR) and bi-wire speaker terminals (two sets, HF and LF, per channel, with jumper bars).
- Power: the analog section, digital section, streamer and power amplifier have separate low-noise supplies to keep their noise apart.

### Fully balanced version (Figures 1 and 2)
- One DAC is used in mono mode for each of the L and R channels, and the Hot and Cold current outputs are each converted by an I/V stage.
- The signal passes through a differential low-pass filter, a balanced electronic volume control and a balanced line buffer, and goes directly to the XLR outputs (2 = Hot, 3 = Cold). The RCA outputs are made by a differential receiver (THAT1240) that converts to single-ended.
- The power amplifier is a Class-D (Eigentakt-type) with balanced input. The signal stays balanced all the way, so it is strong against hum, noise and ground loops.

### Unbalanced version (Figures 3 and 4)
- One DAC is used in stereo mode; after I/V conversion a subtractor (U2) turns the differential signal into single-ended.
- The signal passes through a single-ended low-pass filter, volume control and buffer, and goes directly to the RCA outputs. The XLR outputs, balanced with a THAT1646, are needed only when you want them (optional).
- The power amplifier has a single-ended input. It has fewer parts and is cheaper, but it is more prone to hum and ground loops than the balanced version, so take care with single-point grounding.

### Notes
- The BD34302 documentation is distributed under NDA, and the reference blog reports that its descriptions had errors that needed workarounds. It may not work at first, so the signals and the I2C settings must be checked on a real board. 1536 kHz / DSD1024 over USB needs dedicated UAC2 firmware and support on the playback side.
- Using MQA requires a license for MQA technology (Lenbrook). The sound of the streaming services (U-NEXT, YouTube, Qobuz) follows each service's specification (mostly lossy, or up to 24 bit / 192 kHz).
- Wi-Fi 8 (802.11bn) is still being standardized, so compatible chips and certification must be checked at the time of productization (choose parts compatible with Wi-Fi 7 / 6E). LDAC and aptX on Bluetooth each need a license.
- Playing U-NEXT, YouTube and Qobuz requires each company's certification and contract (Widevine, Google certification, Qobuz Connect and so on). The sound quality follows each service's specification, and bit-perfect output may not be possible.
- Both are reference designs. The component values were only worked out on paper; no simulation or bench measurement has been done. Bench measurement and the necessary certifications and safety standards must be checked before turning them into a product.

### 図 / Figures
- 図9 / Figure 9: ヘッドホンアンプ (VER4) / Headphone amplifier — `amp_hp.jpg`
- 図10 / Figure 10: VER4 のシミュレーション / VER4 simulation — `amp_ver4_sim.jpg`
- 図7 / Figure 7: ボリューム 触覚ハイブリッド / Haptic hybrid volume knob — `amp_volume_haptic.jpg`
- 図8 / Figure 8: 音質改善 VER3 のシミュレーション / VER3 sound-quality simulation — `amp_ver3_sim.jpg`
- 図5 / Figure 5: 筐体内レイアウト(配線最短) / Internal layout for the shortest wiring — `amp_layout_net.jpg`
- 図6 / Figure 6: シミュレーション結果 / Simulation results — `amp_test.jpg`
- 図1 / Figure 1: 完全バランス版 ブロック図 / Fully balanced - block diagram — `streaming_amp_block.jpg`
- 図2 / Figure 2: 完全バランス版 アナログ信号経路 / Fully balanced - analog path — `streaming_amp_analog.jpg`
- 図3 / Figure 3: アンバランス版 ブロック図 / Unbalanced - block diagram — `streaming_amp_block_unbalanced.jpg`
- 図4 / Figure 4: アンバランス版 アナログ信号経路 / Unbalanced - analog path — `streaming_amp_analog_unbalanced.jpg`

## アナログ / Analog amplifier (`analog-amp`)

## 日本語

### アナログ版 最新プリメインアンプ
外付けリニアDC電源で動かす、アナログのプリメインアンプを設計しました。パワーアンプは Class A・Class AB・Class D の3種、プリアンプは半導体と真空管の2種で、組み合わせた6通りで使えます。PRE OUT と SUB OUT (どちらも RCA と XLR) を備え、スピーカー端子はバイワイヤリングに対応します。回路図は日本語と英語の併記です。
- 外付けリニアDC電源: トロイダルトランス → 整流・大容量コンデンサ → リニアレギュレータ。パワー段 (Class A ±24V / Class AB ±45V / Class D +60V)、アナログ ±15V、真空管プリ用の B+ 250V とヒーター 6.3V DC を出力します。
- Class A: MOSFET の共通ソース + 電流サーボ付きの定電流源負荷。アイドル電流 ≈ 2.3A/ch (Vset ÷ R7)、出力 ≈ 20W / 8Ω。
- Class AB: 差動入力段 + VAS + Vbe 倍率バイアス + エミッタフォロワ出力。出力 ≈ 100W / 8Ω。
- Class D: アナログ入力の積分器 + PWM 比較器 + ハーフブリッジ (BTL)。出力 ≈ 150W / 8Ω。
- プリ: 半導体 (OPA1612 のライン段) または真空管 (1本の 12AU7 の双3極管: 片側で電圧増幅、残り半分でカソードフォロワ)。
- 配線短縮 (再設計): 左右完全分離で、入力選択/ボリュームを中央に置き、プリ段 → ラインバッファ → パワーアンプ → 出力リレー → スピーカー端子 を左右へ一直線に並べます (1ch ≈ 95mm、設計目標)。信号ケーブルをなくして基板どうしをコネクタで直結し、各段の横に LDO と局所コンデンサを置きます (図8)。
- シミュレーション (TEST): Python による計算で、LPF の定数・Class D のフィルタ・Class A のバイアス・真空管の利得・外付け電源のトランス電圧を修正しました (図9)。実機測定と SPICE での過渡応答・歪み・安定性は未実施です。
- ボリューム (触覚ハイブリッド): 音量ノブは、LUXMAN L-570 や 真空管プリ L1000 のような「カチッ」というクリック感のある操作感と、クリック感のない滑らかな操作感を、SW6 のスイッチで好みに切り替えられます。ノブの軸に触覚モーターと磁気エンコーダ (MT6701 14bit) を付け、MCU (STM32G4) が位置に応じたトルクを 5kHz で出します。音声は電子ボリューム (MUSES72323 等) またはリレー式アッテネータで調整し、デジタル信号は通しません。すべてのプリメインアンプ (ネットワーク版・アナログ版・真空管プリ版) に搭載します (図10)。
- 音質改善 (VER3): デジタルのボリューム / EQ は SW5 でバイパスできます (ビットパーフェクト)。クロックは目標ジッタ 100fs 以下。Class AB は Cdom 68pF にして位相余裕を約 78.5° にしました (図11、いずれも計算)。
- ヘッドホンアンプ (VER4): 3.5mm (バランス・アンバランス兼用の4極ジャック、TRRS = バランス / TRS = アンバランスを自動検出)、4.4mm バランス、6.35mm アンバランスの3種類の出力を搭載します。スピーカーと同時に鳴らせ (スピーカーの自動ミュートは SW8 で ON / OFF)、通常の音楽をスピーカーで聞いても、イヤホン・ヘッドホンで聞いても同じ調整が両方に同時に効きます。ゲイン調整は2種類で、SW7 で ANALOG (ゲイン段・アッテネータ、ビットパーフェクト維持) と DIGITAL (FPGA のデジタルゲイン) を切り替えます。ヘッドホンアンプは OPA1612 のゲイン段 (0 / +6 / +12 / +18 dB) と LME49600 の電流バッファ (±0.5A/脚) で、出力インピーダンスは帰還後 約 0.1Ω、専用の LDO ±15V から動作します (図12)。
- 音質改善 (VER4): 出力インピーダンスを下げて周波数特性のずれを ±0.02dB にし (10Ω だと約 2dB)、ヘッドホンアンプの入力を 47kΩ にしてバスへの負荷を -0.01dB 以下にしました。最大出力はバランスで 32Ω に 4W、アンバランスで 2.3W (いずれも計算、図13)。
- MQA: MQA はデジタルの機能のため、このアナログ版は、MQA 対応 DAC (ネットワーク対応プリメインアンプの DAC 部) のアナログ出力を入力に接続して使います。
- 共通の注意: どれも参考設計です。部品値は机上計算で、シミュレーションも実機測定もしていません。高電圧 (B+ 250V) と大電流を扱うため、製品化の前に実機測定と安全規格・認証の確認が必要です。

## English

### Analog version of the latest integrated amplifier
I designed an analog integrated amplifier that runs from an external linear DC power supply. There are three power amplifiers (Class A, Class AB and Class D) and two preamplifiers (solid-state and vacuum-tube), which can be combined in six ways. It has PRE OUT and SUB OUT (both RCA and XLR) and bi-wire speaker terminals. The circuit diagrams are in Japanese and English together.
- External linear DC supply: toroidal transformer, rectifier and large capacitors, then linear regulators. It outputs the power-stage rails (Class A ±24 V, Class AB ±45 V, Class D +60 V), analog ±15 V, and B+ 250 V and 6.3 V DC heaters for the tube preamp.
- Class A: common-source MOSFET with a constant-current-source load controlled by a current servo. Idle current about 2.3 A per channel (Vset / R7), output about 20 W into 8 ohm.
- Class AB: differential input stage, VAS, Vbe-multiplier bias and emitter-follower outputs. Output about 100 W into 8 ohm.
- Class D: analog-input integrator, PWM comparator and half-bridge (BTL). Output about 150 W into 8 ohm.
- Preamp: solid-state (OPA1612 line stage) or vacuum-tube (one 12AU7 dual triode: one half for voltage gain, the other half as a cathode follower).
- Shorter wiring (redesign): the layout is fully left/right separated, with input selection and volume in the centre and the preamp stage, line buffer, power amplifier, output relay and speaker terminals lined up straight to each side (about 95 mm per channel, a design target). Signal cables are eliminated, boards are joined directly by connectors, and an LDO and a local capacitor sit next to each stage (Figure 8).
- Simulation (test): calculations in Python fixed the LPF values, the Class D filter, the Class A bias, the tube gain and the external supply transformer voltages (Figure 9). Bench measurement and SPICE checks of transient response, distortion and stability have not been done.
- Volume (haptic hybrid): the volume knob can be switched with SW6 between a clicky feel, like the LUXMAN L-570 and the L1000 tube preamp, and a smooth feel with no clicks. A haptic motor and a magnetic encoder (MT6701, 14 bit) sit on the knob shaft, and an MCU (STM32G4) outputs a position-dependent torque at 5 kHz. The audio is adjusted by an electronic volume (MUSES72323 or similar) or a relay attenuator, so no digital signal passes through it. It is fitted to all integrated amplifiers (network, analog and tube-preamp versions) (Figure 10).
- Sound-quality improvements (VER3): the digital volume / EQ can be bypassed with SW5 (bit-perfect). The clock jitter target is 100 fs or less. The Class AB Cdom was changed to 68 pF, giving a phase margin of about 78.5 degrees (Figure 11, all calculated).
- Headphone amplifier (VER4): three outputs are fitted: 3.5 mm (a 4-pole jack for both balanced and unbalanced use, with TRRS = balanced and TRS = unbalanced detected automatically), 4.4 mm balanced and 6.35 mm unbalanced. It plays at the same time as the speakers (automatic speaker mute can be switched with SW8), so the same adjustments affect both the speakers and the headphones or earphones at once. There are two kinds of gain adjustment: SW7 switches between ANALOG (gain stage and attenuator, bit-perfect kept) and DIGITAL (digital gain in the FPGA). The amplifier uses an OPA1612 gain stage (0 / +6 / +12 / +18 dB) and LME49600 current buffers (+-0.5 A per leg), with an output impedance of about 0.1 ohm after feedback, and runs from dedicated +-15 V LDOs (Figure 12).
- Sound-quality improvements (VER4): the lower output impedance keeps the frequency response within +-0.02 dB (about 2 dB with 10 ohm), and the 47 kohm input of the headphone amplifier loads the bus by only -0.01 dB or less. The maximum power is 4 W into 32 ohm balanced and 2.3 W unbalanced (both calculated, Figure 13).
- MQA: MQA is a digital function, so this analog version is used by connecting the analog output of an MQA-capable DAC (the DAC section of the network integrated amplifier) to its input.
- Common notes: all are reference designs. The component values were only worked out on paper; no simulation or bench measurement has been done. Because high voltage (B+ 250 V) and high current are involved, bench measurement and safety standards and certification must be checked before turning them into a product.

### 図 / Figures
- 図1 / Figure 1: 外付けリニアDC電源 / External linear DC supply — `amp_psu.jpg`
  - 外付けリニアDC電源: ACを EMI フィルタとトロイダルトランスに通し、パワーレール・アナログ ±15V・B+ 250V・ヒーター 6.3V DC をそれぞれ別の巻線と別のレギュレータで作ります。出力は多ピンの太いケーブルで本体へ送り、センス線で電圧降下を補償します。B+ はヒーターが温まってから遅延投入します。
  - External linear DC supply: the AC goes through an EMI filter and a toroidal transformer, and the power rails, analog ±15 V, B+ 250 V and 6.3 V DC heaters are each made from separate windings and regulators. The output goes to the main unit over a thick multi-pin cable, and sense wires compensate for voltage drop. B+ is switched on after the heaters have warmed up.
- 図2 / Figure 2: 半導体プリ版 ブロック図 / Solid-state preamp - block diagram — `amp_block_solid.jpg`
  - 半導体プリ版: アナログ入力 → 入力セレクタ → 半導体プリ (OPA1612) → ボリューム → パワーアンプ (Class A / AB / D のどれか1つ) → DC保護 → バイワイヤ対応スピーカー端子。PRE OUT と SUB OUT は RCA と XLR の両方。パワーアンプは交換式で、入出力と筐体は共通です。
  - Solid-state preamp version: analog inputs, input selector, solid-state preamp (OPA1612), volume, power amplifier (one of Class A / AB / D), DC protection and bi-wire speaker terminals. PRE OUT and SUB OUT have both RCA and XLR. The power amplifier is a swappable module and the inputs, outputs and chassis are common.
- 図3 / Figure 3: 真空管プリ版 ブロック図 / Vacuum-tube preamp - block diagram — `amp_block_tube.jpg`
  - 真空管プリ版: プリを真空管 (12AX7 の電圧増幅 + 12AU7 のカソードフォロワ) に替えた構成です。B+ 250V と ヒーター 6.3V DC は外付けリニアDC電源から供給し、B+ は遅延投入します。パワーアンプ以降は図2と同じです。
  - Vacuum-tube preamp version: the preamp is a tube stage (a 12AX7 for voltage gain and a 12AU7 cathode follower). B+ 250 V and 6.3 V DC heaters come from the external linear DC supply, and B+ is switched on after a delay. From the power amplifier onward it is the same as Figure 2.
- 図4 / Figure 4: 真空管プリアンプ回路 / Vacuum-tube preamplifier stage — `amp_tube_pre.jpg`
  - 真空管プリ: 入力セレクタ → ボリューム (50kΩ) → 1本の 12AU7 の V1 (電圧増幅、プレート負荷 47kΩ、カソード 1kΩ バイパスなし、利得 ≈ 11倍) → 0.1µF で結合 → V2 (残り半分、カソードフォロワ、出力 ≈ 1.4kΩ) → 2.2µF + 100Ω → パワーアンプへ。B+ は Rd 4.7kΩ と 47µF でデカップリングします。
  - Vacuum-tube preamp: input selector, volume (50 kohm), V1 of one 12AU7 (voltage gain, 47 kohm plate load, 1 kohm unbypassed cathode resistor, gain about 11x), 0.1 uF coupling, V2 (the other half, cathode follower, output about 1.4 kohm), then 2.2 uF and 100 ohm to the power amplifier. B+ is decoupled by Rd 4.7 kohm and 47 uF.
- 図5 / Figure 5: Class A パワーアンプ / Class A power amplifier — `amp_classA.jpg`
  - Class A: Nch MOSFET Q1 の共通ソース段を、Pch MOSFET Q2 の定電流源が負荷になります。電流は電流制御アンプ U3 が R7 0.62Ω の両端電圧を Vset (VR1) と比べて決め、約 2.3A (Vset ÷ R7) に保ちます (MOSFET の Vgs のばらつきに左右されない)。U1 (OPA1612) で駆動し、出力から全体帰還 (利得 ≈22)、DC サーボで出力のオフセットを除きます。出力 ≈ 20W / 8Ω、発熱 ≈ 120W/ch。出力は L1 // 10Ω・ゾベル・DC保護リレーを通してバイワイヤ端子へ。
  - Class A: the common-source stage of the N-channel MOSFET Q1 is loaded by a constant current source made from the P-channel MOSFET Q2 (the current is set by the control amplifier U3, which compares the voltage across R7 0.62 ohm with Vset from VR1 and holds about 2.3 A, independent of the MOSFET Vgs spread). It is driven by U1 (OPA1612) with global feedback from the output (gain about 22), and a DC servo removes output offset. Output about 20 W into 8 ohm, dissipation about 120 W per channel. The output goes through L1 // 10 ohm, a Zobel network and a DC-protection relay to the bi-wire terminals.
- 図6 / Figure 6: Class AB パワーアンプ / Class AB power amplifier — `amp_classAB.jpg`
  - Class AB: 差動入力段 (カレントミラー付き) → VAS Q3 (Cdom 68pF) → Vbe 倍率バイアス Q4 (出力段ヒートシンクに取り付け) → ドライバ Q5/Q6 → 出力 Q7/Q8 (2SC5200 / 2SA1943、エミッタ抵抗 0.33Ω)。出力から Rf 22k / Rg 1k で全体帰還。出力 ≈ 100W / 8Ω (±45V)、アイドル電流 ≈ 50mA/組。
  - Class AB: differential input stage (with a current mirror), VAS Q3 (Cdom 68 pF), Vbe-multiplier bias Q4 (mounted on the output heatsink), drivers Q5/Q6 and output transistors Q7/Q8 (2SC5200 / 2SA1943 with 0.33 ohm emitter resistors). Global feedback from the output with Rf 22k / Rg 1k. Output about 100 W into 8 ohm (±45 V), idle current about 50 mA per pair.
- 図7 / Figure 7: Class D パワーアンプ / Class D power amplifier — `amp_classD.jpg`
  - Class D (アナログ入力): 入力 → 積分器 U1 → コンパレータ U2 (三角波 ≈ 500kHz と比較して PWM) → ゲートドライバ (デッドタイム) → ハーフブリッジ Q1/Q2 → LC フィルタ (L2 22µH / C2 0.47µF、BTL 8Ω で Q ≈ 0.58) → DC保護リレー → バイワイヤ端子。フィルタ出力から全体帰還し、BTL では反転 PWM の 2組目で OUT− を作ります。保護は過電流・過熱・DC検出でミュート。
  - Class D (analog input): input, integrator U1, comparator U2 (compares with a triangle wave of about 500 kHz to make PWM), gate driver (dead time), half-bridge Q1/Q2, LC filter (L2 22 uH / C2 0.47 uF, Q about 0.58 at BTL 8 ohm), DC-protection relay and bi-wire terminals. Global feedback is taken from the filter output, and in BTL a second set driven by the inverted PWM makes OUT-. Protection mutes on overcurrent, overheating or DC detection.
- 図8 / Figure 8: 筐体内レイアウト(配線最短・アナログ版) / Internal layout for the shortest wiring - analog version — `amp_layout_analog.jpg`
  - 筐体内レイアウト: 入力セレクタとボリューム (デュアルモノ) を中央に置き、プリ段 → ラインバッファ → パワーアンプ → 出力リレー → スピーカー端子 を左右へ一直線に並べます。1ch の信号経路は約 95mm (設計目標)。基板どうしはコネクタ直結、各段の横に LDO と局所コンデンサ、GND は 1 点アース。外付け電源なので本体にトランスはありません。
  - Internal layout: the input selector and volume (dual mono) sit in the centre, and the preamp stage, line buffer, power amplifier, output relay and speaker terminals line up straight to each side. The signal path is about 95 mm per channel (a design target). Boards are joined by connectors, an LDO and a local capacitor sit next to each stage, and the grounds meet at one point. The transformer is in the external supply, not in the main unit.
- 図9 / Figure 9: シミュレーション結果 / Simulation results — `amp_test.jpg`
  - シミュレーション (Python の計算): LPF の -3dB 周波数、Class D 出力フィルタの特性、Class A のバイアス電流、真空管の動作点と利得、外付け電源のトランス電圧を検証し、誤りを修正しました。ほかに問題がなかった項目と、まだ確認できていない項目も表にまとめています。
  - Simulation (calculations in Python): the -3 dB points of the LPF, the Class D output filter response, the Class A bias current, the tube operating points and gain, and the transformer voltages of the external supply were checked and the errors fixed. The table also lists what showed no problem and what has still not been checked.
- 図10 / Figure 10: ボリューム 触覚ハイブリッド / Haptic hybrid volume knob — `amp_volume_haptic.jpg`
  - ボリューム: ノブの軸に触覚モーターと磁気エンコーダを付け、SW6 でクリック感あり (LUXMAN L-570 や真空管プリ L1000 のような「カチッ」) と、なし (滑らか) を切り替えます。クリック 1 回は 270°÷80 段 ≈ 3.4°、ピークトルク ≈ 6mN·m、エネルギー ≈ 0.11mJ (計算)。音声は電子 / リレー式アッテネータで調整します。
  - Volume: a haptic motor and a magnetic encoder sit on the knob shaft, and SW6 selects a clicky feel (like the LUXMAN L-570 and the L1000 tube preamp) or a smooth feel. One click is 270 deg / 80 steps = about 3.4 deg, with a peak torque of about 6 mN-m and about 0.11 mJ per click (calculated). The audio is adjusted by an electronic or relay attenuator.
- 図11 / Figure 11: 音質改善 VER3 のシミュレーション / VER3 sound-quality simulation — `amp_ver3_sim.jpg`
  - 音質改善 VER3 の計算: クロックジッタ 100fs で SNR 限界 158dB、デジタル減衰で失うビット (アナログ ATT 主体・SW5 でデジタルをバイパス)、Class AB の Cdom 33pF → 68pF で位相余裕 66.6° → 78.5°、触覚ボリュームのトルク。
  - VER3 calculations: the SNR limit of 158 dB at 100 fs clock jitter, the bits lost by digital attenuation (analog attenuator first, digital bypass with SW5), the Class AB phase margin from 66.6 to 78.5 degrees with Cdom 33 -> 68 pF, and the haptic volume torque.
- 図12 / Figure 12: ヘッドホンアンプ (VER4) / Headphone amplifier — `amp_hp.jpg`
  - ヘッドホンアンプ: バス (ラインバッファ出力) から分岐し、アナログゲイン段 (0 / +6 / +12 / +18 dB) → 電流バッファ (LME49600) → 出力リレー → 3.5mm バランス/アンバランス兼用・4.4mm バランス・6.35mm アンバランスの3つのジャック。ジャック検出で自動切替し、TRS を挿すと Cold を切り離します。スピーカーと同時に動作し、ゲインは SW7 で ANALOG / DIGITAL の2種類。
  - Headphone amplifier: taken from the bus (line-buffer output), it goes through the analog gain stage (0 / +6 / +12 / +18 dB), the current buffers (LME49600) and the output relays to three jacks: 3.5 mm balanced/unbalanced, 4.4 mm balanced and 6.35 mm unbalanced. Jack detection switches automatically and a TRS plug disconnects the Cold side. It plays with the speakers, and SW7 selects ANALOG or DIGITAL gain.
- 図13 / Figure 13: VER4 のシミュレーション / VER4 simulation — `amp_ver4_sim.jpg`
  - ヘッドホンアンプの計算: 出力インピーダンスによる周波数特性のずれ (0.1Ω で ±0.02dB、10Ω で約 2dB)、最大出力 (バランス 32Ω で 4W、アンバランス 2.3W)、ゲイン段の雑音 (+18dB でも約 3µV)、2種類のゲイン調整の違い (デジタルは -40dB で 24bit が 17.4bit)。
  - Headphone amplifier calculations: the response error caused by output impedance (+-0.02 dB at 0.1 ohm, about 2 dB at 10 ohm), maximum power (4 W balanced into 32 ohm, 2.3 W unbalanced), gain-stage noise (about 3 uV even at +18 dB) and the difference between the two gain modes (digital: -40 dB turns 24 bit into 17.4 bit).

## まとめ / Summary

### まとめ(日本語)
完全バランス用とアンバランス用の回路図を2つとも作り、日本語と英語の説明をそれぞれ付けて、5ページのPDFにまとめました。ホームページ(audiocafe.tokyo のトップページ)にも掲載しました。

### PDFの構成
- 1〜3ページ目は本文です。URL、英語のPMA-2000RE説明と英語本文、日本語のPMA-2000RE説明と日本語本文の順です。
- 4ページ目は完全バランス設計のアンプ用の回路図で、下に日本語、英語の順で説明を付けています。
- 5ページ目はもともとアンバランス設計のアンプ用の回路図で、下に日本語、英語の説明と共通の注意を付けています。
- 回路図の文字は、どちらも日本語と英語の併記です。

### 2つの回路図の違い
- 加算: 完全バランス用は Hot側とCold側を別々に2系統で加算 / アンバランス用は反転加算1系統
- 位相: 完全バランス用は DPDTで HotとColdを入れ替え / アンバランス用は SPDTで直結(180°)か反転段経由(0°)かを選択
- LPF: 完全バランス用は HotとColdに同じ値で2系統 / アンバランス用は 1系統
- 出力: 完全バランス用は XLRはバッファ経由、RCAは差動レシーバ(THAT1240)で変換 / アンバランス用は RCAはDCカット(4.7µF)と100Ω経由、XLRは任意でTHAT1646でバランス化

どちらも参考設計です。部品値は机上で求めたもので、シミュレーションも実機測定もしていないため、製品化の前に必ず検証してください。

### Summary (English)
I made both circuit diagrams, one for an amplifier that is fully balanced by design and one for an amplifier that was originally unbalanced, added a Japanese and an English explanation to each, and put them together in a 5-page PDF. They are also posted on the top page of audiocafe.tokyo.

### Structure of the PDF
- Pages 1-3 are the text, in this order: the URL, the English PMA-2000RE explanation and English body, then the Japanese PMA-2000RE explanation and Japanese body.
- Page 4 is the circuit diagram for a fully balanced amplifier, with the Japanese explanation followed by the English one below it.
- Page 5 is the circuit diagram for an originally unbalanced amplifier, with the Japanese and English explanations and the common notes below it.
- The text in both diagrams is in English and Japanese together.

### Differences between the two diagrams
- Summing: the fully balanced version sums the Hot side and the Cold side separately in two paths / the unbalanced version uses one inverting summer.
- Phase: the fully balanced version swaps Hot and Cold with a DPDT switch / the unbalanced version selects the direct output (180°) or the inverting stage (0°) with an SPDT switch.
- Low-pass filter: the fully balanced version uses two paths with identical values for Hot and Cold / the unbalanced version uses one path.
- Output: in the fully balanced version the XLR goes through buffers and the RCA is converted by a differential receiver (THAT1240) / in the unbalanced version the RCA goes through a DC-blocking capacitor (4.7 µF) and 100 Ω, and the XLR is optionally balanced with a THAT1646.

Both are reference designs. The component values were only worked out on paper and no simulation or bench measurement has been done, so be sure to verify them before turning them into a product.
