def edit(fn, pairs):
    s = open(fn, encoding='utf-8').read()
    for a, b in pairs:
        assert s.count(a) == 1, (fn, a, s.count(a))
        s = s.replace(a, b)
    open(fn, 'w', encoding='utf-8').write(s)


for fn, bal in (('amp_block_body.py', True), ('draw_amp_block_unb.py', False)):
    edit(fn, [
        ('L("Balanced volume", 1.05)' if bal else 'L("Single-ended volume", 1.0)', 'L("触覚ノブ クリック/なし SW6", 0.95)'),
        ('L("デジタルボリューム・EQ・ルームEQ  Volume / EQ  (MQA は右のデコーダへ)", 1.1)', 'L("デジタル Vol/EQ は SW5 でバイパス (ビットパーフェクト)  (MQA は右のデコーダへ)", 1.1)'),
        ('L("XO ×2 + 外部CLK入力", 1.0)', 'L("≤100fs + 外部CLK", 1.0)'),
    ])
s = open('amp_block_body.py', encoding='utf-8').read()
s = s.replace('Network-Streaming Fully Balanced Integrated Amplifier', 'Network-Streaming Fully Balanced Integrated Amplifier  VER3')
open('amp_block_body.py', 'w', encoding='utf-8').write(s)
s = open('draw_amp_block_unb.py', encoding='utf-8').read()
s = s.replace('Network-Streaming Unbalanced Integrated Amplifier', 'Network-Streaming Unbalanced Integrated Amplifier  VER3')
open('draw_amp_block_unb.py', 'w', encoding='utf-8').write(s)
edit('fig_fg_body.py', [('L("ボリューム", 1.2, True), L("電子 / ALPS", 1.0), L("バランス調整", 0.95)', 'L("ボリューム", 1.2, True), L("電子 / リレー式", 0.95), L("触覚ノブ SW6", 0.95)')])
s = open('fig_fg_body.py', encoding='utf-8').read()
s = s.replace('Analog integrated amplifier - solid-state preamp version', 'Analog integrated amplifier - solid-state preamp version  VER3').replace('Analog integrated amplifier - vacuum-tube preamp version', 'Analog integrated amplifier - vacuum-tube preamp version  VER3')
open('fig_fg_body.py', 'w', encoding='utf-8').write(s)
edit('fig_d_body.py', [('L("ボリューム", 1.1, True), L("50kΩ (ALPS)", 1.0)', 'L("ボリューム", 1.1, True), L("リレー式 ATT + 触覚ノブ", 0.9)')])
edit('fig_b_body.py', [('hcap(67, 50, "C1", "33p", ANA)', 'hcap(67, 50, "C1", "68p", ANA)')])
s = open('fig_b_body.py', encoding='utf-8').read()
s = s.replace('(Cdom 33pF)', '(Cdom 68pF)')
open('fig_b_body.py', 'w', encoding='utf-8').write(s)
s = open('analog_text.py', encoding='utf-8').read()
s = s.replace('Cdom 33pF', 'Cdom 68pF').replace('Cdom 33 pF', 'Cdom 68 pF')
open('analog_text.py', 'w', encoding='utf-8').write(s)
print('ok')
