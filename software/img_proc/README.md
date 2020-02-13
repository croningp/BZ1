This folder contains all the files used to perform the image processing. That is, to classify the oscillations between red and blue.

In order to do so, a SVM was used. If you want the data to train the SVM, you can contact us and we will send you it. It contains a few thousands of images classified as either red or blue.

## To get the SVM working...

* First, generate_dataset.py should be used over several videos to create the dataset.
* Then, train_svm.py should be used against the previosly generated dataset.
* Finally, test_svm.py can be used to test it. In this folder you can find a few dat files which are models already created by us.

## Other files:

* speedupvideo.py. Because the videos are quite long, we used this script to speed them up. Usually by a factor of 15.
* wave_direction.py Is the file used to create the "programming BZ" figure from the manuscript
* record_cam.py is used to start the camera and record a video.
* time_map.py Once a video has been generated, this script will plot it in 2D where the X axes will be time.
* rawvideoTocsv5x5.py given a video, this script will generate a CSV taking the mean colour of each cell.