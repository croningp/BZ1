# splits a CSV in smaller CSVs. The splitting is made by column

import sys
import csv
from numpy import genfromtxt
from numpy import savetxt

SPLIT_PARTS = 2

csv_to_split = sys.argv[1]
csv_data = genfromtxt(csv_to_split, delimiter=',')
data_length = csv_data.shape[1]

parts_length = int(data_length/SPLIT_PARTS)


for i in range(SPLIT_PARTS):
    part = csv_data[ :, i*parts_length:(i+1)*parts_length ]
    savetxt('part'+str(i)+'.csv', part, '%d', delimiter=',')

