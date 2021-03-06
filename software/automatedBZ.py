import time
from pumpsctl.pumpsctl import PumpsCtl
from bzboard.bzboard import BZBoard
from tools.volctl import VolCtl

from img_proc.record_cam import RecordVideo
from datetime import datetime
import os, sys
import pickle


class AutomatedPlatform():


    def __init__(self):

        self.v = VolCtl()
        self.b = BZBoard("/dev/ttyACM1")
        self.p = PumpsCtl('/dev/ttyACM0', self.v)
        self.rv = RecordVideo(60*30)

        # original recipe was 2.5, 20, 12.5, 18, 19 (fe, h2o, h2s, mal, k)
        # but because on average there's a 3 ml remain of theoretically clean water
        # I am reducing the quantity of water to 16 to consider remains
        self.waste =       {'pump':'P0', 'quantity':75, 'speedIn':40, 'speedOut':50}
        self.water =       {'pump':'P4', 'quantity':15,  'speedIn':60, 'speedOut':70}
        self.ferroin =     {'pump':'P1', 'quantity':2.5, 'speedIn':35, 'speedOut':35}
        self.h2so4 =       {'pump':'P2', 'quantity':12.5,'speedIn':60, 'speedOut':70}
        self.h2so4_clean = {'pump':'P2', 'quantity':5,   'speedIn':60, 'speedOut':70}
        self.kbro3 =       {'pump':'P5', 'quantity':19,  'speedIn':110,'speedOut':110}
        self.kbro3_clean = {'pump':'P5', 'quantity':12,  'speedIn':110,'speedOut':110}
        self.malonic =     {'pump':'P3', 'quantity':18,  'speedIn':60, 'speedOut':70}
        self.water_clean = {'pump':'P4', 'quantity':50,  'speedIn':60, 'speedOut':70} 


    def perform_experiment(self, water=15, ferroin=2.5, h2so4=12.5, kbro3=19, malonic=18):

        
        exp_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        print("Starting time: "+exp_time)

        #set experiental parameters 
        self.water['quantity'] = water
        self.ferroin['quantity'] = ferroin
        self.h2so4['quantity'] = h2so4
        self.kbro3['quantity'] = kbro3
        self.malonic['quantity'] = malonic

        #calc volume for one experiment including cleaning
        tot_water =   self.water['quantity'] + 3*self.water_clean['quantity']
        tot_ferroin = self.ferroin['quantity'] 
        tot_h2so4 =   self.h2so4['quantity'] + 2*self.h2so4_clean['quantity']          
        tot_kbro3 =   self.kbro3['quantity'] + 2*self.kbro3_clean['quantity']
        tot_malonic = self.malonic['quantity']             
        tot_waste =   tot_water + tot_ferroin + tot_h2so4 + tot_kbro3 + tot_malonic
        #update required experiment volumes  (expvol) in volctl
        self.v.update_single_experiment_volumes(tot_water,tot_ferroin,tot_h2so4,tot_kbro3,tot_malonic,tot_waste)
        #call countdown and print how many experiments are left
        self.v.countdown_experiments_left()
        #check enough for whole experiment to run and direct to reset if not
        self.v.check_sufficent_volume()

        print("Preparing BZ reaction")
        #dispense the BZ recipe into the arena
        self.p.pump_multiple(self.water, self.malonic, self.kbro3, self.h2so4, 
                self.ferroin)
        # activate all max speed for 60 second to mix
        self.b.activate_all(0, 200)
        time.sleep(60)
        self.b.disable_all()

        print("Waiting 10 minutes")
        # wait for 10 minutes
        time.sleep(60*10)
        
        # activate random pattern for 1 minute 30 times
        # need variable titles
        exp_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        print("Starting actual experiment at "+exp_time)
        self.rv.record_threaded( exp_time )
        time.sleep(1)
        for i in range(15):
            #speeds = self.b.activate_rand_multiple(exp_time)
            speeds = self.b.activate_rand_column(exp_time)
            time.sleep(60*1)
            self.b.repeat_rand(exp_time, speeds)
            time.sleep(60*1)
        self.b.disable_all()
        
        print("Starting cleaning")
        # start cleaning platform
        for i in range(2):
            print("First cleaning phase "+str(i))
            self.p.pump_multiple(self.waste) # send to waste
            self.p.pump_multiple(self.water_clean, self.h2so4_clean, 
                    self.kbro3_clean) # clean system
            time.sleep(2*60)
            
        print("Second cleaning phase")
        for i in range(1):
            self.p.pump_multiple(self.waste)
            self.p.pump_multiple(self.water_clean) 

        print("Last cleaning phase")
        for i in range(2):
            self.p.pump_multiple(self.waste)



if __name__ == "__main__":

    ap = AutomatedPlatform()
    num_experiments = 3

    for i in range(num_experiments): # number of experiments
        print("###################")
        print("###################")
        print("Starting experiment "+str(i))
        ap.perform_experiment()
