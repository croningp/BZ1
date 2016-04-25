/* 
Kevin Donkers
Cronin Group, University of Glasgow, Glasgow

Serial communication to Adafruit 16-Channel PWM/Servo Shield
utilising the Adafruit-PWM-Servo-Driver-Library
[https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library]
and CommandHandler by jgrizou
[https://github.com/croningp/Arduino-CommandHandler]

 */
 
#include <CommandHandler.h>
#include <Adafruit_PWMServoDriver.h>

//Create a CommandHandler Instance (delim,term)
CommandHandler cmdHdl(",", ';');

//Create Adafruit PWM shield instance(s) (address)
Adafruit_PWMServoDriver pwm0 = Adafruit_PWMServoDriver(0x40);
Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x41);

//Default limits
const int MAX_SPEED = 4095;
const int MIN_SPEED = 0;
const int MAX_FREQ = 1000;
const int MIN_FREQ = 60;
const int NUM_PINS = 16;

void setup() {
  Serial.begin(115200);
  pwm0.begin();
  pwm1.begin();
  pwm0.setPWMFreq(MAX_FREQ);
  pwm1.setPWMFreq(MAX_FREQ);
  
  // Setup callbacks for SerialCommand commands
  cmdHdl.addCommand("S", setPWM);             // Set PWM of pin
  cmdHdl.addCommand("F", frequency);          // Change frequency of PWM
  cmdHdl.setDefaultHandler(unrecognized);     // Handler for command that isn't matched  (returns "Quelle?")
}

void loop() {
  cmdHdl.processSerial(Serial);
}

void frequency(){
  int freq;
  freq = cmdHdl.readIntArg();
  if (freq != NULL) {
    if (freq <= MAX_FREQ && freq >= MIN_FREQ) {
      pwm0.setPWMFreq(freq);
      pwm1.setPWMFreq(freq);
      Serial.print("Frequency set to ");
      Serial.println(freq);
    }
    else {
      Serial.println("Frequency value not in range");
    }
  }
  else {
    Serial.println("Define frequency value");
  }
}

void setPWM() {
  int shield;
  int pin;
  int speed;
  shield = cmdHdl.readIntArg();
  if (cmdHdl.argOk==false) {    
    Serial.println("Define shield, pin & speed");
    return;
  }
  pin = cmdHdl.readIntArg();
  if (cmdHdl.argOk==false) {
    Serial.println("Define shield, pin & speed");
    return;
  }
  else if (pin >= NUM_PINS){
    Serial.print("Shields only support ");
    Serial.print(NUM_PINS);
    Serial.println(" pins");
    return;
  }
  speed = cmdHdl.readIntArg();
  if (cmdHdl.argOk==false) {
    Serial.println("Define shield, pin & speed");
    return;
  }
  if (speed <= MAX_SPEED && speed >= MIN_SPEED) {
    if (shield==0){
      pwm0.setPWM(pin,0,speed);
      Serial.print("shield 0, pin ");
      Serial.print(pin);
      Serial.print(", speed ");
      Serial.println(speed);
    }
    else if (shield==1){
      pwm1.setPWM(pin,0,speed);
      Serial.print("shield 1, pin ");
      Serial.print(pin);
      Serial.print(", speed ");
      Serial.println(speed);
    }
    else {
      Serial.print("Shield ");
      Serial.print(shield);
      Serial.println(" not supported");
    }
  }
  else {
    Serial.println("Speed value not in range");
  }
}

void unrecognized(const char *command) {
  Serial.println("???");
}
