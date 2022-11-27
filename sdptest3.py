import jetson_inference
import jetson_utils
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import serial  
from datetime import datetime

# Resize camera stream, higher resolutions decrease framerates
dispW=800
dispH=600

# Flags
preview = True
wide_aoi = False
slice_aoi = False
passCount = 1
failCount = 1

# GPIO board configuration
GPIO.setmode(GPIO.BOARD)

# Configure UART communication 
serial_port = serial.Serial(
    port = "/dev/ttyTHS1",
    baudrate = 115200,
    bytesize = serial.EIGHTBITS,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
)

# Wait for port to initialize
time.sleep(1)

# Instantiate Camera object
cam = jetson_utils.gstCamera(dispW,dispH,'0')

# Transfer learning image detection network (pass, fail)
net = jetson_inference.imageNet(
    'googlenet',
    [
    '--model=/home/nano/Downloads/jetson-inference/python/training/classification/myModel/resnet18.onnx',
    '--input_blob=input_0',
    '--output_blob=output_0',
    '--labels=/home/nano/Downloads/jetson-inference/myTrain/labels.txt'
    ]
)

# Use time library for fps calculation
timeMark = time.time()
# Filter to smooth imagesq
fpsFilter = 0
# OpenCV font
font = cv2.FONT_HERSHEY_SIMPLEX

# File for Logging
file = open('log.txt', 'w')

def log(file, x, rcv):
    file.write(str(x)+ ' ' + rcv + '\n')
    file.flush()

# Loop to display captured frames
while True:
    
    if preview:
        frame, dispW, dispH = cam.CaptureRGBA(zeroCopy=1)
         # Network Classifier to return ID and confidence level
        classID, confident = net.Classify(frame, dispW, dispH)

        frame = jetson_utils.cudaToNumpy(frame,dispW,dispH,4)
        frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2BGR).astype(np.uint8)
        cv2.putText(frame, 'q to quit, w for Wide mode, r for ROI mode',(0,590),font,1,(0,200,255),2)
        cv2.imshow('Preview',frame)
        if cv2.waitKey(1) == ord('w'):
            preview = False
            wide_aoi = True
            slice_aoi = False
            cam.Close()
            cv2.destroyAllWindows()
        elif cv2.waitKey(1) == ord('r'):
            preview = False
            wide_aoi = False
            slice_aoi =True
            cam.Close()
            cv2.destroyAllWindows()
        elif cv2.waitKey(1) == ord('q'):
            break

    if slice_aoi:
        frame, dispW, dispH = cam.CaptureRGBA(zeroCopy=1)
        roi = frame
         # Network Classifier to return ID and confidence level
        classID, confident = net.Classify(roi, dispW, dispH)
        # Calculate time difference for fps
        dt = time.time()-timeMark
        # fps calculation
        fps = 1/dt
        # Smoothing calculation using Filter
        fpsFilter = .95*fpsFilter + .05*fps
        # timeMark for Filter
        timeMark = time.time()
        
        # Convert cuda to numpy for openCV frame format
        frame = jetson_utils.cudaToNumpy(frame,dispW,dispH,4)
        frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2BGR).astype(np.uint8)

        # Region of Interest 
        # Changes classID number into item name
        item = net.GetClassDesc(classID)

        # Keep count of pass/fail
        if item == 'pass':
            passCount += 1
        if item == 'fail':
            failCount += 1

        # Check if too many fails
        if (passCount > 10 and failCount > 10) and (failCount/passCount >= 50):
            result = failCount/passCount
            print(result)
            break

        x = datetime.fromtimestamp(timeMark)
        log(file, x, item)

        # Write to UART
        print("pass Count " + str(passCount))
        print("fail Count " + str(failCount))
        serial_port.write(item.encode())

        # Convert cuda to numpy for openCV frame format
        roi = jetson_utils.cudaToNumpy(roi,dispW,dispH,4)
        roi = cv2.cvtColor(roi,cv2.COLOR_RGBA2BGR).astype(np.uint8)

        # Draw rectangle on frame
        frame=cv2.rectangle(frame,(300,0),(500,dispH),(160,160,160),2)

        # Format text for openCV
        cv2.putText(frame,str(round(confident*100, ndigits=1)) + ' confidence ' + str(round(fpsFilter,1))+ ' fps ' +item,(0,30),font,1,(0,200,255),2)
        cv2.putText(frame, 'q to quit, w for Wide mode',(0,590),font,1,(0,200,255),2)
        # Crop frame for ROI
        roi = frame[0:600,300:500].copy()

        # Display image as camera
        cv2.imshow('AOI',frame)
        # Move display to 0,0 area
        cv2.moveWindow('AOI',0,0)

        cv2.imshow('ROI AOI', roi)
        # Move display to 0,0 area
        cv2.moveWindow('ROI AOI',365,0)
        
        if cv2.waitKey(1) == ord('w'):
            preview = False
            wide_aoi = True
            slice_aoi = False
            cam.Close()
            cv2.destroyAllWindows()
        elif cv2.waitKey(1) == ord('q'):
            break

    if wide_aoi:
         # Capture frame, specify width and height
        frame, dispW, dispH = cam.CaptureRGBA(zeroCopy=1)

        # Network Classifier to return ID and confidence level
        classID, confident = net.Classify(frame, dispW, dispH)
        # Changes classID number into item name
        item = net.GetClassDesc(classID)


        # Write item to pico over UART
        print(item)
        serial_port.write(item.encode())

        # Calculate time difference for fps
        dt = time.time()-timeMark
        # fps calculation
        fps = 1/dt
        # Smoothing calculation using Filter
        fpsFilter = .95*fpsFilter + .05*fps
        # timeMark for Filter
        timeMark = time.time()
        # Convert cuda to numqpy for openCV frame format
        frame = jetson_utils.cudaToNumpy(frame,dispW,dispH,4)
        frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2BGR).astype(np.uint8)

        # Format text for openCV
        cv2.putText(frame,str(round(confident*100, ndigits=1)) + ' confidence ' + str(round(fpsFilter,1))+' fps ' + item,(0,30),font,1,(0,200,255),2)
        cv2.putText(frame, 'q to quit, r for ROI mode',(0,590),font,1,(0,200,255),2)
        # Display image as camera
        cv2.imshow('Wide AOI',frame)
        # Move display to 0,0 area
        cv2.moveWindow('Wide AOI',0,0)
        
        if cv2.waitKey(1) == ord('r'):
            preview = False
            wide_aoi = False
            slice_aoi = True
            cam.Close()
            cv2.destroyAllWindows()
        elif cv2.waitKey(1) == ord('q'):
            break

# Release and destroy windows 
file.close()
print(failCount/passCount) 
cam.Close()
cv2.destroyAllWindows()
