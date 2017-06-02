###############################################################################
#
# This script aims to create a time map of the BZ reaction, like the one that
# can be seen in many BZ papers.
# The idea is to take a column of pixels every frame (always the same one)
# and display an image with these columns adjacent to one another.
#
###############################################################################


import cv2
from generate_dataset import GridClickData
import numpy as np
import sys


def add_column(frame, timemap, bz_coord, xcol):

    x1, y1, x2, y2 = bz_coord
    step_w = int( (x2 - x1) / 5 )
    height = y2 - y1

    for i in range(5):
        col = frame[y1:y2, x1+25-(i*2) + step_w*i]
        timemap[i*height:i*height+height, xcol] = col


if __name__ == "__main__":

    video = cv2.VideoCapture(sys.argv[1])
    click_grid = GridClickData()
    frame_counter = 0
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    timemap = np.zeros((600, total_frames, 3), np.uint8)
    speed = 1

    while(True):

        ret, frame = video.read()

        if frame_counter % speed is not 0:
            continue

        if ret is False:
            break

        # first thing we ask the user to define the 5x5 grid
        if click_grid.finished is False:
            # click_grid is now populated with the x,y corners of the platform
            click_grid.get_platform_corners(frame)
            x1, y1, x2, y2 = click_grid.points
            timemap = np.resize(timemap, ( (y2-y1)*5, total_frames, 3) )
        
        add_column(frame, timemap, click_grid.points, frame_counter)
        

        #cv2.imshow('Time map', timemap)
        #key = cv2.waitKey(1) & 0xFF
        frame_counter += 1


    cv2.imwrite("test.jpg", timemap)
    video.release()

