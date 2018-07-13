/*
 * commands are like P_ M_ C_ D_ S_ E_
 * Each argument starts with a capital letter, followed by numbers (value of arg), no space
 * Each argument is separated by 1 space
 * P means pump, identifies the pump. At the moment it goes from 0 to 6
 * M means motor, identifies motor inside the P declared before. it is 0 or 1, for valve or plunger
 * C means code that identifies the task. Once the task is finished, this code will be send to the Serial
 * D means direction, up or down. 0 or 1
 * S means speed, which is actually the ms per pulse. We usually use values between 20 to 2000
 * E means steps, number of steps. Needs to be bigger than 0. With triconts 100k is full plunger
 * This firmware DOESNT CHECK ANYTHING, make the checks in the code that sends the commands here
 * For example, if you are rotating motor P0 M0, and while its rotating, you sends a new command to the same motor
 * this firmware is likely to fuck itself.
 * An example of command would be: P0 M1 D0 C123 S50 E50000
 *
 * Juan M Parrilla, Cronin group
*/ 


#define MOTORS_PER_PUMP 2
#define BUFFER_SIZE 200

struct Motor
{
	/* INPUTS */
	long pin_en;
	long pin_step;
  long pin_dir;

	/* STATE */
	long msec_per_pulse;
	long remaining_steps;
	long next_state; /* controls pin_step, so it will be high or low */
	long remaining_step_ms;
	long task_code;
};

struct Pump
{
	Motor motors[2]; /* 0 is plunger, 1 is valve */
};

Pump pumps[] = {
	// PX_ENABLE, PX_STEP, PX_DIR -- VX_ENABLE, VX_STEP, VX_DIR
	{ { {4, 3, 2}, {7, 6, 5} } }, 		// pump 1
	{ { {54, 55, 56}, {57, 58, 59} } }, // pump 2
	{ { {60, 61, 62}, {63, 64, 65} } }, // pump 3
	{ { {66, 67, 68}, {69, 53, 52} } }, // pump 4
	{ { {18, 17, 16}, {26, 24, 22} } },	// pump 5
	{ { {13, 12, 11}, {10, 9, 8} } }, 	// pump 6
	{ { {32, 30, 28}, {38, 36, 34} } }, 	// pump 7
	{ { {14, 15, 19}, {20, 21, 23} } } 	// pump 8
};

int n_pumps = sizeof(pumps)/sizeof(pumps[0]);

int read_command(char *buffer) {

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

	while (parameter != NULL) {

		Pump *pump;
		Motor *motor;
		long pumpid, motorid, code, dir, sp, steps;

		switch(parameter[0]) {

			case 'P':
				pumpid = strtol(parameter+1, NULL, 10);
				pump = &pumps[pumpid];
				break;

			case 'M':
				motorid = strtol(parameter+1, NULL, 10);
				motor = &pump->motors[motorid];
				digitalWrite( motor->pin_en, LOW ); //enable motor
				break;

			case 'C':
				code = strtol(parameter+1, NULL, 10);
				motor->task_code = code;
				break;

			case 'D':
				dir = strtol(parameter+1, NULL, 10);
				if (dir == 0) {
					digitalWrite( motor->pin_dir, LOW );
				} else {
					digitalWrite( motor->pin_dir, HIGH );
				}
				break;

			case 'S':
				sp = strtol(parameter+1, NULL, 10);
				motor->msec_per_pulse = sp;
				motor->remaining_step_ms = sp;
				break;

			case 'E':
				steps = strtol(parameter+1, NULL, 10);
				motor->remaining_steps = steps;
				if (steps <= 0) {
					Serial.println(motor->task_code);
				}
				break;
		}
		parameter = strtok(NULL, " ");
	}
	
	for (int x=0; x < BUFFER_SIZE; x++)
		command[x] = '\0';
	
}

void setup() 
{
	Serial.begin(115200);
	Serial.flush();

	for (int pumpi = 0; pumpi < n_pumps; pumpi++) {
		Pump *pump = &pumps[pumpi];
		for (int motori = 0; motori < MOTORS_PER_PUMP; motori++) {
			Motor *motor = &pump->motors[motori];
			motor->remaining_step_ms = 0;
			motor->remaining_steps = 0;
			motor->next_state = 1;
			pinMode(motor->pin_en, OUTPUT);
			pinMode(motor->pin_dir, OUTPUT);
			pinMode(motor->pin_step, OUTPUT);
			digitalWrite(motor->pin_en, HIGH); // HIGH is disabled
		}
	}
}

void loop() 
{
	static char buffer[BUFFER_SIZE];

	if (read_command(buffer) > 0) {
		parse_command(buffer);
	}

	long msec = 2147483647; // max long
	for (int pumpi = 0; pumpi < n_pumps; pumpi++) {
		Pump *pump = &pumps[pumpi];
		for (int motori = 0; motori < MOTORS_PER_PUMP; motori++) {
			Motor *motor = &pump->motors[motori];
			if (motor->remaining_steps > 0) {
				msec = min(msec, motor->remaining_step_ms);
			}
		}
	}

	if (msec < 2147483647)
		delayMicroseconds(msec);

	for (int pumpi = 0; pumpi < n_pumps; pumpi++) {
		Pump *pump = &pumps[pumpi];
		for (int motori = 0; motori < MOTORS_PER_PUMP; motori++) {
			Motor *motor = &pump->motors[motori];
			if (motor->remaining_steps > 0) {
				motor->remaining_step_ms -= msec;
				if ( (motor->remaining_step_ms <= 0) ) {
					/* This motor is ready for the next step */
					digitalWrite(motor->pin_step, motor->next_state);
					motor->next_state = !motor->next_state;
					motor->remaining_step_ms = motor->msec_per_pulse;
					motor->remaining_steps--;
					if (motor->remaining_steps <= 0) { // motor finished task
						digitalWrite( motor->pin_en, HIGH); // disable motor
						motor->remaining_step_ms = 0;
						motor->remaining_steps = 0;
						motor->msec_per_pulse = 0;
						Serial.println(motor->task_code);
					}
				}
			}
		}
	}
}

