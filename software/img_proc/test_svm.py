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


def paint_cells(frame, bz_coordinates, svm):
    ''' Given a frame and the bz coordinates, it extracts the cells 
    and uses the SVM to predict if it will be a blue or red cell'''

    x1, y1, x2, y2 = bz_coordinates
    height = y2 - y1
    width = x2 - x1
    stepw = int(width / 5)
    steph = int(height / 5)

    for i in range(5):
        for j in range(5):
            
            pointA = (x1+9 + stepw * i, y1+9 + steph * j)
            pointB = (x1-9 + stepw * (i+1), y1-9 + steph * (j+1))
            roi = frame[pointA[1]:pointB[1], pointA[0]:pointB[0]]
            roi_blue = roi[:,:,0]
            roi_resized = cv2.resize(roi_blue, (25,25))
            roi1D = roi_resized.reshape(-1)
            result = svm.predict(np.array([roi1D], dtype=np.float32))

            if int(result[1][0][0]) == 0:
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
            get_platform_corners(frame, click_grid)

        # "click_grid" is now populated with the x,y corners of the platform
        draw_grid(frame, click_grid.points)
        paint_cells(frame, click_grid.points, svm)

        cv2.imshow('Video', frame)
        out.write(frame)
        key = cv2.waitKey(33) & 0xFF # 33 means roughly 30FPS 

        if key == ord('p'):
            play = not play


    video.release()
    out.release()
    cv2.destroyAllWindows()

