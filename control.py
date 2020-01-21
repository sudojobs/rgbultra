import RPi.GPIO as GPIO
import time
import os
import signal
import sys

class RGBLEDs:
	RED = 9
	YELLOW = 10
	GREEN = 11

class LEDStates:
        INIT   = 1
	GREEN  = 2
	RED    = 3
	YELLOW = 4

class Ultra:
      ECHO = 24
      TRIGGER = 18

currentState = LEDStates.INIT
count  = 0
pre_val= 0
val    = 0
debug  = 1
GPIO.setmode(GPIO.BCM)
GPIO.setup(Ultra.ECHO,GPIO.IN)
GPIO.setup(Ultra.TRIGGER,GPIO.OUT)

def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

while True:
        if (debug == 1):
            print("Getting Ultrasonic Value")
        val=distance()
        f=open("data.txt", "a+")
        f.write("This is Value: %d\r\n" % (val)) 
	f.close()
        count=count + 1
        if (debug == 1):
            print(count)
        if (currentState == LEDStates.INIT):
	     # Setup Hardware
             GPIO.setwarnings(False)
	     GPIO.setmode(GPIO.BCM)
             GPIO.setup(RGBLEDs.RED, GPIO.OUT)
             GPIO.setup(RGBLEDs.YELLOW, GPIO.OUT)
             GPIO.setup(RGBLEDs.GREEN, GPIO.OUT)
             currentState = LEDStates.GREEN
             print("INIT STATE")
        elif (currentState == LEDStates.GREEN):
	     GPIO.output(RGBLEDs.RED, False)
	     GPIO.output(RGBLEDs.YELLOW, False)
	     GPIO.output(RGBLEDs.GREEN, True)
	     time.sleep(1)
             if (debug == 1):
                 print("GREEN STATE")
             if (count == 31):
		currentState = LEDStates.YELLOW
                count = 0
             elif(val==pre_val):
		currentState = LEDStates.GREEN
        elif (currentState == LEDStates.YELLOW):
	     GPIO.output(RGBLEDs.RED, False)
	     GPIO.output(RGBLEDs.YELLOW, True)
	     GPIO.output(RGBLEDs.GREEN, False)
	     time.sleep(1)
             if (debug == 1):
                 print("YELLOW STATE")
             if (count == 31):
	         currentState = LEDStates.RED
                 count = 0
             elif (val!=pre_val):
	         currentState = LEDStates.GREEN
                 count = 0
             else:
		 currentState = LEDStates.YELLOW
	elif (currentState == LEDStates.RED):
		GPIO.output(RGBLEDs.RED, True)
		GPIO.output(RGBLEDs.YELLOW, False)
		GPIO.output(RGBLEDs.GREEN, False)
                if (debug == 1):
                    print("RED STATE")
		time.sleep(1)
                if (val!=pre_val):
		   currentState = LEDStates.GREEN
                   count = 0
                else: 
		   currentState = LEDStates.RED
		
	else:
		print 'Invalid state!'

        pre_val=val; 
