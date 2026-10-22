exec(open("fix_spk_off.py", encoding="utf-8").read().split("# the figure")[0])
# the user wants separate ON/OFF switches, not automatic muting: replace the automatic-OFF sentences
NEW = {
 "ja": "スピーカー出力とヘッドホン出力は、前面のそれぞれ独立した ON / OFF スイッチで切り替えます (両方 ON で同時に使えます)。",
 "en": "The speaker output and the headphone output each have their own front-panel ON / OFF switch (both ON works at the same time).",
 "ru": "Выход на колонки и выход на наушники переключаются отдельными выключателями ON / OFF на передней панели (при обоих ON работают одновременно).",
 "uk": "Вихід на колонки та вихід на навушники вмикаються окремими перемикачами ON / OFF на передній панелі (за обох ON працюють одночасно).",
 "de": "Lautsprecher- und Kopfhörerausgang haben je einen eigenen EIN-/AUS-Schalter an der Frontplatte (beide EIN arbeiten gleichzeitig).",
 "it": "L'uscita dei diffusori e quella delle cuffie hanno ciascuna un proprio interruttore ON / OFF sul frontale (con entrambi su ON funzionano insieme).",
 "fr": "La sortie enceintes et la sortie casque ont chacune leur propre interrupteur ON / OFF en façade (les deux sur ON fonctionnent ensemble).",
}
OLD_HP = ["ヘッドホンをどれかの端子に挿すと、スピーカー出力は自動で OFF になり (スピーカーリレーを開いてパワー段をミュート)、抜くと自動で元に戻ります。",
          "Plugging headphones into any of the jacks automatically turns the speaker outputs OFF (the speaker relays open and the power stage is muted); unplugging restores them automatically.",
          "При подключении наушников к любому разъёму выходы на колонки автоматически выключаются (реле колонок размыкаются, силовой каскад заглушается); при отключении всё восстанавливается автоматически.",
          "Під час підключення навушників до будь-якого роз'єму виходи на колонки автоматично вимикаються (реле колонок розмикаються, силовий каскад приглушується); після відключення все відновлюється автоматично.",
          "Beim Einstecken eines Kopfhörers in eine der Buchsen werden die Lautsprecherausgänge automatisch ausgeschaltet (die Lautsprecherrelais öffnen, die Endstufe wird stummgeschaltet); beim Abziehen kehrt alles automatisch zurück.",
          "Inserendo le cuffie in una qualsiasi presa, le uscite dei diffusori si spengono automaticamente (i relè dei diffusori si aprono e lo stadio di potenza viene silenziato); estraendole tutto torna automaticamente.",
          "Lorsqu'un casque est branché sur l'une des prises, les sorties enceintes sont automatiquement coupées (les relais d'enceintes s'ouvrent et l'étage de puissance est mis en sourdine) ; en le débranchant, tout revient automatiquement."]
OLD_SV = ["ヘッドホンをどれかの端子に挿すと、スピーカー (サラウンド) 出力は自動で OFF になり、抜くと自動で戻る。",
          "Plugging headphones into any jack automatically turns the surround speaker outputs OFF, and unplugging restores them.",
          "При подключении наушников к любому разъёму выходы на колонки объёмного звука автоматически выключаются, при отключении — восстанавливаются.",
          "Під час підключення навушників до будь-якого роз'єму виходи на колонки об'ємного звучання автоматично вимикаються, після відключення — відновлюються.",
          "Beim Einstecken eines Kopfhörers in eine Buchse werden die Surround-Lautsprecherausgänge automatisch ausgeschaltet und beim Abziehen wieder eingeschaltet.",
          "Inserendo le cuffie in una presa, le uscite dei diffusori surround si spengono automaticamente e riprendono estraendole.",
          "Lorsqu'un casque est branché sur une prise, les sorties des enceintes surround sont automatiquement coupées et rétablies au débranchement."]
order = ["ja", "en", "ru", "uk", "de", "it", "fr"]
patch("hp2_build.py", [(OLD_HP[i], NEW[order[i]]) for i in range(7)])
patch("sv7_texts_add.py", [(OLD_SV[i], NEW[order[i]].replace("前面の", "前面の")) for i in range(7)])
patch("fig_hp2_body.py", [
 ("ヘッドホンを挿すとスピーカー出力は自動で OFF", "スピーカー出力・ヘッドホン出力 各々に ON/OFF スイッチ"),
 ('L("ヘッドホンを挿すとスピーカー出力は自動で OFF (スピーカーリレーを開き、パワー段をミュート)。抜くと自動で復帰", 1.05)', 'L("前面に ON/OFF スイッチを 2 個: スピーカー出力用・ヘッドホン出力用 (独立。信号は通さない非接触スイッチ → 密閉リレーを駆動)", 1.05)'),
])
patch("v7_hpstrip.py", [
 ("(挿すとスピーカー出力は自動で OFF)", "(スピーカー出力とは別の ON/OFF)"),
 ("ヘッドホンを挿すとスピーカー出力は自動で OFF、抜くと復帰。", "前面にスピーカー用・ヘッドホン用の ON/OFF スイッチ (独立)。"),
 ("Plugging in headphones turns the speaker outputs OFF automatically; unplugging restores them.", "Separate front-panel ON / OFF switches for the speaker output and the headphone output."),
])
