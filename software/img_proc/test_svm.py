###############################################################################
#
# This file takes a video (or a stream) and depending on the trained SVM
# decides if its cells are blue or red (based on the colors shown by the
# bz reaction)
#
###############################################################################



import cv2
import numpy as np
import sys, glob, os, multiprocessing
from generate_dataset import GridClickData
from generate_dataset import bz_average_color
from train_svm import equalise_img
from sklearn.externals import joblib
from sklearn.decomposition import PCA
from collections import deque
from time import sleep


class TestSVM():
    '''This class is just the framework to test the SVM
    You must instantiate one of the other classes instead'''


    def __init__(self, svm_file):

        self.svm = cv2.ml.SVM_load(svm_file)


    def paint_cells(self, frame, bz_coordinates, b_color):
        ''' Given a frame and the bz coordinates, it extracts the cells 
        and uses the SVM to predict if it will be a blue or red cell'''

        # top right and bottom right corner of the bz platform
        x1, y1, x2, y2 = bz_coordinates
        height = y2 - y1
        width = x2 - x1
        stepw = int(width / 5)
        steph = int(height / 5)
        blues = [] # list of the blue cells in this frame

        for i in range(5):
            for j in range(5):
                # top left corner of the current cell (i,j)
                pointA = (x1+9 + stepw * i, y1+9 + steph * j)
                # bottom right corner of the current cell (i,j)
                pointB = (x1-9 + stepw * (i+1), y1-9 + steph * (j+1))
                # Define the Region of Interest as the current cell (i, j)
                roi = frame[pointA[1]:pointB[1], pointA[0]:pointB[0]]
                roi = equalise_img(roi)

                if self.roi_to_decision(roi, b_color) == 0:
                    # if predicted as 0, paint it blue, otherwise red
                    cv2.rectangle(frame, pointA, pointB, (255,0,0), -1) 
                    blues.append((i,j)) # add cell to the blue cells list 

                else:
                    cv2.rectangle(frame, pointA, pointB, (0,0,255), -1) 
        
        return blues


    def roi_to_decision(self, roi):
        ''' This is the function that every specific class must provide.
        Given a region of interest (or roi) it will use the SVM to decide
        if it is red or blue'''

        raise NameError('Use a specific class instead')



class BlueChannel(TestSVM):
    '''This class must be used when BlueChannel was used to train the SVM.
    In this case, the SVM is trained and tested only using the blue channel
    of the image, and reducing it to 25 by 25 pixels'''


    def __init__(self, svm_file):
        super().__init__(svm_file)


    def roi_to_decision(self, roi):
        
        # We will only focus on the blue channel
        roi_blue = roi[:,:,0]
        # Resize it to 25,25 as used while training
        roi_resized = cv2.resize(roi_blue, (25,25))
        # And flatten it into a 1D array as require by the SVM
        roi1D = roi_resized.reshape(-1)
        # And use the svm to decide if it is red or blue
        decision = self.svm.predict(np.array([roi1D], dtype=np.float32))

        return int(decision[1][0][0]) 



class RedBlueChannel(TestSVM):
    ''' Very similar to BlueChannel, but use both red and blue, and use 
    15 by 15 images for each channel, instead of 25 by 25
    Only use with a dataset created with the class with the same name
    from train_svm.py'''


    def __init__(self, svm_file):
        super().__init__(svm_file)


    def roi_to_decision(self, roi):
        
        # we resize the roi into 10 by 10
        resized = np.array( cv2.resize(roi, (15,15)), dtype=np.float32 )
        # take the red and blue channels
        rbc =  np.concatenate( (resized[:,:,0], resized[:,:,2]) )  
        # And flatten it into a 1D array as require by the SVM
        roi1D = rbc.reshape(-1)
        # And use the svm to decide if it is red or blue
        decision = self.svm.predict(np.array([roi1D], dtype=np.float32))

        return int(decision[1][0][0]) 



class PCATransform(TestSVM):
    '''This class feeds the SVM with data which went through a PCA
    for dimensionality reduction. The dataset must be generated using the 
    class with the same name from train_svm.py'''


    def __init__(self, svm_file, pca_file):

        super().__init__(svm_file)
        self.pca = joblib.load(pca_file)


    def roi_to_decision(self, roi):

        # resize into 50,50
        resized = cv2.resize(roi, (50, 50))
        resized = np.asarray(resized, dtype=np.float32)
        # flatten it into 1D array
        roi1D = resized.reshape(1, -1)
        # reduce its dimensionality
        pca_out = self.pca.transform(roi1D)
        pca32 = pca_out.astype('float32')
        # And use the svm to decide if it is red or blue
        decision = self.svm.predict(np.array([pca32[0]], dtype=np.float32))

        return int(decision[1][0][0]) 



class HSVHistogram(TestSVM):
    '''Uses a 3D histogram of the HSV color map. This is what Gerardo was
    using. The dataset must be generated using the class with the same name
    from train_svm.py'''


    def __init__(self, svm_file):
        super().__init__(svm_file)


    def roi_to_decision(self, roi, b_color=None):

        roiHSV = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        # calculate histograms for H, S and V
        hist_ocv = cv2.calcHist([roiHSV], [0, 1, 2], None, [8, 8, 8], 
            [0, 256, 0, 256, 0, 256])
        # flatten to 1D
        hist1D = hist_ocv.flatten()
        # eq lighting, idea from HOG
        hist = hist1D / np.sqrt( np.sum( np.power(hist1D,2) ) )
        decision = self.svm.predict(np.array([hist], dtype=np.float32))

        return int(decision[1][0][0]) 



class HSVHistogramBkgMem(TestSVM):
    '''Uses a 3D histogram of the HSV color map. This is what Gerardo was
    using, plus using the average color of the last N frames. 
    The dataset must be generated using the class with the same name
    from train_svm.py'''


    def __init__(self, svm_file):
        super().__init__(svm_file)


    def roi_to_decision(self, roi, b_color):

        b,g,r = b_color
        br = [b/255., r/255.]
        roiHSV = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        # calculate histograms for H, S and V
        hist_ocv = cv2.calcHist([roiHSV], [0, 1, 2], None, [8, 8, 8], 
            [0, 256, 0, 256, 0, 256])
        # flatten to 1D
        hist1D = hist_ocv.flatten()
        # eq lighting, idea from HOG
        hist = hist1D / np.sqrt( np.sum( np.power(hist1D,2) ) )
        hist = np.append(hist, br)
        decision = self.svm.predict(np.array([hist], dtype=np.float32))

        return int(decision[1][0][0]) 


def SVMsinglevideo(path, processLimiter=multiprocessing.Lock()):

    with processLimiter:
        print("Processing video "+path)
        
        # svm = BlueChannel('svm_bluechannel.dat')
        # svm = RedBlueChannel('svm_rbchannel.dat')
        # svm = PCATransform('svm_pca.dat', 'pca.dat')
        # svm = HSVHistogram('hsvhist.dat')
        svm = HSVHistogramBkgMem('hsvhistmem.dat')

        video = cv2.VideoCapture(path)
        # print(video.get(cv2.CAP_PROP_FRAME_COUNT))
        click_grid = GridClickData()    
        play = True # True means play, False means pause

        bkg_window = 3000 # number of avg frame colors we will keep
        frame_color = deque(maxlen=bkg_window) # keeps the average color per frame

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        outname = path.split(".")[0] + "_svm.avi"
        out = cv2.VideoWriter(outname, fourcc, 20.0, (800,600))
        counter = 0

        while(True):

            if play is True:
                ret, frame = video.read()

            if ret is False:
                break

            counter = counter + 1

            # first thing we ask the user to define the 5x5 grid
            if click_grid.finished is False:
                click_grid.get_platform_corners(frame, path)

            # calculate the average color of this frame
            avg_c = bz_average_color(frame, click_grid.points) 
            #avg_c = bz_average_color(frame, [205,80,656,533]) 
            # save it
            frame_color.append(avg_c)
            # calculate the average color of the last n frames
            window_c = np.average(frame_color, axis=0).astype('float32')

            # "click_grid" is now populated with the x,y corners of the platform
            click_grid.draw_grid(frame)
            # we use the svm to decide if the cells are painted red or blue
            svm.paint_cells(frame, click_grid.points, window_c)

            #cv2.imshow('Video', frame)
            out.write(frame)
            #key = cv2.waitKey(33) & 0xFF # 33 means roughly 30FPS 

            # if key == ord('p'):
            #    play = not play


        video.release()
        out.release()
        cv2.destroyAllWindows()
        # print(counter)


def SVMfolder(pathtofolder):
    ''' This function will execute the previous single svm video function
    in all the files of a folder.
    NOT WORKING WITH MULTITHREADING, I am keeping it simple.
    Multithreading was giving some errors with the Xs GTK and Deque'''

    s = multiprocessing.Semaphore(4)
    # we only want to process the videos with fast5 in the name
    allvideos = glob.glob(pathtofolder+'*_fast15.avi')
    for video in allvideos:
        p = multiprocessing.Process(target=SVMsinglevideo, args=(video,s))
        p.start()
        #cpSVMsinglevideo(video)


if __name__ == "__main__":
    
    #SVMsinglevideo(sys.argv[1])
    SVMfolder(sys.argv[1])


