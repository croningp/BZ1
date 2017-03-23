###############################################################################
#
# Mouse callback based on: 
# http://docs.opencv.org/3.1.0/db/d5b/tutorial_py_mouse_handling.html
# I dont like using globals but they were using them in this example...
#
###############################################################################

import numpy as np
import cv2


drawing = False # true if mouse is pressed
ix,iy = -1,-1
video = cv2.VideoCapture('test.avi')
points = [0, 0, 0, 0]

def mouse_grid(event, x, y, flags, param):
    '''mouse callback function'''
    
    global ix, iy, drawing, points

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        points = [x, y, x, y]
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            points = [ix, iy, x, y]

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        points = [ix, iy, x, y]


def draw_grid(frame, points):
    '''draws a 5x5 grid, just the lines. Used for visualization'''

    x1, y1, x2, y2 = points
    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 3)
    height = y2 - y1
    width = x2 - x1
    stepw = int(width / 5)
    steph = int(height / 5)

    for i in range(1, 5):
        cv2.line(frame, (x1+stepw*i,y1),  (x1+stepw*i,y2), (0,0,255), 3)
        cv2.line(frame, (x1,y1+steph*i),  (x2,y1+steph*i), (0,0,255), 3)


def get_platform_corners(frame):
    '''Given a frame, it will let the user click on the platform corners
    in order to obtain its coordinates: top left corner, bottom right corner'''

    cv2.namedWindow('blue channel')
    cv2.setMouseCallback('blue channel', mouse_grid)
    unmodified = frame.copy()

    while(True):
        frame = unmodified.copy()
        draw_grid(frame, points)
        cv2.imshow('blue channel', frame)
        cv2.waitKey(10)

while(True):

    ret, frame = video.read()
    
    if ret is False:
        break
        
    get_platform_corners(frame)

    # we focus on the blue channel because the reaction changes from red to blue
    blue_channel = frame[:,:,0]

    cv2.imshow('blue channel', frame)
    cv2.waitKey(10) # 33 means roughly 30FPS 

video.release()
cv2.destroyAllWindows()

