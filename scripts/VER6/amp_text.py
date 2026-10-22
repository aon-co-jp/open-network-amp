AMP_JA = """#最新ネットワーク対応プリメインアンプ(完全バランス版とアンバランス版)
Wi-Fi 8 (802.11bn) とLAN端子で音楽が聞け、最新のBluetoothにも対応し、ブラウザ対応でHDMIとUSB-Cで画像出力端子内蔵でU-NEXT・YouTube・Qobuzまで再生でき、USB-C / I2S入力でPCM最大32bit/1536kHz、DSD最大DSD1024に対応し、MQAにも対応する、最新のプリメインアンプを2種類設計しました。回路図は日本語と英語の併記で、PDFとJPGで掲載します。

#共通の仕様
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

#完全バランス版 (図1・図2)
- DAC を L 用・R 用に1個ずつモノ・モードで使い、Hot / Cold の電流出力をそれぞれ I/V 変換します。
- 差動 LPF、バランス電子ボリューム、バランスのラインバッファを通し、XLR (2=Hot, 3=Cold) に直接出力します。RCA は差動レシーバ (THAT1240) でシングルエンドに変換します。
- パワーアンプはバランス入力の Class-D (Eigentakt 型) です。最後までバランスのまま処理するので、ハム・ノイズ・グランドループに強い構成です。

#アンバランス版 (図3・図4)
- DAC は1個をステレオ・モードで使い、I/V 変換のあと、減算回路 (U2) で差動をシングルエンドにします。
- シングルエンドの LPF、ボリューム、バッファを通し、RCA に直接出力します。XLR が必要なときだけ THAT1646 でバランス化します (任意)。
- パワーアンプはシングルエンド入力です。部品が少なく安価ですが、バランス版よりハム・グランドループに弱いので、1点アースに注意が必要です。

#注意
- BD34302 の資料は NDA 下で配布され、参考ブログでも「資料の記述に誤りがあり、回避策が必要だった」と報告されています。最初は動作しにくい可能性があるため、実機で信号と I2C 設定の確認が必要です。USB での 1536kHz / DSD1024 は専用の UAC2 ファームウェアと再生側の対応が必要です。
- MQA の利用には MQA 技術のライセンス (Lenbrook) と、MQA ファームウェアの供給元との契約が必要です。配信サービス (U-NEXT・YouTube・Qobuz) の音は、サービス側の仕様 (多くはロッシー、または 24bit/192kHz まで) に従います。
- Wi-Fi 8 (802.11bn) は規格策定中で、対応チップ・認証は製品化の時点で要確認です (Wi-Fi 7 / 6E との互換で選定します)。Bluetooth の LDAC・aptX は各ライセンスが必要です。
- U-NEXT・YouTube・Qobuz の再生には、各社の認証・契約 (Widevine、Google 認証、Qobuz Connect など) が必要です。配信の音質は各サービスの仕様に従い、ビットパーフェクトで出力できない場合があります。
- 2つとも参考設計です。部品値は机上で求めたもので、シミュレーションも実機測定も行っていません。製品化の前に、実機測定と各種認証・安全規格の確認が必要です。"""
AMP_EN = """#Latest network-capable integrated amplifier (fully balanced and unbalanced versions)
I designed two versions of a latest integrated amplifier that plays music over Wi-Fi 8 (802.11bn) and a LAN port, also supports the latest Bluetooth, supports a web browser with built-in HDMI and USB-C video output terminals, can stream U-NEXT, YouTube and Qobuz, and accepts PCM up to 32 bit / 1536 kHz and DSD up to DSD1024 on its USB-C and I2S inputs, and also supports MQA. The circuit diagrams are in Japanese and English together and are published as PDF and JPG.

#Common specifications
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

#Fully balanced version (Figures 1 and 2)
- One DAC is used in mono mode for each of the L and R channels, and the Hot and Cold current outputs are each converted by an I/V stage.
- The signal passes through a differential low-pass filter, a balanced electronic volume control and a balanced line buffer, and goes directly to the XLR outputs (2 = Hot, 3 = Cold). The RCA outputs are made by a differential receiver (THAT1240) that converts to single-ended.
- The power amplifier is a Class-D (Eigentakt-type) with balanced input. The signal stays balanced all the way, so it is strong against hum, noise and ground loops.

#Unbalanced version (Figures 3 and 4)
- One DAC is used in stereo mode; after I/V conversion a subtractor (U2) turns the differential signal into single-ended.
- The signal passes through a single-ended low-pass filter, volume control and buffer, and goes directly to the RCA outputs. The XLR outputs, balanced with a THAT1646, are needed only when you want them (optional).
- The power amplifier has a single-ended input. It has fewer parts and is cheaper, but it is more prone to hum and ground loops than the balanced version, so take care with single-point grounding.

#Notes
- The BD34302 documentation is distributed under NDA, and the reference blog reports that its descriptions had errors that needed workarounds. It may not work at first, so the signals and the I2C settings must be checked on a real board. 1536 kHz / DSD1024 over USB needs dedicated UAC2 firmware and support on the playback side.
- Using MQA requires a license for MQA technology (Lenbrook). The sound of the streaming services (U-NEXT, YouTube, Qobuz) follows each service's specification (mostly lossy, or up to 24 bit / 192 kHz).
- Wi-Fi 8 (802.11bn) is still being standardized, so compatible chips and certification must be checked at the time of productization (choose parts compatible with Wi-Fi 7 / 6E). LDAC and aptX on Bluetooth each need a license.
- Playing U-NEXT, YouTube and Qobuz requires each company's certification and contract (Widevine, Google certification, Qobuz Connect and so on). The sound quality follows each service's specification, and bit-perfect output may not be possible.
- Both are reference designs. The component values were only worked out on paper; no simulation or bench measurement has been done. Bench measurement and the necessary certifications and safety standards must be checked before turning them into a product."""
CAPS = [("図9 / Figure 9: ヘッドホンアンプ (VER4) / Headphone amplifier", "amp_hp.jpg"),
        ("図10 / Figure 10: VER4 のシミュレーション / VER4 simulation", "amp_ver4_sim.jpg"),
        ("図7 / Figure 7: ボリューム 触覚ハイブリッド / Haptic hybrid volume knob", "amp_volume_haptic.jpg"),
        ("図8 / Figure 8: 音質改善 VER3 のシミュレーション / VER3 sound-quality simulation", "amp_ver3_sim.jpg"),
        ("図5 / Figure 5: 筐体内レイアウト(配線最短) / Internal layout for the shortest wiring", "amp_layout_net.jpg"),
        ("図6 / Figure 6: シミュレーション結果 / Simulation results", "amp_test.jpg"),
        ("図1 / Figure 1: 完全バランス版 ブロック図 / Fully balanced - block diagram", "streaming_amp_block.jpg"),
        ("図2 / Figure 2: 完全バランス版 アナログ信号経路 / Fully balanced - analog path", "streaming_amp_analog.jpg"),
        ("図3 / Figure 3: アンバランス版 ブロック図 / Unbalanced - block diagram", "streaming_amp_block_unbalanced.jpg"),
        ("図4 / Figure 4: アンバランス版 アナログ信号経路 / Unbalanced - analog path", "streaming_amp_analog_unbalanced.jpg")]
