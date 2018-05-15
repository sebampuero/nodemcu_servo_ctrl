import time
import RPi.GPIO as GPIO

num = {' ':(1,1,1,1,1,1,1),
    '0':(0,0,0,0,0,0,1),
    '1':(1,0,0,1,1,1,1),
    '2':(0,0,1,0,0,1,0),
    '3':(0,0,0,0,1,1,0),
    '4':(1,0,0,1,1,0,0),
    '5':(0,1,0,0,1,0,0),
    '6':(0,1,0,0,0,0,0),
    '7':(0,0,0,1,1,1,1),
    '8':(0,0,0,0,0,0,0),
    '9':(0,0,0,0,1,0,0),
    'c':(0,1,1,0,0,0,1),
    'e':(0,1,1,0,0,0,0),
    'g':(0,0,1,1,1,0,0),
    'b':(1,1,0,0,0,0,0),
    'h':(1,0,0,1,0,0,0),
    'd':(1,0,0,0,0,1,0),
    'f':(0,1,1,1,0,0,0),
    'l':(1,1,1,0,0,0,1),
    'a':(0,0,0,1,0,0,0)}

# GPIO ports for the 7seg pins
segments =  (10, 23, 18, 24, 26, 15, 16, 22)
digits = (8, 19, 21, 12)
# 7seg_segment_pins (11,7,4,2,1,10,5,3) +  100R inline

def displaySetup():
   #  GPIO.setmode(GPIO.BOARD)
    for segment in segments:
        GPIO.setup(segment, GPIO.OUT)
        GPIO.output(segment, 1)
    for digit in digits:
        GPIO.setup(digit, GPIO.OUT)
        GPIO.output(digit, 0)

def printMsg(message):
    s = str(message).rjust(len(message))
    digit_range = len(s)
    for digit in range(digit_range):
        for loop in range(0,7):
            GPIO.output(segments[loop], num[s[digit]][loop])
        GPIO.output(digits[digit], 1)
        time.sleep(0.001)
        GPIO.output(digits[digit], 0)

