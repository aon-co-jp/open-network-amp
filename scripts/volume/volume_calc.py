"""Volume step calculation: clicky mode 0.5 dB (relay ladder), smooth mode 0.01 dB (relay + digital fine trim).
Pure calculation (no hardware verification)."""
import math

RANGE_DB = 90.0          # 0 .. -90 dB
CLICK_DB = 0.5           # clicky-mode step (latching relay ladder)
TRIM_SPAN = CLICK_DB / 2 # digital fine trim covers +-0.25 dB around the relay position
SMOOTH_DB = 0.01         # smooth-mode resolution
ARC_DEG = 270.0

steps = int(RANGE_DB / CLICK_DB) + 1
print(f"clicky positions: {steps} (0 to -{RANGE_DB} dB)")
print(f"click angle: {ARC_DEG/(steps-1):.3f} deg")

# binary-weighted relay sections in units of 0.5 dB
n = math.ceil(math.log2(RANGE_DB / CLICK_DB + 1))
weights = [CLICK_DB * 2**i for i in range(n)]
print(f"relay sections per leg: {n}, weights dB: {weights}, max {sum(weights)} dB")

# resistor tolerance effect on one step (worst case, 0.1 % thin film)
tol = 0.001
err_db = 20*math.log10(1+tol)
print(f"0.1% resistor -> about {err_db:.4f} dB per section (worst), step {CLICK_DB} dB OK")

# bits lost by digital fine trim of up to 0.25 dB (32-bit path)
lost = -math.log2(10**(-TRIM_SPAN/20))
print(f"digital trim of {TRIM_SPAN} dB loses {lost:.4f} bit of 32 (earlier bug: -40 dB digital alone lost 6.6 bit)")

# smooth mode resolution
print(f"smooth steps per relay position: {int(CLICK_DB/SMOOTH_DB)} ; encoder 14 bit = {2**14} counts/turn,"
      f" counts per click ~{2**14*ARC_DEG/360/(steps-1):.1f}")
