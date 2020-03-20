# calculates the periodicity of the oscillations in each cell 

import sys
import csv
import numpy as np

outname = 'test.csv'

csv_data = np.genfromtxt(sys.argv[1], delimiter=',')
cells = csv_data.shape[0]
databins = [] # np.empty([25,100]) 

for cell in csv_data:
    # first we calculate distance between oscillations
    cell = np.diff(cell) # see doc for diff, similar to 1st derivative
    cell[np.where(cell == -1)] = 0 # replaces -1s with 0s
    periods = np.diff(np.where(cell == 1))[0] # finds pos of 1s
    periods = periods[periods>20] # small periods are caused by ringing
    
    # now we convert from frames to seconds
    # this videos have 2400 frames and thats 30m (or 1800s)
    # thus a frame is 0.75s
    periods = periods*0.75
   
    # now we prepare to save the data into a csv
    length = periods.shape[0]
    periods = np.pad(periods, (0,100-length), 'constant', constant_values=0)
    databins.append(periods)

np.savetxt(outname, databins, '%d', delimiter=',')

