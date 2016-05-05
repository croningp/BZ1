"""
    coding: UTF-8

    bzboard.py

    Created 25/04/2016
    Kevin Donkers, The Cronin Group, University of Glasgow

    Control BZ-CA platform
"""

# system modules
import time, math
import json

# additional modules
import serial
import cv2, cv

# project modules
from commanduino.commandhandler import SerialCommandHandler

# default parameters
DEFAULT_MOTOR_TABLE = {'A1':[0,0]}
DEFAULT_IO_BAUDRATE = 115200
DEFAULT_IO_TIMEOUT = 1
DEFAULT_IO_DELIM = ','
DEFAULT_IO_TERM = ';'

DEFAULT_SPEED = 1024
DEFAULT_FREQ = 100

SET_PWM = 'S'
SET_FREQ = 'F'


class BZBoard(object):

    def __init__(self, port, baudrate=DEFAULT_IO_BAUDRATE, timeout=DEFAULT_IO_TIMEOUT, delim=DEFAULT_IO_DELIM, term=DEFAULT_IO_TERM, motors=DEFAULT_MOTOR_TABLE):
        self.logger = logging.getLogger(self.__class__.__name__)
        # IO
        self.cmdHdl = SerialCommandHandler(port, baudrate, timeout, delim, term)
        self.cmdHdl.start()
        # response handling
        self.cmdHdl.add_default_handler(defaultPrint)
        self.cmdHdl.add_command('E',self.handle_error)
        self.cmdHdl.add_command('M',self.handle_msg)
        # motor lookup table    {'motor':[shield,pin]}
        self.motors = motors
        # set pwm frequency to default
        self.set_freq()

    ##
    @classmethod
    def from_config(cls, config):
        port = config['port']

        if 'baudrate' in config:
            baudrate = config['baudrate']
        else:
            baudrate = DEFAULT_IO_BAUDRATE

        if 'timeout' in config:
            timeout = config['timeout']
        else:
            timeout = DEFAULT_IO_TIMEOUT

        if 'delim' in config:
            delim = config['delim']
        else:
            delim = DEFAULT_IO_DELIM

        if 'term' in config:
            term = config['term']
        else:
            term = DEFAULT_IO_TERM

        if 'motors' in config:
            motors = config['motors']
        else:
            motors = DEFAULT_MOTOR_TABLE

        return cls(port, baudrate, timeout, delim, term, motors)

    @classmethod
    def from_configfile(cls, configfile):
        with open(configfile) as f:
            return cls.from_config(json.load(f))

    def __del__(self):
        self.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.cmdHdl.stop()
        self.cmdHdl.join()

    ##
    def motors_from_config(self, config):
        if 'motors' in config:
            motors = config['motors']
            self.motors = motors
        else:
            print "Error: no motors in config"

    def motors_from_configfile(self, configfile):
        with open(configfile) as f:
            return self.motors_from_config(json.load(f))

    def pattern_from_file(self, patternfile):
        with open(patternfile) as f:
            return json.load(f)

    ##
    def defaultPrint(self, cmd):
        print cmd

    def handle_error(self, msg):
        print "Error: {}".format(msg)

    def handle_msg(self, msg):
        print "Message: {}".format(msg)

    ##
    def set_freq(self, frequency=DEFAULT_FREQ):
        self.cmdHdl.send(SET_FREQ,frequency)

    def activate(self, motor='A1', speed=DEFAULT_SPEED):
        self.cmdHdl.send(SET_PWM,self.motors[motor][0],self.motors[motor][1],speed)

    def activate_all(self, speed=DEFAULT_SPEED):
        for m in self.motors:
            self.activate(m,speed)

    def deactivate(self, motor='A1'):
        self.activate(motor,0)

    def deactivate_all(self):
        for m in self.motors:
            self.activate(m,0)

    def activate_pattern(self,pattern,speed=DEFAULT_SPEED):
        for i in pattern:
            if pattern[i] = 1:
                self.activate(i,speed)
            else:
                self.deactivate(i)
