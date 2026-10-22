import math, json
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\plot_helpers.py", encoding="utf-8").read())
S5 = json.load(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\sim5_results.json", encoding="utf-8"))
text(3, 127, "ハイブリッド音量ボリューム VER2 (耐久性・音質向上)  Hybrid volume VER2 - durability and sound quality", 2.4, INK, "la", True)
text(3, 123.6, "ノブ = 非接触の磁気エンコーダ + 触覚モーター。クリック感 ON (LUXMAN L-570 / L1000 のような「カチッ」) / OFF (滑らか) を SW6 の ON/OFF スイッチで切替  |  全プリメインアンプに搭載", 1.35, GRY)
text(3, 121.2, "参考設計 Reference design  |  トルク・寿命・雑音は設計値 (計算)。触覚の感触・耐久は実機で確認が必要です。 Torque, life and noise are design numbers (calculated).", 1.2, GRY)

# ---- block circuit
box(3, 86, 25, 112, [L("ノブ", 1.3, True), L("(金属・慣性付き)", 1.0), L("軸 = 触覚モーター", 1.0)], ANA)
box(30, 100, 56, 112, [L("磁気エンコーダ", 1.1, True), L("MT6701 14bit 非接触", 0.95)], DIG)
box(30, 84, 56, 96, [L("触覚モーター", 1.1, True), L("BLDC・ボールベアリング", 0.95)], PWR)
box(62, 84, 88, 112, [L("MCU", 1.3, True), L("STM32G4", 1.0), L("触覚ループ 5kHz", 1.0), L("温度でトルクを制限", 0.95)], DIG)
box(62, 66, 88, 78, [L("モータードライバ", 1.1, True), L("TMC6300 等", 1.0)], PWR)
box(94, 100, 128, 112, [L("SW6  クリック ON / OFF", 1.1, True, ORG)], (200, 120, 20))
box(94, 84, 128, 96, [L("表示 / LED リング", 1.1, True), L("音量値 (dB)", 1.0)], DIG)
box(134, 84, 197, 112, [L("音量アッテネータ VER2 (バランス)", 1.2, True), L("ラッチングリレー式 抵抗ラダー (0.1% 薄膜 · 金接点)", 0.95), L("+ 微調整 電子ボリューム (MUSES72323 等)", 0.95), L("リレーは接点を動かすだけ (電流を通さず保持)", 0.95), L("クリック 1 回 = 1 dB、ゼロクロスで切替 (ポップ音防止)", 0.95)], ANA)
arrow([(25, 106), (30, 106)], DIG)
arrow([(56, 106), (62, 106)], DIG)
arrow([(62, 90), (56, 90)], PWR)
arrow([(75, 84), (75, 78)], DIG)
arrow([(62, 72), (43, 72), (43, 84)], PWR)
arrow([(94, 106), (88, 106)], (200, 120, 20))
arrow([(88, 90), (94, 90)], DIG)
arrow([(88, 98), (134, 98)], DIG)
line([(25, 92), (30, 92)], PWR)
text(113, 80.8, "音声はデジタルを通さず、アナログ経路のまま", 1.0, GRY, "mm")

# ---- 1) torque
pitch = 270.0 / 80.0
T0 = 6.0
mx, my = plot(8, 18, 62, 58, 0, 12, -8, 8, True and False, "① クリック ON: トルク  Click ON torque", "ノブ角度 (°)", "mN·m")
line([(mx(a * 0.05), my(-T0 * (math.sin(2 * math.pi * a * 0.05 / pitch) + 0.25 * math.sin(4 * math.pi * a * 0.05 / pitch)))) for a in range(0, 241)], (190, 30, 30), LW)
line([(mx(0), my(-0.4)), (mx(12), my(-0.4))], (25, 115, 60), LW)
text(35, 56.0, "赤: クリック ON (幅 3.4°、約 6mN·m)  緑: OFF (滑らか)", 0.95, INK, "mm")
# ---- 2) ladder noise vs attenuation
vol = S5["volume_ladder"]
att = [-6, -12, -20, -30, -40, -60]
mx2, my2 = plot(72, 18, 126, 58, 0, 60, -150, -115, False, "② ラダー熱雑音 (20Hz〜20kHz)  Ladder noise", "減衰 (dB)", "dBV")
line([(mx2(-a), my2(vol[str(a)]["dBV"])) for a in att], (30, 70, 180), LW)
for a in att:
    text(mx2(-a), my2(vol[str(a)]["dBV"]) + 1.6, "%d: %.0fΩ" % (a, vol[str(a)]["Zout_ohm"]), 0.9, (30, 70, 180), "mm")
text(99, 56.0, "出力 Z が最大 2.5kΩ (-6dB) でも -121 dBV。0.1% 抵抗で誤差 ±0.009 dB", 0.95, INK, "mm")
# ---- 3) relay life
mx3, my3 = plot(136, 18, 190, 58, 100, 5000, 1, 300, True, "③ リレー寿命 (1000 万回)  Relay life", "音量操作 (回/日)", "年")
life = lambda n: 1e7 / (n * 365)
line([(mx3(n), my3(life(n))) if False else (mx3(n), my3(min(300, life(n)))) for n in [100 * (50) ** (i / 60) for i in range(61)]], (120, 60, 160), LW)
for n in (500, 2000):
    text(mx3(n), my3(life(n)) + 2.0, "%d回/日: %.0f年" % (n, life(n)), 0.95, (120, 60, 160), "mm", True)
text(163, 56.0, "磁気エンコーダとモーターは非接触/ボールベアリングで摩耗なし", 0.95, INK, "mm")
text(8, 12.0, "VER1 からの改善: ① 接点のあるポット・エンコーダをやめ、非接触の磁気エンコーダに ② リレー式ラダーで電子ボリューム IC の歪み・雑音の影響を減らす ③ モーター温度でトルク制限", 1.1, INK, "la")
text(8, 9.4, "Improvements over VER1: contactless encoder instead of a wiper or contact encoder; relay ladder lowers the distortion and noise contribution of an electronic-volume IC; motor torque is limited by temperature.", 1.0, GRY, "la")
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_volume_haptic.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
