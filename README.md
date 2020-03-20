# BZ-CA

Platform to physically embody cellular-automaton using Belousov-Zhabotinsky
reaction-diffusion chemistry in addressably stirred cells.

## Aims of project
* Create working platform of addressable magnetic stirrers
* Use platform to demonstrate control over cell oscillations
* Control patterns of oscillating cell arrays using machine learning


## Platform
BZ-CA has a working stirrer array. It is also connected to a series of pump to add/remove liquid.

How to build the platform is explained with detail on the manuscript [pre-print](https://chemrxiv.org/articles/A_programmable_chemical_computer_with_memory_and_pattern_recognition/7712564).  

![stackable_platform](docs/stackable_platform.png)

This document explains how to build the first iteration of the platform, which is what was used to obtain the results obtained there.
It used custom-made electronics.
The current iteration uses the same hardware and 3D-printed parts, but the electronics are controlled using stacked [Adafruit Motor shields](https://learn.adafruit.com/adafruit-motor-shield-v2-for-arduino).

## Software

The software to control this platform is divided into different files:

* [bzboard.py](software/bzboard/bzboard.py) controls the motors that actuate the stirrers.
* [pumpsctl.py](software/pumpsctl/pumpsctl.py) controls the pumps to add and remove liquid from the platform.
* [firmware](software/firmware/) controls the Arduino scripts to control the 2 arduinos that were actuating the stirrers and the pumps.
* [image processing](software/img_proc) is the implementation of the SVM to classify the oscillations between red and blue.

## Example Code
An example of how to use the bzboard.py code is provided below
and in [initBZ.py](software/initBZ.py):


```python

################################################################
# This script should be used before starting the experiments
# to make sure everything is working and tubes are filled
################################################################

import time

from pumpsctl.pumpsctl import PumpsCtl
from bzboard.bzboard import BZBoard
from img_proc.record_cam import RecordVideo
import os, sys
sys.path.append(os.path.abspath('..'))
from tools.volctl import VolCtl 


v = VolCtl()
b = BZBoard("/dev/ttyACM1")
p = PumpsCtl('/dev/ttyACM0', v)

rv = RecordVideo(10)

waste = {'pump':'P0', 'quantity':75, 'speedIn':50, 'speedOut':50}
water = {'pump':'P4', 'quantity':5, 'speedIn':60, 'speedOut':70}
h2so4 = {'pump':'P2', 'quantity':5, 'speedIn':60, 'speedOut':70}
kbro3 = {'pump':'P5', 'quantity':5, 'speedIn':110, 'speedOut':110}
malonic = {'pump':'P3', 'quantity':5, 'speedIn':60, 'speedOut':70}
water_clean = {'pump':'P4', 'quantity':50, 'speedIn':50, 'speedOut':70}
ferroin = {'pump':'P1', 'quantity':2, 'speedIn':50, 'speedOut':50}



# make sure these 4 pumps are filled, I will test ferroin individually 
p.pump_multiple(water, malonic, kbro3, h2so4,ferroin)
# activate all max speed for 30 second to mix
b.activate_all()
time.sleep(30)
b.disable_all()

rv.record_threaded("test")
time.sleep(10)

p.pump_multiple(water_clean, waste)
p.pump_multiple(waste)
```
