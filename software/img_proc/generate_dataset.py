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
import subprocess


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


    def draw_save_cells(self, frame, bz_coordinates, window_c):
        ''' colours and saves the bz cells where the user has clicked. '''

        x1, y1, x2, y2 = bz_coordinates
        height = y2 - y1
        width = x2 - x1
        stepw = int(width / 5)
        steph = int(height / 5)
        color = window_c.astype("int32")

        for click in self.clicks:
            # relative click coordinates to the origin of the bz grid (x1, y1)
            rx, ry = click[0] - x1, click[1] - y1
            # dividing this by step size and rounding we can guess the cell
            icell, jcell = int(rx/stepw), int(ry/steph)
            # now we can just draw the cell and also save it into a file
            pointA = (x1+9 + stepw * icell, y1+9 + steph * jcell)
            pointB = (x1-9 + stepw * (icell+1), y1-9 + steph * (jcell+1))

            if click[2] == 0: # left click

                if click[3] == 0: # not saved it yet
                    # define Region Of Interest around the cell we want
                    roi = frame[pointA[1]:pointB[1], pointA[0]:pointB[0]]
                    new_image = 'blues/'+self.random_filename(5, color)
                    cv2.imwrite(new_image, roi) # save cell
                    click[3] = 1 # we mark it as saved

                #draw rectangle just for visualization    
                cv2.rectangle(frame, pointA, pointB, (255,0,0), -1) 

            else: # right click, see comments just above for following lines

                if click[3] == 0:
                    roi = frame[pointA[1]:pointB[1], pointA[0]:pointB[0]]
                    new_image = 'reds/'+self.random_filename(5, color)
                    cv2.imwrite(new_image, roi)
                    click[3] = 1

                cv2.rectangle(frame, pointA, pointB, (0,0,255), -1) 


    def random_filename(self, size, color):
        ''' to create random names for the dataset pictures '''

        w = ''.join(random.choice(string.ascii_lowercase) for i in range(size))
        w += "_"+str(color[0]) +'_' +str(color[2])
        return w+'.png'



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


    def grid_callback(self, event, x, y, flags, param):
        '''mouse callback function. See OpenCV documentation example'''

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


    def draw_grid(self, frame):
        '''draws a 5x5 grid, just the lines. Used for visualization'''

        x1, y1, x2, y2 = self.points
        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 3)
        height = y2 - y1
        width = x2 - x1
        stepw = int(width / 5)
        steph = int(height / 5)

        for i in range(1, 5):
            cv2.line(frame, (x1+stepw*i,y1),  (x1+stepw*i,y2), (0,0,255), 3)
            cv2.line(frame, (x1,y1+steph*i),  (x2,y1+steph*i), (0,0,255), 3)


    def get_platform_corners(self, frame):
        '''Given a frame, it will let the user click on the platform corners
        in order to obtain its coordinates: 
        top left corner, bottom right corner'''

        cv2.namedWindow('Choose grid')
        cv2.setMouseCallback('Choose grid', self.grid_callback)
        unmodified = frame.copy()

        # grid_callback sets finished to True once the user selects both corners
        while(self.finished is False):
            frame = unmodified.copy()
            self.draw_grid(frame)
            cv2.imshow('Choose grid', frame)
            cv2.waitKey(10)

        cv2.destroyAllWindows()



def bz_average_color(frame, bz_coordinates):
    ''' Given a frame, it gets the bz board, and returns in average color'''

    x1, y1, x2, y2 = bz_coordinates
    height = y2 - y1
    width = x2 - x1
    stepw = int(width / 5)
    steph = int(height / 5)
    cell_colors = []

    for cell in range(25):
        icell = int(cell / 5)
        jcell = cell % 5
        # calculate cell coordinates
        pointA = (x1+9 + stepw * icell, y1+9 + steph * jcell)
        pointB = (x1-9 + stepw * (icell+1), y1-9 + steph * (jcell+1))


        # define Region Of Interest around the cell we want
        roi = frame[pointA[1]:pointB[1], pointA[0]:pointB[0]]
        # calculate its average color
        avg_color_per_row = np.average(roi, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        cell_colors.append(avg_color)

    return np.average(cell_colors, axis=0)



def bz_avg_moving_color(colors, n=100):
    ''' returns the average hue  of the last n frames'''

    frames = min(n, len(colors))
    window = colors[-frames:]
    return np.average(window, axis=0)


if __name__ == "__main__":


    video = cv2.VideoCapture(sys.argv[1])
    click_grid = GridClickData()    
    play = True # True means play, False means pause
    frame_counter = 0
    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    frame_color = [] # keeps the average color per frame

    while(True):

        if play is True:
            ret, frame = video.read()
            click_cell = CellClickData()
            frame_counter += 1
            sys.stdout.write("\r{0} in {1}".format(frame_counter, total_frames))
            sys.stdout.flush()

        if ret is False:
            break

        # first thing we ask the user to define the 5x5 grid
        if click_grid.finished is False:
            click_grid.get_platform_corners(frame)

        if play is True:
            # calculate the average color of this frame
            avg_c = bz_average_color(frame, click_grid.points) 
            # save it
            frame_color.append(avg_c)
            # calculate the average color of the last n frames
            window_c = bz_avg_moving_color(frame_color, 3000).astype('float32')

        # "click_grid" is now populated with the x,y corners of the platform
        click_grid.draw_grid(frame)
       
        # now while the video plays the user can click to save cells as dataset
        cv2.namedWindow('Left blue, Right red')
        cv2.setMouseCallback('Left blue, Right red', click_cell.mouse_cell)
        click_cell.draw_save_cells(frame, click_grid.points, window_c)
        
        cv2.imshow('Left blue, Right red', frame)
        key = cv2.waitKey(33) & 0xFF # 33 means roughly 30FPS 

        if key == ord('p'):
            play = not play


    video.release()
    cv2.destroyAllWindows()

