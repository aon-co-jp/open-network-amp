import os, re, shutil, math
from PIL import Image, ImageDraw, ImageFont
SD = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
c = {}
exec(open(SD + "/hp2_calc.py", encoding="utf-8").read().replace('if __name__ == "__main__":', 'if False:'), c)
V = {"p32s": c["p_max"](32, False), "p32b": c["p_max"](32, True), "p300b": c["p_max"](300, True), "h0": c["hiss_spl"](0, 120, 16), "h18": c["hiss_spl"](18, 120, 16),
     "v16": c["v_for_spl"](100, 120, 16), "v600": c["v_for_spl"](100, 98, 600)}
LANG8 = ["ja", "en", "en-GB", "ru", "uk", "de", "it", "fr"]
NAME8 = {"ja": "日本語", "en": "English (US)", "en-GB": "English (UK)", "ru": "Русский", "uk": "Українська", "de": "Deutsch", "it": "Italiano", "fr": "Français"}
TITLE = {
 "ja": "HP-VER3 — ゲイン調整 (1dB 刻み・3 モード・スピーカー用とヘッドホン用の 2 個) つきヘッドホンアンプ (前面に 3.5mm・4.4mm・6.35mm・XLR (ステレオ 4 ピン + モノラル 3 ピン ×2)、ゲイン調整つき) — 通常プリメインアンプと AV アンプの両方に搭載",
 "en": "HP-VER3 — headphone amplifier (front-panel 3.5 mm, 4.4 mm, 6.35 mm and XLR (stereo 4-pin plus two mono 3-pin), with gain adjustment) for both the regular integrated amplifiers and the AV amplifier",
 "ru": "HP-VER3 — усилитель для наушников (на передней панели 3,5 мм, 4,4 мм, 6,35 мм и XLR (стерео 4-контактный и два моно 3-контактных), с регулировкой усиления) для обычных усилителей и AV-усилителя",
 "uk": "HP-VER3 — підсилювач для навушників (на передній панелі 3,5 мм, 4,4 мм, 6,35 мм і XLR (стерео 4-контактний і два моно 3-контактних), з регулюванням підсилення) для звичайних підсилювачів і AV-підсилювача",
 "de": "HP-VER3 — Kopfhörerverstärker (frontseitig 3,5 mm, 4,4 mm, 6,35 mm und XLR (Stereo 4-polig plus zwei Mono 3-polig), mit Verstärkungseinstellung) für die normalen Vollverstärker und den AV-Verstärker",
 "it": "HP-VER3 — amplificatore per cuffie (sul frontale 3,5 mm, 4,4 mm, 6,35 mm e XLR (stereo a 4 poli più due mono a 3 poli), con regolazione del guadagno) per gli amplificatori integrati normali e per l'amplificatore AV",
 "fr": "HP-VER3 — amplificateur casque (en façade 3,5 mm, 4,4 mm, 6,35 mm et XLR (stéréo 4 broches plus deux mono 3 broches), avec réglage du gain) pour les amplificateurs intégrés normaux et pour l'amplificateur AV",
}
T = {
 "jacks": {
  "ja": "端子 (すべて前面): 3.5mm はバランス (TRRS) とアンバランス (TRS) 兼用 (自動検出)、4.4mm バランス (Pentaconn)、6.35mm (6.5mm と呼ばれることもある) アンバランス、XLR バランス 2 種類: ステレオ 4 ピン 1 個 (1=L+、2=L−、3=R+、4=R−) と、モノラル 3 ピン 2 個 (L 用・R 用、各 1=GND、2=+、3=−)。スピーカー出力とヘッドホン出力は、前面のそれぞれ独立した ON / OFF スイッチで切り替えます (両方 ON で同時に使えます)。",
  "en": "Jacks (all on the front panel): 3.5 mm for both balanced (TRRS) and unbalanced (TRS) with automatic detection, 4.4 mm balanced (Pentaconn), 6.35 mm (sometimes called 6.5 mm) unbalanced and balanced XLR in two forms: one stereo 4-pin (1 = L+, 2 = L-, 3 = R+, 4 = R-) and two mono 3-pin jacks (one for L, one for R; each 1 = GND, 2 = +, 3 = -). The speaker output and the headphone output each have their own front-panel ON / OFF switch (both ON works at the same time).",
  "ru": "Разъёмы (все на передней панели): 3,5 мм — и сбалансированный (TRRS), и несбалансированный (TRS) с автоопределением, 4,4 мм сбалансированный (Pentaconn), 6,35 мм (иногда называют 6,5 мм) несбалансированный и сбалансированный XLR двух видов: один стерео 4-контактный (1 = L+, 2 = L−, 3 = R+, 4 = R−) и два моно 3-контактных (для L и для R; в каждом 1 = GND, 2 = +, 3 = −). Выход на колонки и выход на наушники переключаются отдельными выключателями ON / OFF на передней панели (при обоих ON работают одновременно).",
  "uk": "Роз'єми (усі на передній панелі): 3,5 мм — і збалансований (TRRS), і незбалансований (TRS) з автовизначенням, 4,4 мм збалансований (Pentaconn), 6,35 мм (інколи називають 6,5 мм) незбалансований і збалансований XLR двох видів: один стерео 4-контактний (1 = L+, 2 = L−, 3 = R+, 4 = R−) і два моно 3-контактних (для L і для R; у кожному 1 = GND, 2 = +, 3 = −). Вихід на колонки та вихід на навушники вмикаються окремими перемикачами ON / OFF на передній панелі (за обох ON працюють одночасно).",
  "de": "Buchsen (alle frontseitig): 3,5 mm für symmetrisch (TRRS) und unsymmetrisch (TRS) mit automatischer Erkennung, 4,4 mm symmetrisch (Pentaconn), 6,35 mm (manchmal 6,5 mm genannt) unsymmetrisch und symmetrisches XLR in zwei Formen: eine Stereo-Buchse mit 4 Polen (1 = L+, 2 = L−, 3 = R+, 4 = R−) und zwei Mono-Buchsen mit 3 Polen (für L und für R; jeweils 1 = GND, 2 = +, 3 = −). Lautsprecher- und Kopfhörerausgang haben je einen eigenen EIN-/AUS-Schalter an der Frontplatte (beide EIN arbeiten gleichzeitig).",
  "it": "Prese (tutte sul frontale): 3,5 mm sia bilanciata (TRRS) sia sbilanciata (TRS) con rilevamento automatico, 4,4 mm bilanciata (Pentaconn), 6,35 mm (talvolta detta 6,5 mm) sbilanciata e XLR bilanciata in due forme: una presa stereo a 4 poli (1 = L+, 2 = L−, 3 = R+, 4 = R−) e due prese mono a 3 poli (una per L e una per R; ciascuna 1 = GND, 2 = +, 3 = −). L'uscita dei diffusori e quella delle cuffie hanno ciascuna un proprio interruttore ON / OFF sul frontale (con entrambi su ON funzionano insieme).",
  "fr": "Prises (toutes en façade) : 3,5 mm symétrique (TRRS) et asymétrique (TRS) avec détection automatique, 4,4 mm symétrique (Pentaconn), 6,35 mm (parfois appelée 6,5 mm) asymétrique et XLR symétrique sous deux formes : une prise stéréo à 4 broches (1 = L+, 2 = L−, 3 = R+, 4 = R−) et deux prises mono à 3 broches (une pour L et une pour R ; chacune 1 = GND, 2 = +, 3 = −). La sortie enceintes et la sortie casque ont chacune leur propre interrupteur ON / OFF en façade (les deux sur ON fonctionnent ensemble)."},
 "gain": {
  "ja": "ゲイン調整: アナログのゲイン段 (0 / +6 / +12 / +18dB、リレー切替) と FPGA のデジタルゲイン (±0.5dB 刻み、SW7) の 2 種類で、どちらもスピーカーとヘッドホンの両方に効きます。新機能: ヘッドホンの抵抗を検出 (16〜600Ω) して、低抵抗・高感度ほど 0dB 側を推奨するゲイン自動推奨 (手動でも変更できる)。出力インピーダンスは約 0.1Ω。",
  "en": "Gain adjustment: an analog gain stage (0 / +6 / +12 / +18 dB, relay-switched) and a digital gain in the FPGA (0.5 dB steps, SW7); both act on the speakers and the headphones. New: the headphone resistance is detected (16 to 600 ohm) and an automatic gain recommendation suggests the 0 dB side for low-resistance, high-sensitivity types (it can still be changed by hand). The output impedance is about 0.1 ohm.",
  "ru": "Регулировка усиления: аналоговый каскад усиления (0 / +6 / +12 / +18 дБ, переключение реле) и цифровое усиление в FPGA (шаг 0,5 дБ, SW7); оба действуют и на колонки, и на наушники. Новое: определяется сопротивление наушников (16–600 Ом), и автоматическая рекомендация усиления предлагает 0 дБ для низкоомных чувствительных моделей (можно изменить вручную). Выходное сопротивление около 0,1 Ом.",
  "uk": "Регулювання підсилення: аналоговий каскад підсилення (0 / +6 / +12 / +18 дБ, перемикання реле) і цифрове підсилення в FPGA (крок 0,5 дБ, SW7); обидва діють і на колонки, і на навушники. Нове: визначається опір навушників (16–600 Ом), і автоматична рекомендація підсилення пропонує 0 дБ для низькоомних чутливих моделей (можна змінити вручну). Вихідний опір близько 0,1 Ом.",
  "de": "Verstärkungseinstellung: eine analoge Verstärkungsstufe (0 / +6 / +12 / +18 dB, per Relais) und eine digitale Verstärkung im FPGA (0,5-dB-Schritte, SW7); beide wirken auf Lautsprecher und Kopfhörer. Neu: Der Kopfhörerwiderstand wird erkannt (16 bis 600 Ω), und eine automatische Verstärkungsempfehlung schlägt für niederohmige, empfindliche Modelle die 0-dB-Seite vor (von Hand änderbar). Die Ausgangsimpedanz beträgt etwa 0,1 Ω.",
  "it": "Regolazione del guadagno: uno stadio di guadagno analogico (0 / +6 / +12 / +18 dB, con relè) e un guadagno digitale nell'FPGA (passi da 0,5 dB, SW7); entrambi agiscono su diffusori e cuffie. Novità: viene rilevata la resistenza della cuffia (da 16 a 600 ohm) e una raccomandazione automatica del guadagno suggerisce 0 dB per i modelli a bassa resistenza e alta sensibilità (si può comunque cambiare a mano). L'impedenza d'uscita è di circa 0,1 ohm.",
  "fr": "Réglage du gain : un étage de gain analogique (0 / +6 / +12 / +18 dB, par relais) et un gain numérique dans le FPGA (pas de 0,5 dB, SW7) ; les deux agissent sur les enceintes et le casque. Nouveauté : la résistance du casque est détectée (de 16 à 600 ohms) et une recommandation automatique de gain propose 0 dB pour les modèles de faible résistance et de haute sensibilité (modifiable à la main). L'impédance de sortie est d'environ 0,1 ohm."},
 "sim": {
  "ja": "仮想シミュレーション (Python): ① 32Ω ではアンバランス 約 %(p32s).1fW、バランス 約 %(p32b).1fW、300Ω でもバランス 約 %(p300b).1fW (電圧が 2 倍で 約 4 倍) → 高インピーダンスの機種はバランスが有利。② 不具合: +18dB 固定だと 高感度イヤホン (16Ω・120dB/mW) のヒスが 約 %(h18).0fdB SPL で聞こえる (0dB では約 %(h0).0fdB) → ゲイン自動推奨を追加。③ 100dB SPL に必要な電圧は イヤホンで約 %(v16).2fV、600Ω で約 %(v600).1fV → 4 段のゲインで足りる。",
  "en": "Virtual simulation (Python): (1) at 32 ohm the unbalanced output gives about %(p32s).1f W and the balanced one about %(p32b).1f W; even at 300 ohm the balanced output gives about %(p300b).1f W (twice the voltage, about four times the power), so high-impedance models favour balanced. (2) Bug: a fixed +18 dB makes the hiss of a sensitive earphone (16 ohm, 120 dB/mW) audible at about %(h18).0f dB SPL (about %(h0).0f dB at 0 dB), so the automatic gain recommendation was added. (3) 100 dB SPL needs about %(v16).2f V for the earphone and about %(v600).1f V for 600 ohm, so four gain steps are enough.",
  "ru": "Виртуальное моделирование (Python): (1) на 32 Ом несбалансированный выход даёт около %(p32s).1f Вт, сбалансированный — около %(p32b).1f Вт; даже на 300 Ом сбалансированный даёт около %(p300b).1f Вт (напряжение вдвое, мощность примерно вчетверо), поэтому высокоомным моделям выгоднее симметричное подключение. (2) Ошибка: при фиксированных +18 дБ шум чувствительного вкладыша (16 Ом, 120 дБ/мВт) слышен примерно при %(h18).0f дБ SPL (при 0 дБ около %(h0).0f дБ), поэтому добавлена автоматическая рекомендация усиления. (3) Для 100 дБ SPL нужно около %(v16).2f В для вкладыша и около %(v600).1f В для 600 Ом — четырёх ступеней усиления достаточно.",
  "uk": "Віртуальне моделювання (Python): (1) на 32 Ом незбалансований вихід дає близько %(p32s).1f Вт, збалансований — близько %(p32b).1f Вт; навіть на 300 Ом збалансований дає близько %(p300b).1f Вт (напруга вдвічі, потужність приблизно вчетверо), тому високоомним моделям вигідніше симетричне підключення. (2) Помилка: за фіксованих +18 дБ шум чутливого вкладиша (16 Ом, 120 дБ/мВт) чути приблизно за %(h18).0f дБ SPL (за 0 дБ близько %(h0).0f дБ), тому додано автоматичну рекомендацію підсилення. (3) Для 100 дБ SPL потрібно близько %(v16).2f В для вкладиша і близько %(v600).1f В для 600 Ом — чотирьох ступенів підсилення достатньо.",
  "de": "Virtuelle Simulation (Python): (1) An 32 Ω liefert der unsymmetrische Ausgang etwa %(p32s).1f W, der symmetrische etwa %(p32b).1f W; selbst an 300 Ω gibt der symmetrische etwa %(p300b).1f W (doppelte Spannung, etwa vierfache Leistung), hochohmige Modelle profitieren also vom symmetrischen Anschluss. (2) Fehler: Bei festen +18 dB ist das Rauschen eines empfindlichen In-Ears (16 Ω, 120 dB/mW) bei etwa %(h18).0f dB SPL hörbar (bei 0 dB etwa %(h0).0f dB), daher wurde die automatische Verstärkungsempfehlung ergänzt. (3) Für 100 dB SPL braucht man etwa %(v16).2f V am In-Ear und etwa %(v600).1f V an 600 Ω, vier Verstärkungsstufen genügen.",
  "it": "Simulazione virtuale (Python): (1) su 32 ohm l'uscita sbilanciata dà circa %(p32s).1f W e quella bilanciata circa %(p32b).1f W; anche su 300 ohm la bilanciata dà circa %(p300b).1f W (tensione doppia, potenza circa quadrupla), quindi i modelli ad alta impedenza traggono vantaggio dal collegamento bilanciato. (2) Errore: con +18 dB fissi il fruscio di un auricolare sensibile (16 ohm, 120 dB/mW) si sente a circa %(h18).0f dB SPL (a 0 dB circa %(h0).0f dB), perciò è stata aggiunta la raccomandazione automatica del guadagno. (3) Per 100 dB SPL servono circa %(v16).2f V sull'auricolare e circa %(v600).1f V su 600 ohm, quindi bastano quattro passi di guadagno.",
  "fr": "Simulation virtuelle (Python) : (1) sous 32 ohms la sortie asymétrique donne environ %(p32s).1f W et la symétrique environ %(p32b).1f W ; même sous 300 ohms la symétrique donne environ %(p300b).1f W (tension double, puissance environ quadruple), les modèles à haute impédance profitent donc du branchement symétrique. (2) Erreur : avec +18 dB fixes, le souffle d'un intra-auriculaire sensible (16 ohms, 120 dB/mW) est audible à environ %(h18).0f dB SPL (environ %(h0).0f dB à 0 dB), d'où l'ajout de la recommandation automatique de gain. (3) Pour 100 dB SPL il faut environ %(v16).2f V pour l'intra-auriculaire et environ %(v600).1f V pour 600 ohms ; quatre pas de gain suffisent."},
 "pin": {
  "ja": "注意 (ピン配置と保護): 4.4mm・XLR (4 ピン / 3 ピン)・3.5mm TRRS のピン配置は機器やケーブルにより異なることがあるため、使うケーブルの配線を確認すること。バランスのジャックにアンバランスのプラグを挿しても Cold を GND に落とさないよう、ジャック検出で Cold を切り離す。出力リレーは DC 検出と起動・停止のミュートつきで、ヘッドホンを守る。",
  "en": "Caution (pinout and protection): the pinouts of 4.4 mm, 4-pin XLR and 3.5 mm TRRS differ between equipment and cables, so check the wiring of the cable you use. Plugging an unbalanced plug into a balanced jack must not ground the cold leg, so jack detection disconnects it. The output relays have DC detection and start-up / shut-down muting to protect the headphones.",
  "ru": "Внимание (распайка и защита): распайка 4,4 мм, 4-контактного XLR и 3,5 мм TRRS у разной техники и кабелей различается, поэтому проверяйте распайку своего кабеля. Несбалансированный штекер в сбалансированном гнезде не должен заземлять холодную фазу, поэтому определение штекера отключает её. Выходные реле имеют контроль постоянной составляющей и заглушение при включении и выключении, защищая наушники.",
  "uk": "Увага (розпаювання та захист): розпаювання 4,4 мм, 4-контактного XLR і 3,5 мм TRRS у різної техніки й кабелів відрізняється, тому перевіряйте розпаювання свого кабелю. Незбалансований штекер у збалансованому гнізді не має заземлювати холодну фазу, тому визначення штекера відключає її. Вихідні реле мають контроль постійної складової та приглушення під час вмикання й вимикання, захищаючи навушники.",
  "de": "Hinweis (Pinbelegung und Schutz): Die Pinbelegungen von 4,4 mm, 4-poligem XLR und 3,5 mm TRRS unterscheiden sich je nach Gerät und Kabel, die Verdrahtung des verwendeten Kabels ist also zu prüfen. Ein unsymmetrischer Stecker in einer symmetrischen Buchse darf den Kaltpol nicht auf Masse legen, deshalb trennt die Buchsenerkennung ihn ab. Die Ausgangsrelais haben Gleichspannungserkennung und Stummschaltung beim Ein- und Ausschalten und schützen den Kopfhörer.",
  "it": "Attenzione (piedinatura e protezione): le piedinature di 4,4 mm, XLR a 4 poli e 3,5 mm TRRS variano a seconda di apparecchi e cavi, quindi si controlli il cablaggio del cavo usato. Un jack sbilanciato in una presa bilanciata non deve mettere a massa il polo freddo, perciò il rilevamento della presa lo scollega. I relè d'uscita hanno rilevamento della continua e silenziamento all'accensione e allo spegnimento per proteggere le cuffie.",
  "fr": "Attention (brochage et protection) : les brochages du 4,4 mm, du XLR 4 broches et du 3,5 mm TRRS varient selon les appareils et les câbles, il faut donc vérifier le câblage du câble utilisé. Une fiche asymétrique dans une prise symétrique ne doit pas mettre le point froid à la masse ; la détection de prise le déconnecte donc. Les relais de sortie ont une détection de continu et une coupure au démarrage et à l'arrêt pour protéger le casque."},
 "rest": {
  "ja": "適用: 通常プリメインアンプ (VER7 のA級・A級+AB級・AB級・D級アナログ・真空管プリ版) と AV アンプ (SV-VER7) の前面に、同じ回路を載せる。未実施: 実機測定 (歪み・雑音・出力インピーダンス)、各ヘッドホンでの聴感評価、4.4mm・XLR の規格確認。",
  "en": "Applies to: the regular integrated amplifiers (the VER7 Class A, Class A + AB, Class AB, analog Class D and valve-preamp versions) and the AV amplifier (SV-VER7), with the same circuit on the front panel. Not done: bench measurements (distortion, noise, output impedance), listening tests with real headphones and standards checks of the 4.4 mm and XLR wiring.",
  "ru": "Применяется: в обычных усилителях (версии VER7 класса A, A + AB, AB, аналоговый класс D и с ламповым предусилителем) и в AV-усилителе (SV-VER7), одна и та же схема на передней панели. Не выполнено: измерения (искажения, шум, выходное сопротивление), прослушивание с реальными наушниками и проверка распайки 4,4 мм и XLR по стандартам.",
  "uk": "Застосовується: у звичайних підсилювачах (версії VER7 класу A, A + AB, AB, аналоговий клас D і з ламповим попереднім підсилювачем) та в AV-підсилювачі (SV-VER7), та сама схема на передній панелі. Не виконано: вимірювання (спотворення, шум, вихідний опір), прослуховування з реальними навушниками та перевірка розпаювання 4,4 мм і XLR за стандартами.",
  "de": "Gilt für: die normalen Vollverstärker (die VER7-Versionen Klasse A, Klasse A plus AB, Klasse AB, analoges Klasse D und Röhrenvorstufe) und den AV-Verstärker (SV-VER7), mit derselben Schaltung auf der Frontplatte. Nicht durchgeführt: Messungen (Verzerrung, Rauschen, Ausgangsimpedanz), Hörtests mit echten Kopfhörern und Normprüfungen der 4,4-mm- und XLR-Verdrahtung.",
  "it": "Si applica a: gli amplificatori integrati normali (le versioni VER7 classe A, classe A + AB, classe AB, classe D analogica e con pre a valvole) e l'amplificatore AV (SV-VER7), con lo stesso circuito sul frontale. Non eseguito: misure (distorsione, rumore, impedenza d'uscita), ascolto con cuffie reali e verifiche normative del cablaggio 4,4 mm e XLR.",
  "fr": "S'applique aux amplificateurs intégrés normaux (les versions VER7 classe A, classe A + AB, classe AB, classe D analogique et préampli à tubes) et à l'amplificateur AV (SV-VER7), avec le même circuit en façade. Non réalisé : mesures (distorsion, bruit, impédance de sortie), écoute avec de vrais casques et vérification normative du câblage 4,4 mm et XLR."},
}
for k in T:
    T[k]["en-GB"] = T[k]["en"].replace("analog", "analogue").replace("ground", "earth").replace("tube", "valve")
TITLE["en-GB"] = TITLE["en"]
exec(open(SD + "/sw_texts.py", encoding="utf-8").read())
T.update(T_SW)
exec(open(SD + "/g3_texts.py", encoding="utf-8").read())
T.update(T_G3)
V.update(GV)
D = SD + "/ona/headphone/HP-VER3"
FIGDIR = D + "/figures-only"
os.makedirs(FIGDIR, exist_ok=True)
dec = lambda L, t: re.sub(r"(?<=\d)\.(?=\d)", ",", t) if L in ("ru", "uk", "de", "it", "fr") else t
def fmt(L, k):
    t = T[k][L]
    return dec(L, (t % V) if "%(" in t else t).replace("%%", "%")
W, pad = 3200, 60
colw = (W - 3 * pad) // 2
REG = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", 34)
HD = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", 40)
BIG = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", 51)
TOK = re.compile(r"[\x21-\x7e\u00a0-\u024f\u0400-\u04ff]+|\s|.", re.S)
def wrap(t, font, width):
    out, cur = [], ""
    for tk in TOK.findall(t):
        if font.getlength(cur + tk) > width and cur.strip():
            out.append(cur.rstrip()); cur = tk.lstrip()
        else:
            cur += tk
    out.append(cur.rstrip()); return out
hh = lambda lines: sum(int(f.size * 1.45) for _, f in lines) + 40
def panel(keys, heading):
    blocks = []
    for L in LANG8:
        lines = [(NAME8[L], HD)]
        for k in keys:
            t = dec(L, TITLE[L]) if k == "title" else fmt(L, k)
            for ln in wrap(t, REG, colw): lines.append((ln, REG))
            lines.append(("", REG))
        blocks.append(lines)
    rows = [(blocks[i], blocks[i + 1]) for i in range(0, 8, 2)]
    TH = 140 + sum(max(hh(a), hh(b)) for a, b in rows) + pad
    im = Image.new("RGB", (W, TH), "white"); d = ImageDraw.Draw(im)
    d.text((pad, 40), heading, font=BIG, fill=(20, 30, 60))
    y = 140
    for a, b in rows:
        for col, lines in enumerate((a, b)):
            x, yy = pad + col * (colw + pad), y
            for t, f in lines:
                d.text((x, yy), t, font=f, fill=(20, 30, 60) if f is HD else (40, 40, 40)); yy += int(f.size * 1.45)
        y += max(hh(a), hh(b))
    return im
def compose(fn, keys, heading):
    shutil.copy(SD + "/" + fn, FIGDIR + "/" + fn)
    fig = Image.open(SD + "/" + fn).convert("RGB")
    fig = fig.resize((W, int(fig.height * W / fig.width)))
    p = panel(keys, heading)
    im = Image.new("RGB", (W, fig.height + p.height), "white"); im.paste(fig, (0, 0)); im.paste(p, (0, fig.height))
    im.save(D + "/" + fn, "JPEG", quality=88, dpi=(300, 300)); print(fn, im.size)
compose("amp_gain3.jpg", ["g3", "rest"], "HP-VER3 ゲイン調整 (1dB 刻み・3 モード・2 個) — 説明 / Explanation (8 languages)")
compose("amp_gain3_sim.jpg", ["g3sim", "g3"], "HP-VER3 ゲイン調整の仮想シミュレーション — 説明 / Explanation (8 languages)")
man = panel(["title", "g3", "g3sim", "jacks", "sw", "pin", "rest"], "HP-VER3 説明書 / Manual (8 languages)")
man.save(D + "/manual-hp3.jpg", "JPEG", quality=90, dpi=(300, 300)); man.save(D + "/manual-hp3.pdf", resolution=300)
md = ["# HP-VER3 — %s\n" % TITLE["ja"], "\n> Translation note / 翻訳について: the non-Japanese texts were written by an AI and have NOT been checked by human native speakers. 日本語以外の文章は AI が書いたもので、ネイティブスピーカー (人間) による確認は未実施です。\n",
      "Figures: `amp_gain3.jpg` (gain control: 1 dB steps, three modes, two independent controls for the speaker and the headphone outputs), `amp_gain3_sim.jpg` (virtual simulation), each with the 8-language explanation below; bare figures in `figures-only/`; `manual-hp3.jpg` / `manual-hp3.pdf`; `headphone-hp3-all.pdf`. Reference design, Python calculations, not bench measurements.\n"]
for L in LANG8:
    md.append("## %s\n" % NAME8[L]); md.append("**%s**\n" % dec(L, TITLE[L]))
    for k in ("g3", "g3sim", "jacks", "sw", "pin", "rest"):
        md.append("- " + fmt(L, k))
    md.append("")
open(D + "/README.md", "w", encoding="utf-8").write("\n".join(md))
ims = [Image.open(D + "/" + n).convert("RGB") for n in ("amp_gain3.jpg", "amp_gain3_sim.jpg", "manual-hp3.jpg")]
ims[0].save(D + "/headphone-hp3-all.pdf", save_all=True, append_images=ims[1:], resolution=300)
print("done")
