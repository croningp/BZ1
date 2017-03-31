###############################################################################
#
# This file takes a video (or a stream) and depending on the trained SVM
# decides if its cells are blue or red (based on the colors shown by the
# bz reaction)
#
###############################################################################



import cv2
import numpy as np
import sys
from generate_dataset import GridClickData



def paint_cells(frame, bz_coordinates, svm):
    ''' Given a frame and the bz coordinates, it extracts the cells 
    and uses the SVM to predict if it will be a blue or red cell'''

    # top right and bottom right corner of the bz platform
    x1, y1, x2, y2 = bz_coordinates
    height = y2 - y1
    width = x2 - x1
    stepw = int(width / 5)
    steph = int(height / 5)

    for i in range(5):
        for j in range(5):
            # top left corner of the current cell (i,j)
            pointA = (x1+9 + stepw * i, y1+9 + steph * j)
            # bottom right corner of the current cell (i,j)
            pointB = (x1-9 + stepw * (i+1), y1-9 + steph * (j+1))
            # Define the Region of Interest as the current cell (i, j)
            roi = frame[pointA[1]:pointB[1], pointA[0]:pointB[0]]
            # We will only focus on the blue channel
            roi_blue = roi[:,:,0]
            # Resize it to 25,25 as used while training
            roi_resized = cv2.resize(roi_blue, (25,25))
            # And flatten it into a 1D array as require by the SVM
            roi1D = roi_resized.reshape(-1)
            result = svm.predict(np.array([roi1D], dtype=np.float32))

            if int(result[1][0][0]) == 0:
                # if predicted as 0, paint it blue, otherwise red
                cv2.rectangle(frame, pointA, pointB, (255,0,0), -1) 
            else:
                cv2.rectangle(frame, pointA, pointB, (0,0,255), -1) 



if __name__ == "__main__":

    svm = cv2.ml.SVM_load("svm_data.dat")

    video = cv2.VideoCapture(sys.argv[1])
    click_grid = GridClickData()    
    play = True # True means play, False means pause

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi',fourcc, 30.0, (960,540))

    while(True):

        if play is True:
            ret, frame = video.read()

        if ret is False:
            break

        # first thing we ask the user to define the 5x5 grid
        if click_grid.finished is False:
            click_grid.get_platform_corners(frame)

        # "click_grid" is now populated with the x,y corners of the platform
        click_grid.draw_grid(frame)
        # we use the svm to decide if the cells are painted red or blue
        paint_cells(frame, click_grid.points, svm)

        cv2.imshow('Video', frame)
        out.write(frame)
        key = cv2.waitKey(33) & 0xFF # 33 means roughly 30FPS 

        if key == ord('p'):
            play = not play


    video.release()
    out.release()
    cv2.destroyAllWindows()

