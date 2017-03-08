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

        self.motors = {
            "A1":[1, 8],"A2":[1, 9],"A3":[1,10],"A4":[1,11],"A5":[1,12],
            "B1":[1,14],"B2":[1,15],"B3":[1,13],"B4":[1, 0],"B5":[1, 1],
            "C1":[1, 2],"C2":[1, 3],"C3":[1, 4],"C4":[1, 5],"C5":[1, 6],
            "D1":[1, 7],"D2":[0,4],"D3":[0, 8],"D4":[0, 9],"D5":[0,10],
            "E1":[0,11],"E2":[0,12],"E3":[0,13],"E4":[0,14],"E5":[0,15]
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


    def activate_motor(self, motor_code, speed=70):
        ''' code as in A1 or C2 as marked in the actual board. See the dict motors'''

        shield, pin = self.motors[motor_code]
        command = "A%d P%d S%d\n" % ( shield, pin, speed )
        self.ser.write(command.encode())


    def activate_all(self, speed=100):

        for key in self.motors.keys():
            self.activate_motor(key, speed)
            self.ser.flush()


    def activate_pattern(self, pattern, speed=300):

        for i in pattern:

            if pattern[i] == 1:
                self.activate_motor(i, speed)
            else:
                self.disable_motor(i)


    def disable_motor(self, motor_code):

        shield, pin = self.motors[motor_code]
        command = "A%d P%d S0\n" % ( shield, pin )
        self.ser.write(command.encode())

    
    def disable_all(self):

        for key in self.motors.keys():
            self.disable_motor(key)


if __name__ == "__main__":

    board = BZBoard("/dev/ttyACM0")
