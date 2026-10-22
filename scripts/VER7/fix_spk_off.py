import re
def patch(fn, pairs):
    s = open(fn, encoding="utf-8").read(); n = 0
    for a, b in pairs:
        if a in s:
            s = s.replace(a, b); n += 1
        else:
            print("MISSING in", fn, ":", a[:50])
    open(fn, "w", encoding="utf-8").write(s)
    print(fn, n, "of", len(pairs))

# the figure
patch("fig_hp2_body.py", [
 ("スピーカーと同時に動作", "ヘッドホンを挿すとスピーカー出力は自動で OFF"),
 ('L("SW8: ヘッドホン挿入時にスピーカーを自動ミュートする / しない", 1.05)', 'L("ヘッドホンを挿すとスピーカー出力は自動で OFF (スピーカーリレーを開き、パワー段をミュート)。抜くと自動で復帰", 1.05)'),
])
# HP-VER2 texts (8 languages)
patch("hp2_build.py", [
 ("スピーカーと同時に動作し、挿入するとスピーカーを自動ミュートする / しないを選べる (SW8)。", "ヘッドホンをどれかの端子に挿すと、スピーカー出力は自動で OFF になり (スピーカーリレーを開いてパワー段をミュート)、抜くと自動で元に戻ります。"),
 ("It works together with the speakers, and inserting a plug can mute the speakers automatically or not (SW8).", "Plugging headphones into any of the jacks automatically turns the speaker outputs OFF (the speaker relays open and the power stage is muted); unplugging restores them automatically."),
 ("Работает одновременно с колонками; при подключении колонки можно автоматически отключать или нет (SW8).", "При подключении наушников к любому разъёму выходы на колонки автоматически выключаются (реле колонок размыкаются, силовой каскад заглушается); при отключении всё восстанавливается автоматически."),
 ("Працює одночасно з колонками; після підключення колонки можна автоматично вимикати чи ні (SW8).", "Під час підключення навушників до будь-якого роз'єму виходи на колонки автоматично вимикаються (реле колонок розмикаються, силовий каскад приглушується); після відключення все відновлюється автоматично."),
 ("Es arbeitet gleichzeitig mit den Lautsprechern; beim Einstecken lassen sich die Lautsprecher automatisch stummschalten oder nicht (SW8).", "Beim Einstecken eines Kopfhörers in eine der Buchsen werden die Lautsprecherausgänge automatisch ausgeschaltet (die Lautsprecherrelais öffnen, die Endstufe wird stummgeschaltet); beim Abziehen kehrt alles automatisch zurück."),
 ("Funziona insieme ai diffusori; all'inserimento si possono silenziare automaticamente i diffusori oppure no (SW8).", "Inserendo le cuffie in una qualsiasi presa, le uscite dei diffusori si spengono automaticamente (i relè dei diffusori si aprono e lo stadio di potenza viene silenziato); estraendole tutto torna automaticamente."),
 ("Il fonctionne en même temps que les enceintes ; à l'insertion, les enceintes peuvent être coupées automatiquement ou non (SW8).", "Lorsqu'un casque est branché sur l'une des prises, les sorties enceintes sont automatiquement coupées (les relais d'enceintes s'ouvrent et l'étage de puissance est mis en sourdine) ; en le débranchant, tout revient automatiquement."),
])
# SV-VER7 text
patch("sv7_texts_add.py", [
 ("スピーカー (サラウンド) と同時に使え、挿入でスピーカーを自動ミュートする / しないを選べる。", "ヘッドホンをどれかの端子に挿すと、スピーカー (サラウンド) 出力は自動で OFF になり、抜くと自動で戻る。"),
 ("It works together with the surround speakers, and inserting a plug can mute them automatically or not.", "Plugging headphones into any jack automatically turns the surround speaker outputs OFF, and unplugging restores them."),
 ("Работает одновременно с колонками объёмного звука; при подключении их можно автоматически отключать или нет.", "При подключении наушников к любому разъёму выходы на колонки объёмного звука автоматически выключаются, при отключении — восстанавливаются."),
 ("Працює одночасно з колонками об'ємного звучання; після підключення їх можна автоматично вимикати чи ні.", "Під час підключення навушників до будь-якого роз'єму виходи на колонки об'ємного звучання автоматично вимикаються, після відключення — відновлюються."),
 ("Er arbeitet gleichzeitig mit den Surround-Lautsprechern; beim Einstecken lassen sie sich automatisch stummschalten oder nicht.", "Beim Einstecken eines Kopfhörers in eine Buchse werden die Surround-Lautsprecherausgänge automatisch ausgeschaltet und beim Abziehen wieder eingeschaltet."),
 ("Funziona insieme ai diffusori surround; all'inserimento si possono silenziare automaticamente oppure no.", "Inserendo le cuffie in una presa, le uscite dei diffusori surround si spengono automaticamente e riprendono estraendole."),
 ("Il fonctionne en même temps que les enceintes surround ; à l'insertion, elles peuvent être coupées automatiquement ou non.", "Lorsqu'un casque est branché sur une prise, les sorties des enceintes surround sont automatiquement coupées et rétablies au débranchement."),
])
# the strip in every VER7 figure
patch("v7_hpstrip.py", [
 ("(スピーカーと同時に動作)", "(挿すとスピーカー出力は自動で OFF)"),
 ("SW7 = ANALOG / DIGITAL ゲイン、SW8 = 挿入でスピーカーをミュートする / しない。", "SW7 = ANALOG / DIGITAL ゲイン。ヘッドホンを挿すとスピーカー出力は自動で OFF、抜くと復帰。"),
 ("SW7 = analog / digital gain, SW8 = mute the speakers when a plug is inserted, or not.", "SW7 = analog / digital gain. Plugging in headphones turns the speaker outputs OFF automatically; unplugging restores them."),
 ("関連: 前面のジャック", "関連: 前面のジャック") ,
])
# the English / other HPI sentences do not mention SW8, nothing to change there
