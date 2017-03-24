###############################################################################
#
# The objective of this script is to generate a dataset for the bz platform.
# What we want is to train an SVM (or any other ML method), in order to detect
# when a cell changes color from red to blue.
# Thus, we want to generate a big database of examples of red and blue cells.
#
# The user starts by marking where the grid is: top left and bottom right points
# This code assumes that the bz platform grid is 5 by 5.
# In the future we might add a variable to control this, but at the moment
# the 5 by 5 is hardcoded.
# Once the video starts playing, the user can click "p" to pause or play it.
# Once the video is paused and it shows a frame, the user can left or right
# click in order to mark the cells as red or blue.
# Once a cell is clicked, an image of that cell is saved into a folder
# These folders are named red of blue.
#
# Mouse callback based on: 
# http://docs.opencv.org/3.1.0/db/d5b/tutorial_py_mouse_handling.html
#
###############################################################################


import numpy as np
import cv2
import random, string, sys


class CellClickData:
    '''This class represents the data that is passed from and to
    the cell mouse callback in order to recognize clicks by the user in 
    order to select a cell and save it as red or blue for the database.'''

    def __init__(self):
        # returns a empty clicks array where we will store the user clicks
        # Each position of the array contains a 4 size array, which 4 elements
        # are: x, y, left or right click, saved or not
        self.clicks = np.delete(np.empty([1,4]), 0, axis=0)

    def mouse_cell(self, event, x, y, flags, param):
        '''mouse callback function
        when adding new clicks, 0 will mean left click, and 1 right click'''

        if event == cv2.EVENT_LBUTTONDOWN:
            self.clicks = np.append(self.clicks, [[x,y,0,0]], axis=0)

        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clicks = np.append(self.clicks, [[x,y,1,0]], axis=0)


class GridClickData:
    '''This class represents the data that is passed from and to
    the mouse callback, in order to recognize clicks by the user
    The objective of this class is for the user to mark the corners
    of the grid, so we know its start x,y, width and height.'''

    def __init__(self):
        self.drawing = False # True if mouse is pressed
        self.ix, self.iy = -1, -1 # first click, or top left corner
        self.points = [0, 0, 0, 0] # Platform coordinates
        self.finished = False # True when user releases click


    def mouse_grid(self, event, x, y, flags, param):
        '''mouse callback function'''

        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.points = [x, y, x, y]
            self.ix, self.iy = x,y

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing == True:
                self.points = [self.ix, self.iy, x, y]

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            self.points = [self.ix, self.iy, x, y]
            self.finished = True



def random_filename(length):
    ''' to create random names for the dataset pictures '''

    word = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    return word+'.png'


def draw_save_cells(frame, bz_coordinates, clicks):
    ''' colours and saves the bz cells where the user has clicked. '''

    x1, y1, x2, y2 = bz_coordinates
    height = y2 - y1
    width = x2 - x1
    stepw = int(width / 5)
    steph = int(height / 5)

    for click in clicks:
        # relative click coordinates respect the origin of the bz grid (x1, y1)
        rx, ry = click[0] - x1, click[1] - y1
        # dividing this by step size and rounding we can guess the cell
        icell, jcell = int(rx/stepw), int(ry/steph)
        # now we can just draw the cell and also save it into a file
        pointA = (x1 + stepw * icell, y1 + steph * jcell)
        pointB = (x1 + stepw * (icell+1), y1 + steph * (jcell+1))

        if click[2] == 0: # left click

            if click[3] == 0: # not saved it yet
                roi = frame[pointA[1]:pointB[1], pointA[0]:pointB[0]]
                cv2.imwrite('blues/'+random_filename(8), roi) # save cell
                click[3] = 1 # we mark it as saved

            #draw rectangle just for visualization    
            cv2.rectangle(frame, pointA, pointB, (255,0,0), -1) 

        else: # right click, see comments just above for following lines

            if click[3] == 0:
                roi = frame[pointA[1]:pointB[1], pointA[0]:pointB[0]]
                cv2.imwrite('reds/'+random_filename(8), roi)
                click[3] = 1

            cv2.rectangle(frame, pointA, pointB, (0,0,255), -1) 

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


def get_platform_corners(frame, click_data):
    '''Given a frame, it will let the user click on the platform corners
    in order to obtain its coordinates: top left corner, bottom right corner'''

    cv2.namedWindow('Choose grid')
    cv2.setMouseCallback('Choose grid', click_data.mouse_grid)
    unmodified = frame.copy()

    while(click_data.finished is False):
        frame = unmodified.copy()
        draw_grid(frame, click_data.points)
        cv2.imshow('Choose grid', frame)
        cv2.waitKey(10)

    cv2.destroyAllWindows()



video = cv2.VideoCapture(sys.argv[1])
click_grid = GridClickData()    
play = True # True means play, False means pause

while(True):

    if play is True:
        ret, frame = video.read()
        click_cell = CellClickData()

    if ret is False:
        break

    # first thing we ask the user to define the 5x5 grid
    if click_grid.finished is False:
        get_platform_corners(frame, click_grid)

    # "click_grid" is now populated with the x,y corners of the platform
    draw_grid(frame, click_grid.points)
   
    # now while the video plays the user can click to save cells as dataset
    cv2.namedWindow('Left blue, Right red')
    cv2.setMouseCallback('Left blue, Right red', click_cell.mouse_cell)
    draw_save_cells(frame, click_grid.points, click_cell.clicks)
    
    cv2.imshow('Left blue, Right red', frame)
    key = cv2.waitKey(33) & 0xFF # 33 means roughly 30FPS 

    if key == ord('p'):
        play = not play


video.release()
cv2.destroyAllWindows()
