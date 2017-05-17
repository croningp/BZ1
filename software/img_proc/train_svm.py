###############################################################################
#
# See: http://docs.opencv.org/trunk/dd/d3b/tutorial_py_svm_opencv.html
# for an example of how to use SVM and OpenCV. This is the main framework
# we will use here.
#
# Another example of how the PCA was used with the SVM:
# http://www.raspberryturk.com/notebooks/chess_piece_presence.html
#
###############################################################################



import glob
import cv2
import numpy as np
from sklearn.decomposition import PCA
from sklearn.externals import joblib



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
        # we will use the default SVM parameters from the header link
        svm = cv2.ml.SVM_create()
        svm.setKernel(cv2.ml.SVM_RBF)
        svm.setType(cv2.ml.SVM_C_SVC)
        svm.setC(2) # before 2.67
        svm.setGamma(5) # before 5.383
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



class RedBlueChannel(TrainSVM):
    '''Same as the class BlueChannel, but this one takes both red and blue
    channels, and transform them into 15 by 15 images, and uses that to feed
    the SVM'''


    def __init__(self, dataset, responses):

        super().__init__(dataset, responses)
        # first we transform the images to 10 by 10
        resized = [ cv2.resize(img, (15,15) ) for img in self.dataset]
        resized32 = np.array(resized, dtype=np.float32)
        # take the red and blue channels
        rbc =  [np.concatenate((i[:,:,0], i[:,:,2])) for i in resized32]  
        # flatten it into 1D
        self.dataset = np.array([img.reshape(-1) for img in rbc])



class PCATransform(TrainSVM):
    '''This class will use a PCA transform for every image in order to reduce
    its dimensionality quite a lot. Based on the example linked in the
    headline comment'''


    def __init__(self, dataset, response, pca_file):

        super().__init__(dataset, responses)
        # First we need to prepare the data to feed the PCA
        # we need to make sure all the images are the same size
        resized = [ cv2.resize(img, (50,50) ) for img in self.dataset]
        resized = np.asarray(resized, dtype=np.float32)
        # reshape from (N, size, size, 3) to (N, size*size*3)
        data2D = resized.reshape( resized.shape[0], -1)

        # init the PCA
        pca = PCA(n_components=8, whiten=True)
        # get the eigenvalues / vectors
        pca.fit(data2D)
        # save the model because we will need it during test
        joblib.dump(pca, pca_file) 
        # reduce the dimensionality of the data
        pca_out = pca.transform(data2D)
        self.dataset = pca_out.astype('float32')



class HSVHistogram(TrainSVM):
    '''Transform the image into the HSV channel and calculates a 3D
    histogram. This code follows what Gerardo did'''


    def __init__(self, dataset, response):

        super().__init__(dataset, responses)
        # change to HSV 
        dataHSV = [ cv2.cvtColor(i, cv2.COLOR_BGR2HSV) for i in self.dataset ]
        # calculate histograms for H, S and V
        hist_ocv = [ cv2.calcHist([i], [0, 1, 2], None, [8, 8, 8], 
            [0, 256, 0, 256, 0, 256]) for i in dataHSV ]
        # everything to 1D
        hists1D = [ h.flatten() for h in hist_ocv ]
        # eq lighting, idea from HOG
        hists = [ hist / np.sqrt(np.sum(np.power(hist,2))) for hist in hists1D ]
        self.dataset = np.asarray(hists)



def equalise_img(img):
    '''histogram equalisation. From Gerardo's code'''

    b,g,r = cv2.split(img)
    r_hst = cv2.equalizeHist(r)
    g_hst = cv2.equalizeHist(g)
    b_hst = cv2.equalizeHist(b)
    image_eq = cv2.merge((b_hst, g_hst, r_hst))

    clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(4,4))
    b,g,r = cv2.split(img)
    cl1 = clahe.apply(b)
    cl2 = clahe.apply(g)
    cl3 = clahe.apply(r)
    image_eq = cv2.merge((cl1,cl2,cl3))

    return image_eq



if __name__ == "__main__":

    
    # if we used generate_dataset.py  we should have a "reds" and "blues" folder 
    # with the images we clicked for training
    blues = [cv2.imread(file) for file in glob.glob("blues/*.png")]  
    reds = [cv2.imread(file) for file in glob.glob("reds/*.png")] 

    # and we put everything together into a dataset and equalise it
    dataset = blues + reds 
    dataset = [ equalise_img(img) for img in dataset ]

    # responses will be their "class", 0 for blues, and 1 for reds
    responses = np.array([[0]] * len(blues) + [[1]] * len(reds), dtype=np.int32) 

    # bluechannel_svm = BlueChannel(dataset, responses)
    # bluechannel_svm.train("svm_bluechannel.dat")

    # rbchannel_svm = RedBlueChannel(dataset, responses)
    # rbchannel_svm.train("svm_rbchannel.dat")

    # pca_svm = PCATransform(dataset, responses, "pca.dat")
    # pca_svm.train("svm_pca.dat")

    hsvhist = HSVHistogram(dataset, responses)
    hsvhist.train("hsvhist.dat")
