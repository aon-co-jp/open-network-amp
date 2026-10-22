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
pages.append(fp)

out = SD + r"\mono-sub-out-fully-balanced.pdf"
pages[0].save(out, "PDF", resolution=DPI, save_all=True, append_images=pages[1:])
print(out, len(pages), [p.size for p in pages])
