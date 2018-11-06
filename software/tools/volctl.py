'''Volume control stnadalone system will contain all volume based functions
Author: Andrew Quinn
email: 2186149q@student.gla.ac.uk
'''


import pickle
from tools import emailalert 
import os.path
import os, sys
sys.path.append(os.path.abspath('..'))
from tools import emailalert 

class VolCtl:	
	
	def __init__(self):
		#volume dictionary
        self.volumes = {'P0': {'id':0, 'liquid': 'waste',   'volume':1000, 'limit':5000, 'expvol':0},
                        'P1': {'id':1, 'liquid': 'ferroin', 'volume':0,    'limit':100,  'expvol':0},
                        'P2': {'id':2, 'liquid': 'h2so4',   'volume':900,  'limit':1000, 'expvol':0},
                        'P3': {'id':3, 'liquid': 'malonic', 'volume':700,  'limit':1000, 'expvol':0},
                        'P4': {'id':4, 'liquid': 'water',   'volume':1000, 'limit':5000, 'expvol':0},
                        'P5': {'id':5, 'liquid': 'kbro3',   'volume':900,  'limit':1000, 'expvol':0}}

		#load in volumes if already exist or create new file
		script_path = os.path.dirname(os.path.realpath(__file__))
		vol_db = script_path + '/picklepumps.p'

		if os.path.isfile(self.vol_db) is True:
			self.volumes = pickle.load(open(self.vol_db, "rb"))
		else:	
			pickle.dump(self.volumes, open(self.vol_db, "wb"))

	def volcontrol(self):	
		#display said volumes
		print(volumes)
		#user inputs to reset
		while finished != 'y':
			reset_volumes = input('what would you like to reset? answer as comma seperated list. [w]aste, [f]erroin, [s]ulphuric, [m]alonic, [h]2o, [k]bro3 ')
			split_reset = reset_volumes.split(',')
	                        
			if 'w' in split_reset:
	    		self.volumes['P0']['volume'] = 0
			if 'f' in split_reset:
	    		self.volumes['P1']['volume'] = 0
			if 's' in split_reset:
	    		self.volumes['P2']['volume'] = 0
			if 'm' in split_reset:
	    		self.volumes['P3']['volume'] = 0
			if 'h' in split_reset:
	    		self.volumes['P4']['volume'] = 0
			if 'k' in split_reset:
	    		self.volumes['P5']['volume'] = 0
	    	#confirmation 
	    	finished = input('Are you finished [y/n]?')
		
			#update reset volumes to dictionary 
			update_dic = open(vol_db,"wb")
			pickle.dump(volumes, update_dic)
			update_dic.close()

	
	def expvolinput(self, water, ferroin, h2so4, kbro3, malonic, waste):
		#updates the dictionary for total experiment volumes from automatedBZ file
		if self.volume[key] == 'P0':
			self.volume['P0']['expvol'] = waste
		if self.volume[key] == 'P1':
			self.volume['P1']['expvol'] = ferroin
		if self.volume[key] == 'P2':
			self.volume['P2']['expvol'] = h2so4
		if self.volume[key] == 'P3':
			self.volume['P3']['expvol'] = malonic
		if self.volume[key] == 'P4':
			self.volume['P4']['expvol'] = water
		if self.volume[key] == 'P5':
			self.volume['P5']['expvol'] = kbro3
		#updates dictionary to be used in countdown below 
		update_dic = open(vol_db,"wb")
		pickle.dump(self.volumes, update_dic)
		update_dic.close()						

	def countdown(self):
	#takes in the repective volumes for each experiment and calculates the remaining experiments at that volume
		for keys in self.volumes:
			space = (volumes[keys]['limit'] - volumes[keys]['volume'])
			exp_left = space/self.volumes[key]['expvol']
			if exp_left <= 5:
				alert = 'There are ' + exp_left + 'experiments worth of ' + self.volumes[key]['liquid'] + ' left once changed please run volctl and reset volumes'
				self.p.email_alert(ebody = alert)
			print('There are ' + exp_left + ' worth of ' + self.volumes[key]['liquid'] + ' left at current consumption')

    def pre_exp_check(self):
        # stop program if not enough liquid or waste room
        for key in self.volumes:
        	if (self.volumes[key]['limit'] - self.volumes[key]['volume']) <= self.volumes[key]['expvol']:
        		print('Insufficient ' + self.volumes[key]['liquid'] + ' remaining please change and follow prompts')
        		self.reset_volume(key)

    def reset_volume(self,resetpump):
        while hold_input != 'y':
            hold_input = input('Have you reset ' + self.volumes[resetpump]['liquid'] + ' and is the experiment ready to continue? [y/n]')
            if hold_input == 'y':
                self.volumes[resetpump]['volume'] = 0						