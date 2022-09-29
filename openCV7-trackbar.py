from turtle import width
import cv2

print(cv2.__version__)

dispW=640
dispH=480
flip=2

# Function todo nothing but needs param
def nothing(x):
    pass

#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)

# Add Trackbar to screen
cv2.namedWindow('nanoCam')
cv2.createTrackbar('xVal','nanoCam',0,dispW,nothing)
cv2.createTrackbar('yVal','nanoCam',0,dispH,nothing)
cv2.createTrackbar('width','nanoCam',0,dispW,nothing)
cv2.createTrackbar('height','nanoCam',0,dispH,nothing)

#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    # Draw rectangle using trackbars
    xVal=cv2.getTrackbarPos('xVal','nanoCam')
    yVal=cv2.getTrackbarPos('xVal','nanoCam')
    width=cv2.getTrackbarPos('width','nanoCam')
    height=cv2.getTrackbarPos('height','nanoCam')
    cv2.rectangle(frame,(xVal,yVal),(xVal+width,yVal+height),(255,0,0),3)

    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()