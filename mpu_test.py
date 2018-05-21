import struct
import socket
import math
from servo_hw import servoSetup, updateServos, clean
#from display import displaySetup, printMsg

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = "0.0.0.0"
port = 8088

s.bind((host, port))

print("Listening on {0}:{1}".format(host, port))

try:
    servoSetup()
   # displaySetup()
    while True:
        data = s.recv(16)
        Y = data[0]
        X = data[1]
        # NOTE: NODEMCU HAS TO FILTER NAN VALUES
        # print("ROLL: " + str(X) + "degrees PITCH: " + str(Y) + "degrees")
        # printMsg(str(int(roll)))
        updateServos(X, Y)
finally:
    clean()
    
