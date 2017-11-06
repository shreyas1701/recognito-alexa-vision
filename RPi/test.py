import cv2
##cam=cv2.VideoCapture(0)
##ramp_frames = 5
def get_image():
    cam=cv2.VideoCapture(0)
    img,frame=cam.read()
    del(cam)
    return frame
#k = cv2.waitKey(0)
#print(frame)
##if frame==None:
##    img,frame = cam.read()
##for i in xrange(ramp_frames):
##    temp = get_image()
##    camera_capture = get_image()
##    file = "/home/pi/test_image.png"
##    cv2.imwrite(file,camera_capture)
#cv2.namedwindow("camera", cv2.CV_WINDOW_AUTOSIZE)
#cv2.imshow("camera",frame)
#cv2.waitKey(0)
#cv2.destroywindow("camera")