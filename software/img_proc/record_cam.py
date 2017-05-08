###############################################################################
# Reads from the cam and makes a video until user press q or timeout
###############################################################################

import cv2
import threading
import time


def random_filename(size):
    ''' to create random names for the dataset pictures '''

    w = ''.join(random.choice(string.ascii_lowercase) for i in range(size))
    return w+'.avi'


def kill_video(event, time_to_wait):
    '''Waits for time_wait time.
    Then sets and event so that the timeout is marked and the video recording
    stops'''
    time.sleep(time_to_wait)
    event.set()


if __name__ == "__main__":

    vc = cv2.VideoCapture(0)
    vc.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    cv2.namedWindow("video")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    random_name = random_filename(5)
    out = cv2.VideoWriter(random_name,fourcc, 30.0, (800,600))

    event = threading.Event()
    timer = threading.Thread(target=kill_video, args=(event,5))
    timer.start()

    while(1):
        ret,frame = vc.read()
        out.write(frame)
        cv2.imshow("video",frame)
        key =  cv2.waitKey(30)

        if key == ord('q') or event.is_set():
            break


    vc.release()
    out.release()
    cv2.destroyAllWindows()
                
