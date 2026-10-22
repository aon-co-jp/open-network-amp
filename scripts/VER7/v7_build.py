import os, re, subprocess, textwrap
from PIL import Image, ImageDraw, ImageFont
SD = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
exec(open(SD + r"\v7_texts.py", encoding="utf-8").read())
g = {}
exec(open(SD + r"\v7_calc.py", encoding="utf-8").read().replace('if __name__ == "__main__":', 'if False:'), g)
pk = g["need"](100)
avgw = g["avg_w"](pk)
v = {
    "n90": g["need"](90), "n95": g["need"](95), "n100": g["need"](100),
    "pa": g["P_A"], "spla": g["spl"](g["P_A"]), "ha": g["heat_A"], "ha2": 2 * g["heat_A"], "ka": g["kwh"](2 * g["heat_A"]),
    "ph": g["P_H"], "hh": g["heat_H"], "hh2": 2 * g["heat_H"],
    "hd": 2 * g["pd_D"](avgw), "kd": g["kwh"](2 * g["pd_D"](avgw)),
}
IT = items(v)
IT["V"] = {'ja': '真空管について: 真空管 (12AU7) は あくまでもプリアンプ段 (電圧増幅 + カソードフォロワ) として設計しています。パワー段は半導体の A級・AB級・A級+AB級で、真空管のパワーアンプ (出力トランス付き) は設計していません。', 'en': 'About the tube: the tube (12AU7) is designed purely as the preamplifier stage (voltage gain plus a cathode follower). The power stage is a solid-state Class A, Class AB or Class A + AB; no tube power amplifier (with an output transformer) is designed.', 'ru': 'О лампе: лампа (12AU7) разработана исключительно как каскад предусилителя (усиление напряжения плюс катодный повторитель). Оконечный каскад — полупроводниковый класса A, AB или A + AB; ламповый усилитель мощности (с выходным трансформатором) не разрабатывался.', 'uk': 'Про лампу: лампа (12AU7) розроблена виключно як каскад попереднього підсилювача (підсилення напруги плюс катодний повторювач). Кінцевий каскад — напівпровідниковий класу A, AB або A + AB; ламповий підсилювач потужності (з вихідним трансформатором) не розроблявся.', 'de': 'Zur Röhre: Die Röhre (12AU7) ist ausschließlich als Vorverstärkerstufe (Spannungsverstärkung plus Kathodenfolger) ausgelegt. Die Endstufe ist ein Halbleiter in Klasse A, Klasse AB oder Klasse A plus AB; ein Röhren-Endverstärker (mit Ausgangsübertrager) wurde nicht entworfen.', 'it': "Sulla valvola: la valvola (12AU7) è progettata esclusivamente come stadio di preamplificazione (guadagno di tensione più inseguitore di catodo). Lo stadio finale è a stato solido in classe A, classe AB o classe A + AB; non è stato progettato alcun amplificatore di potenza a valvole (con trasformatore d'uscita).", 'fr': "À propos du tube : le tube (12AU7) est conçu uniquement comme étage de préamplification (gain en tension plus suiveur de cathode). L'étage de puissance est à semi-conducteurs en classe A, classe AB ou classe A + AB ; aucun amplificateur de puissance à tubes (avec transformateur de sortie) n'est conçu."}
# add British English (en-GB): the existing "en" becomes US English
GB = [("analog", "analogue"), ("a ground plane", "an earth plane"), ("ground plane", "earth plane"), ("Ground", "Earth"), ("ground", "earth"), ("heatsink", "heat sink"), ("energy", "electricity"), ("sub-board", "sub-board"), ("Class AB automatically", "Class AB automatically")]
def to_gb(t):
    for a, b in GB:
        t = t.replace(a, b)
    return t
LANG8 = ["ja", "en", "en-GB", "ru", "uk", "de", "it", "fr"]
NAME8 = dict(NAMES, **{"en": "English (US)", "en-GB": "English (UK)"})
TITLE["en-GB"] = to_gb(TITLE["en"]).replace("Class A and tube versions", "Class A and valve versions").replace("tube", "valve")
INTRO["en-GB"] = to_gb(INTRO["en"])
for k in IT:
    IT[k]["en-GB"] = to_gb(IT[k]["en"]).replace("the tube preamp", "the valve preamp").replace("The tube version", "The valve version").replace("tube version", "valve version")
import re as _re
def _dec(L, t):
    return _re.sub(r"(?<=\d)\.(?=\d)", ",", t) if L in ("ru", "uk", "de", "it", "fr") else t
OUT = SD + r"\v7out"
os.makedirs(OUT, exist_ok=True)
# README in 8 languages
md = ["# VER7 — %s\n" % TITLE["ja"], "Figures: `amp_ver7_sim.jpg` (test / debug, 5 rounds), `amp_ver7_classA_AB.jpg` (Class A + AB), `amp_ver7_classA.jpg` (Class A), `manual-v7.jpg` / `manual-v7.pdf` (8-language manual), `amp_ver7_all.pdf`. The tube version uses `../VER6/amp_ver6_tube.jpg`; the improved Class D uses `../classd-analog/CD-VER2` and `../VER6/amp_ver6_classD.jpg`.\n"]
for L in LANG8:
    md.append("## %s\n" % NAME8[L])
    md.append("**%s**\n" % TITLE[L])
    md.append(INTRO[L] + "\n")
    for k in ("need", "A", "V", "H", "D", "C", "N"):
        md.append("- " + _dec(L, IT[k][L]))
    md.append("")
open(OUT + r"\README.md", "w", encoding="utf-8").write("\n".join(md))
# manual image
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
blocks = []
for L in LANG8:
    lines = [(NAME8[L] + " — VER7", HD)]
    for t in [_dec(L, x) for x in [TITLE[L], INTRO[L]] + [IT[k][L] for k in ("need", "A", "V", "H", "D", "C", "N")]]:
        for ln in wrap(t, REG, colw):
            lines.append((ln, REG))
        lines.append(("", REG))
    blocks.append(lines)
def height(lines): return sum(int(f.size * 1.45) for _, f in lines) + 40
rows = [(blocks[i], blocks[i + 1]) for i in range(0, 8, 2)]
H = 140 + sum(max(height(a), height(b)) for a, b in rows) + pad
img = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(img)
d.text((pad, 40), "VER7 説明書 / Manual — 日本語 · English (US/UK) · Русский · Українська · Deutsch · Italiano · Français", font=BIG, fill=(20, 30, 60))
y = 140
for a, b in rows:
    for col, lines in enumerate((a, b)):
        x, yy = pad + col * (colw + pad), y
        for t, f in lines:
            d.text((x, yy), t, font=f, fill=(20, 30, 60) if f is HD else (40, 40, 40)); yy += int(f.size * 1.45)
    y += max(height(a), height(b))
img.save(OUT + r"\manual-v7.jpg", "JPEG", quality=90, dpi=(300, 300))
img.convert("RGB").save(OUT + r"\manual-v7.pdf", resolution=300)
print(img.size, v)
