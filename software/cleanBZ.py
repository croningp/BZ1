import time
from pumpsctl.pumpsctl import PumpsCtl
from bzboard.bzboard import BZBoard
from tools.volctl import VolCtl

b = BZBoard("/dev/ttyACM1")
v = VolCtl()
p = PumpsCtl('/dev/ttyACM0', v)


# I am reducing the quantity of water to 16 to consider remains
waste = {'pump':'P0', 'quantity':75, 'speedIn':40, 'speedOut':50}
h2so4_clean = {'pump':'P2', 'quantity':5, 'speedIn':60, 'speedOut':60}
kbro3_clean = {'pump':'P5', 'quantity':7, 'speedIn':110, 'speedOut':110}
water_clean = {'pump':'P4', 'quantity':50, 'speedIn':60, 'speedOut':60}


for i in range(2):
    p.pump_multiple(waste)
    p.pump_multiple(water_clean, h2so4_clean, kbro3_clean)
    time.sleep(0*60)

for i in range(1):
    p.pump_multiple(waste)
    p.pump_multiple(water_clean)

for i in range(2):
    p.pump_multiple(waste)
