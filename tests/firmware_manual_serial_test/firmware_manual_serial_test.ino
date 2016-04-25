/* 
Kevin Donkers
Cronin Group, University of Glasgow, Glasgow

Serial communication to Adafruit 16-Channel PWM/Servo Shield
utilising the Adafruit-PWM-Servo-Driver-Library
[https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library]
and CommandHandler by jgrizou
[https://github.com/croningp/Arduino-CommandHandler]

Higher level functions allow for manual testing over serial connection

 */
 
#include <CommandHandler.h>
#include <Adafruit_PWMServoDriver.h>

//Create a CommandHandler Instance (delim,term)
CommandHandler cmdHdl(" ", '\n');

//Create Adafruit PWM shield instance(s) (address)
Adafruit_PWMServoDriver pwm0 = Adafruit_PWMServoDriver(0x40);
Adafruit_PWMServoDriver pwm1 = Adafruit_PWMServoDriver(0x41);

//Global variables
int DEFAULT_ON_SPEED;     //globally variable speed
int DEFAULT_OFF_SPEED;

const int MAX_SPEED = 4095;
const int MIN_SPEED = 0;
const int MAX_FREQ = 1000;
const int MIN_FREQ = 60;
const int DEFAULT_DELAY = 1000;   //Delay in ms
const int DEFAULT_BLINK = 2;
const int BLINK_PIN_1 = 0;
const int BLINK_PIN_2 = 1;
const int NUM_PINS = 16;

void setup() {
  Serial.begin(115200);
  pwm0.begin();
  pwm1.begin();
  pwm0.setPWMFreq(MAX_FREQ);
  pwm1.setPWMFreq(MAX_FREQ);
  
  // Setup callbacks for SerialCommand commands
  cmdHdl.addCommand("BLINK", blinkLights);    // Blinks LEDs to check that shields are working
  cmdHdl.addCommand("ON", pwmOn);             // Switch PWM pin on
  cmdHdl.addCommand("OFF", pwmOff);           // Switch PWM pin off
  cmdHdl.addCommand("SPEED", speed);          // Change duty cycle of PWM
  cmdHdl.addCommand("FREQ", frequency);       // Change frequency of PWM
  cmdHdl.setDefaultHandler(unrecognized);     // Handler for command that isn't matched  (returns "Quelle?")

  //Define starting speeds
  DEFAULT_ON_SPEED = MAX_SPEED;
  DEFAULT_OFF_SPEED = MIN_SPEED;
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

void speed(){
  int dutyCycle;
  double percent;
  dutyCycle = cmdHdl.readIntArg();
  if (dutyCycle != NULL) {
    if (dutyCycle <= MAX_SPEED && dutyCycle >= MIN_SPEED) {
      DEFAULT_ON_SPEED = dutyCycle;
      percent = 100*(double)DEFAULT_ON_SPEED/(double)MAX_SPEED;
      Serial.print("Speed set to ");
      Serial.print(DEFAULT_ON_SPEED);
      Serial.print(" (");
      Serial.print(percent, 1);
      Serial.println("%)");
    }
    else {
      Serial.println("Speed value not in range");
    }
  }
  else {
    Serial.println("Define speed value");
  }
}

void blinkLights() {
  int aNumber;
  aNumber = cmdHdl.readIntArg();    // Get the next argument from the SerialCommand object buffer
  if (aNumber != NULL) {    // As long as it existed, take it
    Serial.print("Blinking ");
    Serial.print(aNumber);
    Serial.println(" times");
    for (int i=0; i < aNumber; i++){
      pwm0.setPWM(BLINK_PIN_1,0,DEFAULT_ON_SPEED);
      pwm0.setPWM(BLINK_PIN_2,0,DEFAULT_OFF_SPEED);
      delay(DEFAULT_DELAY);
      pwm0.setPWM(BLINK_PIN_1,0,DEFAULT_OFF_SPEED);
      pwm0.setPWM(BLINK_PIN_2,0,DEFAULT_ON_SPEED);
      delay(DEFAULT_DELAY);
      pwm0.setPWM(BLINK_PIN_1,0,DEFAULT_OFF_SPEED);
      pwm0.setPWM(BLINK_PIN_2,0,DEFAULT_OFF_SPEED);
      delay(DEFAULT_DELAY/2);
    }
  }
  else {
    Serial.println("Here's blinking at you");
    for (int i=0; i < DEFAULT_BLINK; i++){
      pwm0.setPWM(BLINK_PIN_1,0,DEFAULT_ON_SPEED);
      pwm0.setPWM(BLINK_PIN_2,0,DEFAULT_OFF_SPEED);
      delay(DEFAULT_DELAY);
      pwm0.setPWM(BLINK_PIN_1,0,DEFAULT_OFF_SPEED);
      pwm0.setPWM(BLINK_PIN_2,0,DEFAULT_ON_SPEED);
      delay(DEFAULT_DELAY);
      pwm0.setPWM(BLINK_PIN_1,0,DEFAULT_OFF_SPEED);
      pwm0.setPWM(BLINK_PIN_2,0,DEFAULT_OFF_SPEED);
      delay(DEFAULT_DELAY/2);
    }
  }
}

void pwmOn() {
  int shield;
  int pin;
  int speed;
  shield = cmdHdl.readIntArg();
  if (cmdHdl.argOk==false) {    
    Serial.println("Define shield & pin");
    return;
  }
  pin = cmdHdl.readIntArg();
  if (cmdHdl.argOk==false) {
    Serial.println("Define shield & pin");
    return;
  }
  else if (pin >= NUM_PINS){
    Serial.print("Shields only support ");
    Serial.print(NUM_PINS);
    Serial.println(" pins");
    return;
  }
  speed = cmdHdl.readIntArg();
  if (cmdHdl.argOk==false) {  //REMOVE FROM FINAL VERSION
    speed = DEFAULT_ON_SPEED;
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

void pwmOff() {
  int shield;
  int pin;
  shield = cmdHdl.readIntArg();
  if (cmdHdl.argOk==false) {    
    Serial.println("Define shield & pin");
    return;
  }
  pin = cmdHdl.readIntArg();
  if (cmdHdl.argOk==false) {
    Serial.println("Define shield & pin");
  }
  else if (pin >= NUM_PINS){
    Serial.print("Shields only support ");
    Serial.print(NUM_PINS);
    Serial.println(" pins");
  }
  else if (shield==0){
    pwm0.setPWM(pin,0,DEFAULT_OFF_SPEED);
    Serial.print("shield 0, pin ");
    Serial.print(pin);
    Serial.print(", speed ");
    Serial.println(DEFAULT_OFF_SPEED);
  }
  else if (shield==1){
    pwm1.setPWM(pin,0,DEFAULT_OFF_SPEED);
    Serial.print("shield 1, pin ");
    Serial.print(pin);
    Serial.print(", speed ");
    Serial.println(DEFAULT_OFF_SPEED);
  }
  else {
    Serial.print("Shield ");
    Serial.print(shield);
    Serial.println(" not supported");
  }
}

void unrecognized(const char *command) {
  Serial.println("Quelle?");
}
