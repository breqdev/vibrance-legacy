import controller
import math
import time

ctrl = controller.Controller("cloud.itsw.es")

def getColor(radians):
    red = 0x80 + int(0x79*math.sin(radians))
    green = 0x80 + int(0x79*math.sin(radians+math.pi*2/3))
    blue = 0x80 + int(0x79*math.sin(radians+math.pi*4/3))
    return f"{format(red, '02x')}{format(green, '02x')}{format(blue, '02x')}"

frame = 0
while True:
    ctrl.setColor(9001, getColor(frame/2))
    ctrl.setColor(9002, getColor(frame/2+math.pi*1/3))
    ctrl.setColor(9003, getColor(frame/2+math.pi*2/3))
    ctrl.setColor(9004, getColor(frame/2+math.pi))
    ctrl.setColor(9005, getColor(frame/2+math.pi*4/3))
    ctrl.setColor(9006, getColor(frame/2+math.pi*5/3))
    ts = time.time()
    print("Sending update... ")
    ctrl.write()
    print(f"{int((time.time()-ts)*1000)} ms")
    frame += 1
    time.sleep(1 + ts - time.time())
