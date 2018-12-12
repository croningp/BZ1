import time
from bzboard.bzboard import BZBoard

b = BZBoard("/dev/ttyACM1")

#b.activate_motor('D3',900)
#for i in range(100):
b.activate_motor('C3',900)
	#time.sleep(1)
	#b.disable_motor('C3')
	#time.sleep(3)
	# b.activate_motor('D2',900)
	# time.sleep(5)
	# b.disable_motor('D2')
	# b.activate_motor('E3',900)
	# time.sleep(5)
	# b.disable_motor('E3')
	# b.activate_motor('D4',900)
	# time.sleep(5)
	# b.disable_motor('D4')


