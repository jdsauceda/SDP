from machine import Pin, UART
import time, utime
from time import sleep, sleep_ms, sleep_us

# ADC for laser counter
analog_value = machine.ADC(28)
digitalCount = 0
high = True

# LED for status 
greenLED = Pin(0, Pin.OUT)
yellowLED = Pin(2, Pin.OUT)
redLED = Pin(4, Pin.OUT)

#UART 1: Communication channel with motor
uart0 = UART(0, baudrate=115200, tx=Pin(16), rx=Pin(17), bits=8, parity=None, stop=1)
sleep(1)

# File for logging
file = open("test.txt", "w")

# Photodiode input reading
# def pdiode(reading,digitalCount):
#     if high == True:
#         reading = analog_value.read_u16()
#         print("ADC: ", reading)
#         utime.sleep(0.05)
#         if reading <= 10000:
#             while reading <= 10000:
#                 reading = analog_value.read_u16()
#                 utime.sleep(0.05)
#                 if reading >= 10000:
#                     digitalCount += 1
                    


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
        
def log(file, x, rcv):
    file.write(x + ' ' + str(rcv) + '\n')
    file.flush()

# Loop
while True:
    if high == True:
        reading = analog_value.read_u16()
        print("ADC: ", reading)
        utime.sleep(0.05)
        if reading <= 9800:
            while reading <= 9800:
                reading = analog_value.read_u16()
                utime.sleep(0.05)
                if uart0.any() > 0:
                     rcv = uart0.read()
                     readyState(rcv)              #ready state
                     warningState(rcv)            #warning state
                     failureState(rcv)            #failure state
                     x = time.time()
                     print(str(x) + ' ' + str(rcv))
                     log(file, str(x), rcv)               #Logging
                if reading >= 9800:
                    digitalCount += 1
    print(digitalCount)
    # Read incoming UART
    if uart0.any() > 0:
         rcv = uart0.read()
         readyState(rcv)              #ready state
         warningState(rcv)            #warning state
         failureState(rcv)            #failure state
         x = time.time()
         print(str(x) + ' ' + str(rcv))
         log(file, str(x), rcv)               #Logging
        



