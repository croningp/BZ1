import cv2
import sys, time
sys.path.insert(0, 'img_proc')
from collections import deque

import test_svm
from bzboard.bzboard import BZBoard
from generate_dataset import bz_average_color


def activate_motors(motors, board, matrix):
    '''activates the motors from the list given'''

    code = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E'}

    for m in motors:
        i, j = m[0], m[1]
        motor = code[i] + str(5-j)
        if matrix[motor] == 0:
            matrix[motor] = 1
            board.activate_motor(motor)


# this matrix stores if the motors are enabled (1) or disabled (0)
# before writting to serial we check this to not sent writes not needed
matrix = { 
    "A1":0,"A2":0,"A3":0,"A4":0,"A5":0,
    "B1":0,"B2":0,"B3":0,"B4":0,"B5":0,
    "C1":0,"C2":0,"C3":0,"C4":0,"C5":0,
    "D1":0,"D2":0,"D3":0,"D4":0,"D5":0,
    "E1":0,"E2":0,"E3":0,"E4":0,"E5":0
    }

board = BZBoard('/dev/ttyACM0')
svm = test_svm.HSVHistogramBkgMem('img_proc/hsvhistmem.dat')

vc = cv2.VideoCapture(0)
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
raw = cv2.VideoWriter('raw.avi',fourcc, 30.0, (800,600))
out = cv2.VideoWriter('svm.avi',fourcc, 30.0, (800,600))

click_grid = test_svm.GridClickData()    
# number of frame avg background we will keep
bkg_window = 3000
# where we keep the avg background colour
frame_color = deque(maxlen=bkg_window)
start = False
state0 = False


while(True):

    ret,frame = vc.read()

    if ret is False:
        break

    raw.write(frame)
    cv2.imshow("raw", frame)
    
    # first thing we ask the user to define the 5x5 grid
    if click_grid.finished is False:
        click_grid.get_platform_corners(frame)
        
    if start is True and state0 is False:
        board.activate_motor("A4")
        board.activate_motor("A5")
        board.activate_motor("E1")
        board.activate_motor("D1")
        board.activate_motor("B5")
        board.activate_motor("E2")
        state0 = True

    if start is True and state0 is True:
        activate_motors(blue_cells, board, matrix)

    # calculate the average color of this frame
    avg_c = bz_average_color(frame, click_grid.points) 
    # save it
    frame_color.append(avg_c)
    # calculate the average color of the last n frames
    window_c = np.average(frame_color, axis=0).astype('float32')

    # "click_grid" is now populated with the x,y corners of the platform
    click_grid.draw_grid(frame)
    # we use the svm to decide if the cells are painted red or blue
    blue_cells = svm.paint_cells(frame, click_grid.points, window_c)
    cv2.imshow('SVM', frame)
    out.write(frame)
    key = cv2.waitKey(1) & 0xFF 

    if key == ord('q'):
        break

    if key == ord('s'):
        start = True


vc.release()
out.release()
raw.release()
cv2.destroyAllWindows()
