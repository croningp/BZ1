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
