#!/usr/bin/env python
import PySimpleGUI as sg
import cv2
import numpy as np
import jetson_inference
import jetson_utils

"""
Demo program that displays a webcam using OpenCV
"""
# Resize camera stream, higher resolutions decrease framerates


def main():
    
    dispW=480
    dispH=640
    sg.theme('Black')

    # define the window layout
    layout = [[sg.Text('OpenCV Demo', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('Preview', size=(10, 1), font='Helvetica 14'),
               sg.Button('Stop', size=(10, 1), font='Helvetica 14'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14'), ]]

    # create the window and show it without the plot
    window = sg.Window('Demo AOI Application',
                       layout, location=(800, 400))

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    # cap = cv2.VideoCapture(0)
    cam = jetson_utils.gstCamera(dispW,dispH,'0')
    recording = False

    while True:
        event, values = window.read(timeout=20)  # type: ignore
        if event == 'Exit' or event == sg.WIN_CLOSED:
            return

        elif event == 'Preview':
            recording = True

        elif event == 'Stop':
            recording = False
            img = np.full((480, 640), 255)
            # this is faster, shorter and needs less includes
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)

        if recording:
            # ret, frame = cap.read()
            frame, dispW, dispH = cam.CaptureRGBA(zeroCopy=1)
            frame = jetson_utils.cudaToNumpy(frame,dispW,dispH,4)
            frame = cv2.cvtColor(frame,cv2.COLOR_RGBA2BGR).astype(np.uint8)
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            window['image'].update(data=imgbytes)


main()
