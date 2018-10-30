())

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

        rand_list.write(self.rand_speed)
        #appends list
        rand_list.write(datetime.now().strftime('%H:%M')) 
    	# write random values to stirer matrix
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