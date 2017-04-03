###############################################################################
#
# See: http://docs.opencv.org/trunk/dd/d3b/tutorial_py_svm_opencv.html
# for an example of how to use SVM and OpenCV
#
###############################################################################

import glob
import cv2
import numpy as np



class TrainSVM:
    '''This class is the abstract one to train SVMs. Use one of the specific
    ones instead'''


    def __init__(self, dataset, responses):

        self.dataset = dataset
        self.responses = responses


    def train(self, file_to_save):
        '''Trains the SVM with the dataset provided, and stores it in
        file_to_save'''

        # first we shuffle both dataset and responses
        # we create a seed because we want both shuffles to be identical
        seed = np.random.randint(np.iinfo(np.int32).max)
        np.random.seed(seed)
        np.random.shuffle(self.dataset)
        np.random.seed(seed)
        np.random.shuffle(self.responses)

        # now we separate dataset between train and test
        # If train = test, it is because we are testing now with actual videos
        # so we used all the data to train
        trainData = self.dataset 
        testData = self.dataset

        # see the link in the header to see how the svm is init. 
        # we also use the same parameters as they do for C and gamma
        svm = cv2.ml.SVM_create()
        svm.setKernel(cv2.ml.SVM_LINEAR)
        svm.setType(cv2.ml.SVM_C_SVC)
        svm.setC(2.67)
        svm.setGamma(5.383)
        svm.train(trainData, cv2.ml.ROW_SAMPLE, responses)
        svm.save(file_to_save)
        result = svm.predict(testData)
        mask = result[1]==responses
        correct = np.count_nonzero(mask)
        print( correct*100.0/len(result[1]) )
    


class BlueChannel(TrainSVM):
    ''' This class trains the SVM just using the blue channel of the cells,
    after converting them into a 25 by 25 pixel image.
    This is one of the simplest representations, and the svm implementation
    follows the opencv documentation. See the opening file commet.'''


    def __init__(self, dataset, responses):

        super().__init__(dataset, responses)

        # only take blue channel from dataset
        bc =  [img[:,:,0] for img in self.dataset]  
        # transform it into 25 by 25
        b25 =  np.array([cv2.resize(i, (25,25)) for i in bc], dtype=np.float32)
        # flatten it into 1D
        self.dataset = np.array([img.reshape(-1) for img in b25])



if __name__ == "__main__":

    
    # if we used generate_dataset.py  we should have a "reds" and "blues" folder 
    # with the images we clicked for training
    blues = [cv2.imread(file) for file in glob.glob("blues/*.png")]  
    reds = [cv2.imread(file) for file in glob.glob("reds/*.png")] 

    # and we put everything together into a dataset
    dataset = blues + reds 

    # responses will be their "class", 0 for blues, and 1 for reds
    responses = np.array([[0]] * len(blues) + [[1]] * len(reds), dtype=np.int32) 

    bluechannel_svm = BlueChannel(dataset, responses)
    bluechannel_svm.train("svm_bluechannel.dat")
