import cv2

print(cv2.__version__)

# Display resolution of Stream
dispW=320
dispH=240
flip=0  # Webcam=0 piCam=2

# Uncomment if using Raspberry pi camera
#camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=640, height=480, format=NV12, framerate=20/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
# cam=cv2.VideoCapture(camSet)

# Logitech C270 webcam first method, better for manipulations
camSet='v4l2src device=/dev/video0 ! video/x-raw,width=640,height=360,framerate=15/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw(memory:NVMM), format=I420, width='+str(dispW)+', height='+str(dispH)+' ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! queue ! appsink'
cam=cv2.VideoCapture(camSet)

# VideoWriter to read from captured video file
cam=cv2.VideoCapture('videos/myCam.avi')
# VideoWriter to output captured source video
#outVid=cv2.VideoWriter('videos/myCam.avi',cv2.VideoWriter_fourcc(*'XVID'),15,(dispW,dispH))      #reference from cwd

# Logitech C270 webcam second method
#cam=cv2.VideoCapture(0)             # Camera=0 if only one device connected
#cam.set(cv2.CAP_PROP_FRAME_WIDTH,dispW)    # Resize webcam
#cam.set(cv2.CAP_PROP_FRAME_HEIGHT,dispH)   

# Loop to read frames from camera
while True:
    ret, frame=cam.read()
    cv2.imshow('Camera', frame)

    # Convert frame to gray video
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    cv2.imshow('grayVideo', gray)

    # Resize camera frames
    frameSmall=cv2.resize(frame,(320,240))
    graySmall=cv2.resize(gray,(320,240))

    # Write outVid object
    #outVid.write(frame)

    if cv2.waitKey(1)==ord('q'):    # Press q in camera window to quit
        break

# Release cam object and close windows
cam.release()
outVid.release()
cv2.destroyAllWindows()