import time

from pumpsctl.pumpsctl import PumpsCtl
from bzboard.bzboard import BZBoard


b = BZBoard("/dev/ttyACM0")
p = PumpsCtl('/dev/ttyACM1')


waste = {'pump':'P0', 'quantity':100, 'speedIn':25, 'speedOut':25}
water = {'pump':'P4', 'quantity':20, 'speedIn':25, 'speedOut':25}
ferroin = {'pump':'P1', 'quantity':2.5, 'speedIn':25, 'speedOut':25}
h2so4 = {'pump':'P2', 'quantity':12.5, 'speedIn':25, 'speedOut':25}
kbro3 = {'pump':'P5', 'quantity':19, 'speedIn':25, 'speedOut':25}
malonic = {'pump':'P3', 'quantity':18, 'speedIn':25, 'speedOut':25}


p.pump_multiple(water, malonic, kbro3, h2so4, ferroin)

b.activate_all()
time.sleep(10)
b.disable_all()

p.pump_multiple(waste)
