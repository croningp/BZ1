/*
This code tries to be a minimal firmware implementation.
It uses: https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library/
In particular the file pwmtest.ino adding basic serial reading.
It doesn't have callbacks or error checking, so the user must be
sure everything sent here is OK beforehand.

The commands are like A_ P_ S_
Each argument starts with a capital letter, followed by numbers (value of arg), no space
Each argument is separated by 1 space
A means Adafruit board, it must be 0 or 1
P means pins, it must be a number between 0 and 15
S means speed, which will define the PWM signal. Max in 4096
Commands must end with '\n'
*/

#include <Adafruit_PWMServoDriver.h>

#define BUFFER_SIZE 200

// Init both adafruit boards
Adafruit_PWMServoDriver pwm0 = Adafruit_PWMServoDriver(0x40);
Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x41);


int read_command(char *buffer)
{

	static int pos = 0;
	int rpos;

	if (Serial.available() > 0) {
		char readch = Serial.read();

		switch (readch) {

			case '\n':
				rpos = pos;
				pos = 0; // Reset position index ready for next time
				return rpos;

			default:

				if (pos < BUFFER_SIZE -1) {
					buffer[pos++] = readch;
					buffer[pos] = '\0';
				} else {
					Serial.println("666"); //buffer overflow
				}
		}
	}
	// no end line or char found, return -1
	return -1;

}


void parse_command(char* command) 
{

	char* parameter;
	parameter = strtok(command, " ");
	long shield, pin, speed;

	while (parameter != NULL) {

		switch(parameter[0]) {

			case 'A':
				shield = strtol(parameter+1, NULL, 10);
				break;

			case 'P':
				pin = strtol(parameter+1, NULL, 10);
				break;

			case 'S':
				speed = strtol(parameter+1, NULL, 10);
				break;

		}
		parameter = strtok(NULL, " ");
	}
	
	for (int x=0; x < BUFFER_SIZE; x++)
		command[x] = '\0';
	
  if (shield == 0)
    pwm0.setPWM(pin, 0, speed);

  if (shield == 1)
    pwm1.setPWM(pin, 0, speed);

}


void setup() 
{
  
  Serial.begin(19200);
  Serial.flush();

  pwm0.begin();
  pwm0.setPWMFreq(100);  //Max is 1600, Kevin was using 1000
  pwm1.begin();
  pwm1.setPWMFreq(100);

}


void loop() 
{
  
  static char buffer[BUFFER_SIZE];

  if (read_command(buffer) > 0)
    parse_command(buffer);
    
}
