'''Volume control stnadalone system will contain all volume based functions
Author: Andrew Quinn
email: 2186149q@student.gla.ac.uk
'''


import pickle
import os.path
import os, sys
sys.path.append(os.path.abspath('..'))
from tools.emailalert import email_alert 



class VolCtl:	
	

	def __init__(self):
		#volume dictionary
		self.volumes = {'P0': {'id':0, 'liquid': 'waste',   'volume':0, 'limit':5000, 'expvol':0},
						'P1': {'id':1, 'liquid': 'ferroin', 'volume':0, 'limit':100,  'expvol':0},
						'P2': {'id':2, 'liquid': 'h2so4',   'volume':0, 'limit':1000, 'expvol':0},
						'P3': {'id':3, 'liquid': 'malonic', 'volume':0, 'limit':1000, 'expvol':0},
						'P4': {'id':4, 'liquid': 'water',   'volume':0, 'limit':5000, 'expvol':0},
						'P5': {'id':5, 'liquid': 'kbro3',   'volume':0, 'limit':1000, 'expvol':0}}

		#load in volumes if already exist or create new file
		script_path = os.path.dirname(os.path.realpath(__file__))
		self.vol_db = script_path + '/picklepumps2.p'

		if os.path.isfile(self.vol_db) is True:
			self.volumes = pickle.load(open(self.vol_db, "rb"))
		else:	
			pickle.dump(self.volumes, open(self.vol_db, "wb"))

		for key in self.volumes:
			print(self.volumes[key]['liquid'],self.volumes[key]['volume'],self.volumes[key]['limit'])			


	def volume_control(self):	
		#allow the user to reset the volumes either to 0 or specify a volume
		
		#display volumes
		for key in self.volumes:
			print(self.volumes[key]['liquid'],self.volumes[key]['volume'],self.volumes[key]['limit'])		
		
		finished = 'n'
		while finished != 'y':
			#give option to reset to 0 or enter actual values
			primary_input = input('would you like to (r)eset volumes, enter (s)pecific values or do (n)othing?: \n')
			#reset to 0
			if primary_input == 'r':
				reset_volumes = input('what would you like to reset? answer as comma seperated list. [w]aste, [f]erroin, [s]ulphuric, [m]alonic, [h]2o, [k]bro3: \n')
				split_reset = reset_volumes.split(',')							
				for i in split_reset:
					if i == 'w':
						self.volumes['P0']['volume'] = 0
						print('waste reset')        
					if i == 'f':
						self.volumes['P1']['volume'] = 0
						print('ferroin reset')
					if i == 's':
						self.volumes['P2']['volume'] = 0
						print('sulpuric acid reset')
					if i == 'm':
						self.volumes['P3']['volume'] = 0
						print('malonic acid reset')
					if i == 'h':
						self.volumes['P4']['volume'] = 0
						print('water reset')
					if i == 'k':
						self.volumes['P5']['volume'] = 0
						print('potassium bromate reset')
					if i not in split_reset:
						print('invalid input detected')
			
			#specific values 
			if primary_input == 's':
				value_input = input('what volume would you like to enter? answer as comma seperated list. [w]aste, [f]erroin, [s]ulphuric, [m]alonic, [h]2o, [k]bro3: \n')
				split_reset_2 = value_input.split(',')							
				if 'w' in split_reset_2:
					waste_volume = int(input('How much waste is there in ml '))
					try:
						self.volumes['P0']['volume'] = self.volumes['P0']['limit'] - waste_volume
					except ValueError:
						print(waste_volume + ' is not an intiger please try again')
				if 'f' in split_reset_2:
					ferroin_volume = int(input('How much ferroin is there in ml '))
					try:
						self.volumes['P1']['volume'] = self.volumes['P1']['limit'] - ferroin_volume
					except ValueError:
						print(ferroin_volume + ' is not an intiger please try again')				
				if 's' in split_reset_2:
					sulphuric_volume = int(input('How much sulphuric is there in ml '))
					try:
						self.volumes['P2']['volume'] = self.volumes['P2']['limit'] - sulphuric_volume
					except ValueError:
						print(sulphuric_volume + ' is not an intiger please try again')				
				if 'm' in split_reset_2:
					malonic_volume = int(input('How much malonic is there in ml '))
					try:
						self.volumes['P3']['volume'] = self.volumes['P3']['limit'] - malonic_volume
					except ValueError:
						print(malonic_volume + ' is not an intiger please try again')				
				if 'h' in split_reset_2:
					water_volume = int(input('How much water is there in ml '))
					try:
						self.volumes['P4']['volume'] = self.volumes['P4']['limit'] - water_volume
					except ValueError:
						print(water_volume + ' is not an intiger please try again')				
				if 'k' in split_reset_2:
					kbro3_volume = int(input('How much Potasium Bromide is there in ml '))
					try:
						self.volumes['P5']['volume'] = self.volumes['P5']['limit'] - kbro3_volume
					except ValueError:
						print(kbro3_volume + ' is not an intiger please try again')			
			
			#confirmation or back to loop
			finished = input('Are you finished [y/n]? ')
		
			#update reset volumes to dictionary 
			update_dic = open(self.vol_db,"wb")
			pickle.dump(self.volumes, update_dic)
			update_dic.close()


	def update_single_experiment_volumes(self, volwater, volferroin, volh2so4, volkbro3, volmalonic, volwaste):
		#updates the dictionary for total experiment volumes from automatedBZ file needed for below
		for key in self.volumes:
			if key == 'P0':
				self.volumes['P0']['expvol'] = volwaste
			if key == 'P1':
				self.volumes['P1']['expvol'] = volferroin
			if key == 'P2':
				self.volumes['P2']['expvol'] =  volh2so4
			if key == 'P3':
				self.volumes['P3']['expvol'] = volmalonic
			if key == 'P4':
				self.volumes['P4']['expvol'] = volwater
			if key == 'P5':
				self.volumes['P5']['expvol'] = volkbro3
		
		#updates dictionary to be used in countdown below 
		update_dic = open(self.vol_db,"wb")
		pickle.dump(self.volumes, update_dic)
		update_dic.close()					


	def countdown_experiments_left(self):
	#takes in the repective volumes for each experiment and calculates the remaining experiments at that volume
		for key in self.volumes:
			space = (self.volumes[key]['limit'] - self.volumes[key]['volume'])
			exp_left = space/(self.volumes[key]['expvol']+1)
			str_left = str(exp_left)
			print('There are ' + str_left + ' experiments worth of ' + self.volumes[key]['liquid'] + ' left at current consumption')
			if exp_left <= 2:
				alert = 'There are ' + str_left + ' experiments worth of ' + self.volumes[key]['liquid'] + ' left once changed please run volctl and reset volumes'
				email_alert(ebody = alert)
			


	def check_sufficent_volume(self):
		# checks there is enough volume for one experiment and will stop program if not enough liquid or waste room untill reset
		for key in self.volumes:
			if (self.volumes[key]['limit'] - self.volumes[key]['volume']) <= self.volumes[key]['expvol']:
				print('Insufficient ' + self.volumes[key]['liquid'] + ' remaining please change and follow prompts')
				close_alert = 'There is insufficent ' + self.volumes[key]['liquid'] + ' for experiment to proceed experiment is held untill volume is reset'
				email_alert(ebody = close_alert)
				self.reset_volume(key)


	def reset_volume(self,resetpump):
		#check_sufficent_volume redirects here if there is not enough 'liquid' for one experiment
		hold_input = 'n'
		while hold_input != 'y':
			hold_input = input('Have you reset ' + self.volumes[resetpump]['liquid'] + ' and is the experiment ready to continue? [y/n]')
			if hold_input == 'y':
				self.volumes[resetpump]['volume'] = 0


	def update_volumes(self,pump,quantity):
		#update the volumes when pumps fire pass on waste to fix problem with waste counting more than true value
		if pump == 'P0':
			pass
		else:
			self.volumes[pump]['volume'] = self.volumes[pump]['volume'] + quantity
			self.volumes['P0']['volume'] = self.volumes['P0']['volume'] + quantity
			#updates dictionary with added inputs
			update_dic = open(self.vol_db,"wb")
			pickle.dump(self.volumes, update_dic)
			update_dic.close()


if __name__ == '__main__':

	v = VolCtl()										