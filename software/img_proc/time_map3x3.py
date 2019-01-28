###############################################################################
#
# This script aims to create a time map of the BZ reaction, like the one that
# can be seen in many BZ papers.
# The idea is to take a column of pixels every frame (always the same one)
# and display an image with these columns adjacent to one another.
#
###############################################################################



import cv2
import numpy as np
import sys



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
        stepw = int(width / 3)
        steph = int(height / 3)

        for i in range(1, 3):
            cv2.line(frame, (x1+stepw*i,y1),  (x1+stepw*i,y2), (0,0,255), 3)
            cv2.line(frame, (x1,y1+steph*i),  (x2,y1+steph*i), (0,0,255), 3)


    def get_platform_corners(self, frame, name=""):
        '''Given a frame, it will let the user click on the platform corners
        in order to obtain its coordinates: 
        top left corner, bottom right corner'''

        cv2.namedWindow('Choose grid '+name)
        cv2.setMouseCallback('Choose grid '+name, self.grid_callback)
        unmodified = frame.copy()

        # grid_callback sets finished to True once the user selects both corners
        while(self.finished is False):
            frame = unmodified.copy()
            self.draw_grid(frame)
            cv2.imshow('Choose grid '+name, frame)
            cv2.waitKey(10)

        cv2.destroyWindow('Choose grid '+name)



def add_column(frame, timemap, bz_coord, xcol):

    x1, y1, x2, y2 = bz_coord
    step_w = int( (x2 - x1) / 3 )
    step_h = int( (y2 - y1) / 3 )
    height = y2 - y1
    width = x2 - x1

    for i in range(3):
        pad = 0
        if i == 0:
            pad = 50
        if i == 1:
            pad = 50
        if i == 2:
            pad = 90
        col = frame[y1:y2, x1+25-(i*0)+pad + step_w*i]
        timemap[i*height:i*height+height, xcol] = col
        #row = frame[y1+20-(i*2) + step_h*i, x1:x2]
        #timemap[i*width:i*width+width, xcol] = row



if __name__ == "__main__":

    video = cv2.VideoCapture(sys.argv[1])
    click_grid = GridClickData()
    frame_counter = 0
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    #total_frames = int(total_frames/30)+1
    timemap = np.zeros((600, total_frames, 3), np.uint8)
    speed = 1

    start_frame = 0 # 0 from beggining, 1800 half,...
    video.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
     
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
            timemap = np.resize(timemap, ( (y2-y1)*3, total_frames-start_frame, 3) )
        
        add_column(frame, timemap, click_grid.points, frame_counter)

        #cv2.imshow('Time map', timemap)
        #key = cv2.waitKey(1) & 0xFF
        frame_counter += 1


    outname = sys.argv[1].split(".")[0] + ".png"
    cv2.imwrite(outname, timemap)
    video.release()

