import os
SD = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
exec(open(SD + r"\manual_text.py", encoding="utf-8").read())
src = open(SD + r"\compose_v5.py", encoding="utf-8").read()
src = src.split("def build(")[0]
exec(src)
# manual page JPG / PDF
L, h1, h2 = grid_height(MANUAL)
tmp = ImageDraw.Draw(Image.new("RGB", (W, 10), "white"))
y = pad
for k in LANGS:
    tmp.text((pad, y), TITLE[k], font=HD, fill=INK)
    y += int(HD.size * 1.5)
top = y + int(FS * 0.6)
im = Image.new("RGB", (W, top + h1 + h2 + int(FS * 0.6) + pad), "white")
d = ImageDraw.Draw(im)
y = pad
for k in LANGS:
    d.text((pad, y), TITLE[k], font=HD, fill=(60, 80, 150))
    y += int(HD.size * 1.5)
draw_grid(d, top, L, h1, h2)
outdir = SD + r"\site\manual"
os.makedirs(outdir, exist_ok=True)
im.save(outdir + r"\manual-v5.jpg", "JPEG", quality=88, dpi=(300, 300))
im.save(outdir + r"\manual-v5.pdf", "PDF", resolution=3200 / 11.69)
print("manual", im.size)
# README.md (four languages)
nr = SD + r"\newrepo"
os.makedirs(nr, exist_ok=True)
parts = ["# Integrated amplifier — VER5 (design files)\n",
         "Fully balanced and unbalanced integrated amplifiers with a haptic hybrid volume knob, DDC + DAC, headphone amplifier and dedicated mono subwoofer terminals (RCA + XLR).\n",
         "Reference designs only (Python calculations, not bench measurements). See https://audiocafe.tokyo/ for the figures, PDF and JPG files.\n",
         "Languages: [日本語](#ja) · [English](#en) · [Deutsch](#de) · [Русский](#ru)\n"]
for k, nm in (("ja", "日本語"), ("en", "English"), ("de", "Deutsch"), ("ru", "Русский")):
    parts.append('\n<a id="%s"></a>\n## %s\n\n### %s\n' % (k, nm, TITLE[k]))
    for line in MANUAL[k].split("\n"):
        if line.startswith("#"):
            parts.append("\n#### " + line[1:] + "\n")
        else:
            parts.append(line + "\n")
parts.append("\n## Files\n\n- `streaming-amp/`, `analog-amp/`, `mono-sub-out/`, `manual/`: JPG and PDF (Japanese / English / German / Russian explanations inside).\n")
open(nr + r"\README.md", "w", encoding="utf-8").write("".join(parts))
print("README", len("".join(parts)))
