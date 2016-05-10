import os, sys  # add path of bzboard.py, relative to /bz_ca/test
lib_path = os.path.abspath(os.path.join('..', 'software', 'python'))
sys.path.append(lib_path)
import bzboard

import time

SETUP_CONFIG_FILE = './bz_setup_config_test.json'

bz = bzboard.BZBoard.from_configfile(SETUP_CONFIG_FILE)

for m in bz.motors:
    bz.activate(m)
    time.sleep(0.5)
    bz.deactivate(m)
