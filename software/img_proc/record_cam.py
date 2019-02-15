##############################################################################
# Reads from the cam and makes a video until user press q or timeout
##############################################################################

import cv2
import threading
import time, random, string, sys


class RecordVideo():


    def __init__(self, user_time):

        self.duration = user_time


    def random_filename(self, size):
        ''' to create random names for the dataset pictures '''

        w = ''.join(random.choice(string.ascii_lowercase) for i in range(size))
        return w+'.avi'


    def kill_video(self, event, time_to_wait):
        '''Waits for time_wait time.
        Then sets and event so that the timeout is marked and the video recording
        stops'''
        time.sleep(time_to_wait+1) # cam always takes around 1s to warm up
        event.set()


    def record_video(self, filename):

        vc = cv2.VideoCapture(0)
        vc.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
        vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
        vc.set(cv2.CAP_PROP_BRIGHTNESS, 190)
        vc.set(cv2.CAP_PROP_SATURATION, 200)
        vc.set(cv2.CAP_PROP_CONTRAST, 10)
        cv2.namedWindow("video")

        fourcc = cv2.VideoWriter_fourcc(*'X264')
        random_name = self.random_filename(0)
        out = cv2.VideoWriter(filename+random_name, fourcc, 20.0, (800,600))

        event = threading.Event()
        
        if self.duration > 0:
            timer = threading.Thread(target=self.kill_video, 
                    args=(event,self.duration))
            timer.start()

        frame_counter = 0

        while(1):
            # start_time = time.process_time() * 1000 # seconds to ms
            frame_counter += 1
            ret,frame = vc.read()
            out.write(frame)
            cv2.imshow("video",frame)

            # end_time = time.process_time() * 1000
            # wait_time = 33333 - (end_time - start_time)*1000
            key = cv2.waitKey(1)#int(wait_time/1000))

            if key == ord('q') or event.is_set():
                break

        vc.release()
        out.release()
        cv2.destroyAllWindows()


    def record_threaded(self, filename="test"):
        threading.Thread(target=self.record_video, args=(filename,)).start()


if __name__ == "__main__":

    if len(sys.argv) > 1:
        user_time = float(sys.argv[1])
    else:
        user_time = 0

    rv = RecordVideo(user_time)
    rv.record_threaded()
