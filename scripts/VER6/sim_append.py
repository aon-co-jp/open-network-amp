SIM_JA = """#仮想シミュレーション結果
テスト、修正、配線短縮の再設計、サブウーファー回路VER2のコミット・push・VPS反映まで完了しました。続けて、先ほどの質問への回答もまとめて報告します。
遅くなってすみません。テストと修正、配線短縮の再設計、サブウーファー回路のVER2を済ませ、GitHubにコミット・pushして、VPS(audiocafe.tokyo)へ反映しました。公開サイトに記載があること、PDF・JPGが取得できること(HTTP 200)も確認しました。
#ご質問「テスト結果は一番上の回路図にも応用するか」について
はい、反映しています。一番上のネットワーク対応プリメインアンプ(図6)と、アナログ版(図9)の両方に、シミュレーション結果と修正内容をまとめて載せました。
#できた検証は Python の計算まで
- 本物のSPICE(ngspice や LTspice)は入っていなかったため、Python で周波数応答、直流動作点、真空管モデル、設計計算をしました。
- 過渡応答、歪み(THD)、位相余裕、ノイズ、熱は未実施で、実機の測定もしていません。
- ngspice などをインストールすれば本格的なSPICEも試せますが、ダウンロードになるため、許可をもらってからにします。
#テストで見つけて直した問題
- サブウーファーのLPF: −3dB が 74.7 / 102 / 112 Hz とずれていました。抵抗を 12.7k / 10.2k / 8.45k に切り替えて、80.6 / 100.3 / 121.2 Hz にしました。
- サブウーファーの低域: DCや超低域まで通していたため、7.2Hz の高域通過フィルタ(HPF)を追加しました。これが VER2 の変更点です。
- Class D の出力フィルタ: 10µH/1µF だと BTL 8Ω で +2.8dB のピークがあったため、22µH/0.47µF にしました。
- Class A のバイアス: ゼナー固定だと電流が 0.2〜4.2A とばらつくため、電流サーボ(約 2.3A)にしました。
- 真空管プリ: 12AX7 では利得が 35dB と高すぎたため、12AU7(双3極管)の片側(約 21dB)と残り半分のカソードフォロワにしました。
- 外付けリニア電源: トランス二次電圧が足りなかったため、2×24V / 2×40V / 2×52V に直しました。
#配線短縮の再設計
- 左右完全分離(デュアルモノ)で、DAC(アナログ版は入力セレクタとボリューム)を中央に置き、信号を左右へ一直線に並べるレイアウトにしました。
- 1chの信号経路は約 95mm(設計目標)です。基板どうしはコネクタ直結で信号ケーブルをなくし、各段の横に LDO と局所コンデンサを置き、GND は 1 点にまとめます。
- ネットワーク版(図5)とアナログ版(図8)のレイアウト図を作りました。
#確認してほしい点
- 配線長は設計目標で、実機で確認が必要です。
- 古い VER1 のPDFもサイトに残っていますが、ページ上のリンクは VER2 に切り替えました。
- ネットワーク版のJPG・PDFは、説明文が増えて縦に長くなりました(PDF は約 22MB)。軽くしたい場合は教えてください。"""

SIM_EN = """#Virtual simulation results
Testing, fixes, the redesign for shorter wiring, and the subwoofer circuit VER2 are done, including the commit, the push and the upload to the VPS. The answer to the earlier question follows.
Sorry for the delay. The tests and fixes, the shorter-wiring redesign and the subwoofer circuit VER2 are finished, committed and pushed to GitHub, and uploaded to the VPS (audiocafe.tokyo). I confirmed that the public site contains them and that the PDF and JPG files can be fetched (HTTP 200).
#About the question "is the test summary applied to the top circuit diagrams too?"
Yes. The simulation results and the fixes are summarized for both the network integrated amplifier at the very top (Figure 6) and the analog version (Figure 9).
#What could be verified: Python calculations only
- A real SPICE (ngspice or LTspice) was not installed, so frequency response, DC operating points, tube models and design arithmetic were calculated in Python.
- Transient response, distortion (THD), phase margin, noise and heat were not checked, and nothing was measured on real hardware.
- A full SPICE could be tried by installing ngspice or similar, but that is a download, so it will be done only with your permission.
#Problems found and fixed by the tests
- Subwoofer LPF: the -3 dB points were off at 74.7 / 102 / 112 Hz. Switching the resistors to 12.7k / 10.2k / 8.45k gives 80.6 / 100.3 / 121.2 Hz.
- Subwoofer low end: DC and very low frequencies passed through, so a 7.2 Hz high-pass filter (HPF) was added. This is the change in VER2.
- Class D output filter: 10 uH / 1 uF had a +2.8 dB peak at BTL 8 ohm, so it was changed to 22 uH / 0.47 uF.
- Class A bias: a fixed zener bias let the current vary from 0.2 to 4.2 A, so a current servo (about 2.3 A) is used.
- Tube preamp: the 12AX7 gave 35 dB of gain, which is too high, so one half of a 12AU7 dual triode (about 21 dB) plus the other half as a cathode follower is used.
- External linear supply: the transformer secondary voltages were too low, so they were corrected to 2x24 V / 2x40 V / 2x52 V.
#Redesign for shorter wiring
- The layout is fully left/right separated (dual mono) with the DAC (the input selector and volume in the analog version) in the centre, and the signal lined up straight to each side.
- The signal path of one channel is about 95 mm (a design target). Boards are joined directly by connectors so there are no signal cables, an LDO and a local capacitor sit next to each stage, and the grounds meet at one point.
- Layout diagrams were made for the network version (Figure 5) and the analog version (Figure 8).
#Points to confirm
- The wire lengths are design targets and must be checked on real hardware.
- The old VER1 PDF still remains on the site, but the links on the page now point to VER2.
- The JPG and PDF of the network version became tall because of the added text (the PDF is about 22 MB). Tell me if you want them lighter."""


def append_sim(im):
    rj = layout(SIM_JA, colw)
    re_ = layout(SIM_EN, colw)
    th = max(height(rj), height(re_))
    new = Image.new("RGB", (im.width, im.height + int(FS * 1.5) + th + pad), "white")
    new.paste(im, (0, 0))
    d2 = ImageDraw.Draw(new)
    y0 = im.height + int(FS * 1.0)
    d2.line([(pad, y0 - int(FS * 0.4)), (im.width - pad, y0 - int(FS * 0.4))], fill=(150, 160, 190), width=3)
    draw_rows(d2, pad, y0, rj)
    draw_rows(d2, 2 * pad + colw, y0, re_)
    return new
