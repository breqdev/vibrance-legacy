import colorsys

import mido

import controller
import notemap

ctrl = controller.Controller("cloud.itsw.es", "password")

with mido.open_input("vibrance", virtual=True) as inport:
    for msg in inport:
        print("msg", msg)
        if msg.type == "note_on":
            octNote = msg.note % 12
            octave = msg.note // 12

            if octave > 9:
                continue # Reserved for future use

            color = notemap.PALETTE[octNote]
            zones = notemap.ZONEMAP[octave]

            for i, zone in enumerate(zones):
                if zone:
                    ctrl.setColor(i+9001, color)
            ctrl.write()
