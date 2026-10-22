pairs = [
 # Russian
 ("пики до около", "пики примерно до"), ("как небольшой обогреватель", "как у небольшого обогревателя"),
 ("Два выходных прибора параллельно", "Два выходных транзистора включены параллельно"), ("на прибор.", "на транзистор."),
 ("не нуждается в токе смещения", "не нуждается в токе покоя"), ("самовозбуждающийся усилитель класса D", "самоколебательный усилитель класса D"),
 ("снижает пик на 16 Ом с 7,6 дБ до 0,7 дБ", "снижает пик АЧХ на нагрузке 16 Ом с 7,6 дБ до 0,7 дБ"),
 ("внешний линейный блок питания постоянного тока (R-сердечник)", "внешний линейный источник питания постоянного тока (с R-образным сердечником)"),
 ("в одну сторону от входа к выходу по пути около 40 мм над слоем земли", "в одном направлении от входа к выходу по трассе около 40 мм над сплошным слоем земли (земляным полигоном)"),
 ("блокировочные 0,1 мкФ в пределах 2 мм от прибора", "блокировочные конденсаторы 0,1 мкФ не далее 2 мм от каждого прибора"),
 ("резисторы 0,1 % тонкоплёночные на входе", "тонкоплёночные резисторы 0,1 % на входе"),
 ("пульсирующим током не более 50 %", "током пульсаций не более 50 % от допустимого"), ("электролиты на 63 В", "электролитические конденсаторы на 63 В"),
 ("измерения на устройстве", "измерения на образце"), ("Класс D не всегда звучит лучше.", "Класс D не обязательно звучит лучше."),
 ("Для экономии добавлен", "Для экономии электроэнергии добавлен"),
 ("тонкоплёночные 0,1 % и C0G / плёночные детали", "тонкоплёночные резисторы 0,1 % и конденсаторы C0G / плёночные"),
 ("Шины силового каскада — нестабилизированные батареи больших конденсаторов; аналоговая часть и такт — малошумящие линейные", "Шины питания выходного каскада — нестабилизированные, с батареями больших конденсаторов; питание аналоговой части и тактового генератора — малошумящее линейное"),
 ("в духе 4DX как в SV-VER1", "в стиле 4DX — как в SV-VER1"), ("AV-ресивер объёмного звука", "AV-усилитель объёмного звука"),
 ("Фильмы идут от тихого до громкого", "Фильмы идут от тихих сцен до громких"), ("выделяет лишь около", "рассеивает лишь около"),
 ("сигнал в одну сторону около 40 мм, слой земли", "сигнал идёт в одном направлении по трассе около 40 мм, земляной полигон"),
 ("0,1 мкФ в пределах 2 мм,", "блокировочные конденсаторы 0,1 мкФ в пределах 2 мм,"), ("Не выполнено: измерения, сертификация HDMI", "Не выполнено: измерения на образце, сертификация HDMI"),
 # Ukrainian
 ("шляхом близько 40 мм над шаром землі", "трактом завдовжки близько 40 мм над земляною площиною"),
 ("блокувальні 0,1 мкФ у межах 2 мм від приладу", "блокувальні конденсатори 0,1 мкФ не далі ніж за 2 мм від кожного приладу"),
 ("Два вихідні прилади паралельно", "Два вихідні транзистори паралельно"), ("термічно пов'язаний із радіатором", "перебуває в тепловому контакті з радіатором"),
 ("не SPICE і не вимірювання", "не SPICE-моделювання і не вимірювання"), ("(тип Eigentakt)", "(типу Eigentakt)"),
 ("блок живлення постійного струму (R-осердя)", "блок живлення постійного струму (з R-осердям)"),
 ("електроліти на 63 В зі струмом пульсацій не більше 50 %", "електролітичні конденсатори на 63 В зі струмом пульсацій не більше 50 % від допустимого"),
 ("Клас D не завжди звучить краще", "Клас D не обов'язково звучить краще"), ("від тихої до робочої гучності", "від тихої до практичної гучності"),
 ("дві колонки", "два гучномовці"), ("Не виконано: вимірювання на пристрої", "Не виконано: вимірювання на реальному зразку"),
 ("AV-ресивер об'ємного звуку", "AV-підсилювач об'ємного звучання"), ("Фільми йдуть від тихого до гучного", "Фільми містять і тихі, і гучні сцени"),
 ("використовують покращений аналоговий клас D із VER7", "виконано за схемою покращеного аналогового класу D із VER7"),
 ("сигнал в один бік близько 40 мм, шар землі", "тракт сигналу односпрямований, завдовжки близько 40 мм, земляна площина"),
 ("0,1 мкФ у межах 2 мм,", "конденсатори 0,1 мкФ не далі ніж 2 мм від виводів,"), ("тонкоплівкові 0,1 % і C0G / плівкові деталі", "тонкоплівкові резистори 0,1 % і конденсатори C0G / плівкові"),
 ("електроліти на 63 В в окремому", "електролітичні конденсатори на 63 В в окремому"), ("аналогова частина та такт — малошумні лінійні", "аналогова частина та тактовий генератор живляться від малошумних лінійних стабілізаторів"),
 ("в дусі 4DX як у SV-VER1", "в стилі 4DX залишено такими ж, як у SV-VER1"), ("Не виконано: вимірювання, сертифікація", "Не виконано: вимірювання на реальному зразку, сертифікація"),
 # German
 ("Die Ruhewärme beträgt", "Die Ruheverlustleistung beträgt"), ("je Transistor", "je Ausgangstransistor"), ("(etwas lauter, im Mittel etwa 85 dB)", "(recht laut, im Mittel etwa 85 dB)"),
 ("Ein Schalter BIAS ECO (0,75 A, etwa 2 W, halbe Wärme)", "Ein Umschalter BIAS ECO (0,75 A, etwa 2 W, halbe Verlustleistung)"),
 ("braucht keinen Ruhestrom, um den Klang zu halten; die Ruhewärme", "braucht keinen hohen Ruhestrom, um die Klangqualität zu sichern; die Ruheverlustleistung"),
 ("liegt die Stereowärme bei etwa", "beträgt die Verlustleistung stereo etwa"), ("(R-Kern) verwendet.", "(R-Kern-Trafo) verwendet."),
 ("Das Signal läuft einseitig vom Eingang zum Ausgang über etwa 40 mm", "Das Signal läuft in nur einer Richtung vom Eingang zum Ausgang auf einer Strecke von etwa 40 mm"),
 ("höchstens 2 mm vom Bauteil;", "höchstens 2 mm vom Bauteil entfernt;"), ("Einschalten mit NTC und Relais, Gleichstromblocker", "Einschaltstrombegrenzung mit NTC und Relais, DC-Blocker"),
 ("von leise bis praxisgerechter Lautstärke", "von leise bis zu praxisgerechter Lautstärke"),
 ("Alle 11 Kanäle verwenden das verbesserte analoge Klasse D von VER7", "Alle 11 Kanäle verwenden den verbesserten analogen Klasse-D-Verstärker von VER7"),
 ("ist an den Ansatz von VER7 angeglichen", "wurde an den Ansatz von VER7 angeglichen"), ("einseitiger Signalfluss über etwa 40 mm", "Signalfluss in nur einer Richtung auf etwa 40 mm"),
 ("0,1 µF innerhalb von 2 mm,", "0,1 µF innerhalb von 2 mm vom Bauteil,"),
 ("Die Endstufenschienen sind ungeregelte große Kondensatorbänke; Analog und Takt sind rauscharm linear", "Die Endstufen-Versorgungsschienen werden aus ungeregelten, großen Kondensatorbänken gespeist; Analogteil und Takt werden rauscharm linear versorgt"),
 ("Eine IMAX-Enhanced-, Dolby- oder DTS-Zertifizierung liegt nicht vor", "Eine Zertifizierung für IMAX Enhanced, Dolby und DTS liegt nicht vor"), ("gibt der ganze Verstärker bei", "gibt der gesamte Verstärker bei"),
 # Italian
 ("finché la corrente d'uscita raggiunge", "finché la corrente di uscita non raggiunge"), ("con polarizzazione di 1,5 A per canale", "con corrente di polarizzazione (bias) di 1,5 A per canale"),
 ("con una polarizzazione alta di 0,75 A", "con una corrente di polarizzazione elevata di 0,75 A"), ("il doppio della polarizzazione", "il doppio della corrente di polarizzazione"),
 ("è il pre a valvole", "è il preamplificatore a valvole"), ("ventola a controllo di temperatura", "ventola a regolazione termica"), ("e transistor di polarizzazione accoppiato", "e il transistor di polarizzazione accoppiato"),
 ("un classe D autooscillante", "un amplificatore in classe D autooscillante"), ("non richiede polarizzazione per mantenere il suono", "non richiede una corrente di polarizzazione elevata per mantenere la qualità del suono"),
 ("Uno Zobel nel filtro d'uscita", "Una rete di Zobel nel filtro di uscita"), ("l'alimentatore esterno lineare in continua", "l'alimentatore lineare esterno in corrente continua"),
 ("condensatori di bypass da 0,1 µF", "condensatori di disaccoppiamento da 0,1 µF"), ("cavo in continua da 6 mm² lungo 0,8 m", "cavo di alimentazione in c.c. da 6 mm², lungo 0,8 m"),
 ("corrente di ripple al massimo al 50%", "corrente di ripple non superiore al 50% del valore nominale,"), ("blocco della continua", "blocco della componente continua (DC blocker)"),
 ("misure sul dispositivo", "misure su banco"), ("prove di sicurezza", "prove di conformità alle norme di sicurezza"),
 ("alimentatore esterno lineare con nucleo R", "alimentatore lineare esterno con nucleo R"), ("I film vanno dal volume basso a quello alto", "I film spaziano dai volumi bassi a quelli alti"),
 ("Le linee dello stadio di potenza sono banchi di condensatori non stabilizzati; analogico e clock sono lineari a basso rumore", "Le linee di alimentazione dello stadio di potenza sono non stabilizzate, con grandi banchi di condensatori; le alimentazioni dell'analogico e del clock sono lineari a basso rumore"),
 ("elettrolitici da 63 V in un contenitore", "condensatori elettrolitici da 63 V in un contenitore"), ("certificazione HDMI, ascolto.", "certificazione HDMI, prove d'ascolto."),
 # French
 ("câble continu de 6 mm² sur 0,8 m", "câble d'alimentation continue de 6 mm², long de 0,8 m"), ("bloqueur de continu", "bloqueur de composante continue"),
 ("l'alimentation externe linéaire en continu (noyau R)", "l'alimentation linéaire externe à courant continu (noyau R)"), ("(calculs en Python, ni SPICE ni mesures)", "(calculs en Python, sans SPICE ni mesures)"),
 ("3 m d'écoute", "distance d'écoute de 3 m"), ("mise sous tension avec NTC et relais", "mise sous tension progressive par CTN et relais"),
 ("alimentation externe linéaire à noyau R", "alimentation linéaire externe à noyau R"), ("signal dans un seul sens sur environ 40 mm", "signal circulant dans un seul sens sur environ 40 mm"),
 ("banques de condensateurs non régulées", "batteries de condensateurs non régulées"), ("l'analogique et l'horloge sont linéaires à faible bruit", "les alimentations analogiques et d'horloge sont linéaires à faible bruit"),
 ("de style 4DX restent celles de SV-VER1", "de type 4DX restent identiques à celles de SV-VER1"),
]
for fn in ("v7_texts.py", "sv5_build.py"):
    s = open(fn, encoding="utf-8").read(); n = 0
    for a, b in pairs:
        if a in s:
            s = s.replace(a, b); n += 1
    open(fn, "w", encoding="utf-8").write(s)
    print(fn, "applied", n, "of", len(pairs))
# decimal comma for ru/uk/de/it/fr and UK spelling, in the build scripts
helper = 'import re as _re\ndef _dec(L, t):\n    return _re.sub(r"(?<=\\d)\\.(?=\\d)", ",", t) if L in ("ru", "uk", "de", "it", "fr") else t\n'
s = open("v7_build.py", encoding="utf-8").read()
if "_dec(" not in s:
    s = s.replace('OUT = SD + r"\\v7out"', helper + 'OUT = SD + r"\\v7out"', 1)
    s = s.replace('md.append("- " + IT[k][L])', 'md.append("- " + _dec(L, IT[k][L]))')
    s = s.replace("for t in [TITLE[L], INTRO[L]] + [IT[k][L] for k in", "for t in [_dec(L, x) for x in [TITLE[L], INTRO[L]] + [IT[k][L] for k in")
    s = s.replace('("need", "A", "H", "D", "C", "N")]:\n        for ln in wrap', '("need", "A", "H", "D", "C", "N")]]:\n        for ln in wrap')
    s = s.replace('GB = [("ground plane", "earth plane"), ("Ground", "Earth"), ("ground", "earth"),', 'GB = [("analog", "analogue"), ("a ground plane", "an earth plane"), ("ground plane", "earth plane"), ("Ground", "Earth"), ("ground", "earth"),')
    open("v7_build.py", "w", encoding="utf-8").write(s)
s = open("sv5_build.py", encoding="utf-8").read()
if "_dec(" not in s:
    s = s.replace('OUT = SD + r"\\sv5out"', helper + 'OUT = SD + r"\\sv5out"', 1)
    open("sv5_build.py", "w", encoding="utf-8").write(s)
print("done")
