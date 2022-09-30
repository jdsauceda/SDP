import cv2
import numpy as np

print(cv2.__version__)

dispW=640
dispH=480
flip=2
img1=np.zeros((480,640,1),np.uint8)
img1[0:480,0:320]=[255]

img2=np.zeros((480,640,1),np.uint8)
img2[190:290,270:370]=[255]

bitAnd=cv2.bitwise_and(img1,img2)
bitOr=cv2.bitwise_or(img1,img2)
bitXor=cv2.bitwise_xor(img1,img2)

#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)

#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    
    cv2.imshow('img1',img1)
    cv2.moveWindow('img1',0,500)
    cv2.imshow('img2',img2)
    cv2.moveWindow('img2',700,0)
    cv2.imshow('AND',bitAnd)
    cv2.moveWindow('AND',700,500)
    cv2.imshow('OR',bitOr)
    cv2.moveWindow('OR',1340,0)
    cv2.imshow('XOR',bitXor)
    cv2.moveWindow('XOR',1340,500)
    frame=cv2.bitwise_and(frame,frame,mask=img1)
    cv2.imshow('nanoCam',frame)
    cv2.moveWindow('nanoCam',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()