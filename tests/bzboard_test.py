# -*- coding: utf-8 -*-

import time

# add path of bzboard.py, relative to /bz_ca/tests
import os, sys
lib_path = os.path.abspath(os.path.join('..', 'software', 'python'))
sys.path.append(lib_path)
# then load module
import bzboard

# link to config file
SETUP_CONFIG_FILE = './bz_setup_config_test.json'
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
pattern = bz.pattern_from_file(PATTERN_FILE)
bz.activate_pattern(pattern)
