# -*- coding: utf-8 -*-
"""Revised hybrid-volume schematic in 10 languages -> JPG per language + one multi-page PDF.
Usage: python volume_fig_ml.py <ver8|sv11> <out_dir>
Texts are AI-written, not checked by native speakers. Numbers come from volume_sim.py (Python emulation, not bench measurements)."""
import sys, os, math
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
LANGS = ["ja","en","de","ru","uk","it","fr","es","ar","fa"]
NAMES = {"ja":"日本語","en":"English","de":"Deutsch","ru":"Русский","uk":"Українська","it":"Italiano","fr":"Français","es":"Español","ar":"العربية","fa":"فارسی"}
Z0 = 200.0
def tpad(a, z0=Z0):
    k = 10 ** (a / 20); return z0 * (k - 1) / (k + 1), 2 * z0 * k / (k * k - 1)
D = lambda *a: list(a)
T = {
"ja": dict(
 title="ハイブリッド音量 (見直し版): クリック式 0.5dB ⇄ 滑らか式 0.01dB",
 status="設計案。音質エミュレーター = Python の計算 (実機測定ではありません)。図の説明は AI が書いたもので、ネイティブ確認は未実施です。",
 knob=D("音量ノブ","磁気エンコーダ 14bit","ブラシレスモーター (触覚)"),
 ctrl=D("FPGA / MCU","SW6: クリック式 / 滑らか式","32bit 微調整 ±0.25dB","誤差テーブル (181 位置)"),
 relay=D("ラッチ式リレー駆動","1 脚あたり 10 個","ゼロ電流側で切替"),
 inbuf=D("入力バッファ","出力抵抗 = Z0"), outbuf=D("出力バッファ","+6dB (整合による損失分)"),
 fine="微調整セル (2 進)  T 型減衰", coarse="粗調整セル 16dB × 5 (温度計コード)", lad="1 脚分のラダー (整合 Z0 = 200Ω): 全セル定インピーダンス T 型減衰器",
 clicky=D("クリック式 (SW6 = ON)","1 クリック = 0.5dB (1.5°)、181 位置","モーターの保持トルクでカチッ、5dB ごとに強く","微調整 = 0 (ビットパーフェクト可)"),
 smooth=D("滑らか式 (SW6 = OFF)","保持トルク無し・静か、刻み 0.01dB","リレー = 0.5dB 位置、間は 32bit 微調整","切替点は ∓0.5dB 同時に動かし段差を作らない"),
 emu=D("音質エミュレーターの結果","整合: 位置誤差 0.030dB 以内、隣との差 0.017dB (0.1% 抵抗 200 組)","不整合 (50Ω / 100kΩ): 最大 5.3dB ずれる → 整合が必須","ラダー雑音 0.26µV (20kHz)、−60dB の位置で SN 72dB","誤差テーブルで ±0.005dB、32bit 微調整の雑音 −194dB"),
 chg=D("旧案からの変更","① 2 進 8 セル (最大 64dB、分路抵抗 0.25Ω) → 微調整 5 + 16dB×5 (最小 65Ω)","② 入出力をバッファして Z0 で整合 (損失 6dB は出力で補う)","③ 工場で 181 位置の誤差を測り、テーブルで補正"),
 av="AV アンプ: 全 12ch が差動、各 ch・各脚に同じラダー (12×2×10 = 240 個)。ch 間の連動は誤差テーブルで揃える。"),
"en": dict(
 title="Hybrid volume (revised): clicky 0.5 dB ⇄ smooth 0.01 dB",
 status="Design proposal. The sound-quality emulator is a Python calculation, not a bench measurement. Texts were written by an AI and not checked by native speakers.",
 knob=D("Volume knob","14-bit magnetic encoder","Brushless motor (haptics)"),
 ctrl=D("FPGA / MCU","SW6: clicky / smooth","32-bit trim ±0.25 dB","Error table (181 positions)"),
 relay=D("Latching relay driver","10 relays per leg","Switching at zero current"),
 inbuf=D("Input buffer","Output impedance = Z0"), outbuf=D("Output buffer","+6 dB (matching loss)"),
 fine="Fine cells (binary)  T-pad", coarse="Coarse cells 16 dB × 5 (thermometer code)", lad="One leg of the ladder (matched Z0 = 200 ohm): every cell is a constant-impedance T-pad",
 clicky=D("Clicky mode (SW6 = ON)","One click = 0.5 dB (1.5°), 181 positions","Motor holding torque gives the click, stronger every 5 dB","Trim = 0 (bit-perfect possible)"),
 smooth=D("Smooth mode (SW6 = OFF)","No holding torque, quiet, 0.01 dB steps","Relays = 0.5 dB positions, 32-bit trim in between","At a switching point the trim moves ∓0.5 dB at once, no step"),
 emu=D("Sound-quality emulator results","Matched: position error within 0.030 dB, step error 0.017 dB (200 sets of 0.1% resistors)","Mismatched (50 ohm / 100 kohm): up to 5.3 dB off, so matching is mandatory","Ladder noise 0.26 µV (20 kHz), SNR 72 dB at the -60 dB position","Error table: ±0.005 dB; 32-bit trim noise -194 dB"),
 chg=D("Changes from the earlier plan","1) Binary 8 cells (up to 64 dB, shunt 0.25 ohm) -> 5 fine + 5 × 16 dB (smallest 65 ohm)","2) Buffers at input and output, matched at Z0 (the 6 dB loss is made up at the output)","3) The 181 errors are measured at the factory and corrected from a table"),
 av="AV amplifier: all 12 channels differential, the same ladder on every channel and leg (12 × 2 × 10 = 240 relays). Channel tracking is aligned with the error table."),
"de": dict(
 title="Hybrid-Lautstärke (überarbeitet): klickend 0,5 dB ⇄ gleitend 0,01 dB",
 status="Entwurf. Der Klangqualitäts-Emulator ist eine Python-Rechnung, keine Messung am Gerät. Texte von einer KI, nicht von Muttersprachlern geprüft.",
 knob=D("Lautstärkeknopf","Magnetischer Encoder 14 Bit","Bürstenloser Motor (Haptik)"),
 ctrl=D("FPGA / MCU","SW6: klickend / gleitend","32-Bit-Feinkorrektur ±0,25 dB","Fehlertabelle (181 Stellungen)"),
 relay=D("Latching-Relais-Treiber","10 Relais je Zweig","Schalten bei Nullstrom"),
 inbuf=D("Eingangspuffer","Ausgangsimpedanz = Z0"), outbuf=D("Ausgangspuffer","+6 dB (Anpassungsverlust)"),
 fine="Feinzellen (binär)  T-Glied", coarse="Grobzellen 16 dB × 5 (Thermometercode)", lad="Ein Zweig der Kette (angepasst, Z0 = 200 Ohm): jede Zelle ist ein T-Dämpfungsglied mit konstanter Impedanz",
 clicky=D("Klickmodus (SW6 = EIN)","Ein Klick = 0,5 dB (1,5°), 181 Stellungen","Haltemoment des Motors = Klick, alle 5 dB stärker","Korrektur = 0 (Bit-Perfect möglich)"),
 smooth=D("Gleitmodus (SW6 = AUS)","Kein Haltemoment, leise, 0,01-dB-Schritte","Relais = 0,5-dB-Stellungen, dazwischen 32-Bit-Korrektur","Am Schaltpunkt wandert die Korrektur um ∓0,5 dB, kein Sprung"),
 emu=D("Ergebnisse des Klangqualitäts-Emulators","Angepasst: Stellungsfehler bis 0,030 dB, Schrittfehler 0,017 dB (200 Sätze 0,1-%-Widerstände)","Fehlangepasst (50 Ohm / 100 kOhm): bis 5,3 dB daneben, Anpassung ist Pflicht","Rauschen der Kette 0,26 µV (20 kHz), SNR 72 dB bei −60 dB","Fehlertabelle: ±0,005 dB; Rauschen der 32-Bit-Korrektur −194 dB"),
 chg=D("Änderungen gegenüber dem früheren Entwurf","1) Binär 8 Zellen (bis 64 dB, Nebenschluss 0,25 Ohm) -> 5 fein + 5 × 16 dB (kleinster 65 Ohm)","2) Puffer an Ein- und Ausgang, Anpassung auf Z0 (die 6 dB Verlust gleicht der Ausgang aus)","3) Die 181 Fehler werden im Werk gemessen und per Tabelle korrigiert"),
 av="AV-Verstärker: alle 12 Kanäle differenziell, dieselbe Kette je Kanal und Zweig (12 × 2 × 10 = 240 Relais). Der Gleichlauf der Kanäle wird mit der Fehlertabelle abgeglichen."),
"ru": dict(
 title="Гибридная громкость (переработано): щелчки 0,5 дБ ⇄ плавно 0,01 дБ",
 status="Проект. Эмулятор качества звука — расчёт на Python, а не измерение на устройстве. Тексты написал ИИ, носители языка не проверяли.",
 knob=D("Ручка громкости","Магнитный энкодер 14 бит","Бесколлекторный мотор (тактильная отдача)"),
 ctrl=D("ПЛИС / MCU","SW6: щелчки / плавно","32-бит подстройка ±0,25 дБ","Таблица ошибок (181 положение)"),
 relay=D("Драйвер реле с фиксацией","10 реле на плечо","Переключение при нулевом токе"),
 inbuf=D("Входной буфер","Выходное сопротивление = Z0"), outbuf=D("Выходной буфер","+6 дБ (потери согласования)"),
 fine="Точные ячейки (двоичные)  Т-аттенюатор", coarse="Грубые ячейки 16 дБ × 5 (термометрический код)", lad="Одно плечо цепочки (согласование Z0 = 200 Ом): каждая ячейка — Т-аттенюатор с постоянным импедансом",
 clicky=D("Режим щелчков (SW6 = ВКЛ)","Один щелчок = 0,5 дБ (1,5°), 181 положение","Удерживающий момент мотора даёт щелчок, сильнее каждые 5 дБ","Подстройка = 0 (возможен бит-в-бит)"),
 smooth=D("Плавный режим (SW6 = ВЫКЛ)","Без удерживающего момента, тихо, шаг 0,01 дБ","Реле = положения через 0,5 дБ, между ними 32-бит подстройка","В точке переключения подстройка смещается на ∓0,5 дБ, скачка нет"),
 emu=D("Результаты эмулятора качества звука","Согласовано: ошибка положения до 0,030 дБ, шага 0,017 дБ (200 наборов резисторов 0,1 %)","Рассогласование (50 Ом / 100 кОм): до 5,3 дБ — согласование обязательно","Шум цепочки 0,26 мкВ (20 кГц), SNR 72 дБ в положении −60 дБ","Таблица ошибок: ±0,005 дБ; шум 32-бит подстройки −194 дБ"),
 chg=D("Изменения по сравнению с прежним проектом","1) Двоичные 8 ячеек (до 64 дБ, шунт 0,25 Ом) -> 5 точных + 5 × 16 дБ (минимум 65 Ом)","2) Буферы на входе и выходе, согласование по Z0 (6 дБ потерь компенсирует выход)","3) 181 ошибку измеряют на заводе и исправляют по таблице"),
 av="AV-усилитель: все 12 каналов дифференциальные, одна цепочка на каждый канал и плечо (12 × 2 × 10 = 240 реле). Согласование каналов выравнивается таблицей ошибок."),
"uk": dict(
 title="Гібридна гучність (перероблено): клацання 0,5 дБ ⇄ плавно 0,01 дБ",
 status="Проєкт. Емулятор якості звуку — розрахунок на Python, а не вимірювання на пристрої. Тексти написав ШІ, носії мови не перевіряли.",
 knob=D("Ручка гучності","Магнітний енкодер 14 біт","Безколекторний мотор (тактильний відгук)"),
 ctrl=D("ПЛІС / MCU","SW6: клацання / плавно","32-біт підстроювання ±0,25 дБ","Таблиця похибок (181 положення)"),
 relay=D("Драйвер реле з фіксацією","10 реле на плече","Перемикання при нульовому струмі"),
 inbuf=D("Вхідний буфер","Вихідний опір = Z0"), outbuf=D("Вихідний буфер","+6 дБ (втрати узгодження)"),
 fine="Точні комірки (двійкові)  Т-атенюатор", coarse="Грубі комірки 16 дБ × 5 (термометричний код)", lad="Одне плече ланцюжка (узгодження Z0 = 200 Ом): кожна комірка — Т-атенюатор зі сталим імпедансом",
 clicky=D("Режим клацань (SW6 = УВІМК)","Одне клацання = 0,5 дБ (1,5°), 181 положення","Утримувальний момент мотора дає клацання, сильніше кожні 5 дБ","Підстроювання = 0 (можливий біт-у-біт)"),
 smooth=D("Плавний режим (SW6 = ВИМК)","Без утримувального моменту, тихо, крок 0,01 дБ","Реле = положення через 0,5 дБ, між ними 32-біт підстроювання","У точці перемикання підстроювання зміщується на ∓0,5 дБ, стрибка немає"),
 emu=D("Результати емулятора якості звуку","Узгоджено: похибка положення до 0,030 дБ, кроку 0,017 дБ (200 наборів резисторів 0,1 %)","Неузгоджено (50 Ом / 100 кОм): до 5,3 дБ — узгодження обов'язкове","Шум ланцюжка 0,26 мкВ (20 кГц), SNR 72 дБ у положенні −60 дБ","Таблиця похибок: ±0,005 дБ; шум 32-біт підстроювання −194 дБ"),
 chg=D("Зміни порівняно з попереднім проєктом","1) Двійкові 8 комірок (до 64 дБ, шунт 0,25 Ом) -> 5 точних + 5 × 16 дБ (мінімум 65 Ом)","2) Буфери на вході й виході, узгодження за Z0 (6 дБ втрат компенсує вихід)","3) 181 похибку вимірюють на заводі й виправляють за таблицею"),
 av="AV-підсилювач: усі 12 каналів диференціальні, один ланцюжок на кожен канал і плече (12 × 2 × 10 = 240 реле). Узгодження каналів вирівнюється таблицею похибок."),
"it": dict(
 title="Volume ibrido (rivisto): a scatti 0,5 dB ⇄ fluido 0,01 dB",
 status="Proposta di progetto. L'emulatore di qualità sonora è un calcolo in Python, non una misura su hardware. Testi scritti da un'IA, non verificati da madrelingua.",
 knob=D("Manopola del volume","Encoder magnetico a 14 bit","Motore brushless (feedback tattile)"),
 ctrl=D("FPGA / MCU","SW6: a scatti / fluido","Regolazione fine a 32 bit ±0,25 dB","Tabella degli errori (181 posizioni)"),
 relay=D("Pilota dei relè a ritenuta","10 relè per ramo","Commutazione a corrente zero"),
 inbuf=D("Buffer d'ingresso","Impedenza d'uscita = Z0"), outbuf=D("Buffer d'uscita","+6 dB (perdita di adattamento)"),
 fine="Celle fini (binarie)  attenuatore a T", coarse="Celle grosse 16 dB × 5 (codice a termometro)", lad="Un ramo della scala (adattata, Z0 = 200 ohm): ogni cella è un attenuatore a T a impedenza costante",
 clicky=D("Modalità a scatti (SW6 = ON)","Uno scatto = 0,5 dB (1,5°), 181 posizioni","La coppia di tenuta del motore dà lo scatto, più forte ogni 5 dB","Regolazione fine = 0 (bit-perfect possibile)"),
 smooth=D("Modalità fluida (SW6 = OFF)","Senza coppia di tenuta, silenziosa, passi da 0,01 dB","Relè = posizioni da 0,5 dB, in mezzo la regolazione a 32 bit","Al punto di commutazione la regolazione si sposta di ∓0,5 dB, nessun gradino"),
 emu=D("Risultati dell'emulatore di qualità sonora","Adattato: errore di posizione entro 0,030 dB, di passo 0,017 dB (200 serie di resistenze allo 0,1 %)","Disadattato (50 ohm / 100 kohm): fino a 5,3 dB di scarto, l'adattamento è obbligatorio","Rumore della scala 0,26 µV (20 kHz), SNR 72 dB alla posizione −60 dB","Tabella errori: ±0,005 dB; rumore della regolazione a 32 bit −194 dB"),
 chg=D("Modifiche rispetto al piano precedente","1) Binarie 8 celle (fino a 64 dB, shunt 0,25 ohm) -> 5 fini + 5 × 16 dB (minimo 65 ohm)","2) Buffer in ingresso e in uscita, adattamento su Z0 (i 6 dB persi sono recuperati in uscita)","3) I 181 errori sono misurati in fabbrica e corretti con una tabella"),
 av="Amplificatore AV: tutti i 12 canali differenziali, la stessa scala su ogni canale e ramo (12 × 2 × 10 = 240 relè). L'inseguimento tra i canali si allinea con la tabella degli errori."),
"fr": dict(
 title="Volume hybride (révisé) : crans 0,5 dB ⇄ fluide 0,01 dB",
 status="Proposition de conception. L'émulateur de qualité sonore est un calcul Python, pas une mesure sur matériel. Textes écrits par une IA, non vérifiés par des locuteurs natifs.",
 knob=D("Bouton de volume","Codeur magnétique 14 bits","Moteur brushless (retour haptique)"),
 ctrl=D("FPGA / MCU","SW6 : crans / fluide","Réglage fin 32 bits ±0,25 dB","Table d'erreurs (181 positions)"),
 relay=D("Pilote de relais à verrouillage","10 relais par branche","Commutation à courant nul"),
 inbuf=D("Tampon d'entrée","Impédance de sortie = Z0"), outbuf=D("Tampon de sortie","+6 dB (perte d'adaptation)"),
 fine="Cellules fines (binaires)  atténuateur en T", coarse="Cellules grosses 16 dB × 5 (code thermomètre)", lad="Une branche de l'échelle (adaptée, Z0 = 200 ohms) : chaque cellule est un atténuateur en T à impédance constante",
 clicky=D("Mode à crans (SW6 = ON)","Un cran = 0,5 dB (1,5°), 181 positions","Le couple de maintien du moteur donne le cran, plus fort tous les 5 dB","Réglage fin = 0 (bit-perfect possible)"),
 smooth=D("Mode fluide (SW6 = OFF)","Sans couple de maintien, silencieux, pas de 0,01 dB","Relais = positions de 0,5 dB, entre elles le réglage 32 bits","Au point de commutation le réglage se déplace de ∓0,5 dB, sans marche"),
 emu=D("Résultats de l'émulateur de qualité sonore","Adapté : erreur de position jusqu'à 0,030 dB, de pas 0,017 dB (200 jeux de résistances à 0,1 %)","Désadapté (50 ohms / 100 kohms) : jusqu'à 5,3 dB d'écart, l'adaptation est obligatoire","Bruit de l'échelle 0,26 µV (20 kHz), SNR 72 dB à la position −60 dB","Table d'erreurs : ±0,005 dB ; bruit du réglage 32 bits −194 dB"),
 chg=D("Changements par rapport au plan précédent","1) Binaire 8 cellules (jusqu'à 64 dB, shunt 0,25 ohm) -> 5 fines + 5 × 16 dB (minimum 65 ohms)","2) Tampons en entrée et en sortie, adaptation sur Z0 (les 6 dB perdus sont rattrapés en sortie)","3) Les 181 erreurs sont mesurées en usine et corrigées par table"),
 av="Amplificateur AV : les 12 canaux différentiels, la même échelle sur chaque canal et branche (12 × 2 × 10 = 240 relais). Le suivi entre canaux est aligné par la table d'erreurs."),
"es": dict(
 title="Volumen híbrido (revisado): clics 0,5 dB ⇄ suave 0,01 dB",
 status="Propuesta de diseño. El emulador de calidad de sonido es un cálculo en Python, no una medición en hardware. Textos escritos por una IA, no revisados por hablantes nativos.",
 knob=D("Mando de volumen","Codificador magnético de 14 bits","Motor sin escobillas (háptico)"),
 ctrl=D("FPGA / MCU","SW6: clics / suave","Ajuste fino de 32 bits ±0,25 dB","Tabla de errores (181 posiciones)"),
 relay=D("Controlador de relés de enclavamiento","10 relés por rama","Conmutación con corriente cero"),
 inbuf=D("Búfer de entrada","Impedancia de salida = Z0"), outbuf=D("Búfer de salida","+6 dB (pérdida de adaptación)"),
 fine="Celdas finas (binarias)  atenuador en T", coarse="Celdas gruesas 16 dB × 5 (código termómetro)", lad="Una rama de la escalera (adaptada, Z0 = 200 ohmios): cada celda es un atenuador en T de impedancia constante",
 clicky=D("Modo con clics (SW6 = ON)","Un clic = 0,5 dB (1,5°), 181 posiciones","El par de retención del motor da el clic, más fuerte cada 5 dB","Ajuste fino = 0 (posible bit-perfect)"),
 smooth=D("Modo suave (SW6 = OFF)","Sin par de retención, silencioso, pasos de 0,01 dB","Relés = posiciones de 0,5 dB, entre ellas el ajuste de 32 bits","En el punto de conmutación el ajuste se mueve ∓0,5 dB, sin escalón"),
 emu=D("Resultados del emulador de calidad de sonido","Adaptado: error de posición hasta 0,030 dB, de paso 0,017 dB (200 juegos de resistencias al 0,1 %)","Desadaptado (50 ohmios / 100 kohmios): hasta 5,3 dB de desvío, la adaptación es obligatoria","Ruido de la escalera 0,26 µV (20 kHz), SNR 72 dB en la posición −60 dB","Tabla de errores: ±0,005 dB; ruido del ajuste de 32 bits −194 dB"),
 chg=D("Cambios respecto al plan anterior","1) Binario de 8 celdas (hasta 64 dB, derivación 0,25 ohmios) -> 5 finas + 5 × 16 dB (mínimo 65 ohmios)","2) Búferes en entrada y salida, adaptación en Z0 (los 6 dB perdidos se recuperan en la salida)","3) Los 181 errores se miden en fábrica y se corrigen con una tabla"),
 av="Amplificador AV: los 12 canales diferenciales, la misma escalera en cada canal y rama (12 × 2 × 10 = 240 relés). El seguimiento entre canales se alinea con la tabla de errores."),
"ar": dict(
 title="مستوى صوت هجين (منقَّح): نقرات 0.5 ديسيبل ⇄ سلس 0.01 ديسيبل",
 status="مقترح تصميم. محاكي جودة الصوت حسابات بلغة Python وليس قياسًا على جهاز فعلي. كتب الذكاء الاصطناعي النصوص ولم يراجعها ناطقون أصليون.",
 knob=D("مقبض مستوى الصوت","مشفّر مغناطيسي 14 بت","محرّك بلا فرش (استجابة لمسية)"),
 ctrl=D("FPGA / MCU","SW6: نقرات / سلس","ضبط دقيق 32 بت ±0.25 ديسيبل","جدول أخطاء (181 موضعًا)"),
 relay=D("مشغّل المرحّلات ذات التثبيت","10 مرحّلات لكل فرع","التبديل عند تيار صفري"),
 inbuf=D("مخزن الدخل","مقاومة الخرج = Z0"), outbuf=D("مخزن الخرج","+6 ديسيبل (فقد التوافق)"),
 fine="خلايا دقيقة (ثنائية)  مخفّض T", coarse="خلايا خشنة 16 ديسيبل × 5 (شفرة ترمومتر)", lad="فرع واحد من السلّم (توافق Z0 = 200 أوم): كل خلية مخفّض T ثابت المعاوقة",
 clicky=D("وضع النقرات (SW6 = تشغيل)","نقرة = 0.5 ديسيبل (1.5°)، 181 موضعًا","عزم تثبيت المحرّك يعطي النقرة، وأقوى كل 5 ديسيبل","الضبط الدقيق = 0 (ممكن بت بيرفكت)"),
 smooth=D("الوضع السلس (SW6 = إيقاف)","بلا عزم تثبيت، هادئ، خطوة 0.01 ديسيبل","المرحّلات = مواضع 0.5 ديسيبل، وبينها ضبط 32 بت","عند نقطة التبديل يتحرك الضبط ∓0.5 ديسيبل فلا قفزة"),
 emu=D("نتائج محاكي جودة الصوت","متوافق: خطأ الموضع حتى 0.030 ديسيبل، وخطأ الخطوة 0.017 (200 مجموعة مقاومات 0.1%)","غير متوافق (50 أوم / 100 كيلو أوم): انحراف حتى 5.3 ديسيبل فالتوافق إلزامي","ضجيج السلّم 0.26 µV (20 كيلوهرتز)، SNR 72 ديسيبل عند موضع −60","جدول الأخطاء: ±0.005 ديسيبل؛ ضجيج ضبط 32 بت −194 ديسيبل"),
 chg=D("التغييرات عن الخطة السابقة","1) ثنائي 8 خلايا (حتى 64 ديسيبل، تفرّع 0.25 أوم) -> 5 دقيقة + 5 × 16 ديسيبل (الأدنى 65 أوم)","2) مخزنان عند الدخل والخرج وتوافق عند Z0 (يُعوَّض فقد 6 ديسيبل عند الخرج)","3) تُقاس الأخطاء الـ181 في المصنع وتُصحَّح بجدول"),
 av="مضخّم AV: القنوات الـ12 كلها تفاضلية، والسلّم نفسه لكل قناة وفرع (12 × 2 × 10 = 240 مرحّلًا). يُوحَّد تطابق القنوات بجدول الأخطاء."),
"fa": dict(
 title="ولوم ترکیبی (بازبینی‌شده): کلیکی 0.5 دسی‌بل ⇄ نرم 0.01 دسی‌بل",
 status="پیشنهاد طراحی. شبیه‌ساز کیفیت صدا محاسبهٔ پایتون است و اندازه‌گیری روی سخت‌افزار نیست. متن‌ها را هوش مصنوعی نوشته و گویشوران بومی بررسی نکرده‌اند.",
 knob=D("دستگیرهٔ ولوم","انکودر مغناطیسی 14 بیتی","موتور بدون جاروبک (بازخورد لمسی)"),
 ctrl=D("FPGA / MCU","SW6: کلیکی / نرم","تنظیم دقیق 32 بیتی ±0.25 دسی‌بل","جدول خطا (181 موقعیت)"),
 relay=D("راه‌انداز رله‌های قفل‌شونده","10 رله برای هر شاخه","سوئیچ در جریان صفر"),
 inbuf=D("بافر ورودی","امپدانس خروجی = Z0"), outbuf=D("بافر خروجی","+6 دسی‌بل (تلفات تطبیق)"),
 fine="سلول‌های ریز (دودویی)  تضعیف‌کنندهٔ T", coarse="سلول‌های درشت 16 دسی‌بل × 5 (کد دماسنجی)", lad="یک شاخه از نردبان (تطبیق Z0 = 200 اهم): هر سلول تضعیف‌کنندهٔ T با امپدانس ثابت است",
 clicky=D("حالت کلیکی (SW6 = روشن)","هر کلیک = 0.5 دسی‌بل (1.5°)، 181 موقعیت","گشتاور نگهدارندهٔ موتور کلیک می‌دهد، هر 5 دسی‌بل قوی‌تر","تنظیم دقیق = 0 (بیت‌پرفکت ممکن)"),
 smooth=D("حالت نرم (SW6 = خاموش)","بدون گشتاور نگهدارنده، آرام، گام 0.01 دسی‌بل","رله‌ها = موقعیت‌های 0.5 دسی‌بل، میان آن‌ها تنظیم 32 بیتی","در نقطهٔ سوئیچ تنظیم ∓0.5 دسی‌بل جابه‌جا می‌شود، بدون پله"),
 emu=D("نتایج شبیه‌ساز کیفیت صدا","تطبیق‌یافته: خطای موقعیت تا 0.030 دسی‌بل، خطای گام 0.017 (200 مجموعه مقاومت 0.1٪)","نامتطبق (50 اهم / 100 کیلواهم): تا 5.3 دسی‌بل انحراف، پس تطبیق الزامی است","نویز نردبان 0.26 µV (20 کیلوهرتز)، SNR 72 دسی‌بل در موقعیت −60","جدول خطا: ±0.005 دسی‌بل؛ نویز تنظیم 32 بیتی −194 دسی‌بل"),
 chg=D("تغییرات نسبت به طرح قبلی","1) دودویی 8 سلول (تا 64 دسی‌بل، شنت 0.25 اهم) -> 5 ریز + 5 × 16 دسی‌بل (کمینه 65 اهم)","2) بافر در ورودی و خروجی و تطبیق در Z0 (تلفات 6 دسی‌بل در خروجی جبران می‌شود)","3) 181 خطا در کارخانه اندازه‌گیری و با جدول اصلاح می‌شود"),
 av="آمپلی‌فایر AV: هر 12 کانال تفاضلی‌اند، همان نردبان روی هر کانال و شاخه (12 × 2 × 10 = 240 رله). هم‌گامی کانال‌ها با جدول خطا یکسان می‌شود."),
}
W, H = 3200, 2080
def font(l, sz, bold=False):
    if l == "ja": return ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc" if bold else "C:/Windows/Fonts/meiryo.ttc", sz)
    return ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf", sz)
def shape(l, s):
    if l != "ja": s = s.replace("⇄", "↔").replace("∓", "-/+")
    return get_display(arabic_reshaper.reshape(s)) if l in ("ar", "fa") else s
def wrap(l, s, f, w):
    words, out, cur = s.split(" "), [], ""
    if l == "ja" or l == "zh":
        words = list(s)
    for wd in words:
        t = (cur + ("" if l == "ja" else " ") + wd).strip() if cur else wd
        if f.getlength(shape(l, t)) > w and cur: out.append(cur); cur = wd
        else: cur = t
    out.append(cur); return out
def build(kind, outdir):
    name = "SV-VER11" if kind == "sv11" else "VER8"
    os.makedirs(outdir, exist_ok=True); pages = []
    INK, GR, OR, BL = (20, 30, 60), (25, 115, 60), (190, 100, 20), (30, 70, 180)
    for l in LANGS:
        t = T[l]; im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
        F = lambda sz, b=False: font(l, sz, b)
        def txt(x, y, s, sz, col=INK, b=False, anchor="mm", wmax=None):
            f = F(sz, b); lines = wrap(l, s, f, wmax) if wmax else [s]
            for i, ln in enumerate(lines): d.text((x, y + i * sz * 1.3), shape(l, ln), font=f, fill=col, anchor=anchor)
            return len(lines)
        def box(x0, y0, x1, y1, lines, col, szs=(40, 34)):
            d.rectangle([x0, y0, x1, y1], outline=col, width=6, fill=(250, 250, 240))
            y = y0 + 28
            for i, s in enumerate(lines):
                n = txt((x0 + x1) / 2, y, s, szs[0] if i == 0 else szs[1], INK, i == 0, "mt", x1 - x0 - 40)
                y += int((szs[0] if i == 0 else szs[1]) * 1.3 * n + 10)
        def arrow(x0, y, x1, col):
            d.line([x0, y, x1, y], fill=col, width=7); d.polygon([(x1, y), (x1 - 26, y - 14), (x1 - 26, y + 14)], fill=col)
        txt(60, 50, name + "  " + t["title"], 64, INK, True, "lm" if l not in ("ar", "fa") else "rm") if False else None
        d.text((60 if l not in ("ar", "fa") else W - 60, 40), shape(l, name + " — " + t["title"]), font=F(64, True), fill=INK, anchor="la" if l not in ("ar", "fa") else "ra")
        for i, ln in enumerate(wrap(l, t["status"], F(34), W - 120)):
            d.text((60 if l not in ("ar", "fa") else W - 60, 130 + i * 44), shape(l, ln), font=F(34), fill=(190, 30, 30), anchor="la" if l not in ("ar", "fa") else "ra")
        # top row blocks
        box(60, 230, 640, 560, t["knob"], GR); arrow(640, 395, 720, BL)
        box(720, 230, 1400, 560, t["ctrl"], BL); arrow(1400, 395, 1480, OR)
        box(1480, 230, 2160, 560, t["relay"], OR)
        # ladder
        txt(60, 610, t["lad"], 38, INK, True, "lt", W - 120)
        y = 880; x = 60
        box(x, y - 120, x + 330, y + 120, t["inbuf"], GR, (34, 30)); x += 330; arrow(x, y, x + 50, GR); x += 50
        cells = [0.5, 1, 2, 4, 8] + [16] * 5; cw, gap = 215, 24
        for i, a in enumerate(cells):
            r1, r2 = tpad(a)
            d.rectangle([x, y - 120, x + cw, y + 120], outline=(BL if i < 5 else OR), width=6, fill=(245, 248, 255) if i < 5 else (255, 248, 240))
            txt(x + cw / 2, y - 100, "K%d" % (i + 1), 38, INK, True, "mt")
            txt(x + cw / 2, y - 50, "%g dB" % a, 40, INK, True, "mt")
            txt(x + cw / 2, y + 5, "R1 %.1f Ω" % r1, 28, (90, 90, 90), False, "mt")
            txt(x + cw / 2, y + 45, "R2 %.1f Ω" % r2, 28, (90, 90, 90), False, "mt")
            d.line([x - gap, y, x, y], fill=INK, width=5)
            x += cw + gap
        arrow(x - gap, y, x + 20, GR); x += 20
        box(x, y - 120, W - 60, y + 120, t["outbuf"], GR, (34, 30))
        txt(60 + 330 + 50, y + 150, t["fine"], 32, BL, True, "lt"); txt(60 + 330 + 50 + 5 * (cw + gap) + 10, y + 150, t["coarse"], 32, OR, True, "lt")
        # bottom boxes
        bw = (W - 60 * 2 - 40 * 3) // 4
        b = [(t["clicky"], OR), (t["smooth"], BL), (t["emu"], GR), (t["chg"], (150, 30, 90))]
        for i, (lines, col) in enumerate(b):
            box(60 + i * (bw + 40), 1150, 60 + i * (bw + 40) + bw, 1790, lines, col, (40, 32))
        if kind == "sv11":
            d.rectangle([60, 1840, W - 60, 1990], outline=INK, width=5, fill=(240, 244, 255))
            for i, ln in enumerate(wrap(l, t["av"], F(38), W - 160)):
                d.text((W / 2, 1870 + i * 50), shape(l, ln), font=F(38), fill=INK, anchor="mt")
        d.text((W - 60, H - 40), "%s  %s" % (name, NAMES[l]), font=F(30), fill=(110, 110, 110), anchor="rd")
        p = os.path.join(outdir, "%s-volume-%s.jpg" % (kind, l)); im.save(p, "JPEG", quality=90, dpi=(300, 300)); pages.append(im)
    pdf = os.path.join(outdir, "%s-volume-10lang.pdf" % kind)
    pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=300); print(outdir, "done", pdf)
if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2])
