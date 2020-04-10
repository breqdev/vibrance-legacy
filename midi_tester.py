import colorsys

import mido

while True:
    with mido.open_output("vibrance") as outport:
        while True:
            note = int(input("Note> "))
            velocity = int(input("Vel> "))

            msg = mido.Message("note_on")
            msg.note = note
            msg.velocity = velocity

            if outport.closed:
                break

            outport.send(msg)
