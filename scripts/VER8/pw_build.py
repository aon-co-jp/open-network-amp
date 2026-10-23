import os, re, shutil
from PIL import Image, ImageDraw, ImageFont
SD = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
exec(open(SD + "/pw_texts.py", encoding="utf-8").read())
dec = lambda L, t: re.sub(r"(?<=\d)\.(?=\d)", ",", t) if L in ("ru", "uk", "de", "it", "fr") else t
W, pad = 3200, 60
colw = (W - 3 * pad) // 2
REG = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 34)
HD = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", 40)
BIG = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", 51)
TOK = re.compile(r"[\x21-\x7e\u00a0-\u024f\u0400-\u04ff]+|\s|.", re.S)
def wrap(t, font, width):
    out, cur = [], ""
    for tk in TOK.findall(t):
        if font.getlength(cur + tk) > width and cur.strip():
            out.append(cur.rstrip()); cur = tk.lstrip()
        else:
            cur += tk
    out.append(cur.rstrip()); return out
hh = lambda lines: sum(int(f.size * 1.45) for _, f in lines) + 40
def panel(keys, heading):
    blocks = []
    for L in LANG8:
        lines = [(NAME8[L], HD)]
        for k in keys:
            t = dec(L, TITLE[L]) if k == "title" else dec(L, T[k][L])
            for ln in wrap(t, REG, colw): lines.append((ln, REG))
            lines.append(("", REG))
        blocks.append(lines)
    rows = [(blocks[i], blocks[i + 1]) for i in range(0, 8, 2)]
    TH = 140 + sum(max(hh(a), hh(b)) for a, b in rows) + pad
    im = Image.new("RGB", (W, TH), "white"); d = ImageDraw.Draw(im)
    d.text((pad, 40), heading, font=BIG, fill=(20, 30, 60))
    y = 140
    for a, b in rows:
        for col, lines in enumerate((a, b)):
            x, yy = pad + col * (colw + pad), y
            for t, f in lines:
                d.text((x, yy), t, font=f, fill=(20, 30, 60) if f is HD else (40, 40, 40)); yy += int(f.size * 1.45)
        y += max(hh(a), hh(b))
    return im
def build(D, label):
    os.makedirs(D + "/figures-only", exist_ok=True)
    shutil.copy(SD + "/power_input.jpg", D + "/figures-only/power_input.jpg")
    fig = Image.open(SD + "/power_input.jpg").convert("RGB")
    fig = fig.resize((W, int(fig.height * W / fig.width)))
    p = panel(["pw", "neg", "con", "eff", "rest"], label + " 電源入力 — 説明 / Explanation (8 languages)")
    im = Image.new("RGB", (W, fig.height + p.height), "white"); im.paste(fig, (0, 0)); im.paste(p, (0, fig.height))
    im.save(D + "/power_input.jpg", "JPEG", quality=88, dpi=(300, 300))
    man = panel(["title", "pw", "neg", "con", "eff", "rest"], label + " 説明書 / Manual (8 languages)")
    man.save(D + "/manual-power.jpg", "JPEG", quality=90, dpi=(300, 300)); man.save(D + "/manual-power.pdf", resolution=300)
    ims = [Image.open(D + "/" + n).convert("RGB") for n in ("power_input.jpg", "manual-power.jpg")]
    ims[0].save(D + "/power-input-all.pdf", save_all=True, append_images=ims[1:], resolution=300)
    md = ["# %s — %s\n" % (label, TITLE["ja"]),
          "\n> Translation note / 翻訳について: the texts other than Japanese were written by an AI and have NOT been checked by human native speakers. 日本語以外の文章は AI が書いたもので、ネイティブスピーカー (人間) による確認は未実施です。\n",
          "\n> Status / 位置づけ: a design proposal (concept). Patentability, prior art, laws, safety and EMC have not been verified, and no prototype exists. 設計案 (概念) です。特許性・先行技術・法規・安全・EMC は未確認で、試作もありません。\n",
          "\nFigures: `power_input.jpg` (the diagram with the 8-language explanation below it; the bare diagram is in `figures-only/`), `manual-power.jpg` / `manual-power.pdf`, `power-input-all.pdf`, and the detailed Japanese note `power-input-design-ja.md` (procedure, claim-style statements, prior-art leads, issues).\n"]
    for L in LANG8:
        md.append("## %s\n" % NAME8[L]); md.append("**%s**\n" % dec(L, TITLE[L]))
        for k in ("pw", "neg", "con", "eff", "rest"):
            md.append("- " + dec(L, T[k][L]))
        md.append("")
    open(D + "/README.md", "w", encoding="utf-8").write("\n".join(md))
    shutil.copy(SD + "/power-input-design-ja.md", D + "/power-input-design-ja.md")
    print(D, "done")
build(SD + "/ona/VER8", "VER8")
build(SD + "/avamp/SV-VER10", "SV-VER10")
