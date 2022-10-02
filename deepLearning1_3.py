import jetson_inference
import jetson_utils
import time
import cv2
import numpy as np

width=1280
height=720
flip=2
dispW=width
dispH=height

# Instantiate Camera object using openCV
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=20/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam=cv2.VideoCapture(camSet)

# Network to use for object detection
net=jetson_inference.imageNet('alexnet')
# Use time library for fps calculation
timeMark=time.time()
# Filter to smooth images
fpsFilter=0
# OpenCV font
font=cv2.FONT_HERSHEY_SIMPLEX

# Loop to keep display open until closed
while True:
    # Capture frame using OpenCV
    _,frame=cam.read()
    # Convert image from BGR to RGBA
    img=cv2.cvtColor(frame,cv2.COLOR_BGR2RGBA).astype(np.float32)
    # Convert to cuda from numpy
    img=jetson_utils.cudaFromNumpy(img)
    # Network Classifier to return ID and confidence level
    classID, confident=net.Classify(img, width, height)
    # Changes classID number into item name
    item=net.GetClassDesc(classID)
    # Calculate time difference for fps
    dt=time.time()-timeMark
    # fps calculation
    fps=1/dt
    # Smoothing calculation using Filter
    fpsFilter=.95*fpsFilter + .05*fps
    # timeMark for Filter
    timeMark=time.time()
    # Format text for openCV
    cv2.putText(frame,str(round(fpsFilter,1))+' fps '+ item,(0,30),font,1,(0,0,255),2)
    # Display image as recCam
    cv2.imshow('recCam',frame)
    # Move display to 0,0 area
    cv2.moveWindow('recCam',0,0)

    # Loop to exit from recCam
    if cv2.waitKey(1)==ord('q'):
        break
# Release and destroy windows
cam.release()
cv2.destroyAllWindows()
