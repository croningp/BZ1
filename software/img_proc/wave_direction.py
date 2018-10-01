################################################################################
#
# Inputs a BZ video, and tries to guess the direction of the BZ wave using
# the moments function from OpenCV
#
################################################################################


import cv2
import sys
import math
import numpy as np
from generate_dataset import GridClickData


def only_bz_liquid(frame, bz_coordinates):
    '''Given a frame, this function will return only the BZ working area.
    Thus it will ignore the plastic corners, and everything outside the platform
    in the frame, and only return the liquid.'''

    # top right and bottom right corner of the bz platform
    x1, y1, x2, y2 = bz_coordinates
    height = y2 - y1
    width = x2 - x1
    stepw = int(width / 5)
    steph = int(height / 5)
    liquid = np.zeros((height-18*5, width-18*5), np.uint8)

    for i in range(5):
        for j in range(5):
            # top left corner of the current cell (i,j)
            pointA = (x1+9 + stepw * i, y1+9 + steph * j)
            # bottom right corner of the current cell (i,j)
            pointB = (x1-9 + stepw * (i+1), y1-9 + steph * (j+1))
            # Define the Region of Interest as the current cell (i, j)
            roi = frame[pointA[1]:pointB[1], pointA[0]:pointB[0]]
            # add roi to the final liquid image
            xroi, yroi = roi.shape
            liquid[j*xroi:j*xroi+xroi, i*yroi:i*yroi+yroi] = roi 
    
    return liquid


if __name__ == '__main__':

    video = cv2.VideoCapture(sys.argv[1])
    click_grid = GridClickData()
    play = True # True means play, False means pause
    frame_skip = 1 # 1 plays every frame, 2 takes one out, 3 takes 2 out,...
    start_frame = 0 # 0 from beggining, 1800 half,...
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter("output.avi", fourcc, 30.0, (800,600))
    
    prevcX, prevcY = 0,0
    # angles = []
    cXs = []
    cYs = []

    while(True):

        if play is True:
            for _ in range(frame_skip):
                ret, frame = video.read()

        if ret is False:
            break

        # first thing we ask the user to define the 5x5 grid
        if click_grid.finished is False:
            click_grid.get_platform_corners(frame)

        # get only the liquid of the video, ignoring plastic parts
        liquid = only_bz_liquid(frame[:,:,0], click_grid.points)        
        # calculate the moments of the blue channel
        M = cv2.moments(liquid)
        # calculate center of moments
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # calculate angle respect to previous frame moment
        # angle = math.degrees(math.atan2(cX-prevcX, cY-prevcY))
        # angles.append(angle)
        cXs.append(cX)
        cYs.append(cY)
        prevcX, prevcY = cX, cY

        cv2.circle(frame, (int(cX*2.2), int(cY*1.75)), 7, (1, 1, 255), -1)
        out.write(frame)
        cv2.imshow('Blue liquid', frame)
        key = cv2.waitKey(1) & 0xFF # 33 means roughly 30 FPS

        if key == ord('p'):
            play = not play

        if key == ord('q'):
            break

    # print(angles)
    print(cXs)
    print(cYs)

    # video.release()
    # cv2.destroyAllWindows()

