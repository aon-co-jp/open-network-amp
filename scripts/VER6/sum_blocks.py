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
