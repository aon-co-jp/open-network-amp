SUM_JA = """#まとめ(日本語)
完全バランス用とアンバランス用の回路図を2つとも作り、日本語と英語の説明をそれぞれ付けて、5ページのPDFにまとめました。ホームページ(audiocafe.tokyo のトップページ)にも掲載しました。

#PDFの構成
- 1〜3ページ目は本文です。URL、英語のPMA-2000RE説明と英語本文、日本語のPMA-2000RE説明と日本語本文の順です。
- 4ページ目は完全バランス設計のアンプ用の回路図で、下に日本語、英語の順で説明を付けています。
- 5ページ目はもともとアンバランス設計のアンプ用の回路図で、下に日本語、英語の説明と共通の注意を付けています。
- 回路図の文字は、どちらも日本語と英語の併記です。

#2つの回路図の違い
- 加算: 完全バランス用は Hot側とCold側を別々に2系統で加算 / アンバランス用は反転加算1系統
- 位相: 完全バランス用は DPDTで HotとColdを入れ替え / アンバランス用は SPDTで直結(180°)か反転段経由(0°)かを選択
- LPF: 完全バランス用は HotとColdに同じ値で2系統 / アンバランス用は 1系統
- 出力: 完全バランス用は XLRはバッファ経由、RCAは差動レシーバ(THAT1240)で変換 / アンバランス用は RCAはDCカット(4.7µF)と100Ω経由、XLRは任意でTHAT1646で平衡化

どちらも参考設計です。部品値は机上で求めたもので、シミュレーションも実機測定もしていないため、製品化の前に必ず検証してください。"""
SUM_EN = """#Summary (English)
I made both circuit diagrams, one for an amplifier that is fully balanced by design and one for an amplifier that was originally unbalanced, added a Japanese and an English explanation to each, and put them together in a 5-page PDF. They are also posted on the top page of audiocafe.tokyo.

#Structure of the PDF
- Pages 1-3 are the text, in this order: the URL, the English PMA-2000RE explanation and English body, then the Japanese PMA-2000RE explanation and Japanese body.
- Page 4 is the circuit diagram for a fully balanced amplifier, with the Japanese explanation followed by the English one below it.
- Page 5 is the circuit diagram for an originally unbalanced amplifier, with the Japanese and English explanations and the common notes below it.
- The text in both diagrams is in English and Japanese together.

#Differences between the two diagrams
- Summing: the fully balanced version sums the Hot side and the Cold side separately in two paths / the unbalanced version uses one inverting summer.
- Phase: the fully balanced version swaps Hot and Cold with a DPDT switch / the unbalanced version selects the direct output (180°) or the inverting stage (0°) with an SPDT switch.
- Low-pass filter: the fully balanced version uses two paths with identical values for Hot and Cold / the unbalanced version uses one path.
- Output: in the fully balanced version the XLR goes through buffers and the RCA is converted by a differential receiver (THAT1240) / in the unbalanced version the RCA goes through a DC-blocking capacitor (4.7 µF) and 100 Ω, and the XLR is optionally balanced with a THAT1646.

Both are reference designs. The component values were only worked out on paper and no simulation or bench measurement has been done, so be sure to verify them before turning them into a product."""


EX_BAL_JA = """#回路図1: アンプ自体が完全バランス設計の場合
- 入力: ボリューム後段のバランス信号 (L±, R±) をそのまま使います。サブウーファーの音量はメイン音量に連動します。
- 加算: Hot同士 (L+, R+) と Cold同士 (L−, R−) を、それぞれ 10 kΩ (0.1%) で反転加算します (U1A / U1B)。利得は 0.5 倍で、L=R の低音が 0 dB になるよう揃えます。
- 位相: SW2 (DPDT) で Hot と Cold を入れ替えると 180° 反転します。
- LPF: 2次バターワース (Sallen-Key) を Hot / Cold に同じ値で用意し、80 / 100 / 120 Hz / BYPASS を SW3 で切り替えます。
- 出力: バッファ (U4A / U4B) と 47 Ω を通して XLR (2=Hot, 3=Cold, 1=シールド) に出します。RCA は差動レシーバ (U5, THAT1240) でシングルエンドに変換します。
- 特徴: 最後まで平衡のまま処理するので、ハム・ノイズ・グランドループに強い構成です。"""
EX_BAL_EN = """#Circuit 1: for an amplifier that is fully balanced by design
- Input: The balanced signal after the volume control (L±, R±) is used as it is, so the subwoofer level follows the main volume.
- Summing: The Hot signals (L+, R+) and the Cold signals (L−, R−) are each summed by an inverting summer with 10 kΩ (0.1%) resistors (U1A / U1B). The gain is 0.5, so bass with L=R comes out at 0 dB.
- Phase: Swapping Hot and Cold with the DPDT switch SW2 inverts the phase by 180°.
- Low-pass filter: A 2nd-order Butterworth (Sallen-Key) filter with identical values is used on both Hot and Cold; SW3 selects 80 / 100 / 120 Hz or BYPASS.
- Output: Buffers (U4A / U4B) and 47 Ω resistors feed the XLR (2 = Hot, 3 = Cold, 1 = shield). The RCA output comes from a differential receiver (U5, THAT1240) that converts to single-ended.
- Feature: The signal stays balanced all the way, so this design is strong against hum, noise and ground loops."""
EX_UNB_JA = """#回路図2: アンプが元々アンバランス (シングルエンド) 設計の場合
- 入力: ボリューム後段の L / R のシングルエンド信号 (RCA) を使います。
- 加算: 反転加算回路 1 つ (U1A) で L+R を加算します (利得 0.5)。バランス版の半分の部品で済みます。
- 位相: SW2 (SPDT) で、U1A の出力を直結 (180°) するか、U1B の反転段を通す (0°) かを選びます。
- LPF: 2次バターワース 1 系統で、80 / 100 / 120 Hz / BYPASS を SW3 で切り替えます。
- 出力: RCA は DC カットコンデンサ (4.7 µF) と 100 Ω の直列抵抗を通して出します。XLR が必要なときだけ THAT1646 で平衡化します (任意)。
- 特徴: 部品が少なく安価ですが、バランス版よりハム・グランドループに弱いので、アースの取り方 (1点アース) に注意が必要です。"""
EX_UNB_EN = """#Circuit 2: for an amplifier that is unbalanced (single-ended) by design
- Input: The single-ended L / R signals (RCA) after the volume control are used.
- Summing: One inverting summer (U1A) adds L+R (gain 0.5). It needs about half the parts of the balanced version.
- Phase: SW2 (SPDT) selects either the direct output of U1A (180°) or the signal passed through the inverting stage U1B (0°).
- Low-pass filter: A single 2nd-order Butterworth filter; SW3 selects 80 / 100 / 120 Hz or BYPASS.
- Output: The RCA output goes through a DC-blocking capacitor (4.7 µF) and a 100 Ω series resistor. The XLR output, balanced with a THAT1646, is needed only when you want it (optional).
- Feature: Few parts and low cost, but it is more prone to hum and ground loops than the balanced version, so take care with grounding (single-point ground)."""
CAV_JA = """#共通の注意
- 2つの図はどちらも参考設計です。部品値は机上で求めたもので、シミュレーションも実機測定もしていません。製品化の前に必ず検証してください。
- 図の文字は英語と日本語の併記です。"""
CAV_EN = """#Common notes
- Both diagrams are reference designs. The component values were only worked out on paper; no simulation or bench measurement has been done. Be sure to verify them before turning them into a product.
- The text in the diagrams is in both English and Japanese."""

NM = 110


def fig_page(path, blocks):
    fig = Image.open(path).convert("RGB")
    m = 24
    base = Image.new("RGB", (fig.width + 2 * m, fig.height + 2 * m), "white")
    base.paste(fig, (m, m))
    base = base.resize((int(11.69 * DPI), int(base.height * (11.69 * DPI) / base.width)))
    nw = base.width - 2 * NM
    laid = []
    total = int(FS * 1.2)
    for blk in blocks:
        for para in blk.split(chr(10)):
            if not para.strip():
                continue
            if para.startswith("#"):
                font, t, gap, bullet, pre = HD, para[1:], 0.35, False, 0.7
            elif para.startswith("- "):
                font, t, gap, bullet, pre = REG, para[2:], 0.3, True, 0
            else:
                font, t, gap, bullet, pre = REG, para, 0.5, False, 0
            lh = int(font.size * 1.55)
            lines = wrap(t, font, nw - (int(FS * 1.2) if bullet else 0))
            total += int(FS * pre) + lh * len(lines) + int(FS * gap)
            laid.append((font, lines, lh, gap, bullet, pre))
        total += int(FS * 0.8)
    canvas = Image.new("RGB", (base.width, base.height + total + NM // 2), "white")
    canvas.paste(base, (0, 0))
    cd = ImageDraw.Draw(canvas)
    yy = base.height + int(FS * 1.2)
    for font, lines, lh, gap, bullet, pre in laid:
        yy += int(FS * pre)
        for i, ln in enumerate(lines):
            if bullet and i == 0:
                cd.text((NM, yy), "•", font=font, fill=(20, 30, 60))
            cd.text((NM + (int(FS * 1.2) if bullet else 0), yy), ln, font=font, fill=(20, 30, 60))
            yy += lh
        yy += int(FS * gap)
    return canvas


pages.append(fig_page(SD + r"\mono_sub_out_schematic.jpg", [EX_BAL_JA, EX_BAL_EN]))
pages.append(fig_page(SD + r"\mono_sub_out_unbalanced.jpg", [EX_UNB_JA, EX_UNB_EN, CAV_JA, CAV_EN, SUM_JA, SUM_EN]))

out = SD + r"\mono-sub-out-fully-balanced.pdf"
pages[0].save(out, "PDF", resolution=DPI, save_all=True, append_images=pages[1:])
print(out, len(pages), [p.size for p in pages])
for i, p in enumerate(pages):
    p.resize((p.width // 2, p.height // 2)).save(SD + r"\pg%d.png" % (i + 1))
