import time

from pumpsctl.pumpsctl import PumpsCtl
from bzboard.bzboard import BZBoard


b = BZBoard("/dev/ttyACM1")
p = PumpsCtl('/dev/ttyACM0')

pat11 = b.pattern_from_file("/home/juanma/Code/BZ_platform/software/bzboard/patterns/pattern11.json")

waste = {'pump':'P0', 'quantity':100, 'speedIn':25, 'speedOut':25}
water = {'pump':'P4', 'quantity':20, 'speedIn':25, 'speedOut':25}
ferroin = {'pump':'P1', 'quantity':2.5, 'speedIn':25, 'speedOut':25}
h2so4 = {'pump':'P2', 'quantity':12.5, 'speedIn':25, 'speedOut':25}
kbro3 = {'pump':'P5', 'quantity':19, 'speedIn':25, 'speedOut':25}
malonic = {'pump':'P3', 'quantity':18, 'speedIn':25, 'speedOut':25}
water_clean = {'pump':'P4', 'quantity':80, 'speedIn':25, 'speedOut':25}

#dispense the BZ recipe into the arena
p.pump_multiple(water, malonic, kbro3, h2so4, ferroin)

# activate all max speed for 10 second to mix
b.activate_all(3000)
time.sleep(30)
b.disable_all()

# wait for 10 minutes
time.sleep(60*10)

# activate experimental pattern and wait for 30 minutes
b.activate_pattern(pat11)
time.sleep(60*30)
b.disable_all()

for i in range(5):
    p.pump_multiple(waste, water_clean)

for i in range(2):
    p.pump_multiple(waste)
