import os, re, shutil
from PIL import Image, ImageDraw, ImageFont
SD = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
# reuse the texts built for the README (IT dict with 8 languages)
src = open(SD + r"\v7_build.py", encoding="utf-8").read()
head = src.split('OUT = SD + r"\\v7out"')[0]
g = {}
exec(head, g)
IT, TITLE, INTRO, LANG8, NAME8 = g["IT"], g["TITLE"], g["INTRO"], g["LANG8"], g["NAME8"]
_dec = g["_dec"] if "_dec" in g else (lambda L, t: t)
B = {
 "ja": "AB級版: 8Ω に最大 100W (ピーク 100dB 以上)。1 素子約 50mA の低バイアスで、アイドル発熱は小さい (約 4.5W/ch)。出力素子 2 並列、エミッタ抵抗 0.33Ω (無誘導)、Cdom は C0G、Vbe 倍率はヒートシンクに熱結合。A級の音を重視するなら A級+AB級版を選ぶ。",
 "en": "Class AB version: up to 100 W into 8 ohm (peaks of 100 dB and more). A low bias of about 50 mA per device keeps the idle heat small (about 4.5 W per channel). Two output devices in parallel, non-inductive 0.33 ohm emitter resistors, a C0G Cdom and the Vbe multiplier coupled to the heatsink. For more Class A sound choose the Class A + AB version.",
 "ru": "Версия класса AB: до 100 Вт на 8 Ом (пики 100 дБ и выше). Низкий ток покоя около 50 мА на транзистор — тепловыделение в покое невелико (около 4,5 Вт на канал). Два выходных транзистора параллельно, безындуктивные эмиттерные резисторы 0,33 Ом, Cdom типа C0G, умножитель Vbe связан с радиатором. Для большего звучания класса A выберите версию A + AB.",
 "uk": "Версія класу AB: до 100 Вт на 8 Ом (піки 100 дБ і вище). Низький струм спокою близько 50 мА на транзистор — тепловиділення в спокої невелике (близько 4,5 Вт на канал). Два вихідні транзистори паралельно, безіндуктивні емітерні резистори 0,33 Ом, Cdom типу C0G, помножувач Vbe пов'язаний із радіатором. Для більшого звучання класу A оберіть версію A + AB.",
 "de": "Klasse-AB-Version: bis 100 W an 8 Ω (Spitzen von 100 dB und mehr). Ein niedriger Ruhestrom von etwa 50 mA je Transistor hält die Ruheverlustleistung klein (etwa 4,5 W je Kanal). Zwei Endtransistoren parallel, induktionsarme 0,33-Ω-Emitterwiderstände, Cdom als C0G, Vbe-Multiplikator thermisch mit dem Kühlkörper gekoppelt. Für mehr Klasse-A-Klang die Klasse-A-plus-AB-Version wählen.",
 "it": "Versione classe AB: fino a 100 W su 8 ohm (picchi di 100 dB e oltre). Una polarizzazione bassa di circa 50 mA per dispositivo mantiene ridotto il calore a riposo (circa 4,5 W per canale). Due dispositivi di uscita in parallelo, resistenze di emettitore da 0,33 ohm non induttive, Cdom in C0G e moltiplicatore di Vbe accoppiato al dissipatore. Per più suono in classe A scegliere la versione classe A + AB.",
 "fr": "Version classe AB : jusqu'à 100 W sous 8 ohms (crêtes de 100 dB et plus). Une polarisation faible d'environ 50 mA par transistor limite la chaleur au repos (environ 4,5 W par canal). Deux transistors de sortie en parallèle, résistances d'émetteur de 0,33 ohm non inductives, Cdom en C0G et multiplicateur de Vbe couplé au dissipateur. Pour plus de son classe A, choisir la version classe A + AB.",
}
B["en-GB"] = B["en"]
IT["B"] = B
bx = {}
exec(open(SD + "/v7b_texts.py", encoding="utf-8").read().replace('if __name__ == "__main__":', 'if False:'), bx)
for k in bx["R"]:
    IT["R" + k] = {L: (bx["R"][k][L] % bx["V"] if "%(" in bx["R"][k][L] else bx["R"][k][L]).replace("%%", "%") for L in LANG8}
FIGS = {
 "amp_ver7b_sim.jpg": ("追加の仮想シミュレーション TEST 6-10 / Additional simulation", ["R1", "R2", "R3", "R4", "R5", "R6"]),  # file -> (title key text, items)
 "amp_ver7_classA.jpg": ("A級 / Class A", ["need", "A", "V", "C", "N"]),
 "amp_ver7_classA_AB.jpg": ("A級+AB級 / Class A + AB", ["need", "H", "C", "N"]),
 "amp_ver7_classAB.jpg": ("AB級 / Class AB", ["need", "B", "C", "N"]),
 "amp_ver7_classD.jpg": ("D級アナログ / Analog Class D", ["need", "D", "C", "N"]),
 "amp_ver7_tube_AB.jpg": ("真空管プリ+AB級 / Valve preamp + Class AB", ["V", "B", "C", "N"]),
 "amp_ver7_tube_A_AB.jpg": ("真空管プリ+A+AB級 / Valve preamp + Class A + AB", ["V", "H", "C", "N"]),
 "amp_ver7_tube_D.jpg": ("真空管プリ+クラスDアナログ / Valve preamp + analog Class D", ["V", "D", "C", "N"]),
 "amp_ver7_tube.jpg": ("真空管プリ+A級 / Valve preamp + Class A", ["V", "A", "C", "N"]),
 "amp_ver7_sim.jpg": ("仮想シミュレーション / Virtual simulation", ["need", "A", "H", "D", "N"]),
}
W, pad = 3200, 60
colw = (W - 3 * pad) // 2
FS = 34
REG = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", FS)
HD = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", int(FS * 1.2))
BIG = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", int(FS * 1.5))
TOK = re.compile(r"[\x21-\x7e\u00a0-\u024f\u0400-\u04ff]+|\s|.", re.S)


def wrap(t, font, width):
    out, cur = [], ""
    for tk in TOK.findall(t):
        if font.getlength(cur + tk) > width and cur.strip():
            out.append(cur.rstrip()); cur = tk.lstrip()
        else:
            cur += tk
    out.append(cur.rstrip())
    return out


hh = lambda lines: sum(int(f.size * 1.45) for _, f in lines) + 40
D = os.path.join(SD, "ona", "VER7")
FIGDIR = os.path.join(D, "figures-only")
os.makedirs(FIGDIR, exist_ok=True)
for fn, (ttl, keys) in FIGS.items():
    orig = os.path.join(FIGDIR, fn)
    if not os.path.exists(orig):
        shutil.copy(os.path.join(D, fn), orig)         # keep the figure without the explanation
    fig = Image.open(orig).convert("RGB")
    fig = fig.resize((W, int(fig.height * W / fig.width)))
    blocks = []
    for L in LANG8:
        lines = [(NAME8[L], HD)]
        for k in keys:
            for ln in wrap(_dec(L, IT[k][L]), REG, colw):
                lines.append((ln, REG))
            lines.append(("", REG))
        blocks.append(lines)
    rows = [(blocks[i], blocks[i + 1]) for i in range(0, 8, 2)]
    TH = 140 + sum(max(hh(a), hh(b)) for a, b in rows) + pad
    img = Image.new("RGB", (W, fig.height + TH), "white")
    img.paste(fig, (0, 0))
    d = ImageDraw.Draw(img)
    d.text((pad, fig.height + 40), "VER7 " + ttl + " — 説明 / Explanation (8 languages)", font=BIG, fill=(20, 30, 60))
    y = fig.height + 140
    for a, b in rows:
        for col, lines in enumerate((a, b)):
            x, yy = pad + col * (colw + pad), y
            for t, f in lines:
                d.text((x, yy), t, font=f, fill=(20, 30, 60) if f is HD else (40, 40, 40)); yy += int(f.size * 1.45)
        y += max(hh(a), hh(b))
    img.save(os.path.join(D, fn), "JPEG", quality=88, dpi=(300, 300))
    print(fn, img.size)
