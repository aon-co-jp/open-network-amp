import ast
# ---- 1) HP-VER4 build script (from the HP-VER3 one)
s = open("hp3_build.py", encoding="utf-8").read()
s = s.replace("ona/headphone/HP-VER3", "ona/headphone/HP-VER4").replace("headphone-hp3-all.pdf", "headphone-hp4-all.pdf").replace("manual-hp3", "manual-hp4").replace("HP-VER3", "HP-VER4")
s = s.replace('exec(open(SD + "/g3_texts.py", encoding="utf-8").read())\nT.update(T_G3)\nV.update(GV)', 'exec(open(SD + "/g4_texts.py", encoding="utf-8").read())\nT.update(T_G4)\nV.update(GV4)')
s = s.replace("amp_gain3", "amp_gain4").replace('["g3", "rest"]', '["g4", "rest"]').replace('["g3sim", "g3"]', '["g4sim", "g4"]')
s = s.replace('["title", "g3", "g3sim", "jacks", "sw", "pin", "rest"]', '["title", "g4", "g4sim", "jacks", "sw", "pin", "rest"]').replace('for k in ("g3", "g3sim", "jacks", "sw", "pin", "rest"):', 'for k in ("g4", "g4sim", "jacks", "sw", "pin", "rest"):')
s = s.replace("ゲインと音量の調整 (各 1dB 刻み・3 モード・スピーカー出力とヘッドホン出力の両方) つきヘッドホンアンプ", "音量と低音・高音の 2 種のゲイン (各 1dB 刻み・3 モード・スピーカー出力とヘッドホン出力の両方) つきヘッドホンアンプ")
s = s.replace("(gain and volume control in 1 dB steps with three modes, on both the speaker and the headphone outputs: four controls)", "(volume and two gains, low-frequency and high-frequency, in 1 dB steps with three modes, on both the speaker and the headphone outputs: six controls)")
s = s.replace("HP-VER4 ゲインと音量の調整", "HP-VER4 音量・低音ゲイン・高音ゲイン")
ast.parse(s)
open("hp4_build.py", "w", encoding="utf-8").write(s)
# ---- 2) strips of the VER7 figures
h = open("v7_hpstrip.py", encoding="utf-8").read(); n = 0
pairs = [
 ("ゲインと音量 (各 1dB 刻み・ANALOG / DIGITAL / ANALOG+DIGITAL の 3 モード。スピーカー用とヘッドホン用の両方)", "音量と、低い音・高い音の 2 種のゲイン (各 1dB 刻み・ANALOG / DIGITAL / ANALOG+DIGITAL の 3 モード。スピーカー用とヘッドホン用の両方)"),
 ("gain and volume controls in 1 dB steps (three modes: ANALOG / DIGITAL / ANALOG + DIGITAL; for both the speakers and the headphones)", "a volume control and two gains, low-frequency and high-frequency, in 1 dB steps (three modes: ANALOG / DIGITAL / ANALOG + DIGITAL; for both the speakers and the headphones)"),
 ("регуляторы усиления и громкости с шагом 1 дБ (три режима: ANALOG / DIGITAL / ANALOG + DIGITAL; и для колонок, и для наушников)", "регулятор громкости и два усиления — низких и высоких частот — с шагом 1 дБ (три режима: ANALOG / DIGITAL / ANALOG + DIGITAL; и для колонок, и для наушников)"),
 ("регулятори підсилення та гучності з кроком 1 дБ (три режими: ANALOG / DIGITAL / ANALOG + DIGITAL; і для колонок, і для навушників)", "регулятор гучності та два підсилення — низьких і високих частот — з кроком 1 дБ (три режими: ANALOG / DIGITAL / ANALOG + DIGITAL; і для колонок, і для навушників)"),
 ("Verstärkungs- und Lautstärkeregler in 1-dB-Schritten (drei Modi: ANALOG / DIGITAL / ANALOG + DIGITAL; für Lautsprecher und Kopfhörer)", "ein Lautstärkeregler und zwei Verstärkungen, für Tiefen und für Höhen, in 1-dB-Schritten (drei Modi: ANALOG / DIGITAL / ANALOG + DIGITAL; für Lautsprecher und Kopfhörer)"),
 ("controlli di guadagno e volume a passi di 1 dB (tre modi: ANALOG / DIGITAL / ANALOG + DIGITAL; per diffusori e cuffie)", "un controllo del volume e due guadagni, per i bassi e per gli alti, a passi di 1 dB (tre modi: ANALOG / DIGITAL / ANALOG + DIGITAL; per diffusori e cuffie)"),
 ("commandes de gain et de volume par pas de 1 dB (trois modes : ANALOG / DIGITAL / ANALOG + DIGITAL ; pour les enceintes et le casque)", "une commande de volume et deux gains, pour les graves et pour les aigus, par pas de 1 dB (trois modes : ANALOG / DIGITAL / ANALOG + DIGITAL ; pour les enceintes et le casque)"),
 ('"ゲインと音量 各 1dB 刻み: ANALOG / DIGITAL / A+D", "スピーカー用・ヘッドホン用の両方 (計 4 個)"', '"音量 + 低音ゲイン + 高音ゲイン (各 1dB 刻み)", "ANALOG / DIGITAL / A+D・スピーカー用とヘッドホン用 (計 6 個)"'),
 ("ゲイン・音量 1dB 刻み 3 モード (HP-VER3)。", "音量・低音ゲイン・高音ゲイン 各 1dB 刻み 3 モード (HP-VER4)。"),
 ("Gain and volume in 1 dB steps, three modes (HP-VER3).", "Volume, low-frequency gain and high-frequency gain in 1 dB steps, three modes (HP-VER4)."),
]
for a, b in pairs:
    if a in h:
        h = h.replace(a, b); n += 1
    else:
        print("MISSING", a[:40])
h = h.replace("HP-VER3", "HP-VER4")
open("v7_hpstrip.py", "w", encoding="utf-8").write(h)
print(n, "of", len(pairs))
# ---- 3) AV amplifier SV-VER9
b = open("surround_v8_block_body.py", encoding="utf-8").read()
b = b.replace("SV-VER8", "SV-VER9").replace("surround_v8_%s.jpg", "surround_v9_%s.jpg").replace("HP-VER3", "HP-VER4")
b = b.replace('L("ゲイン・音量 各 1dB 刻み 3 モード", 0.85)', 'L("音量・低音/高音ゲイン 各 1dB 3 モード", 0.85)')
b = b.replace('L("I/V → LPF → 音量・ゲイン → バッファ", 1.1, True)', 'L("I/V → LPF → 音量・低音/高音ゲイン → バッファ", 1.05, True)')
b = b.replace("音量・ゲインは 1dB 刻み 3 モード (ANALOG / DIGITAL / A+D)", "音量・低音ゲイン・高音ゲイン 各 1dB 刻み 3 モード")
b = b.replace("ゲインと音量はスピーカー用・ヘッドホン用 各 1dB 刻み 3 モード", "音量と低音/高音ゲインはスピーカー用・ヘッドホン用 各 1dB 刻み 3 モード (計 6 個)")
open("surround_v9_block_body.py", "w", encoding="utf-8").write(b)
t = open("sv8_texts_add.py", encoding="utf-8").read()
t = t.replace("g3_texts.py", "g4_texts.py").replace('T["g3"] = T_G3["g3"]', 'T["g4"] = T_G4["g4"]').replace("HP-VER3", "HP-VER4")
t = t.replace("ゲインと音量は 1dB 刻み・3 モードで調整でき (下記)", "音量と低音・高音の 2 種のゲインは 1dB 刻み・3 モードで調整でき (下記)")
t = t.replace("Gain and volume are adjusted in 1 dB steps with three modes (see below)", "The volume and two gains (low and high) are adjusted in 1 dB steps with three modes (see below)")
open("sv9_texts_add.py", "w", encoding="utf-8").write(t)
sb = open("sv8_build.py", encoding="utf-8").read()
sb = sb.replace("SV-VER8", "SV-VER9").replace("surround_v8_", "surround_v9_").replace("manual-sv8", "manual-sv9").replace("avamp/SV-VER8", "avamp/SV-VER9").replace("surround-av-amp-v8", "surround-av-amp-v9").replace("sv8_texts_add.py", "sv9_texts_add.py").replace('"g3"', '"g4"').replace("HP-VER3", "HP-VER4")
open("sv9_build.py", "w", encoding="utf-8").write(sb)
print("done")
