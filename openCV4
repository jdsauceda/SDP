import cv2

print(cv2.__version__)

# Display resolution of Stream
dispW=320
dispH=240
flip=0  # Webcam=0 piCam=2

# Logitech C270 webcam first method, better for manipulations
camSet='v4l2src device=/dev/video0 ! video/x-raw,width=640,height=360,framerate=30/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw(memory:NVMM), format=I420, width='+str(dispW)+', height='+str(dispH)+' ! nvvidconv ! video/x-raw, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! queue ! appsink'
cam=cv2.VideoCapture(camSet)

# Loop to read frames from camera
while True:
    ret, frame=cam.read()
    
    # Draw rectangle on frame
    frame=cv2.rectangle(frame,(140,100),(180,140),(255,250,0),4)
    # Draw circle on frame
    frame=cv2.circle(frame,(50,50),20,(0,0,255),5)
    # Draw txt on frame
    fnt=cv2.FONT_HERSHEY_DUPLEX
    frame=cv2.putText(frame, 'Hello from me', (100,100),fnt,0.5,(255,0,150),2)
    # Draw line on frame
    frame=cv2.line(frame,(10,10),(320,240), (0,0,0),4)
    # Draw arrow on frame
    frame=cv2.arrowedLine(frame,(10,20),(320,0),(255,255,255),3)

    cv2.imshow('Camera', frame)
    # Resize camera frames
    frameSmall=cv2.resize(frame,(320,240))

    if cv2.waitKey(1)==ord('q'):    # Press q in camera window to quit
        break

# Release cam object and close windows
cam.release()
cv2.destroyAllWindows()
