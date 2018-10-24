import time
from pumpsctl.pumpsctl import PumpsCtl
from bzboard.bzboard import BZBoard
from img_proc.record_cam import RecordVideo
from datetime import datetime

class AutomatedPlatform():


    def __init__(self):

        self.b = BZBoard("/dev/ttyACM1")
        self.p = PumpsCtl('/dev/ttyACM0')

        self.rv = RecordVideo(30*60)

        # original recipe was 2.5, 20, 12.5, 18, 19 (fe, h2o, h2s, mal, k)
        # but because on average there's a 3 ml remain of theoretically clean water
        # I am reducing the quantity of water to 16 to consider remains
        self.waste =       {'pump':'P0', 'quantity':100, 'speedIn':40, 'speedOut':50}
        self.water =       {'pump':'P4', 'quantity':15,  'speedIn':60, 'speedOut':60}
        self.ferroin =     {'pump':'P1', 'quantity':2.5, 'speedIn':35, 'speedOut':35}
        self.h2so4 =       {'pump':'P2', 'quantity':12.5,'speedIn':60, 'speedOut':60}
        self.h2so4_clean = {'pump':'P2', 'quantity':5,   'speedIn':60, 'speedOut':60}
        self.kbro3 =       {'pump':'P5', 'quantity':19,  'speedIn':110,'speedOut':110}
        self.kbro3_clean = {'pump':'P5', 'quantity':15,  'speedIn':110,'speedOut':110}
        self.malonic =     {'pump':'P3', 'quantity':18,  'speedIn':60, 'speedOut':60}
        self.water_clean = {'pump':'P4', 'quantity':50,  'speedIn':60, 'speedOut':60} # what does clean and waste do here


    def perform_experiment(self, water=15, ferroin=2.5, h2so4=12.5, kbro3=19, malonic=18):

        self.water['quantity'] = water
        self.ferroin['quantity'] = ferroin
        self.h2so4['quantity'] = h2so4
        self.kbro3['quantity'] = kbro3
        self.malonic['quantity'] = malonic

        
        #dispense the BZ recipe into the arena
        self.p.pump_multiple(self.water, self.malonic, self.kbro3, self.h2so4, 
                self.ferroin)
        # activate all max speed for 30 second to mix
        self.b.activate_all(3000)
        time.sleep(30)
        self.b.disable_all()

        # wait for 10 minutes
        time.sleep(60*10)
        
        #cannabalised old pattern function
        self.rv.record_threaded( str(kbro3)+"kbro3" )
        # activate random pattern for 1 minute 30 times
                # need variable titles
        exp_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        for i in range(30):
            self.b.activate_rand(exp_time)
            time.sleep(60*1)

        # start cleaning platform
        for i in range(2):
            self.p.pump_multiple(self.waste) # send to waste
            self.p.pump_multiple(self.water_clean, self.h2so4_clean, 
                    self.kbro3_clean) # clean system
            time.sleep(3*60)

        for i in range(1):
            self.p.pump_multiple(self.waste)
            self.p.pump_multiple(self.water_clean) 

        for i in range(2):
            self.p.pump_multiple(self.waste)


if __name__ == "__main__":

    ap = AutomatedPlatform()

    for i in [15, 16]: # why
        ap.perform_experiment(kbro3=i)