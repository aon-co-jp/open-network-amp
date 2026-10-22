s = open("v7_hpstrip.py", encoding="utf-8").read(); n = 0
pairs = [
 ("アナログゲイン 0 / +6 / +12 / +18dB (またはデジタルゲイン)", "1dB 刻みのゲイン (ANALOG / DIGITAL / ANALOG+DIGITAL の 3 モード。スピーカー用とヘッドホン用に 2 個)"),
 ("an analog gain of 0 / +6 / +12 / +18 dB (or a digital gain)", "a gain in 1 dB steps (three modes: ANALOG / DIGITAL / ANALOG + DIGITAL; two controls, one for the speakers and one for the headphones)"),
 ("аналоговое усиление 0 / +6 / +12 / +18 дБ (или цифровое)", "усиление с шагом 1 дБ (три режима: ANALOG / DIGITAL / ANALOG + DIGITAL; два регулятора — для колонок и для наушников)"),
 ("аналогове підсилення 0 / +6 / +12 / +18 дБ (або цифрове)", "підсилення з кроком 1 дБ (три режими: ANALOG / DIGITAL / ANALOG + DIGITAL; два регулятори — для колонок і для навушників)"),
 ("analoge Verstärkung von 0 / +6 / +12 / +18 dB (oder eine digitale)", "Verstärkung in 1-dB-Schritten (drei Modi: ANALOG / DIGITAL / ANALOG + DIGITAL; zwei Regler, einer für die Lautsprecher und einer für die Kopfhörer)"),
 ("guadagno analogico di 0 / +6 / +12 / +18 dB (o digitale)", "guadagno a passi di 1 dB (tre modi: ANALOG / DIGITAL / ANALOG + DIGITAL; due controlli, uno per i diffusori e uno per le cuffie)"),
 ("gain analogique de 0 / +6 / +12 / +18 dB (ou numérique)", "gain par pas de 1 dB (trois modes : ANALOG / DIGITAL / ANALOG + DIGITAL ; deux commandes, une pour les enceintes et une pour le casque)"),
 ('"アナログゲイン 0 / +6 / +12 / +18 dB (リレー)", "またはデジタルゲイン (±0.5 dB)"', '"ゲイン 1dB 刻み: ANALOG / DIGITAL / ANALOG+DIGITAL", "スピーカー用・ヘッドホン用に 2 個 (独立)"'),
 ("SW7 = ANALOG / DIGITAL ゲイン。", "ゲイン 1dB 刻み 3 モード (HP-VER3)。"),
 ("SW7 = analog / digital gain.", "Gain in 1 dB steps, three modes (HP-VER3)."),
]
for a, b in pairs:
    if a in s:
        s = s.replace(a, b); n += 1
    else:
        print("MISSING", a[:40])
open("v7_hpstrip.py", "w", encoding="utf-8").write(s)
print(n, "of", len(pairs))
