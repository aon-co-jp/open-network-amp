import re
from PIL import Image, ImageDraw, ImageFont

SD = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
DPI = 3200 / 11.69          # figure page = 11.69 in wide, full width
PW, PH = int(8.27 * DPI), int(11.69 * DPI)
MX, MY = int(0.7 * DPI), int(0.7 * DPI)
FS = int(0.135 * DPI)       # ~9.7pt
REG = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", FS)
BLD = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", FS)
HD = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", int(FS * 1.25))

EN_PMA = ("Difference from the PMA-2000RE: the PRE OUT of the PMA-2000RE is a terminal whose output follows the volume, "
          "and it can also be used for a subwoofer. This point is confirmed by the PHILE WEB article, which mentions a "
          "pre-out terminal convenient for connecting a subwoofer. (PHILE WEB (Japanese))")
EN_BLOCK = """#Title
With a fully balanced design, going mono makes it easy to add a subwoofer output.

For a fully balanced integrated amplifier, wouldn't it be easy to design, manufacture and sell a mono subwoofer output on both XLR and RCA, as part of the pre-out? Please also describe the benefits of making the subwoofer output mono. I put this question to a paid AI called Claude.

Yes, it is technically quite easy. The extra parts are only one or two op-amps, some resistors and XLR/RCA jacks, so the cost is small. However, there are a few points to get right if you want a clean result.

#Design points
- Mixing position: If you sum L+R after the volume control, the subwoofer level follows the main volume.
- Balanced summing: Sum the Hot signals together and the Cold signals together, each through its own resistors, and receive them with a buffer. This keeps the circuit fully balanced and gives a mono XLR output.
- RCA output: Feed it through a differential-to-single-ended conversion circuit. Simply taking only the Hot signal is easy, but it is worse for noise.
- Channel isolation: Use summing resistors of roughly a few kΩ to 10 kΩ. This prevents the main L/R outputs from interfering with each other and prevents crosstalk from getting worse.
- Buffer insertion: Make sure the subwoofer's input impedance does not load the main pre-outs.
- Gain adjustment: Highly correlated bass rises by about +6 dB when summed, so compensate the gain with the resistor values.
- Options: A Stereo/Mono switch, a simple low-pass filter (about 80–120 Hz) and a phase-invert switch would make the product more attractive.

#Benefits of a mono subwoofer output
- Little effect on imaging: Bass below about 100 Hz has almost no sense of direction, so mono causes virtually no disadvantage in listening.
- Simple connection: One cable is enough. It connects directly to subwoofers that have only a mono input, and no Y-splitter cable is needed.
- Good match with the source: In mixing, bass is generally placed in the center, and vinyl records also have their low frequencies made mono because of cutting limitations.
- Better S/N ratio: Summing L+R raises the signal level, which is advantageous against noise on the subwoofer side.
- Easy multi-unit use: When two or more subwoofers are placed at different positions in the room to even out room modes (standing waves), sending the same mono signal to all of them is the basic approach.
- Compatibility with balanced transmission: The cable run to the subwoofer tends to be long, and XLR is resistant to hum and ground loops, so it shows its real value here.

#Cautions (drawbacks)
- Out-of-phase bass (some live recordings, synthesizer sources, etc.) cancels when summed and sounds thin.
- For people who want stereo low-frequency imaging (spatial spread) with two subwoofers, it is safest to include a switch.
- On the manufacturing and sales side, the circuit is small and can be handled by adding a board or mounting it on an existing board. For a mid-price or higher fully balanced amplifier, it is a strong enough point of differentiation."""

JA_PMA = ("PMA-2000RE との違い: PMA-2000RE の PRE OUT は、音量に連動する出力としてサブウーファーにも使える端子です。"
          "この点は、PHILE WEBの記事に「サブウーファーとの接続による便利なプリアウト端子」と記載があり、裏付けが取れています。（参考: PHILE WEB）")
JA_BLOCK = """#タイトル
完全バランス設計なら、モノラル化すれば、サブウーファー端子が簡単に付けられます。

完全バランス設計のプリメインアンプは、プリアウトのXLRとRCAのサブウーファー端子は、モノラルなら、簡単に設計、製造、販売出来るのではありませんか？サブウーファー端子をモノラル化するメリットも記載して。CLAUDEと言う、有料のAIに質問して見ました。

はい、技術的にはかなり簡単です。追加部品はオペアンプ1〜2個と抵抗、XLR/RCA端子程度で、コストも小さく済みます。ただし、きれいに作るにはいくつか押さえるべき点があります。

#設計のポイント
- ミックス位置：ボリューム回路の後で L+R を加算すると、サブウーファーの音量がメイン音量に連動します。
- バランス加算：Hot同士、Cold同士を別々に抵抗で加算し、バッファで受けます。これで完全バランス構成のまま、モノラルのXLR出力が得られます。
- RCA出力：差動からシングルエンドへの変換回路を通して出します。Hotだけを取り出す方式は簡単ですが、ノイズ面では不利です。
- チャンネル間の分離：加算抵抗は数kΩ〜10kΩ程度にします。メインのL/R出力同士が干渉したり、クロストークが悪化したりするのを防ぐためです。
- バッファの挿入：サブウーファー側の入力インピーダンスが、メインのプリアウトに負荷をかけないようにします。
- ゲイン調整：相関の強い低音は加算すると約+6dBになるため、抵抗値でゲインを補正します。
- オプション：Stereo/Monoの切替スイッチ、簡易ローパスフィルター（約80〜120Hz）、位相反転スイッチがあると商品力が上がります。

#サブウーファー出力をモノラル化するメリット
- 定位への影響が小さい：約100Hz以下の低音は方向感がほとんどないため、モノラルでも聴感上の不利はほぼありません。
- 接続が簡単：ケーブル1本で済みます。モノラル入力しかないサブウーファーにもそのまま繋がり、Y分岐ケーブルも不要です。
- ソースとの相性が良い：ミックスでは低音を中央に定位させるのが一般的で、アナログ盤もカッティングの都合で低域をモノラル化しています。
- S/N比の向上：L+Rを加算すると信号レベルが上がるため、サブウーファー側のノイズに対して有利になります。
- 複数台の運用がしやすい：2台以上を部屋の別々の位置に置いてルームモード（定在波）を均す使い方では、全台に同じモノラル信号を送るのが基本です。
- バランス伝送との相性：サブウーファーまでの配線は長くなりがちですが、XLRならハムやグランドループに強く、ここで真価を発揮します。

#注意点（デメリット）
- 逆相成分の低音（一部のライブ録音やシンセ音源など）は、加算すると打ち消し合って痩せます。
- 2台のサブウーファーで低域のステレオ感（空間の広がり）まで狙う層向けに、切替スイッチを付けておくのが無難です。
- 製造・販売面では、回路は小規模で、基板の追加か既存基板への実装で対応できます。中価格帯以上の完全バランスアンプなら差別化要素として十分に成立します。"""

TOK = re.compile(r"[\x21-\x7e]+|\s|.", re.S)


def wrap(text, font, width):
    out, cur = [], ""
    for t in TOK.findall(text):
        if font.getlength(cur + t) > width and cur.strip():
            out.append(cur.rstrip())
            cur = t.lstrip()
        else:
            cur += t
    out.append(cur.rstrip())
    return out


pages = []
page = d = None
y = 0


def new_page():
    global page, d, y
    page = Image.new("RGB", (PW, PH), "white")
    d = ImageDraw.Draw(page)
    y = MY
    pages.append(page)


def put(text, font, indent=0, gap=0.45, bullet=False):
    global y
    lh = int(font.size * 1.55)
    width = PW - 2 * MX - indent
    lines = wrap(text, font, width - (int(FS * 1.2) if bullet else 0))
    if y + lh * len(lines) > PH - MY:
        new_page()
    for i, ln in enumerate(lines):
        x = MX + indent + (int(FS * 1.2) if bullet else 0)
        if bullet and i == 0:
            d.text((MX + indent, y), "•", font=font, fill=(20, 30, 60))
        d.text((x, y), ln, font=font, fill=(20, 30, 60))
        y += lh
    y += int(FS * gap)


def render(pma, block):
    put(pma, REG, gap=0.9)
    for para in block.split("\n"):
        if not para.strip():
            continue
        if para.startswith("#"):
            y_gap = int(FS * 0.5)
            global y
            y += y_gap
            put(para[1:], HD, gap=0.3)
        elif para.startswith("- "):
            put(para[2:], REG, bullet=True, gap=0.3)
        else:
            put(para, REG, gap=0.6)


new_page()
put("https://audiocafe.tokyo/", BLD, gap=1.0)
render(EN_PMA, EN_BLOCK)
y += int(FS * 1.2)
render(JA_PMA, JA_BLOCK)

# figure page: full width, tiny margins, page size = figure size
fig = Image.open(SD + r"\mono_sub_out_schematic.jpg").convert("RGB")
m = 24
fp = Image.new("RGB", (fig.width + 2 * m, fig.height + 2 * m), "white")
fp.paste(fig, (m, m))
fp = fp.resize((int(11.69 * DPI) + 0, int(fp.height * (11.69 * DPI) / fp.width)))

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

out = SD + r"\mono-sub-out-fully-balanced.pdf"
pages[0].save(out, "PDF", resolution=DPI, save_all=True, append_images=pages[1:])
print(out, len(pages), [p.size for p in pages])
