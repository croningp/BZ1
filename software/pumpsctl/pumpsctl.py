from time import sleep
from serial import Serial
import threading

class PumpsCtl:

    def __init__(self, port):

        self.pumps_ser = Serial(port, 115200)
        sleep(2) # pyserial recommends 2 seconds wait after connection
        self.pumps_ser.flush(); self.pumps_ser.flushInput(); self.pumps_ser.flushOutput();

        # syringe means the volume of the syringe attached in ml
        # pumps must start its valve in input state 
        # plunger position in steps, 0 means when the plunger is up, no liquid inside
        self.pumps = {'P0' : {'id':0, 'syringe':12.5, 'valve': 'input', 'plunger' : 0} ,
                        'P1': {'id':1, 'syringe':5, 'valve': 'input', 'plunger' : 0},
                        'P2': {'id':2, 'syringe':5, 'valve': 'input', 'plunger' : 0},
                        'P3': {'id':3, 'syringe':5, 'valve': 'input', 'plunger' : 0},
                        'P4': {'id':4, 'syringe':5, 'valve': 'input', 'plunger' : 0},
                        'P5': {'id':5, 'syringe':5, 'valve': 'input', 'plunger' : 0}}

        self.ser_lock = threading.Lock() # to control access to serial port
        # to control access to individual pumps
        self.pump_locks = [threading.Lock() for i in range(len(self.pumps))]

    def wait_response(self):
        ''' Syncs pumps and Arduino '''

        self.ser_lock.acquire()
        try:
            response = self.pumps_ser.readline()#.strip()
        finally:
            self.ser_lock.release()


    def rotate_valve(self, pump, valve):
        ''' positions the valve to input or output '''

        pump_id = self.pumps[pump]['id'] 
        code = int( str(pump_id) + str(1) )

        if valve is 'input' and self.pumps[pump]['valve'] is not 'input':
            command = "P%d M1 C%d D0 S400 E2208\n" % ( pump_id, code )
            self.pumps_ser.write(command.encode())
            self.wait_response()
            self.pumps[pump]['valve'] = 'input'


        if valve is 'output' and self.pumps[pump]['valve'] is not 'output':
            command = "P%d M1 C%d D1 S400 E2208\n" % ( pump_id, code )
            self.pumps_ser.write(command.encode())
            self.wait_response()
            self.pumps[pump]['valve'] = 'output'


    def actuate_pump(self, pump, speed, abs_steps):
        ''' abs_steps means absolute steps position, being 1 fully pushed and 100000 fully pulled'''

        pump_id = self.pumps[pump]['id'] 
        code = int( str(pump_id) + str(0) )
        
        if abs_steps < 1: abs_steps = 1
        if abs_steps > 100000: abs_steps = 100000
        if speed < 20: speed = 20

        if abs_steps > self.pumps[pump]['plunger'] : direction = 0
        else: direction = 1

        required_steps = abs( abs_steps - self.pumps[pump]['plunger'] )

        command = "P%d M0 C%d D%d S%d E%d\n" % ( pump_id, code, direction, speed, required_steps )
        self.pumps_ser.write(command.encode())
        self.wait_response()
        self.pumps[pump]['plunger'] = abs_steps


    def absorb(self, pump, speed, abs_steps):
        ''' abs_steps means absolute steps, being 1 fully pushed and 50000 fully pulled
        pulls liquid inside pump through input tube'''

        self.rotate_valve(pump, 'input')
        self.actuate_pump(pump, speed, abs_steps)


    def release(self, pump, speed):
        ''' pushes liquid outside pump through output tube '''

        self.rotate_valve(pump, 'output')
        self.actuate_pump(pump, speed, 1)


    def pump_in(self, pump, quantity=1, speedIn=50, speedOut=50):
        '''quantity in ml'''

        pump_id = self.pumps[pump]['id']
        pump_lock = self.pump_locks[pump_id]
            
        pump_lock.acquire()
        
        try:
            syringe = self.pumps[pump]['syringe']
            steps_left = (quantity / syringe) * 100000 # plunger is 100000 steps 

            while steps_left > 0:
                steps_now = min(steps_left, 100000) 
                steps_left = steps_left - steps_now
                self.absorb(pump, speedIn,  steps_now)
                self.release(pump, speedOut)
                self.rotate_valve(pump, 'input')
        
        finally:
            pump_lock.release()


    def pump(self, pump, quantity=1, speedIn=50, speedOut=50):
        ''' This fuction basically launches pump_in a separate thread
        so you can execute several of them at the same time.
        You need to control when they are finished'''

        t = threading.Thread(target=self.pump_in, args=(pump, quantity,
            speedIn, speedOut,))
        t.start()

    
    def close(self):

        for p in self.pumps.keys():
            self.rotate_valve( p, 'input')

        del self

        print("Pumps closed.\n")



if __name__ == '__main__':

    p = PumpsCtl('/dev/ttyACM0')
