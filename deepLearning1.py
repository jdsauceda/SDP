import jetson_inference
import jetson_utils
import time
import cv2
import numpy as np

width=1280
height=720

# Instantiate Camera object
cam=jetson_utils.gstCamera(width,height,'0')
# Instantiate display object
display=jetson_utils.glDisplay()
# Font for display
font=jetson_utils.cudaFont()
# Network to use for object detection
net=jetson_inference.imageNet('googlenet')
# Use time library for fps calculation
timeMark=time.time()
# Filter to smooth images
fpsFilter=0

# Loop to keep display open until closed
while display.IsOpen():
    # Capture frame
    frame, width, height=cam.CaptureRGBA()
    # Network Classifier to return ID and confidence level
    classID, confident=net.Classify(frame, width, height)
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
    # Overlay item name on frame, format text
    font.OverlayText(frame, width, height, str(round(fpsFilter,1)) + ' fps ' + item, 5,5, font.Magenta, font.Blue)
    # Display all information to screen
    display.RenderOnce(frame, width, height)
