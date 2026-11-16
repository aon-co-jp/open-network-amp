import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "..", "VER8", "volume_hybrid.jpg")
src = open(HERE + "/amp_head.py", encoding="utf-8").read().replace("W, H = 200, 150", "W, H = 200, 130")
src += "\n" + open(HERE + "/ah2_extra.py", encoding="utf-8").read() + "\n" + open(HERE + "/fig_volume_body.py", encoding="utf-8").read()
exec(compile(src, "vol", "exec"))
