import colorsys

import mido

import controller

ctrl = controller.Controller("cloud.itsw.es", "password")

with mido.open_input("vibrance", virtual=True) as inport:
    for msg in inport:
        print("msg", msg)
        if msg.type == "note_on":
            port = msg.channel + 9001
            note = msg.note % 12
            octave = msg.note // 12
            hue = note / 12
            saturation = octave / 9
            value = msg.velocity / 127

            red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
            red = int(red * 255)
            green = int(green * 255)
            blue = int(blue * 255)
            colorstring = f"{format(red, '02x')}{format(green, '02x')}{format(blue, '02x')}"
            print(colorstring)
            ctrl.setColor(port, colorstring)
            ctrl.write()
            

