import cv2

vc = cv2.VideoCapture(0)
vc.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
vc.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
cv2.namedWindow("video")


fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 30.0, (800,600))

while(1):
    ret,frame = vc.read()
    out.write(frame)
    cv2.imshow("video",frame)
    key =  cv2.waitKey(30)

    if key == ord('q'):
        break


vc.release()
out.release()
cv2.destroyAllWindows()
            
