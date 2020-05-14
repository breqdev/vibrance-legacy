import midi_api
import notemap

api = midi_api.Interface("cloud.itsw.es")

@api.onAny
def test(msg):
    print(msg)
    if msg.type == "note_on":
        octNote = msg.note % 12
        octave = msg.note // 12

        if octave > 9:
            return midi_api.NoUpdate() # Reserved for future use

        color = notemap.PALETTE[octNote]
        zones = notemap.ZONEMAP[octave]

        for i, zone in enumerate(zones):
            if zone:
                api.add(i+9001, color)
            elif msg.velocity > 75:
                api.add(i+9001, "000000")

@api.onTelemetry
def onTelemetry(telemetry):
    print(telemetry)

api.run()
