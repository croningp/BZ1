import sys
sys.path.insert(0, "img_proc")

import test_svm
from bzboard.bzboard import BZBoard

board = test.BZBoard('/dev/ttyACM0')
svm = HSVHistogram('test_svm/hsvhist.dat')

board.activate_all()

vc = cv2.VideoCapture(0)
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
raw = cv2.VideoWriter('raw.avi',fourcc, 30.0, (600,600))
out = cv2.VideoWriter('svm.avi',fourcc, 30.0, (600,600))

click_grid = test_svm.GridClickData()    

while(True):

    ret,frame = vc.read()

    if key == ord('q') or ret is False:
        break

    raw.write(frame)
    cv2.imshow("raw", frame)
    
    # first thing we ask the user to define the 5x5 grid
    if click_grid.finished is False:
        click_grid.get_platform_corners(frame)

    # "click_grid" is now populated with the x,y corners of the platform
    click_grid.draw_grid(frame)
    # we use the svm to decide if the cells are painted red or blue
    svm.paint_cells(frame, click_grid.points)

    cv2.imshow('SVM', frame)
    out.write(frame)
    key = cv2.waitKey(1) & 0xFF 


vc.release()
out.release()
cv2.destroyAllWindows()
