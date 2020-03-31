#!/usr/bin/env python3

import subprocess as sb
import pigpio
import sys
import time
import os
import fcntl as F

def set_burner(power_level,GPIO_PIN=17,
               MAX_PULSE=1850, #this map to min gas
               MIN_PULSE=1105, #this map to max gas
               OFF_PULSE=2500,
               IGNITION_PULSE=850,state_filename='burner_state'):

    try:
    	with open(state_filename, 'r') as state_file:
            previous_state=state_file.read()
    except:
        previous_state='OFF'
    
    if power_level==0:
        pulse_width=OFF_PULSE
    else:
        pulse_width=(100-power_level)/100.0 *(MAX_PULSE-MIN_PULSE)+MIN_PULSE
        
        
    if pulse_width<2500:
        state='ON'
    else:
        state='OFF'
           
    pi.set_servo_pulsewidth(GPIO_PIN, pulse_width) 
    
    if previous_state=='OFF' and state=='ON':
        time.sleep(1.0)
        pi.set_servo_pulsewidth(GPIO_PIN, IGNITION_PULSE)
        time.sleep(0.5)
        pi.set_servo_pulsewidth(GPIO_PIN, pulse_width)
        
    with open(state_filename, 'w+') as state_file:
        state_file.write(state)
        
    return pulse_width
    
    
    
if __name__== "__main__":
    
    #sb.call('sudo pigpiod',shell=True)
    pi = pigpio.pi()
    
    try:
        power_level=int(sys.argv[1])
    except:
        print('you need to provide a number between 0 and 100')
        sys.exit(1)
    power_level=max(0,min(power_level,100))
    set_burner(power_level,state_filename='/home/pi/Kaka_PID_Control/burner_state')


