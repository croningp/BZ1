Because we couldn't get the full-fledged software designed by Keving working, we will try now to just implement a minimal package that does the basic stuff without error checking or anything. Just to be sure if the problem was software related or platform related.

If we a minimal implementation it still fails, then we know the problem was in the hardware. Otherwise we know it is in the software.

Thus, this implementation will only have 2 files:

- The arduino ino file, which will be a copy paste from the adafruit library removing all the unnecessary stuff, and adding basic reading from the serial port. (https://github.com/adafruit/Adafruit-PWM-Servo-Driver-Library)

- A python file which will just send serial commands as defined by the user, without callbacks, checks or anything.
