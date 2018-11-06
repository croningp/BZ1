import time
from pumpsctl.pumpsctl import PumpsCtl
from bzboard.bzboard import BZBoard
from img_proc.record_cam import RecordVideo
from datetime import datetime
import os, sys
sys.path.append(os.path.abspath('..'))
from tools import volctl
import pickle


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
        self.water_clean = {'pump':'P4', 'quantity':50,  'speedIn':60, 'speedOut':60} 


    def perform_experiment(self, water=15, ferroin=2.5, h2so4=12.5, kbro3=19, malonic=18):

        #set experiental parameters 
        self.water['quantity'] = water
        self.ferroin['quantity'] = ferroin
        self.h2so4['quantity'] = h2so4
        self.kbro3['quantity'] = kbro3
        self.malonic['quantity'] = malonic

        #calc volume for one experiment including cleaning
        vol_check_water =   self.water['quantity'] + 3*self.water_clean['quantity']
        vol_check_ferroin = self.ferroin['quantity'] 
        vol_check_h2so4 =   self.h2so4['quantity'] + 2*self.h2so4_clean['quantity']          
        vol_check_kbro3 =   self.kbro3['quantity'] + 2*self.kbro3_clean['quantity']
        vol_check_malonic = self.malonic['quantity']             
        vol_check_waste =   vol_check_water + vol_check_ferroin + vol_check_h2so4 + vol_check_kbro3 + vol_check_malonic
        #update required experiment volumes  (expvol) in volctl
        self.p.expvolinput(self,vol_check_water,vol_check_ferroin,vol_check_h2so4,vol_check_kbro3,vol_check_malonic,vol_check_waste)
        #call countdown and print how many experiments are left
        self.p.countdown()
        #check enough for whole experiment to run and direct to reset if not
        self.p.pre_exp_check()


        #dispense the BZ recipe into the arena
        self.p.pump_multiple(self.water, self.malonic, self.kbro3, self.h2so4, 
                self.ferroin)
        # activate all max speed for 30 second to mix
        self.b.activate_all(3000)
        time.sleep(60)
        self.b.disable_all()

        # wait for 10 minutes
        time.sleep(60*10)
        
        # activate random pattern for 1 minute 30 times
        # need variable titles
        exp_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.rv.record_threaded( exp_time )
        for i in range(30):
            self.b.activate_rand(exp_time)
            time.sleep(60*1)
        self.b.disable_all()

        # start cleaning platform
        for i in range(2):
            self.p.pump_multiple(self.waste) # send to waste
            self.p.pump_multiple(self.water_clean, self.h2so4_clean, 
                    self.kbro3_clean) # clean system
            time.sleep(2*60)

        for i in range(1):
            self.p.pump_multiple(self.waste)
            self.p.pump_multiple(self.water_clean) 

        for i in range(2):
            self.p.pump_multiple(self.waste)


if __name__ == "__main__":

    ap = AutomatedPlatform()

    for i in range(1): # number of experiments
        ap.perform_experiment()
