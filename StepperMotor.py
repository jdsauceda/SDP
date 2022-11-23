from machine import Pin, UART
from time import sleep, sleep_ms, sleep_us

def map(x, in_min, in_max, out_min, out_max): 
    return int((x - in_min) * (out_max - out_min) /
               (in_max - in_min) + out_min)
    
class STEPMOTOR:
    def __init__(self, step_pin, dir_pin):
        self.step = Pin(step_pin, Pin.OUT)
        self.dir = Pin(dir_pin, Pin.OUT)

    def rotate(self, angle=0, rotation='cw'):
        num_of_steps = map(angle, 0, 360, 0, 200)
        if rotation=='cw':
            self.dir.value(0)
            for i in range(0,num_of_steps,1):
                self.step.value(1)
                sleep_us(500)
                self.step.value(0)
                sleep_us(500)
        if rotation=='ccw':
            self.dir.value(1)
            for i in range(num_of_steps-1,-1,-1):
               self.step.value(1)
               sleep_us(500)
               self.step.value(0)
               sleep_us(500)       

stepper = STEPMOTOR(step_pin=17, dir_pin=16)

# GPIO pins
greenLED = Pin(0, Pin.OUT)
yellowLED = Pin(2, Pin.OUT)
redLED = Pin(4, Pin.OUT)

#UART 0: Communication channel between boards
# uart0 = UART(0, baudrate=115200, tx=Pin(12), rx=Pin(13), bits=8, parity=None, stop=1)
#UART 1: Communication channel with motor
uart1 = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9), bits=8, parity=None, stop=1)
sleep(1)

# File for logging
file = open("test.txt", "w")


def readyState(rcv):
    if rcv == b"pass":    #binary encoded string b"string"
        greenLED.value(1)
        redLED.value(0)
        yellowLED.value(0)
        
def warningState(rcv):
    if rcv == b"blank":
        yellowLED.value(1)
        greenLED.value(0)
        redLED.value(0)

def failureState(rcv):
    if rcv == b"fail":
        redLED.value(1)
        greenLED.value(0)
        yellowLED.value(0)
        
def log(file, rcv):
    file.write(str(rcv) + '\n')
    file.flush()

# Loop
while True:    
    # Read incoming UART
    if uart1.any() > 0:
        rcv = uart1.read()
        print(rcv)
        readyState(rcv)              #ready state
        warningState(rcv)            #warning state
        failureState(rcv)            #failure state
        log(file, rcv)               #Logging
        stepper.rotate(5760,'cw')    #stepper movement 360*16 = 5760
        stepper.rotate(360,'ccw')   #stepper movement ccw
        
        


