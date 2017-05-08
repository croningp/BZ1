'''
This is a minimal implementation of the bz_board python interface.
For some reason the full fledge implementation done by Kevin
was giving some problems we couldn't solve, so we are
doing this minimal implementation instead.

If you want better functionality, error handling,... check the other one

motor D2 is 0,4

'''

import serial, time, json


class BZBoard:


    def __init__(self, port):

        self.ser = serial.Serial(port, 9600, timeout=120)
        time.sleep(2) # serial docs recommend a wait just after connection
        self.ser.flush(); self.ser.flushInput(); self.ser.flushOutput();

        self.motors = { # [adafruit_shield, pin, min_speed]
            "A1":[1, 8, 500],"A2":[1, 9, 530],"A3":[1,10, 550],"A4":[1,11, 550],"A5":[1,12, 600],
            "B1":[1,14, 540],"B2":[1,15, 570],"B3":[1,13, 580],"B4":[1, 0, 600],"B5":[1, 1, 600],
            "C1":[1, 2, 580],"C2":[1, 3, 570],"C3":[1, 4, 570],"C4":[1, 5, 500],"C5":[1, 6, 620],
            "D1":[1, 7, 550],"D2":[0,4, 550],"D3":[0, 8, 550],"D4":[0, 9, 550],"D5":[0,10, 500],
            "E1":[0,11, 550],"E2":[0,12, 530],"E3":[0,13, 550],"E4":[0,14, 580],"E5":[0,15, 550]
            }

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


    def close(self):

        self.disable_all()
        self.ser.close()
        del self.ser


    def pattern_from_file(self, patternfile):

        with open(patternfile) as f:
            return json.load(f)


    def activate_motor(self, motor_code, speed=None):
        ''' code as in A1 or C2 as marked in the actual board. See the dict motors'''

        if speed == None:
            shield, pin, speed = self.motors[motor_code] 
        else:
            shield, pin, _  = self.motors[motor_code] 

        # because sometimes we can send here a speed 0 to disable it
        # the following if will be longer than expected
        if self.matrix[motor_code] < 1 and speed > 0: # we need to activate it
            #The following line is a dirty trick. Some of the motors need to be
            # kickstarted at a higher speed
            command = "A%d P%d S2000\n" % (shield, pin)
            # and then we send the desired speed
            command += "A%d P%d S%d\n" % ( shield, pin, speed )
            self.matrix[motor_code] = 1 # mark it as enabled
            self.ser.write(command.encode())

        elif self.matrix[motor_code] < 1 and speed == 0: # we keep it disabled
            pass

        if self.matrix[motor_code] > 0 and speed > 0: # just update speed
            command = "A%d P%d S%d\n" % ( shield, pin, speed )
            self.ser.write(command.encode())

        if self.matrix[motor_code] > 0 and speed == 0: # we disable it
            board.disable_motor(motor_code)


    def activate_all(self, speed=None):

        for key in self.motors.keys():
            self.activate_motor(key, speed)
            self.ser.flush()


    def activate_pattern(self, pattern, speed=None):

        for i in pattern:

            if pattern[i] == 1:
                self.activate_motor(i, speed)
            else:
                self.disable_motor(i)


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

    b = BZBoard("/dev/ttyACM0")