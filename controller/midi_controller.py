import colorsys
import time
import os

import mido

import controller
import notemap

ctrl = controller.Controller("cloud.itsw.es")

# Find Vibrance Port
if os.name == "posix":
    # macOS or Linux systems
    # Just create a virtual port
    inport = mido.open_input("vibrance", virtual=True)
elif os.name == "nt":
    # Windows system
    # Rely on external MIDI loopback software
    inport = mido.open_input("vibrance_loopback 3")
else:
    raise ValueError("unsupported OS")

try:
    for msg in inport:
        print(msg)
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
                elif msg.velocity > 75:
                    ctrl.setColor(i+9001, "000000")
            print("Writing...", end="")
            ts = time.time()
            ctrl.write()
            print(int((time.time()-ts)*1000), "ms")
finally:
    inport.close()
