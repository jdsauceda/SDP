from ctypes.wintypes import PINT
import cv2
import numpy as np

print(cv2.__version__)

# Predefined mouse event
evt=-1
# Empty array to store coordinates, global in python
coord=[]

img=np.zeros((250,250,3),np.uint8)

# Click function for Mouse Callback
def click(event,x,y,flag,params):
    # global variables to expose to capture function
    global pnt 
    global evt 
    if event==cv2.EVENT_LBUTTONDOWN:
        print('mouse event was: ',event)
        print(x,',',y)
        pnt=(x,y)
        coord.append(pnt)
        evt=event
    # Retrieve BGR of right button press, open in new window
    if event==cv2.EVENT_RBUTTONDOWN:
        print(x,y)
        blue=frame[y,x,0]
        green=frame[y,x,1]
        red=frame[y,x,2]
        print(blue,green,red)
        colorString=str(blue)+','+str(green)+','+str(red)
        img[:]=[blue,green,red]
        fnt=cv2.FONT_HERSHEY_PLAIN
        r=255-int(red)
        g=255-int(green)
        b=255-int(blue) 
        tp=(b,g,r)
        cv2.putText(img,colorString,(10,25),fnt,1,tp,2)
        cv2.imshow('myColor',img)

dispW=640
dispH=480
flip=2

# Listener for Mouse Action Callback
cv2.namedWindow('nanoCam')
cv2.setMouseCallback('nanoCam',click)

#Uncomment These next Two Line for Pi Camera
camSet='nvarguscamerasrc !  video/x-raw(memory:NVMM), width=3264, height=2464, format=NV12, framerate=21/1 ! nvvidconv flip-method='+str(flip)+' ! video/x-raw, width='+str(dispW)+', height='+str(dispH)+', format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam= cv2.VideoCapture(camSet)

#Or, if you have a WEB cam, uncomment the next line
#(If it does not work, try setting to '1' instead of '0')
#cam=cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    # Print coordinates and x,y text
    for pnts in coord:
        cv2.circle(frame,pnts,5,(0,0,255),-1)
        font=cv2.FONT_HERSHEY_PLAIN
        myStr=str(pnts)
        cv2.putText(frame,myStr,pnts,font,1.5,(255,0,0),2)

    cv2.imshow('nanoCam',frame)
    # keyEvent to quit or clear points
    keyEvent=cv2.waitKey(1)
    if keyEvent==ord('q'):
        break
    if keyEvent==ord('c'):
        coord=[]
cam.release()
cv2.destroyAllWindows()