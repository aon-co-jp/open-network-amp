# 音量ノブの刻み幅の仕様 / Volume knob step specification

参考設計(机上計算のみ・実機未検証)。対象: 触覚ハイブリッド音量ノブ(SW6)。計算は `scripts/volume/volume_calc.py`。

## 日本語
- **クリック感あり(モーター式)**: 1 クリック = **0.5 dB**(従来は 1 dB)。0〜−90 dB で 181 位置、270° を 180 等分 = 1 クリック 1.5°。ラッチングリレーのバランス抵抗ラダーを、0.5 / 1 / 2 / 4 / 8 / 16 / 32 / 64 dB の 8 区間(2 進)で構成(各脚)。0.1% 薄膜抵抗の誤差は 1 区間あたり最大約 0.009 dB で、0.5 dB の刻みに対して十分小さい。ノブの触覚は、5 dB ごとに強いクリック(アクセント)を入れる案。
- **クリック感なし(滑らか)**: 刻みを **0.01 dB**(旧: 分解能の記載なし)に。リレーは 0.5 dB ごとの位置を担当し、その間の ±0.25 dB は FPGA のデジタル微調整(32bit)で埋める。±0.25 dB のデジタル減衰で失うビットは約 0.04 bit で、旧来の「デジタルだけで −40 dB 下げると約 6.6 bit 失う」問題は起きない。磁気エンコーダ(14 bit)は 1 クリック分の角度あたり約 68 カウントで、0.5 dB の間の 50 段(0.01 dB)を分けるのに足りる。リレーの切替位置では、デジタル微調整を ∓0.5 dB 同時に動かしてレベルの段差を作らない(切替の短時間ミュート/ランプは実機で要確認)。
- **SW5(ビットパーフェクト、デジタル微調整を使わない)のとき**: 滑らか側の分解能は 0.5 dB に落ちる(リレーのみ)。0.01 dB の刻みはデジタル微調整を使うときだけ。
- 未実施: リレーの切替音・寿命、実機での触覚、THD。

## English
- **Clicky (motor) mode**: one click = **0.5 dB** (was 1 dB). 181 positions over 0 to -90 dB; the 270 deg arc is split into 180 clicks of 1.5 deg. A latching-relay balanced resistor ladder of 8 binary sections per leg (0.5 / 1 / 2 / 4 / 8 / 16 / 32 / 64 dB). 0.1% thin-film resistors add at most about 0.009 dB per section, well below the 0.5 dB step. Proposed feel: a stronger accent click every 5 dB.
- **Smooth (no-click) mode**: resolution **0.01 dB** (previously unspecified). The relays cover every 0.5 dB position; the +-0.25 dB between them is filled by a 32-bit digital fine trim in the FPGA. A trim of +-0.25 dB costs about 0.04 bit, so the earlier problem (-40 dB by digital alone loses about 6.6 bits) does not occur. The 14-bit magnetic encoder gives about 68 counts per click angle, enough for the 50 sub-steps (0.01 dB) between relay positions. At a relay switch point the fine trim moves by -/+0.5 dB at the same time so there is no level step (any brief mute/ramp during switching must be checked on hardware).
- **With SW5 (bit-perfect, digital trim off)**: smooth resolution falls back to 0.5 dB (relays only). The 0.01 dB resolution needs the digital trim.
- Not done: relay switching noise and life, real haptic feel, THD.
