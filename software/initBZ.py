################################################################
# This script should be used before starting the experiments
# to make sure everything is working and tubes are filled
################################################################

import time

from pumpsctl.pumpsctl import PumpsCtl
from bzboard.bzboard import BZBoard
from img_proc.record_cam import RecordVideo
import os, sys
sys.path.append(os.path.abspath('..'))
from tools.volctl import VolCtl 


v = VolCtl()
b = BZBoard("/dev/ttyACM1")
p = PumpsCtl('/dev/ttyACM0', v)

rv = RecordVideo(10)

waste = {'pump':'P0', 'quantity':75, 'speedIn':50, 'speedOut':50}
water = {'pump':'P4', 'quantity':5, 'speedIn':60, 'speedOut':60}
h2so4 = {'pump':'P2', 'quantity':5, 'speedIn':60, 'speedOut':60}
kbro3 = {'pump':'P5', 'quantity':10, 'speedIn':110, 'speedOut':110}
malonic = {'pump':'P3', 'quantity':5, 'speedIn':60, 'speedOut':60}
water_clean = {'pump':'P4', 'quantity':50, 'speedIn':50, 'speedOut':50}
ferroin = {'pump':'P1', 'quantity':1, 'speedIn':35, 'speedOut':35}



# make sure these 4 pumps are filled, I will test ferroin individually 
p.pump_multiple(water, malonic, kbro3, h2so4,ferroin)
# activate all max speed for 30 second to mix
b.activate_all(3000)
time.sleep(30)
b.disable_all()

rv.record_threaded("test")
time.sleep(10)

p.pump_multiple(water_clean, waste)
p.pump_multiple(waste)
