from ctypes.wintypes import PINT
import cv2

print(cv2.__version__)

# Predefined mouse event
evt=-1

# Click function for Mouse Callback
def click(event,x,y,flag,params):
    # global variables to expose to capture function
    global pnt 
    global evt 
    if event==cv2.EVENT_LBUTTONDOWN:
        print('mouse event was: ',event)
        print(x,',',y)
        pnt=(x,y)
        evt=event

dispW=640
dispH=480
flip=2

# Mouse Action Callback
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
   
    if evt==1:
        # Print circle to screen upon mouse click
        cv2.circle(frame,pnt,2,(0,0,255),-1)
        # Print x,y text from circle
        font=cv2.FONT_HERSHEY_PLAIN
        myStr=str(pnt)
        cv2.putText(frame,myStr,pnt,font,1,(255,0,0),2)
    cv2.imshow('nanoCam',frame)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()