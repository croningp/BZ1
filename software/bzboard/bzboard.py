'''
This is a minimal implementation of the bz_board python interface.
For some reason the full fledge implementation done by Kevin
was giving some problems we couldn't solve, so we are
doing this minimal implementation instead.

If you want better functionality, error handling,... check the other one

'''


import serial, time, json, random, csv
from datetime import datetime


class BZBoard:


    def __init__(self, port): # creates objects to pass through function for each self

        self.ser = serial.Serial(port, 9600, timeout=120)
        time.sleep(2) # serial docs recommend a wait just after connection
        self.ser.flush(); self.ser.flushInput(); self.ser.flushOutput();

        self.motors = { # [adafruit_shield, pin, min_speed]
            "A1":[1, 8, 500],"A2":[1, 9, 565],"A3":[1,10, 525],"A4":[1,11, 545],"A5":[1,12, 590],
            "B1":[1,14, 510],"B2":[1,15, 600],"B3":[1,13, 580],"B4":[1, 0, 610],"B5":[1, 1, 565],
            "C1":[1, 2, 640],"C2":[1, 3, 605],"C3":[1, 4, 550],"C4":[1, 5, 530],"C5":[1, 6, 620],
            "D1":[1, 7, 575],"D2":[0, 4, 595],"D3":[0, 8, 650],"D4":[0, 9, 545],"D5":[0,10, 510],
            "E1":[0,11, 565],"E2":[0,12, 550],"E3":[0,13, 565],"E4":[0,14, 560],"E5":[0,15, 520]
            }
        # inactive but not off stirers for mixing

        # this matrix stores if the motors are enabled (1) or disabled (0)
        # before writting to serial we check this to not sent writes not needed
        self.matrix = { 
            "A1":0,"A2":0,"A3":0,"A4":0,"A5":0,
            "B1":0,"B2":0,"B3":0,"B4":0,"B5":0,
            "C1":0,"C2":0,"C3":0,"C4":0,"C5":0,
            "D1":0,"D2":0,"D3":0,"D4":0,"D5":0,
            "E1":0,"E2":0,"E3":0,"E4":0,"E5":0
            }
    

    def __del__(self):

        self.disable_all()
        self.ser.close()
        del self.ser
        # disables all motors and clears variables


    def close(self):

        self.disable_all()
        self.ser.close()
        del self.ser
        # seems to do the same 


    def pattern_from_file(self, patternfile):

        with open(patternfile) as f:
            return json.load(f)
        # opens pattern 


    def activate_motor(self, motor_code, speed=None):
        ''' code as in A1 or C2 as marked in the actual board. See the dict motors'''

        if speed == None:
            shield, pin, speed = self.motors[motor_code] # sets motor speed if defined in pattern as 0 
        else:
            shield, pin, _  = self.motors[motor_code] # now if not 0 so loop isn't running over null
        
        # because sometimes we can send here a speed 0 to disable it
        # the following if will be longer than expected
        if self.matrix[motor_code] < 1 and speed > 0: # we need to activate it
            #The following line is a dirty trick. Some of the motors need to be
            # kickstarted at a higher speed
            command = "A%d P%d S3000\n" % (shield, pin)
            # and then we send the desired speed
            command += "A%d P%d S%d\n" % ( shield, pin, speed )
            self.matrix[motor_code] = 1 # mark it as enabled
            self.ser.write(command.encode()) # encode helps program run 

        elif self.matrix[motor_code] < 1 and speed == 0: # we keep it disabled (it's off with 0 speed)
            pass

        elif self.matrix[motor_code] > 0 and speed > 0: # just update speed
            command = "A%d P%d S%d\n" % ( shield, pin, speed )
            self.ser.write(command.encode())

        elif self.matrix[motor_code] > 0 and speed == 0: # we disable it (on with no speed)
            self.disable_motor(motor_code)

        else:
            print("something bad happened when updating a motor") # broken


    def activate_all(self, speed=None):

        for key in self.motors.keys(): # set to min stiring speed 
            self.activate_motor(key, speed)
            self.ser.flush() #flush variables


    def activate_pattern(self, pattern, speed=None):

        for i in pattern:
            _, _, speed = self.motors[i] 

            if pattern[i] == 1:
                self.activate_motor(i, speed*2) # x5 before
            else:
                self.activate_motor(i, speed*0) # x1 before if motor is off speed off
    

    def activate_rand(self, filename):
        '''Activate a random pattern - each motor at a random speed - and append
        this random configuration to the end of the file filename'''

        # need variable titles
        exp_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        # opens/creates csv in append mode
        rand_list = open(filename +'.csv','a')
        # random 5*5 speed

        self.rand_speed = { 
                    "A1":randint(0,4000),"A2":randint(0,4000),"A3":randint(0,4000),"A4":randint(0,4000),"A5":randint(0,4000),
                    "B1":randint(0,4000),"B2":randint(0,4000),"B3":randint(0,4000),"B4":randint(0,4000),"B5":randint(0,4000),
                    "C1":randint(0,4000),"C2":randint(0,4000),"C3":randint(0,4000),"C4":randint(0,4000),"C5":randint(0,4000),
                    "D1":randint(0,4000),"D2":randint(0,4000),"D3":randint(0,4000),"D4":randint(0,4000),"D5":randint(0,4000),
                    "E1":randint(0,4000),"E2":randint(0,4000),"E3":randint(0,4000),"E4":randint(0,4000),"E5":randint(0,4000)
                    }
        
        # append list
        rand_list.write(datetime.now().strftime('%H:%M'))
    	
        # enable the motors with the random speeds
        for i in self.motors.keys():
            speed = self.rand_speed[i]
            self.activate_motor(i, speed)
            

    def disable_motor(self, motor_code):

        shield, pin, _ = self.motors[motor_code]
        command = "A%d P%d S0\n" % ( shield, pin )

        if self.matrix[motor_code] > 0: # so it was enabled
            self.ser.write(command.encode())
            self.matrix[motor_code] = 0 # mark it disabled


    def disable_all(self):

        for key in self.motors.keys():
            self.disable_motor(key)



if __name__ == "__main__":

    b = BZBoard("/dev/ttyACM1")
