# activate each motor for 0.5 seconds each
for m in bz.motors:
    bz.activate(m)
    time.sleep(0.5)
    bz.deactivate(m)