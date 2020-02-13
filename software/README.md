This folder contains all the software written to develop this project.

* bzboard contains the python script to actuate as middleman between the firmware and the stirrers. This is the one used by the user to perform experiments.
* pumpsctl is a similar file to bzboard, but in this case to control the liquid pumps.
* img_proc contains all the files used to perform the Computer Vision using a SVM and classify the oscillations between red and blue.
* tools contains two files, one of them to send emails from the platform when a message needs to be sent, and another one to check the volume of the different reactants and the waste bottle.
* firmware contains the Arduino-C code to control both the pumps and the stirrers. 2 different Arduino Mega boards were used, one for each.
* Data Analysis contains a Jupyter Notebook to analyse the dataset used to train the SVM.

All the other python files in this folder were used to directly run experiments.

* initBZ.py should be executed before starting the experiments. It's objective is to check that everything works fine. This must be visually inspected by the user, this script will merely run quickly all the components.
* cleanBZ.py is a script used to clean the area with waste and water.
* main.py is a basic script which will load the BZ medium into the platform, and then drain in. Code here can be injected to execute one experiments.
* automatedBZ.py is the script we used the most, and it will perform all the steps required to perform one experiment.
* experiment_parent.py and randompatter.py are OO implementations of the previous one.
* cellular_automata.py is an attempt of creating a CA using this platform, and it can be used to dynamically actuate the motors based on the visual information from the image processing. Nevertheless, the CA never really worked on this iteration of the platform.