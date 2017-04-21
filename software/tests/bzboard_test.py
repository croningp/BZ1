"""
    coding: UTF-8
    Python 2.7

    robot.py

    Created 05/05/2016
    Kevin Donkers, The Cronin Group, University of Glasgow

    Example of how to use bzboard.py
"""
# system imports
import time
import os, sys

# add path of bzboard.py, relative to /bz_ca/tests
lib_path = os.path.abspath(os.path.join('..', 'bzboard'))
sys.path.append(lib_path)
# then load module
import bzboard

# link to config file
SETUP_CONFIG_FILE = './bzboard_config_wintest.json'
# link to pattern file
PATTERN_FILE = './pattern_test.json'

# load config file in BZBoard
bz = bzboard.BZBoard.from_configfile(SETUP_CONFIG_FILE)

# activate each motor for 0.5 seconds each
for m in bz.motors:
    bz.activate(m)
    time.sleep(0.5)
    bz.deactivate(m)

# load and run a pattern from pattern file
file_pattern = bz.pattern_from_file(PATTERN_FILE)
bz.activate_pattern(file_pattern)
time.sleep(10)

# or manually set pattern
man_pattern = {
"A1":1,"A2":0,"A3":0,"A4":0,"A5":0,
"B1":0,"B2":1,"B3":0,"B4":0,"B5":0,
"C1":0,"C2":0,"C3":1,"C4":0,"C5":0,
"D1":0,"D2":0,"D3":0,"D4":1,"D5":0,
"E1":0,"E2":0,"E3":0,"E4":0,"E5":1
}
bz.activate_pattern(man_pattern)
time.sleep(10)

# all motors can be switched on/off
bz.activate_all()
time.sleep(5)
bz.deactivate_all()
