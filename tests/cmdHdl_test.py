from commanduino.commandhandler import SerialCommandHandler

PORT = 'COM6'

def defaultPrint(cmd):
    print cmd

cmdHdl = SerialCommandHandler(PORT)
cmdHdl.add_default_handler(defaultPrint)
cmdHdl.start()

quit = False
while not quit:
    msg = raw_input()
    if msg == "QUIT":
        isRunning = False
        quit = True
    else:
        cmdHdl.write(msg)

cmdHdl.stop()
cmdHdl.join()
