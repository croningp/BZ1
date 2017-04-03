###############################################################################
#
# See: http://docs.opencv.org/trunk/dd/d3b/tutorial_py_svm_opencv.html
# for an example of how to use SVM and OpenCV
#
###############################################################################

import glob
import cv2
import numpy as np

# if we used generate_dataset.py  we should have a "reds" and "blues" folder 
# with the images we clicked for training. We load then only the blue channel
blues = [cv2.imread(file)[:,:,0] for file in glob.glob("blues/*.png")]  
reds = [cv2.imread(file)[:,:,0] for file in glob.glob("reds/*.png")] 
# we also convert them to 25 by 25, so all of them have the same size
blues = np.array([cv2.resize(img, (25,25)) for img in blues], dtype=np.float32)
reds = np.array([cv2.resize(img, (25,25)) for img in reds], dtype=np.float32)
# and we put everything together into a dataset
dataset = np.concatenate([blues,reds]) 
# and we make every image a flat 1D array
dataset = np.array([img.reshape(-1) for img in dataset])
# responses will be their "class", 0 for blues, and 1 for reds
responses = np.array([[0]] * len(blues) + [[1]] * len(reds), dtype=np.int32) 

# no we will divide dataset between train and set
# first we shuffle both dataset and responses
# we need to create because we want both shuffles to be identical
seed = np.random.randint(np.iinfo(np.int32).max)
np.random.seed(seed)
np.random.shuffle(dataset)
np.random.seed(seed)
np.random.shuffle(responses)
# If train = test, it is because we are testing now with actual videos, so we
# used all the data to train
trainData = dataset
testData = dataset

# see the link in the header to see how the svm is init. we also use the same
# parameters for C and gamma
svm = cv2.ml.SVM_create()
svm.setKernel(cv2.ml.SVM_LINEAR)
svm.setType(cv2.ml.SVM_C_SVC)
svm.setC(2.67)
svm.setGamma(5.383)
svm.train(trainData, cv2.ml.ROW_SAMPLE, responses)
svm.save('svm_data.dat')
result = svm.predict(testData)
mask = result[1]==responses
correct = np.count_nonzero(mask)
print( correct*100.0/len(result[1]) )
