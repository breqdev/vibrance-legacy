import time
import colorsys

import mido

with mido.open_output("vibrance") as outport:
    while True:
        port = int(input("Channel> "))
        hexcode = int(input("Color> "), base=16)
        red = (hexcode & 0xFF0000) >> 16
        green = (hexcode & 0x00FF00) >> 8
        blue = hexcode & 0x0000FF

        hue, saturation, value = colorsys.rgb_to_hsv(red/255, green/255, blue/255)
        
        msg = mido.Message("note_on")
        msg.channel = port
        msg.note = int(hue * 12 + int(saturation*9) * 12)
        msg.velocity = int(value * 127)

        print("msg", msg)
        
        outport.send(msg)
        time.sleep(1)
