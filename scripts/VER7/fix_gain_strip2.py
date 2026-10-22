s = open("v7_hpstrip.py", encoding="utf-8").read(); n = 0
pairs = [
 ("1dB 刻みのゲイン (ANALOG / DIGITAL / ANALOG+DIGITAL の 3 モード。スピーカー用とヘッドホン用に 2 個)", "ゲインと音量 (各 1dB 刻み・ANALOG / DIGITAL / ANALOG+DIGITAL の 3 モード。スピーカー用とヘッドホン用の両方)"),
 ("a gain in 1 dB steps (three modes: ANALOG / DIGITAL / ANALOG + DIGITAL; two controls, one for the speakers and one for the headphones)", "gain and volume controls in 1 dB steps (three modes: ANALOG / DIGITAL / ANALOG + DIGITAL; for both the speakers and the headphones)"),
 ("усиление с шагом 1 дБ (три режима: ANALOG / DIGITAL / ANALOG + DIGITAL; два регулятора — для колонок и для наушников)", "регуляторы усиления и громкости с шагом 1 дБ (три режима: ANALOG / DIGITAL / ANALOG + DIGITAL; и для колонок, и для наушников)"),
 ("підсилення з кроком 1 дБ (три режими: ANALOG / DIGITAL / ANALOG + DIGITAL; два регулятори — для колонок і для навушників)", "регулятори підсилення та гучності з кроком 1 дБ (три режими: ANALOG / DIGITAL / ANALOG + DIGITAL; і для колонок, і для навушників)"),
 ("Verstärkung in 1-dB-Schritten (drei Modi: ANALOG / DIGITAL / ANALOG + DIGITAL; zwei Regler, einer für die Lautsprecher und einer für die Kopfhörer)", "Verstärkungs- und Lautstärkeregler in 1-dB-Schritten (drei Modi: ANALOG / DIGITAL / ANALOG + DIGITAL; für Lautsprecher und Kopfhörer)"),
 ("guadagno a passi di 1 dB (tre modi: ANALOG / DIGITAL / ANALOG + DIGITAL; due controlli, uno per i diffusori e uno per le cuffie)", "controlli di guadagno e volume a passi di 1 dB (tre modi: ANALOG / DIGITAL / ANALOG + DIGITAL; per diffusori e cuffie)"),
 ("gain par pas de 1 dB (trois modes : ANALOG / DIGITAL / ANALOG + DIGITAL ; deux commandes, une pour les enceintes et une pour le casque)", "commandes de gain et de volume par pas de 1 dB (trois modes : ANALOG / DIGITAL / ANALOG + DIGITAL ; pour les enceintes et le casque)"),
 ('"ゲイン 1dB 刻み: ANALOG / DIGITAL / ANALOG+DIGITAL", "スピーカー用・ヘッドホン用に 2 個 (独立)"', '"ゲインと音量 各 1dB 刻み: ANALOG / DIGITAL / A+D", "スピーカー用・ヘッドホン用の両方 (計 4 個)"'),
 ("ゲイン 1dB 刻み 3 モード (HP-VER3)。", "ゲイン・音量 1dB 刻み 3 モード (HP-VER3)。"),
 ("Gain in 1 dB steps, three modes (HP-VER3).", "Gain and volume in 1 dB steps, three modes (HP-VER3)."),
 ("HP-VER2 ヘッドホン段", "HP-VER3 ヘッドホン段"),
]
for a, b in pairs:
    if a in s:
        s = s.replace(a, b); n += 1
    else:
        print("MISSING", a[:40])
s = s.replace("HP-VER2", "HP-VER3")
open("v7_hpstrip.py", "w", encoding="utf-8").write(s)
print(n, "of", len(pairs))
