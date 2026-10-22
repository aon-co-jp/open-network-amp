s = open('build_pdf.py', encoding='utf-8').read()
new = '''
NOTES_EN = """#English
I handed over the PDF and the JPG of the circuit diagram in a downloadable form.

#PDF (4 pages)
- Pages 1-3 are the text, in this order: the audiocafe.tokyo URL, the English PMA-2000RE explanation, the English body, the Japanese PMA-2000RE explanation, and the Japanese body.
- Page 4 is the circuit diagram. The page has the same proportions as the diagram, so there are almost no left or right margins.

#Circuit diagram (English and Japanese together)
- The structure is: balanced L+R summing, phase switch (SW2), low-pass filter (SW3, 80/100/120 Hz), buffers, XLR output and differential RCA output.
- The MONO/STEREO switch (SW1), power-supply notes and a bill of materials are included.

#Notes
- The diagram is a reference design. The component values were only worked out on paper; no simulation or bench measurement has been done. Be sure to verify it before turning it into a product.
- In the Japanese body, the misspelling of "subwoofer" was corrected. It can be changed back if you prefer the original.
- You may have wanted the diagram near page 2; it is placed at the end. Tell me if you want the position changed.
- The audiocafe.tokyo website itself has not been edited."""

NOTES_JA = """#日本語
PDFと回路図のJPGを、ダウンロードできる形で渡しました。

#PDF(4ページ)
- 1〜3ページ目は本文です。audiocafe.tokyo のURL、英語のPMA-2000RE説明、英語本文、日本語のPMA-2000RE説明、日本語本文の順に並べています。
- 4ページ目が回路図です。ページを図と同じ比率にして、左右の余白はほぼありません。

#回路図(英語と日本語の併記)
- 構成は、L+Rバランス加算、位相切替(SW2)、LPF(SW3、80/100/120Hz)、バッファ、XLR出力と差動RCA出力です。
- MONO/STEREO切替(SW1)、電源の注意、部品表も載せています。

#注意点
- 図は参考設計です。部品値はグラフィックで計算しただけで、シミュレーションも実機測定もしていません。製品化の前に必ず検証してください。
- 日本語本文の「サフウーファー」は「サブウーファー」に直しています。そのままがよければ戻します。
- 図は2ページ目付近に載せたかったかもしれませんが、末尾に置いています。位置を変える場合は教えてください。
- audiocafe.tokyo のサイト自体は編集していません。"""

NM = 110
nw = fp.width - 2 * NM
rows = []   # (font, text, indent, gap)
for blk in (NOTES_EN, NOTES_JA):
    for para in blk.split(chr(10)):
        if not para.strip():
            continue
        if para.startswith("#"):
            rows.append((HD, para[1:], 0, 0.35, False, 0.6))
        elif para.startswith("- "):
            rows.append((REG, para[2:], 0, 0.3, True, 0))
        else:
            rows.append((REG, para, 0, 0.5, False, 0))
    rows.append((REG, "", 0, 1.0, False, 0))
laid = []
total = int(FS * 1.2)
for font, t, ind, gap, bullet, pre in rows:
    lh = int(font.size * 1.55)
    lines = wrap(t, font, nw - (int(FS * 1.2) if bullet else 0)) if t else []
    total += int(FS * pre) + lh * len(lines) + int(FS * gap)
    laid.append((font, lines, lh, gap, bullet, pre))
canvas = Image.new("RGB", (fp.width, fp.height + total + NM // 2), "white")
canvas.paste(fp, (0, 0))
cd = ImageDraw.Draw(canvas)
yy = fp.height + int(FS * 1.2)
for font, lines, lh, gap, bullet, pre in laid:
    yy += int(FS * pre)
    for i, ln in enumerate(lines):
        if bullet and i == 0:
            cd.text((NM, yy), "•", font=font, fill=(20, 30, 60))
        cd.text((NM + (int(FS * 1.2) if bullet else 0), yy), ln, font=font, fill=(20, 30, 60))
        yy += lh
    yy += int(FS * gap)
fp = canvas
pages.append(fp)
'''
assert s.count("pages.append(fp)\n") == 1
s = s.replace("pages.append(fp)\n", new)
open('build_pdf2.py', 'w', encoding='utf-8').write(s)
