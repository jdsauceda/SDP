import PySimpleGUI as sg
import cv2
import numpy as np
import jetson_inference
import jetson_utils
import time
import serial
import RPi.GPIO as GPIO

"""
GUI demo of SDP
"""


def main():
    # GUI theme
    sg.theme('Dark2')
    # Display size
    dispW=800
    dispH=600

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

    # define the window layout
    layout = [
              [sg.Text('AOI Demo',size=(42,1), relief='solid', justification='center', font='Helvetica 25')],
              [sg.Image(filename='', key='image')],
            #   [sg.Text('Result',size=(10,1), justification='left', font='Helvetica 14')],
            #   [sg.Multiline(size=(10,1), font='Helvetica 14', write_only=True, reroute_stdout=True, autoscroll=True, auto_refresh=True)],
            #   [sg.Text('Confidence',size=(10,1), justification='left', font='Helvetica 14')],
            #   [sg.Multiline(size=(10,1), font='Helvetica 14', write_only=True, reroute_stdout=True, autoscroll=True, auto_refresh=True)],
              [sg.HorizontalSeparator(pad=10)],
              [sg.Button('Preview Video', size=(10, 1), font='Helvetica 14', button_color='Black', expand_x=True),
               sg.Button('Wide AOI', size=(10, 1), font='Helvetica 14', button_color='Black', expand_x=True),
               sg.Button('ROI AOI', size=(10, 1), font='Helvetica 14', button_color='Black', expand_x=True),
               sg.Button('Stop Video', size=(10, 1), font='Helvetica 14', button_color='Black', expand_x=True),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14', button_color='Black', expand_x=True), ]               
               ]

    # create the window and show it without the plot
    window = sg.Window('Demo GUI - AOI Integration',
                       layout, location=(dispW, 400))

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
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

    roi_aoi = False
    preview = False
    wide_roi = False
    stop = False

    while True:
        event, values = window.read(timeout=20)
        
        if event == 'Exit' or event == sg.WIN_CLOSED:
            cam.Close()
            cv2.destroyAllWindows()
            window.close()
            return

        elif event == 'Preview Video':
            wide_roi = False
            preview= True
            stop = False
            roi_aoi = False

        elif event == 'Wide AOI':
            wide_roi = True
            preview = False
            stop = False
            roi_aoi = False

        elif event == 'ROI AOI':
            wide_roi = False
            preview = False
            stop = False
            roi_aoi = True

        elif event == 'Stop Video':
            wide_roi = False
            preview = False
            stop = True
            roi_aoi = False

        if preview:
            # # Capture frame, specify width and height
            # frame, dispW, dispH = cam.CaptureRGBA(zeroCopy=1)
            #  # Convert cuda to numpy for openCV frame format
            # frame = jetson_utils.cudaToNumpy(frame, dispW, dispH, 4)
            # frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR).astype(np.uint8)
            # imgbytes = cv2.imencode('.png',frame)[1].tobytes()
            # window['image'].update(data=imgbytes)
            frame, dispW, dispH = cam.CaptureRGBA(zeroCopy=1)
            # Network Classifier to return ID and confidence level
            classID, confident = net.Classify(frame, dispW, dispH)
            # Changes classID number into item name
            item = net.GetClassDesc(classID)            
            # Calculate time difference for fps
            dt = time.time()-timeMark
            # fps calculation
            fps = 1/dt
            # Smoothing calculation using Filter
            fpsFilter = .95*fpsFilter + .05*fps
            # timeMark for Filter
            timeMark = time.time()
            # Convert cuda to numqpy for openCV frame format
            frame = jetson_utils.cudaToNumpy(frame, dispW, dispH, 4)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR).astype(np.uint8)
            # Format text for openCV
            cv2.putText(frame, str(round(fpsFilter,1))+' fps ',(0,30),font,1,(0,200,255),2)
            # Display video frame to windows
            imgbytes = cv2.imencode('.png',frame)[1].tobytes()
            window['image'].update(data=imgbytes)

        if wide_roi:
            frame, dispW, dispH = cam.CaptureRGBA(zeroCopy=1)
            # Network Classifier to return ID and confidence level
            classID, confident = net.Classify(frame, dispW, dispH)
            # Changes classID number into item name
            item = net.GetClassDesc(classID)

            # Write to UART 
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
            frame = jetson_utils.cudaToNumpy(frame, dispW, dispH, 4)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR).astype(np.uint8)
            # Format text for openCV
            cv2.putText(frame,str(round(confident*100, ndigits=1)) + ' confidence ' + str(round(fpsFilter,1))+' fps ' + item,(0,30),font,1,(0,200,255),2)
            # Display video frame to windows
            imgbytes = cv2.imencode('.png',frame)[1].tobytes()
            window['image'].update(data=imgbytes)

        if roi_aoi:
            frame, dispW, dispH = cam.CaptureRGBA(zeroCopy=1)
            roi = frame
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
            # Network Classifier to return ID and confidence level
            classID, confident = net.Classify(roi, dispW, dispH)
            # Changes classID number into item name
            item = net.GetClassDesc(classID)

            # Write to UART
            print(item)
            serial_port.write(item.encode())

            # Convert cuda to numpy for openCV frame format
            roi = jetson_utils.cudaToNumpy(roi,dispW,dispH,4)
            roi = cv2.cvtColor(roi,cv2.COLOR_RGBA2BGR).astype(np.uint8)

            # Draw rectangle on frame
            roi=cv2.rectangle(frame,(300,0),(500,dispH),(160,160,160),2)

            # Format text for openCV
            cv2.putText(frame,str(round(confident*100, ndigits=1)) + ' confidence ' + str(round(fpsFilter,1))+ ' fps ' +item,(0,30),font,1,(0,200,255),2)
            # Crop frame for ROI
            roi = frame[0:600,300:500].copy()
        
            imgbytes = cv2.imencode('.png', roi)[1].tobytes()
            window['image'].update(data=imgbytes)
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()
            window['image'].update(data=imgbytes)

        if stop:
            img = np.full((dispH, dispW), 0)
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)
         
main()