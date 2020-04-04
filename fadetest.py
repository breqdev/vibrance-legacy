import controller
import math
import time

ctrl = controller.Controller()

frame = 0
while True:
    red = 0x80 + int(0x79*math.sin(frame/10))
    green = 0x80 + int(0x79*math.sin(frame/10 + math.pi*2/3))
    blue = 0x80 + int(0x79*math.sin(frame/10 + math.pi*4/3))
    color = f"{format(red, '02x')}{format(green, '02x')}{format(blue, '02x')}"
    for port in range(9001, 9007):
        ctrl.setColor(port, color)
    ctrl.write()
    frame += 1
    time.sleep(0.1)
