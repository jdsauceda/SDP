from machine import Pin, UART
import time, utime
from time import sleep


# Random number generator for testing
# import random


# ADC and variables for laser counter
analog_value = machine.ADC(28)
oldThreadCount = 0
newThreadCount = 0
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
file = open("count.txt", "w")


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
        
def log(file, oldThreadCount, newThreadCount):
    if newThreadCount >= oldThreadCount:
        file.write(str(newThreadCount) + '\n')
        file.flush()
    
    
# statusLED to report ready condition
statusLED.value(1)

#
while True:
       
    # yellow to show threadCounter
    yellowLED.value(1)
    
    # read ADC
    reading = analog_value.read_u16()
    time.sleep(0.25)
    
    print("ADC: ", reading)                  #debugging ADC reading
    
    if reading > 9800: # value from photodiode
        high = True
        time.sleep(0.1)                       # timing for falling edge
        reading = analog_value.read_u16()
        if reading < 9800:
            low = True
            high = False
            time.sleep(0.1)                   # timing for rising edge
            reading = analog_value.read_u16()
            if reading > 9800 and low == True:
                oldThreadCount = newThreadCount
                newThreadCount += 1
                log(file, oldThreadCount, newThreadCount)        #log threadCount
                low = False
                yellowLED.value(0)
                time.sleep(0.05)                # show yellow blink
                

    print('threads ' + str(newThreadCount))      #debugging threads
    
    # statusLED will flash during communication
    if uart0.any():
        statusLED.toggle()
        rcv = uart0.read(4)              #need to be aware of buffer size
        
#         print(rcv)                     #debugging UART
        
        passState(rcv)                   #ready state
        countState(rcv)                  #warning state
        failureState(rcv)                #failure state
#        uart0.write(str(newThreadCount))    #write threadCount to Nano
        

