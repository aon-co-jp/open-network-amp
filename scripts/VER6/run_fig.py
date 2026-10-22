import sys
SD = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
body = sys.argv[1]
Hh = int(sys.argv[2]) if len(sys.argv) > 2 else 130
h = open(SD + r"\amp_head.py", encoding="utf-8").read().replace("W, H = 200, 150", "W, H = 200, %d" % Hh)
src = h + "\n" + open(SD + r"\ah2_extra.py", encoding="utf-8").read() + "\n" + open(SD + "\\" + body, encoding="utf-8").read()
exec(compile(src, body, "exec"))
