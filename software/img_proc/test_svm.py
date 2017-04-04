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
from sklearn.decomposition import PCA
from sklearn.externals import joblib



class TestSVM():
    '''This class is just the framework to test the SVM
    You must instantiate one of the other classes instead'''


    def __init__(self, svm_file):

        self.svm = cv2.ml.SVM_load(svm_file)


    def paint_cells(self, frame, bz_coordinates):
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

                if self.roi_to_decision(roi) == 0:
                    # if predicted as 0, paint it blue, otherwise red
                    cv2.rectangle(frame, pointA, pointB, (255,0,0), -1) 
                else:
                    cv2.rectangle(frame, pointA, pointB, (0,0,255), -1) 


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



if __name__ == "__main__":

    # svm = BlueChannel('svm_bluechannel.dat')
    # svm = RedBlueChannel('svm_rbchannel.dat')
    svm = PCATransform('svm_pca.dat', 'pca.dat')

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
        svm.paint_cells(frame, click_grid.points)

        cv2.imshow('Video', frame)
        out.write(frame)
        key = cv2.waitKey(33) & 0xFF # 33 means roughly 30FPS 

        if key == ord('p'):
            play = not play


    video.release()
    out.release()
    cv2.destroyAllWindows()

