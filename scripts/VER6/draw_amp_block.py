from PIL import Image, ImageDraw, ImageFont

W, H = 200, 130
S = 32
img = Image.new("RGB", (W * S, H * S), "white")
d = ImageDraw.Draw(img)
LW = int(S * 0.13)
INK = (20, 30, 60)
HOT = (190, 30, 30)
COLD = (30, 70, 180)
GRY = (110, 110, 110)
ORG = (170, 90, 10)


def F(size, bold=False):
    name = "meiryob.ttc" if bold else "meiryo.ttc"
    return ImageFont.truetype("C:/Windows/Fonts/" + name, int(size * S * 0.92))


def P(x, y):
    return (x * S, (H - y) * S)


def line(pts, col=INK, w=LW):
    pp = [P(*p) for p in pts]
    d.line(pp, fill=col, width=w, joint="curve")
    for p in (pp[0], pp[-1]):
        d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=col)


def dot(x, y, col=INK):
    px, py = P(x, y)
    r = S * 0.32
    d.ellipse([px - r, py - r, px + r, py + r], fill=col)


def text(x, y, s, size=1.6, col=INK, anchor="la", bold=False):
    d.text(P(x, y), s, fill=col, font=F(size, bold), anchor=anchor)


def circ(x, y, r, col, fill="white"):
    px, py = P(x, y)
    d.ellipse([px - S * r, py - S * r, px + S * r, py + S * r], outline=col, width=LW, fill=fill)


def res(x, y, label, val, col=INK, vertical=False):
    L, Wd = 8, 2.6
    if vertical:
        d.rectangle([*P(x - Wd / 2, y + L / 2), *P(x + Wd / 2, y - L / 2)], outline=col, width=LW)
        text(x + 2.2, y + 0.3, label, 1.5, col, "lm", True)
        text(x + 2.2, y - 1.4, val, 1.3, GRY, "lm")
    else:
        d.rectangle([*P(x - L / 2, y + Wd / 2), *P(x + L / 2, y - Wd / 2)], outline=col, width=LW)
        text(x, y + 3.6, label, 1.5, col, "mm", True)
        text(x, y + 1.9, val, 1.3, GRY, "mm")


def vcap(x, y, label, val, col=INK, left=False):
    g, h = 0.9, 2.6
    line([(x - h, y + g), (x + h, y + g)], col)
    line([(x - h, y - g), (x + h, y - g)], col)
    if left:
        text(x - 3.4, y + 0.3, label, 1.5, col, "rm", True)
        text(x - 3.4, y - 1.4, val, 1.3, GRY, "rm")
    else:
        text(x + 3.4, y + 0.3, label, 1.5, col, "lm", True)
        text(x + 3.4, y - 1.4, val, 1.3, GRY, "lm")


def gnd(x, y):
    line([(x, y), (x, y - 1.5)])
    line([(x - 1.8, y - 1.5), (x + 1.8, y - 1.5)])
    line([(x - 1.1, y - 2.3), (x + 1.1, y - 2.3)])
    line([(x - 0.4, y - 3.1), (x + 0.4, y - 3.1)])


def opamp(cx, cy, name, part, plus_top=False, w=11, h=13):
    x0, x1 = cx - w / 2, cx + w / 2
    pts = [P(x0, cy + h / 2), P(x0, cy - h / 2), P(x1, cy)]
    d.polygon(pts, outline=INK, fill=(250, 250, 235))
    d.line(pts + [pts[0]], fill=INK, width=LW)
    top, bot = cy + h / 4, cy - h / 4
    plus_y, minus_y = (top, bot) if plus_top else (bot, top)
    text(x0 + 1.0, plus_y, "+", 2.0, INK, "lm", True)
    text(x0 + 1.0, minus_y, "\u2212", 2.0, INK, "lm", True)
    text(cx - 1.2, cy + h / 2 + 1.2, name, 1.7, INK, "mm", True)
    text(cx - 1.2, cy - h / 2 - 1.6, part, 1.3, GRY, "mm")
    return (x0, plus_y), (x0, minus_y), (x1, cy)


def frame(x0, y0, x1, y1, title):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=(150, 160, 190), width=int(LW * 0.7))
    text(x0 + 1, y1 - 0.8, title, 1.9, (60, 80, 150), "la", True)


DIG = (30, 70, 180)
ANA = (25, 115, 60)
PWR = (190, 100, 20)
CTL = (110, 110, 110)


def box(x0, y0, x1, y1, lines, col, fill=(250, 250, 240)):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=col, width=LW, fill=fill)
    n = len(lines)
    cy = (y0 + y1) / 2
    top = cy + (n - 1) * 1.05
    for i, (t, sz, b, c) in enumerate(lines):
        text((x0 + x1) / 2, top - 2.1 * i, t, sz, c or INK, "mm", b)


def arrow(pts, col=INK):
    line(pts, col)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    import math
    a = math.atan2(y1 - y0, x1 - x0)
    L = 1.8
    for s in (0.45, -0.45):
        line([(x1, y1), (x1 - L * math.cos(a - s), y1 - L * math.sin(a - s))], col)


def L(t, sz=1.15, b=False, c=None):
    return (t, sz, b, c)


text(3, 127, "最新ネットワーク対応 全段バランス プリメインアンプ  Network-Streaming Fully Balanced Integrated Amplifier  VER5", 2.4, INK, "la", True)
text(3, 123.6, "WiFi / LAN・ブラウザ: U-NEXT・YouTube・Qobuz 再生 (HDMI / USB-C 映像出力つき)  |  USB-C / I2S: PCM 最大 32bit/1536kHz・DSD 最大 DSD1024  |  "
     "PRE OUT (XLR+RCA)・SUB OUT (XLR+RCA)・バイワイヤリング対応スピーカー端子", 1.45, GRY)
text(3, 121.2, "参考設計 Reference design  |  DAC: AK4191 + BD34302 (PCM 1536kHz / DSD1024)  すべて MQA 対応 (専用の MQA フルデコーダ XU316 を DAC とは別に搭載)  All versions support MQA.", 1.2, GRY)
text(150, 119.0, "青 digital", 1.2, DIG, "la", True)
text(163, 119.0, "緑 analog", 1.2, ANA, "la", True)
text(176, 119.0, "橙 power", 1.2, PWR, "la", True)
text(188, 119.0, "灰 control", 1.2, CTL, "la", True)

# ---------------- row 1 : inputs
box(2, 99, 24, 116, [L("無線LAN / 有線LAN", 1.2, True), L("Wi-Fi 8 (802.11bn) *", 1.05, True), L("GbE / RJ45 端子", 1.05)], DIG)
box(28, 99, 64, 116, [L("ネットワーク・ストリーマ", 1.2, True), L("Network streamer", 1.1), L("Android系SoC (認証取得済モジュール)", 1.0), L("ブラウザ / U-NEXT / YouTube / Qobuz", 1.0), L("Roon / AirPlay / UPnP", 1.05)], DIG)
box(68, 99, 94, 116, [L("USB-C 入力 (UAC2)", 1.2, True), L("DDC 内蔵 USB→I2S", 1.1, True), L("Pisces III 型 STM32+FPGA", 1.0), L("PCM 1536k / DSD1024", 1.0)], DIG)
box(98, 99, 124, 116, [L("I2S 入力", 1.2, True), L("LVDS / HDMI形 or RJ45", 1.05), L("PCM 32bit/1536k", 1.05), L("DSD1024", 1.05)], DIG)
box(128, 99, 154, 116, [L("Bluetooth + その他入力", 1.2, True), L("Bluetooth 6.x / LE Audio", 1.0), L("Auracast / LC3", 1.0), L("LDAC / aptX Adaptive・Lossless", 0.95), L("光 / 同軸 / AES (任意)", 1.0)], DIG)
box(158, 99, 198, 116, [L("制御 Control", 1.3, True), L("MCU + 表示 + リモコン", 1.1), L("アプリ / OTA更新", 1.1), L("保護・温度監視", 1.1), L("モード: DDC+DAC / DAC / DDC / なし", 1.0)], CTL)

# ---------------- row 2 : digital core
box(28, 68, 96, 88, [L("デジタル・フロントエンド (FPGA)  Digital front end", 1.4, True),
                     L("入力選択・形式 / レート自動検出  Input select & format detect", 1.15),
                     L("PCM 1536kHz / DSD1024 をそのまま AK4191 へ・I2C で DAC 設定  Pass-through, I2C setup", 1.1),
                     L("DSD1024 ネイティブ / DoP 対応  Native DSD1024", 1.15),
                     L("デジタル Vol/EQ は SW5 でバイパス (ビットパーフェクト)  (MQA は右のデコーダへ)", 1.1)], DIG)
box(2, 68, 24, 88, [L("超低ジッタ", 1.2, True), L("クロック", 1.2, True), L("45.1584 /", 1.1), L("49.152 MHz", 1.1), L("≤100fs + 外部CLK", 1.0)], DIG)
box(128, 68, 154, 88, [L("デジタル", 1.2, True), L("アイソレータ", 1.2, True), L("Si86xx / ADuM 系", 1.0), L("GND分離", 1.1)], DIG)
arrow([(46, 99), (46, 88)], DIG)
line([(111, 99), (111, 90.5), (90, 90.5)], DIG)
arrow([(90, 90.5), (90, 88)], DIG)
arrow([(141, 99), (141, 91), (126, 91), (126, 88)] if False else [(141, 99), (141, 88)], DIG)
arrow([(24, 116 - 8.5), (28, 116 - 8.5)], DIG)
# ---- USB-C DDC : ON/OFF of the I2S-connected DDC
arrow([(81, 99), (81, 96)], DIG)
box(70, 92, 92, 96, [L("SW1 DDC+DAC I2S ON/OFF", 0.95, True, (170, 90, 10))], (200, 120, 20))
arrow([(81, 92), (81, 88)], DIG)
text(83, 90.0, "ON", 1.0, DIG, "lm", True)
box(50, 90.5, 66, 97.5, [L("I2S OUT RJ45/HDMI", 0.95, True), L("(外部DAC用)", 0.95)], DIG)
arrow([(70, 94), (66, 94)], DIG)
text(68, 97.4, "OFF", 1.0, DIG, "rm", True)
box(2, 89.2, 24, 97.8, [L("映像出力 HDMI + USB-C", 1.0, True), L("(DP Alt) ブラウザ画面", 0.95)], DIG)
arrow([(28, 101), (26, 101), (26, 93.5), (24, 93.5)], DIG)
box(158, 89.5, 198, 97.5, [L("音質改善回路・機能 (最新)", 1.05, True, PWR), L("SW3 無線 ON/OFF・RFシールド・別LDO・再クロック", 0.95)], PWR)

arrow([(24, 78), (28, 78)], DIG)
box(100, 68, 124, 88, [L("MQA フル", 1.1, True), L("デコーダ", 1.1, True), L("XMOS XU316", 1.0), L("+ MQA FW", 1.0), L("(ライセンス版)", 0.95)], (170, 90, 10))
arrow([(96, 82), (100, 82)], DIG)
arrow([(100, 74), (96, 74)], DIG)
arrow([(124, 78), (128, 78)], DIG)
text(112, 66.4, "MQA時のみ展開 / 他はバイパス", 0.95, DIG, "mm")

# ---------------- row 3 : DAC / analog
box(100, 42, 154, 62, [L("DAC: AK4191 + BD34302 ×2 (L用 / R用 HDモノラル)", 1.25, True),
                       L("AK4191 (デジタルフィルタ + ΔΣ変調) → BD34302 (32bit DAC)", 1.05),
                       L("PCM 1536kHz / DSD1024 / MQA (デコード済みPCM)", 1.1),
                       L("Balanced current output, HD monaural mode", 1.1)], DIG)
arrow([(141, 68), (141, 67)], DIG)
box(128, 63, 154, 67, [L("SW2 DAC ON/OFF (電源+I2S)", 0.95, True, (170, 90, 10))], (200, 120, 20))
arrow([(141, 63), (141, 62)], DIG)
box(60, 42, 96, 62, [L("I/V変換 + LPF", 1.3, True), L("OPA1612 バランス構成", 1.15), L("I/V + low-pass (Hot / Cold)", 1.1)], ANA)
arrow([(100, 52), (96, 52)], ANA)
box(2, 42, 24, 62, [L("アナログ入力", 1.3, True), L("XLR / RCA", 1.15), L("(デジタル化せず直結)", 1.0)], ANA)
box(28, 42, 56, 62, [L("バランス・ボリューム", 1.25, True), L("電子ボリューム ×2/ch", 1.05), L("+ 入力セレクタ", 1.05), L("触覚ノブ クリック/なし SW6", 0.95)], ANA)
arrow([(24, 52), (28, 52)], ANA)
arrow([(60, 52), (56, 52)], ANA)

# ---------------- row 4 : outputs
box(28, 16, 56, 36, [L("ラインバッファ", 1.3, True), L("OPA1612 + 47Ω", 1.1), L("Line buffer (Hot / Cold)", 1.05)], ANA)
arrow([(42, 42), (42, 36)], ANA)
box(2, 26, 24, 36, [L("PRE OUT", 1.3, True), L("XLR + RCA", 1.15)], ANA)
box(2, 16, 24, 24, [L("SUB OUT (モノ)", 1.2, True), L("XLR + RCA", 1.1)], ANA)
arrow([(28, 31), (24, 31)], ANA)
arrow([(28, 20), (24, 20)], ANA)
box(60, 16, 100, 36, [L("パワーアンプ (Class-D バランス)", 1.3, True), L("Eigentakt型モジュール 例: Purifi 1ET400A", 1.05),
                      L("設計目標 2×150W / 8Ω", 1.1), L("Balanced Class-D power amp", 1.05)], ANA)
arrow([(56, 26), (60, 26)], ANA)
box(104, 16, 128, 36, [L("DC保護 +", 1.2, True), L("スピーカーリレー", 1.2, True), L("Protection", 1.05)], ANA)
arrow([(100, 26), (104, 26)], ANA)
box(132, 14, 154, 38, [L("スピーカー端子", 1.2, True), L("バイワイヤ対応", 1.2, True), L("HF+ / HF−", 1.05), L("LF+ / LF−", 1.05), L("(Lch・Rch 各2組)", 1.0)], ANA)
arrow([(128, 26), (132, 26)], ANA)

# ---------------- power column
box(158, 16, 198, 48, [L("ヘッドホンアンプ (VER5)", 1.2, True, ANA), L("3.5mm バランス/SE 兼用 · 4.4mm バランス", 0.95), L("6.35mm SE (3種類)", 0.95), L("スピーカーと同時に動作", 0.95), L("ゲイン: SW7 ANALOG / DIGITAL", 0.95), L("(両方に同時に効く)", 0.95)], ANA)
line([(42, 16), (42, 13.3), (178, 13.3)], ANA)
arrow([(178, 13.3), (178, 16)], ANA)
box(158, 52, 198, 88, [L("電源 Power supply", 1.3, True, PWR),
                       L("トロイダル or 低ノイズSMPS", 1.05),
                       L("パワーアンプ用 独立電源", 1.05),
                       L("↓", 1.1),
                       L("アナログ ±15V", 1.1),
                       L("LT3045 / LT3094", 1.05),
                       L("DAC AVCC 5V / デジタル 3.3V・1.5V", 1.0),
                       L("それぞれ独立LDO", 1.05),
                       L("ストリーマ 5V (別巻線)", 1.05),
                       L("ノイズ源は分離", 1.05),
                       L("Separate rails per block", 1.0)], PWR)

# ---------------- notes
frame(1, 0.5, 199, 12.5, "注意 NOTES")
notes = [
    "* AK4191: PCM 最大1536kHz・DSD最大DSD1024 (製品概要)。BD34302: PCM 最大1536kHz・DSD 22.5MHz (データシート)。組み合わせは参考ブログの報告 (THD <0.001%、SNR ≈116dB)。ROHM資料に不確かな点があり実機確認が必要。USBでの1536kHz/DSD1024は専用UAC2ファームと再生側の対応が必要。",
    "* U-NEXT / YouTube / Qobuz は各社の認証・契約が必要 (Widevine、Google認証、Qobuz Connect 等)。配信の音質は各サービスの仕様に従い、ビットパーフェクト出力できない場合があります。*Wi-Fi 8 (802.11bn) は規格策定中: 対応チップ・認証は要確認 (Wi-Fi 7/6E との互換で選定)。",
    "MQA: 専用の MQA フルデコーダ (XMOS XU316 + MQA ファームウェア、ライセンス版) を AK4191 + BD34302 とは別に搭載。MQA を検出するとここで展開・レンダリングし、PCM を AK4191 へ渡す。A separate MQA full decoder (XU316) is fitted apart from the DAC.",
    "USB-C: DDC回路(USB→I2S, MUSICIAN Pisces III を参考)を内蔵。SW1 ON = DDC→DAC を内部I2Sで接続(FPGA経由) / OFF = DDCを内部DACから切り離し、I2S OUTから外部DACへ出力(DDCとして使用)。SW1 switches the internal DDC-to-DAC I2S link ON or OFF. SW2 = DAC ON/OFF: DAC only, or neither DDC nor DAC (analog inputs only), can also be chosen.",
    "SUB OUT は前の図の「モノラル加算 + LPF + 位相」回路を使用。スピーカー端子は HF / LF を分離し、ジャンパー板で通常接続にも対応。参考設計: 実機測定・各種認証・安全規格の確認が必要。",
]
for i, t in enumerate(notes):
    text(24, 10.4 - 2.0 * i, t, 1.0, GRY)

img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\streaming_amp_block.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
