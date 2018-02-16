from bzboard.bzboard import BZBoard
from pumpsctl.pumpsctl import PumpsCtl


board = BZBoard('/dev/ttyACM0')
pumps = PumpsCtl('/dev/ttyACM1')

# prepare experiment
# our BZ recipe is (all in ml) 2.5 ferroin, 20 water, 12.5 h2so4
#                               18 malonic, 19 kbromate
ferroin = {'pump':'P1', 'quantity':2.5, 'speedIn':20, 'speedOut':10}
h2so4 = {'pump':'P2', 'quantity':12.5, 'speedIn':20, 'speedOut':10}
malonic = {'pump':'P3', 'quantity':18, 'speedIn':20, 'speedOut':10}
water = {'pump':'P4', 'quantity':20, 'speedIn':20, 'speedOut':10}
kbromate = {'pump':'P5', 'quantity':19, 'speedIn':20, 'speedOut':10}

pumps.pump_multiple(h2so4, water)
pumps.pump_multiple(ferroin, malonic)
pumps.pump_multiple(kbromate)


# activate stirrers
# activate camera
# let experiment go

# clean it - the volume of the experiment was 72 ml
# we can go mental and at first drain 100ml
pumps.pump_in('P0', 100, 30, 30) # P0 is drain, 100 is ml

pumps.close()
del pumps
