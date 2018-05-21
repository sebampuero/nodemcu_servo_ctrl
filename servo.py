import RPi.GPIO as GPIO

servoXpin = 13
servoYpin = 15
servoY = 0
servoX = 0


def servoSetup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servoYpin, GPIO.OUT)
    GPIO.setup(servoXpin, GPIO.OUT)
    global servoY
    servoY = GPIO.PWM(servoYpin, 50)
    servoY.start(6.5)
    global servoX
    servoX = GPIO.PWM(servoXpin, 50)
    servoX.start(6.5)

def updateServos(x, y):
    DCX = -1.0/18.0 * (x) + 12
    DCY = -1.0/18.0 * (y) + 12
    servoY.ChangeDutyCycle(DCY)
    servoX.ChangeDutyCycle(DCX)
    
def clean():
    servoY.stop()
    servoX.stop()
    GPIO.cleanup()
