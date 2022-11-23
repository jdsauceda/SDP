from machine import Pin
from time import sleep_ms
from time import sleep_us


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

stepper = STEPMOTOR(step_pin=19, dir_pin=18)


# The following lines of codes can be tested using the REPL:
# 1. To rotate the stepper motor in clockwise direction:
# stepper.rotate(360, 'cw')
# The first parameter, sets the angle of rotation
# The second parameter, sets the direction

# 2. To rotate it in counter clockwise direction:
# stepper.rotate(360, 'ccw')
