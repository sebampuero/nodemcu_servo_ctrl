import pigpio

x_pin_bcm = 27
y_pin_bcm = 22
pi = None

def servoSetup():
    try:
        global pi
        pi = pigpio.pi()
        pi.set_mode(x_pin_bcm, pigpio.OUTPUT)
        pi.set_mode(y_pin_bcm, pigpio.OUTPUT)
    except Exception as e:
        print(e)
        pi.stop()
        exit()

def updateServos(x, y):
    duty_cycle_x = -10 * (x) + 2450
    duty_cycle_y = -10 * (y) + 2450
    pi.set_servo_pulsewidth(x_pin_bcm, duty_cycle_x)
    pi.set_servo_pulsewidth(y_pin_bcm, duty_cycle_y)

def clean():
    pi.stop()
