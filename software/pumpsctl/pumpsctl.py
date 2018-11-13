from time import sleep
from serial import Serial
import threading

# path hack to load a python script from a sibling folder
import os, sys
sys.path.append(os.path.abspath('..'))
from tools import VolCtl 
import pickle
import os.path



class PumpsCtl:

    def __init__(self, port):
        
        self.v = VolCtl()
        self.pumps_ser = Serial(port, 115200)
        sleep(2) # pyserial recommends 2 seconds wait after connection
        self.pumps_ser.flush(); self.pumps_ser.flushInput(); self.pumps_ser.flushOutput();

        # syringe means the volume of the syringe attached in ml
        # pumps must start its valve in input state 
        # plunger position in steps, 0 means when the plunger is up, no liquid inside
        self.pumps =   {'P0': {'id':0, 'syringe':12.5, 'valve': 'input', 'plunger' : 0},
                        'P1': {'id':1, 'syringe':5.00, 'valve': 'input', 'plunger' : 0},
                        'P2': {'id':2, 'syringe':12.5, 'valve': 'input', 'plunger' : 0},
                        'P3': {'id':3, 'syringe':12.5, 'valve': 'input', 'plunger' : 0},
                        'P4': {'id':4, 'syringe':12.5, 'valve': 'input', 'plunger' : 0},
                        'P5': {'id':5, 'syringe':12.5, 'valve': 'input', 'plunger' : 0}}         
       
        # to control access to serial port
        self.ser_lock = threading.Lock() 
        d = threading.Thread(target=self.read_serial, daemon=True)
        # to control access to individual pumps
        self.pump_locks = [threading.Lock() for i in range(len(self.pumps))]
        # a list of current tasks so we know if something is running or not
        self.current_tasks = []
        # to make it thread safe, no idea if erase() is thread safe
        self.ctasks_lock = threading.Lock()
      
        d.start()


    def read_serial(self):
        ''' reads from serial and populates the current tasks list
        which tells which tasks have been completed
        This is supposed to be executed as a daemon'''

        while True:
            with self.ser_lock:
                response = self.pumps_ser.readline().strip()

            if response is not None:
                self.current_tasks.append(int(response))

            sleep(0.3)


    def wait_response(self, code):
        ''' Waits for this task code to be completed '''

        while code not in self.current_tasks:
            sleep(0.1)

        with self.ctasks_lock: 
            self.current_tasks.remove(code)


    def rotate_valve(self, pump, valve):
        ''' positions the valve to input or output '''

        pump_id = self.pumps[pump]['id'] 
        code = int( str(pump_id) + str(1) )

        if valve is 'input' and self.pumps[pump]['valve'] is not 'input':
            command = "P%d M1 C%d D0 S400 E2208\n" % ( pump_id, code )
            self.pumps_ser.write(command.encode())
            self.wait_response(code)
            self.pumps[pump]['valve'] = 'input'


        if valve is 'output' and self.pumps[pump]['valve'] is not 'output':
            command = "P%d M1 C%d D1 S400 E2208\n" % ( pump_id, code )
            self.pumps_ser.write(command.encode())
            self.wait_response(code)
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
        self.wait_response(code)
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
        '''quantity in ml
        Read MOTD Threading'''

        pump_id = self.pumps[pump]['id']
        pump_lock = self.pump_locks[pump_id]
        #call function to update volumes in volctl
        self.v.update_volumes(self,pump,quantity):

        with pump_lock:
            syringe = self.pumps[pump]['syringe']
            steps_left = (quantity / syringe) * 100000 # plunger is 100000 steps 

            while steps_left > 0:
                steps_now = min(steps_left, 100000) 
                steps_left = steps_left - steps_now
                self.absorb(pump, speedIn,  steps_now)
                self.release(pump, speedOut)
                self.rotate_valve(pump, 'input')
        

    def pump_multiple(self, *actions):
        ''' This will execute several pumps at the same time.
        The main thread will wait until all are finished.
        The *args parameter will be a list where each position
        is a dict, with pump, quantity, speedIn and speedOut.
        Read MOTD threading'''

        threads = [ 
                threading.Thread(
                    target=self.pump_in, 
                    args=(a['pump'], a['quantity'], a['speedIn'], a['speedOut'])
                )
                for a in actions 
        ]

        for t in threads:
            t.start()

        for t in threads:
            t.join()       
  

    def close(self):

        for p in self.pumps.keys():
            self.rotate_valve( p, 'input')

        del self

        print("Pumps closed.\n")



if __name__ == '__main__':

    p = PumpsCtl('/dev/ttyACM0')
