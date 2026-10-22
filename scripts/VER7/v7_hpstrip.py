from PIL import Image, ImageDraw, ImageFont
HPI = {
 "ja": "ヘッドホンアンプ (前面、HP-VER2) はこの版にも搭載しています。ボリューム後の信号から分岐し (真空管版は真空管プリの出力から)、アナログゲイン 0 / +6 / +12 / +18dB (またはデジタルゲイン) → 電流バッファ → 前面の 3.5mm (バランス / アンバランス)・4.4mm バランス・6.35mm アンバランス・XLR (ステレオ 4 ピン 1 個とモノラル 3 ピン 2 個)。ヘッドホンの抵抗を検出してゲインを自動推奨します。ヘッドホン段は半導体で、真空管はプリ段のみです。",
 "en": "The front-panel headphone amplifier (HP-VER2) is included in this version too. It branches from the signal after the volume (from the valve preamp output in the valve versions) and goes through an analog gain of 0 / +6 / +12 / +18 dB (or a digital gain) and a current buffer to the front-panel 3.5 mm (balanced / unbalanced), 4.4 mm balanced, 6.35 mm unbalanced and XLR (one stereo 4-pin and two mono 3-pin) jacks. The headphone resistance is detected and a gain is recommended automatically. The headphone stage is solid state; the valve is the preamp stage only.",
 "ru": "Усилитель для наушников (передняя панель, HP-VER2) есть и в этой версии. Он ответвляется от сигнала после регулятора громкости (в ламповых версиях — от выхода лампового предусилителя) и через аналоговое усиление 0 / +6 / +12 / +18 дБ (или цифровое) и токовый буфер выводится на переднюю панель: 3,5 мм (сбалансированный / несбалансированный), 4,4 мм сбалансированный, 6,35 мм несбалансированный и XLR (один стерео 4-контактный и два моно 3-контактных). Сопротивление наушников определяется, усиление рекомендуется автоматически. Каскад для наушников полупроводниковый, лампа — только предусилитель.",
 "uk": "Підсилювач для навушників (передня панель, HP-VER2) є і в цій версії. Він відгалужується від сигналу після регулятора гучності (у лампових версіях — від виходу лампового попереднього підсилювача) і через аналогове підсилення 0 / +6 / +12 / +18 дБ (або цифрове) та струмовий буфер виводиться на передню панель: 3,5 мм (збалансований / незбалансований), 4,4 мм збалансований, 6,35 мм незбалансований і XLR (один стерео 4-контактний і два моно 3-контактних). Опір навушників визначається, підсилення рекомендується автоматично. Каскад для навушників напівпровідниковий, лампа — лише попередній підсилювач.",
 "de": "Der Kopfhörerverstärker (Frontplatte, HP-VER2) ist auch in dieser Version enthalten. Er zweigt nach dem Lautstärkeregler ab (bei den Röhrenversionen vom Ausgang der Röhrenvorstufe) und führt über eine analoge Verstärkung von 0 / +6 / +12 / +18 dB (oder eine digitale) und einen Strompuffer zu den frontseitigen Buchsen: 3,5 mm (symmetrisch / unsymmetrisch), 4,4 mm symmetrisch, 6,35 mm unsymmetrisch und XLR (eine Stereo-Buchse mit 4 Polen und zwei Mono-Buchsen mit 3 Polen). Der Kopfhörerwiderstand wird erkannt und eine Verstärkung automatisch empfohlen. Die Kopfhörerstufe ist ein Halbleiter, die Röhre nur die Vorstufe.",
 "it": "L'amplificatore per cuffie (frontale, HP-VER2) è presente anche in questa versione. Si deriva dal segnale dopo il volume (nelle versioni a valvole dall'uscita del pre a valvole) e passa attraverso un guadagno analogico di 0 / +6 / +12 / +18 dB (o digitale) e un buffer di corrente fino alle prese frontali: 3,5 mm (bilanciata / sbilanciata), 4,4 mm bilanciata, 6,35 mm sbilanciata e XLR (una stereo a 4 poli e due mono a 3 poli). La resistenza della cuffia viene rilevata e il guadagno è raccomandato automaticamente. Lo stadio per cuffie è a stato solido; la valvola è solo lo stadio di preamplificazione.",
 "fr": "L'amplificateur casque (façade, HP-VER2) est aussi présent dans cette version. Il dérive du signal après le volume (pour les versions à tubes, de la sortie du préampli à tubes) et passe par un gain analogique de 0 / +6 / +12 / +18 dB (ou numérique) et un tampon de courant jusqu'aux prises en façade : 3,5 mm (symétrique / asymétrique), 4,4 mm symétrique, 6,35 mm asymétrique et XLR (une stéréo à 4 broches et deux mono à 3 broches). La résistance du casque est détectée et un gain est recommandé automatiquement. L'étage casque est à semi-conducteurs ; le tube n'est que l'étage de préamplification.",
}
HPI["en-GB"] = HPI["en"].replace("analog", "analogue")
SRC = {
 "amp_ver7_classA.jpg": "ボリューム後のラインバッファ (PRE) から分岐 / branches from the line buffer after the volume",
 "amp_ver7_classA_AB.jpg": "ボリューム後のラインバッファ (PRE) から分岐 / branches from the line buffer after the volume",
 "amp_ver7_classAB.jpg": "ボリューム後のラインバッファ (PRE) から分岐 / branches from the line buffer after the volume",
 "amp_ver7_classD.jpg": "ボリューム後のバッファから分岐 / branches from the buffer after the volume",
 "amp_ver7_tube.jpg": "真空管プリの PRE OUT から分岐 / branches from the valve preamp output",
 "amp_ver7_tube_AB.jpg": "真空管プリの PRE OUT から分岐 / branches from the valve preamp output",
 "amp_ver7_tube_A_AB.jpg": "真空管プリの PRE OUT から分岐 / branches from the valve preamp output",
 "amp_ver7_tube_D.jpg": "真空管プリの PRE OUT から分岐 / branches from the valve preamp output",
}


def hp_strip(fn, W=3200):
    H = 620
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", 44)
    f2 = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 32)
    f3 = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 28)
    col = (25, 115, 60); pw = (190, 100, 20); ink = (20, 30, 60); grey = (110, 110, 110)
    d.text((60, 22), "ヘッドホンアンプ HP-VER2 (前面)  Headphone amplifier on the front panel — この版の接続 / connection in this version", font=f1, fill=ink)

    def box(x0, y0, x1, y1, lines, c):
        d.rectangle([x0, y0, x1, y1], outline=c, width=5, fill=(250, 250, 240))
        yy = y0 + 18
        for i, t in enumerate(lines):
            d.text(((x0 + x1) // 2, yy), t, font=f2 if i else f1, fill=ink if i == 0 else (60, 60, 60), anchor="ma"); yy += 50 if i == 0 else 42

    def arrow(x0, y, x1, c):
        d.line([x0, y, x1, y], fill=c, width=6)
        d.polygon([(x1, y), (x1 - 26, y - 14), (x1 - 26, y + 14)], fill=c)
    box(60, 110, 760, 360, ["入力の分岐", SRC[fn].split(" / ")[0], SRC[fn].split(" / ")[1], "(挿すとスピーカー出力は自動で OFF)"], col)
    arrow(760, 235, 840, col)
    box(840, 110, 1700, 360, ["HP-VER2 ヘッドホン段", "アナログゲイン 0 / +6 / +12 / +18 dB (リレー)", "またはデジタルゲイン (±0.5 dB)", "抵抗検出 → ゲイン自動推奨", "電流バッファ (±0.5A×2)・出力 約 0.1Ω"], col)
    arrow(1700, 235, 1780, col)
    xs = [(1780, 2090, "3.5mm", "TRRS バランス|TRS アンバランス|(自動検出)"), (2110, 2420, "4.4mm", "バランス|(Pentaconn)"), (2440, 2750, "6.35mm", "アンバランス|(6.5mm)"), (2770, 3140, "XLR ×2種類", "ステレオ 4 ピン 1 個|+ モノラル 3 ピン 2 個|(L 用・R 用)")]
    for x0, x1, a, b in xs:
        d.rectangle([x0, 110, x1, 360], outline=col, width=5, fill=(250, 250, 240))
        d.text(((x0 + x1) // 2, 150), a, font=f1, fill=ink, anchor="ma")
        for li, part in enumerate(b.split("|")):
            d.text(((x0 + x1) // 2, 215 + li * 40), part, font=f3, fill=(60, 60, 60), anchor="ma")
    d.text((1780, 372), "前面のジャック: ジャック検出・起動/停止ミュート・DC 保護", font=f3, fill=grey)
    d.text((60, 440), "電源: ヘッドホン専用 LDO ±15V (LT3045 / LT3094) を外付けリニア電源の専用巻線から。SW7 = ANALOG / DIGITAL ゲイン。ヘッドホンを挿すとスピーカー出力は自動で OFF、抜くと復帰。", font=f2, fill=ink)
    d.text((60, 492), "Power: dedicated LDO +-15 V from a winding of the external linear supply. SW7 = analog / digital gain. Plugging in headphones turns the speaker outputs OFF automatically; unplugging restores them.", font=f3, fill=grey)
    d.text((60, 540), "詳細・仮想シミュレーション: headphone/HP-VER2 (open-network-amp)  /  Details and simulation: headphone/HP-VER2. 真空管はプリ段のみ、ヘッドホン段は半導体 / the valve is the preamp stage only.", font=f3, fill=grey)
    return im
