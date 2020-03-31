#!/usr/bin/env python3

import subprocess as sb
import pigpio
import sys
import time
import os
import fcntl as F
import errno

def set_burner(power_level,GPIO_PIN=17,
               MAX_PULSE=1900, #this map to min gas
               MIN_PULSE=1055, #this map to max gas
               OFF_PULSE=2500,
               IGNITION_PULSE=850,state_filename='burner_state'):
    
    
    with open(state_filename, "r+") as state_file:

        F.flock(state_file, F.LOCK_EX)
        previous_state=state_file.read()

        if power_level==0:
            pulse_width=OFF_PULSE
        else:
            pulse_width=(100-power_level)/100.0 *(MAX_PULSE-MIN_PULSE)+MIN_PULSE

        if pulse_width<2500:
            state='ON'
        else:
            state='OFF'
        
        print( 'Previous State:',previous_state,'Current State:',state)
        pi.set_servo_pulsewidth(GPIO_PIN, pulse_width) 

        if previous_state=='OFF' and state=='ON':
            print('Ignition!')
            time.sleep(1.0)
            pi.set_servo_pulsewidth(GPIO_PIN, IGNITION_PULSE)
            time.sleep(0.5)
            pi.set_servo_pulsewidth(GPIO_PIN, pulse_width)
        else:
            print('No ignition necessary we were already [%s]' % previous_state)
        state_file.seek(0)
        state_file.truncate(0)
        state_file.write(state)
        
        print('Success!')
        return pulse_width

    
if __name__== "__main__":
    
    pi = pigpio.pi()
    
    try:
        power_level=int(sys.argv[1])
    except:
        print('you need to provide a number between 0 and 100')
        sys.exit(1)
    power_level=max(0,min(power_level,100))
    
    state_filename='/home/pi/Kaka_PID_Control/burner_state'
    
    #if the file doesn't exist we create it and exit
    if not os.path.exists(state_filename):
        with open(state_filename,'w+') as state_file:
            F.flock(state_file, F.LOCK_EX)
            state_file.write('OFF')
            print('State file was not present, creating it...')

    
    set_burner(power_level,state_filename=state_filename)


