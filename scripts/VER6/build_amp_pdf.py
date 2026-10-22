exec(open('build_head.py', encoding='utf-8').read())
exec(open('amp_text.py', encoding='utf-8').read())
pages.clear()
new_page()
for para in AMP_JA.split(chr(10)) + [""] + AMP_EN.split(chr(10)):
    if not para.strip():
        y += int(FS * 0.8)
        continue
    if para.startswith("#"):
        y += int(FS * 0.5)
        put(para[1:], HD, gap=0.3)
    elif para.startswith("- "):
        put(para[2:], REG, bullet=True, gap=0.3)
    else:
        put(para, REG, gap=0.6)
NM = 110
for cap, fn in CAPS:
    fig = Image.open(SD + "\\" + fn).convert("RGB")
    m = 24
    base = Image.new("RGB", (fig.width + 2 * m, fig.height + 2 * m + int(FS * 3)), "white")
    ImageDraw.Draw(base).text((NM, m), cap, font=HD, fill=(20, 30, 60))
    base.paste(fig, (m, m + int(FS * 2.4)))
    base = base.resize((int(11.69 * DPI), int(base.height * (11.69 * DPI) / base.width)))
    pages.append(base)
out = SD + r"\streaming-integrated-amp.pdf"
pages[0].save(out, "PDF", resolution=DPI, save_all=True, append_images=pages[1:])
print(out, len(pages), [p.size for p in pages])
