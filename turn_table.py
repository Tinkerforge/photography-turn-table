#!/usr/bin/env python
# -*- coding: utf-8 -*-  

HOST = "localhost"
PORT = 4223
UID_STEPPER = "6kqBVU" 
UID_QUAD_RELAY = "mT6"

from tinkerforge.ip_connection import IPConnection
from tinkerforge.brick_stepper import Stepper
from tinkerforge.bricklet_industrial_quad_relay import IndustrialQuadRelay

import time
import threading
import signal

STEP_MODE = 8

# Change this value to change the number of pictures taken
STEPS_PER_ROTATION = 10*STEP_MODE
FULL_ROTATION = 200*STEP_MODE

steps = 0
lock = threading.Lock()

signal.signal(signal.SIGINT, signal.SIG_DFL)

def take_photo():
    print "Waiting for rotation to stop"
    time.sleep(1)
    print "Taking Photo"
    iqr.set_value(0xFF)
    time.sleep(0.5)
    iqr.set_value(0)

def cb_reached(stepper, ipcon, position):
    global steps
    global lock

    take_photo()

    steps += STEPS_PER_ROTATION
    if steps >= FULL_ROTATION:
        lock.release()
        return

    print "Starting next rotation: " + str(steps/STEP_MODE*1.8) + "°"
    print
    stepper.set_steps(STEPS_PER_ROTATION)

    
if __name__ == "__main__":
    ipcon = IPConnection() # Create IP connection
    stepper = Stepper(UID_STEPPER, ipcon) # Create device object
    iqr = IndustrialQuadRelay(UID_QUAD_RELAY, ipcon)

    ipcon.connect(HOST, PORT) # Connect to brickd
    # Don't use device before ipcon is connected

    stepper.full_brake()
    stepper.disable()

    stepper.set_motor_current(1000) 
    stepper.set_step_mode(STEP_MODE) 
    stepper.set_max_velocity(100)

    stepper.set_speed_ramping(25, 25) 

    stepper.register_callback(stepper.CALLBACK_POSITION_REACHED, lambda x: cb_reached(stepper, ipcon, x))
    stepper.enable()
    stepper.set_steps(1)

    lock.acquire()
    lock.acquire()

    stepper.disable()
    ipcon.disconnect()
