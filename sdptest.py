import jetson_inference
import jetson_utils
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
import serial  

# Resize camera stream, higher resolutions decrease framerates
width=1024
height=768

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
cam = jetson_utils.gstCamera(width,height,'0')

# Standard image detection network
# net=jetson_inference.imageNet('googlenet') 

# Transfer learning image detection network (pass, fail)
net = jetson_inference.imageNet('googlenet', ['--model=/home/nano/Downloads/jetson-inference/python/training/classification/myModel/resnet18.onnx', '--input_blob=input_0','--output_blob=output_0','--labels=/home/nano/Downloads/jetson-inference/myTrain/labels.txt'])

# Use time library for fps calculation
timeMark = time.time()
# Filter to smooth imagesq
fpsFilter = 0
# OpenCV font
font = cv2.FONT_HERSHEY_SIMPLEX

# Loop to display captured frames
while True:
    # Capture frame, specify width and height
    frame, width, height = cam.CaptureRGBA(zeroCopy=1)

    # Network Classifier to return ID and confidence level
    classID, confident = net.Classify(frame, width, height)
    # Changes classID number into item name
    item = net.GetClassDesc(classID)


    # Write item to pico over UART
    # try:
    #     if item != 'mail':
    serial_port.write(item.encode())

    # except:
    #     print('Continuing')

    # Motor control ?
    

    # Calculate time difference for fps
    dt = time.time()-timeMark
    # fps calculation
    fps = 1/dt
    # Smoothing calculation using Filter
    fpsFilter = .95*fpsFilter + .05*fps
    # timeMark for Filter
    timeMark = time.time()
    # Convert cuda to numqpy for openCV frame format
    frame = jetson_utils.cudaToNumpy(frame,width,height,4)
    frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2BGR).astype(np.uint8)

    # Format text for openCV
    cv2.putText(frame,str(round(confident*100, ndigits=1)) + ' confidence ' + str(round(fpsFilter,1))+' fps '+  item,(0,30),font,1,(0,200,255),2)

    # Display image as camera
    cv2.imshow('Camera',frame)
    # Move display to 0,0 area
    cv2.moveWindow('Camera',0,0)

    # Loop to exit from camera
    if cv2.waitKey(1) == ord('q'):
        break

        
# Release and destroy windows
cam.release()
cv2.destroyAllWindows()

