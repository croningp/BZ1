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
  cmdHdl.addCommand("T", testMsg);
  cmdHdl.setDefaultHandler(unrecognized);     // Handler for command that isn't matched  (returns "???")
}

void loop() {
  cmdHdl.processSerial(Serial);
}

void frequency(){
  int freq;
  String msg;
  freq = cmdHdl.readIntArg();
  if (freq != NULL) {
    if (freq <= MAX_FREQ && freq >= MIN_FREQ) {
      pwm0.setPWMFreq(freq);
      pwm1.setPWMFreq(freq);
      msg = msg + "frequency " + freq;
      sendMsg(msg);
    }
    else {
      errorMsg("Frequency value not in range");
    }
  }
  else {
    errorMsg("Define frequency value");
  }
}

void setPWM() {
  int shield;
  int pin;
  int speed;
  String msg;
  shield = cmdHdl.readIntArg();
  if (cmdHdl.argOk==false) {
    errorMsg("Shield not defined");
    return;
  }
  pin = cmdHdl.readIntArg();
  if (cmdHdl.argOk==false) {
    errorMsg("Pin not defined");
    return;
  }
  else if (pin >= NUM_PINS){
    msg = msg + "Shields only supports " + NUM_PINS + " pins";
    errorMsg(msg);
    return;
  }
  speed = cmdHdl.readIntArg();
  if (cmdHdl.argOk==false) {
    errorMsg("Speed not defined");
    return;
  }
  if (speed <= MAX_SPEED && speed >= MIN_SPEED) {
    if (shield==0){
      pwm0.setPWM(pin,0,speed);
      msg = msg + "shield " + shield + " pin " + pin + " speed " + speed;
      sendMsg(msg);
    }
    else if (shield==1){
      pwm1.setPWM(pin,0,speed);
      msg = msg + "shield " + shield + " pin " + pin + " speed " + speed;
      sendMsg(msg);
    }
    else {
      msg = msg + "Shield " + shield + " not supported";
      errorMsg(msg);
    }
  }
  else {
    errorMsg("Speed value not in range");
  }
}

void unrecognized(const char *command) {
  errorMsg("Unrecognized");
}

void errorMsg(String msg) {
  char command[COMMANDHANDLER_BUFFER+1];
  msg.toCharArray(command,COMMANDHANDLER_BUFFER+1);
  cmdHdl.initCmd();
  cmdHdl.addCmdString("E");
  cmdHdl.addCmdDelim();
  cmdHdl.addCmdString(command);
  cmdHdl.addCmdTerm();
  cmdHdl.sendCmdSerial();
}

void sendMsg(String msg) {
  char command[COMMANDHANDLER_BUFFER+1];
  msg.toCharArray(command,COMMANDHANDLER_BUFFER+1);
  cmdHdl.initCmd();
  cmdHdl.addCmdString("M");
  cmdHdl.addCmdDelim();
  cmdHdl.addCmdString(command);
  cmdHdl.addCmdTerm();
  cmdHdl.sendCmdSerial();
}

void testMsg() {
    int shield = 1;
    int pin = 2;
    int speed = 3;
    String msg;
    msg = msg + "test:shield" + shield + "pin" + pin + "speed" + speed;
    sendMsg(msg);
    Serial.println(msg);
}
