import sys
SD = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
for tube in (False, True):
    h = open(SD + r"\amp_head.py", encoding="utf-8").read().replace("W, H = 200, 150", "W, H = 200, 130")
    src = h + "\nTUBE = %r\n" % tube + open(SD + r"\ah2_extra.py", encoding="utf-8").read() + "\n" + open(SD + r"\fig_fg_body.py", encoding="utf-8").read()
    exec(compile(src, "fg", "exec"), {})
