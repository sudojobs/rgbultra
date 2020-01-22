import RPi.GPIO as GPIO
import time
import os
import signal
import sys

class RGBLEDs:
	RED = 13
	YELLOW = 26
	GREEN = 19

class LEDStates:
        INIT   = 1
	GREEN  = 2
	YELLOW = 3
	RED    = 4

GPIO_ECHO = 24
GPIO_TRIGGER = 23

currentState = LEDStates.INIT
count  = 0
pre_val= 0
debug  = 1
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_ECHO,GPIO.IN)
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)


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

try:
  while True:
        val=round(distance(),0)
        if (debug == 1):
            abs_val=abs(pre_val-val) 
            print("Current_State : %s Ultrasonic Value : %d Previous Value :%d Count Value:%d modulus:%d" % (currentState,val,pre_val,count,abs_val))  
        time.sleep(1)
        f=open("data.txt", "a+")
        f.write("This is Value: %d\r\n" % (val)) 
	f.close()
        count=count + 1
        if (currentState == LEDStates.INIT):
	     # Setup Hardware
             GPIO.setup(RGBLEDs.RED, GPIO.OUT)
             GPIO.setup(RGBLEDs.YELLOW, GPIO.OUT)
             GPIO.setup(RGBLEDs.GREEN, GPIO.OUT)
             currentState = LEDStates.GREEN
        elif (currentState == LEDStates.GREEN):
	     GPIO.output(RGBLEDs.RED, True)
	     GPIO.output(RGBLEDs.YELLOW, False)
	     GPIO.output(RGBLEDs.GREEN, True)
             if (count == 31):
		currentState = LEDStates.YELLOW
                count = 0
             elif(abs_val>2):
		currentState = LEDStates.GREEN
                count = 0
        elif (currentState == LEDStates.YELLOW):
	     GPIO.output(RGBLEDs.RED, True)
	     GPIO.output(RGBLEDs.YELLOW, True)
	     GPIO.output(RGBLEDs.GREEN, False)
             if (count == 31):
	         currentState = LEDStates.RED
                 count = 0
             elif (abs_val>2):
	         currentState = LEDStates.GREEN
                 count = 0
             else:
		 currentState = LEDStates.YELLOW
	elif (currentState == LEDStates.RED):
		GPIO.output(RGBLEDs.RED, False)
		GPIO.output(RGBLEDs.YELLOW, True)
		GPIO.output(RGBLEDs.GREEN, True)
                if (abs_val>2):
		   currentState = LEDStates.GREEN
                   count = 0
                else: 
		   currentState = LEDStates.RED
		
	else:
		print 'Invalid state!'

        pre_val=val


except KeyboardInterrupt:
	print "Keyboard Interrupt Occured"


finally:
    GPIO.cleanup()
