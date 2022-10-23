import jetson_inference
import jetson_utils
import time
import cv2
import numpy as np
import RPi.GPIO as GPIO  #GPIO Library
import time
import serial  

width=640
height=480

# Configure UART
serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
GPIO.setmode(GPIO.BOARD)
# Wait for port to initialize
time.sleep(1)

# Instantiate Camera object
cam=jetson_utils.gstCamera(width,height,'0')
# Network to use for object detection
net=jetson_inference.imageNet('resnet-18')
# Use time library for fps calculation
timeMark=time.time()
# Filter to smooth images
fpsFilter=0
# OpenCV font
font=cv2.FONT_HERSHEY_SIMPLEX

# Loop to keep display open until closed
while True:
    # Capture frame
    frame, width, height=cam.CaptureRGBA(zeroCopy=1)
    # Network Classifier to return ID and confidence level
    classID, confident=net.Classify(frame, width, height)
    # Changes classID number into item name
    item=net.GetClassDesc(classID)

    # Write item to pico
    serial_port.write(item.encode())
    print(item)

    # Calculate time difference for fps
    dt=time.time()-timeMark
    # fps calculation
    fps=1/dt
    # Smoothing calculation using Filter
    fpsFilter=.95*fpsFilter + .05*fps
    # timeMark for Filter
    timeMark=time.time()
    # Convert cuda to numpy for openCV frame format
    frame=jetson_utils.cudaToNumpy(frame,width,height,4)
    frame=cv2.cvtColor(frame,cv2.COLOR_RGBA2BGR).astype(np.uint8)
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
