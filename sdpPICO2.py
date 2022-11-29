from machine import Pin, UART
import time, utime
from time import sleep, sleep_ms, sleep_us

# Random number generator for testing
import random


# ADC and variables for laser counter
analog_value = machine.ADC(28)
threadCount = 0
high = False
low = False

# LED for status
statusLED = Pin(25, Pin.OUT)
greenLED = Pin(0, Pin.OUT)
yellowLED = Pin(2, Pin.OUT)
redLED = Pin(4, Pin.OUT)

#UART 0: Communication channel
uart0 = UART(0, baudrate=115200, tx=Pin(16), rx=Pin(17), bits=8, parity=None, stop=1)
#UART 0: Communication channel
# uart1 = UART(1, baudrate=115200, tx=Pin(8), rx=Pin(9), bits=8, parity=None, stop=1)


# File for logging
file = open("test.txt", "w")


def passState(rcv):
    if rcv == b"pass":    #binary encoded string b"string"
        greenLED.value(1)
        redLED.value(0)
        yellowLED.value(0)
        
def countState(rcv):
    if rcv == b"blank":
        yellowLED.value(1)
        greenLED.value(0)
        redLED.value(0)

def failureState(rcv):
    if rcv == b"fail":
        redLED.value(1)
        greenLED.value(0)
        yellowLED.value(0)
        
def log(file, x, rcv):
    file.write(x + ' ' + str(rcv) + '\n')
    file.flush()
    
# statusLED to report ready condition
statusLED.value(1)

#
while True:
    
    # testing UART and led with counter(very slow)
#     x = random.randint(0,1)
#     print(x)
#     if x == 0:
#         uart0.write('pass')
#     if x == 1:
#         uart0.write('fail')
    
    # yellow to show threadCounter
    yellowLED.value(1)
    
    # read ADC
    reading = analog_value.read_u16()
    time.sleep(0.25)
    
#     print("ADC: ", reading)			#debugging ADC reading
    
    if reading > 60000:
        high = True
        time.sleep(0.025)				# timing for falling edge
        reading = analog_value.read_u16()
        if reading < 60000:
            low = True
            high = False
            time.sleep(0.025)			# timing for rising edge
            reading = analog_value.read_u16()
            if reading > 60000 and low == True:
                threadCount += 1
                low = False
                yellowLED.value(0)
                time.sleep(0.05)		# show yellow blink
                

#     print('threads ' + str(threadCount)) 				#debugging threads
    
    # statusLED will flash during communication
    if uart0.any() > 0:
        statusLED.toggle()
        rcv = uart0.read(4)			 #need to be aware of buffer size
        
#         print(rcv)					 #debugging UART
        
        passState(rcv)              #ready state
        countState(rcv)            #warning state
        failureState(rcv)            #failure state
        
        uart0.write(str(threadCount))# write threadCount to Nano
        
