from ..software.bz-ca import bzboard

import time

SETUP_CONFIG_FILE = './bz_setup_config_test.json'

bz = bzboard.BZBoard.from_configfile(SETUP_CONFIG_FILE)

for m in bz.motors:
    bz.activate(m)
    time.sleep(0.5)
    bz.deactivate(m)
    
