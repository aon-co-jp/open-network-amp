import re
def load(fn):
    g = {}
    exec(open(fn, encoding='utf-8').read(), g)
    return g
A, N, S, V = load('amp_text.py'), load('analog_text.py'), load('sum_blocks.py'), load('v5_text.py')
def clean(t):
    t = re.sub(r'「平衡」の表記はすべて「バランス」に統一しました。', '', t)
    t = re.sub(r'The (word|term)[^.]*balanced[^.]*Japanese[^.]*\.', '', t)
    return t.replace('平衡', 'バランス')
def md(t):
    out = []
    for ln in t.split('\n'):
        out.append('### ' + ln[1:] if ln.startswith('#') else ln)
    return '\n'.join(out)
def figs(caps): return '\n'.join('- %s — `%s`' % (c, f) for c, f in caps)
note = {
 1: 'VER1', 2: 'VER2', 3: 'VER3', 4: 'VER4'}
def older(n):
    head = '# VER%d — 説明 / Explanation\n\n' % n
    if n < 4:
        head += ('> 注: VER%d の図(JPG/PDF)の中の説明は画像で、文字として読めませんでした。下は、VER1〜VER4 の説明を集約した最新(VER4)の文章です。後の版で加わった機能 (VER3 以降の触覚ボリューム、VER4 のヘッドホンアンプなど) は、この版には含まれないことがあります。\n'
                 '> Note: the explanation inside the VER%d figures is part of the images and not machine-readable. Below is the consolidated text of VER4, the newest of the older versions; features added later (the haptic volume from VER3, the headphone amplifier of VER4) may not be part of this version.\n\n' % (n, n))
    body = '## ストリーミング / Streaming amplifier (`streaming-amp`)\n\n## 日本語\n\n' + md(A['AMP_JA']) + '\n\n## English\n\n' + md(A['AMP_EN']) + '\n\n### 図 / Figures\n' + figs(A['CAPS'])
    body += '\n\n## アナログ / Analog amplifier (`analog-amp`)\n\n## 日本語\n\n' + md(N['INTRO_JA']) + '\n\n## English\n\n' + md(N['INTRO_EN'])
    body += '\n\n### 図 / Figures\n' + '\n'.join('- %s — `%s`\n  - %s\n  - %s' % (f[1], f[0], f[2], f[3]) for f in N['FIGS'])
    body += '\n\n## まとめ / Summary\n\n' + md(S['SUM_JA']) + '\n\n' + md(S['SUM_EN'])
    return clean(head + body) + '\n'
for n in (1, 2, 3, 4):
    open('ona/VER%d/README.md' % n, 'w', encoding='utf-8').write(older(n))
# VER5
L = {'ja': '日本語', 'en': 'English', 'de': 'Deutsch', 'ru': 'Русский'}
o = '# VER5 — 説明 / Explanation / Erklärung / Описание\n\n詳しい説明書は [`manual/`](manual) の JPG・PDF と、リポジトリ直下の README にあります。\n\n'
for k in ('ja', 'en', 'de', 'ru'):
    o += '## %s\n\n%s\n\n' % (L[k], md(V['SUMMARY'][k]))
o += '## 図の説明 / Figure captions\n\n'
seen = set()
for k, st in V['SETS'].items():
    for fn in st['files']:
        if fn in seen or fn not in V['CAP']: continue
        seen.add(fn)
        o += '### `%s`\n' % fn + '\n'.join('- **%s**: %s' % (kk, V['CAP'][fn][kk]) for kk in ('ja', 'en', 'de', 'ru')) + '\n\n'
open('ona/VER5/README.md', 'w', encoding='utf-8').write(clean(o))
