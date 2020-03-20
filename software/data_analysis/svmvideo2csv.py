###############################################################################
#
# This file takes a video which has been already processed by the SVM to decide
# if the cells are blue or red (so the video has been binarized) and created
# a svm which is a matrix of 25 by N, where each position is 0 for red or 1 for
# for blue
#
################################################################################



import cv2
import csv, sys, glob
import multiprocessing
import numpy as np
from generate_dataset import GridClickData



def addframe2data(frame, databins, bz_coord, col):

    x1, y1, x2, y2 = bz_coord
    stepw = int( (x2 - x1) / 5 )
    steph = int( (y2 - y1) / 5 )
    height = y2 - y1
    width = x2 - x1

    for i in range(5):
        for j in range(5):

            # top left corner of the current cell (i,j)
            pointA = (x1+9 + stepw * i, y1+9 + steph * j)
            # bottom right corner of the current cell (i,j)
            pointB = (x1-9 + stepw * (i+1), y1-9 + steph * (j+1))
            # Define the Region of Interest as the current cell (i, j)
            roi = frame[ pointA[1]:pointB[1], pointA[0]:pointB[0] ]
            # taking pixel in middle of frame, only blue channel
            color = roi[int(stepw/2), int(steph/2)][0]

            if color > 100:
                databins[i*5+j, col] = 1
            else:
                databins[i*5+j, col] = 0


def generate_singlevideo_csv(path, processLimiter=multiprocessing.Lock()):

    with processLimiter:
        print("Processing video "+path)

        video = cv2.VideoCapture(path) # read video file from term 1st arg
        click_grid = GridClickData() # to store the 5x5 grid coordinates
        frame_skip = 1 # 1 plays every frame, 2 takes one out, 3 takes 2 out,...
        start_frame = 0 # 0 from beggining, 1800 half,...
        video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
        frame_counter = 0
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        
        databins = np.zeros((25, total_frames), np.uint8) 

        while(True):

            for _ in range(frame_skip):
                ret, frame = video.read()

            if ret is False:
                break

            # first thing we ask the user to define the 5x5 grid
            #if click_grid.finished is False:
            #    click_grid.get_platform_corners(frame, path)

            #addframe2data(frame, databins, click_grid.points, frame_counter) 
            addframe2data(frame, databins, [205,80,656,533], frame_counter) 
            frame_counter += 1


        outname = path.split(".")[0] + ".csv"
        np.savetxt(outname, databins, '%d', delimiter=',')
        video.release()
        cv2.destroyAllWindows()


def CSVfolder(pathtofolder):
    ''' This function will execute the previous single csv video function
    in all the files of a folder.
    NOT WORKING WITH MULTITHREADING, I am keeping it simple.
    Multithreading was giving some errors with the Xs GTK and Deque'''

    s = multiprocessing.Semaphore(14)
    # we only want to process the videos with fast5 in the name
    allvideos = glob.glob(pathtofolder+'*_svm.avi')
    
    for video in allvideos:
        p = multiprocessing.Process(target=generate_singlevideo_csv, args=(video,s))
        p.start()

if __name__ == '__main__':

    CSVfolder(sys.argv[1])
    #generate_singlevideo_csv(sys.argv[1])
