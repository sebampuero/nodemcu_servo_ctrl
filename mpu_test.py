import struct
import socket
import math
from servo import servoSetup, updateServos, clean
from display import displaySetup, printMsg

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host = "0.0.0.0"
port = 8088

s.bind((host, port))

print("Listening on {0}:{1}".format(host, port))

try:
    servoSetup()
    displaySetup()
    while True:
        data = s.recv(1024)
        Y = data[:len(data)//2] # // forces int division in Python3
        X = data[len(data)//2:]
        roll = float(struct.unpack('f', X)[0]) + 90.0 # convert byte array into float
        pitch = float(struct.unpack('f', Y)[0]) + 90.0 # add 90 bc esp8266 sends angles -90 -> 90
        if math.isnan(roll) or math.isnan(pitch):
          printMsg("h0la") 
          print("RESET")
        else: 
           print("ROLL: " + str(int(roll)) + "degrees PITCH: " + str(int(pitch)) + "degrees")
           printMsg(str(int(roll)))
           updateServos(int(roll), int(pitch))  
finally:
    clean()
    
