import colorsys

def rgb_to_note(hexcode):
    red = (hexcode & 0xFF0000) >> 16
    green = (hexcode & 0x00FF00) >> 8
    blue = hexcode & 0x0000FF

    hue, saturation, value = colorsys.rgb_to_hsv(red/255, green/255, blue/255)

    note = int(hue * 12 + int(saturation*9) * 12)
    velocity = int(value * 127)
    return note, velocity

def note_to_rgb(note, velocity):
    noteInOct = note % 12
    octave = note // 12
    hue = noteInOct / 12
    saturation = octave / 9
    value = velocity / 127

    red, green, blue = colorsys.hsv_to_rgb(hue, saturation, value)
    red = int(red * 255)
    green = int(green * 255)
    blue = int(blue * 255)
    return f"{format(red, '02x')}{format(green, '02x')}{format(blue, '02x')}"

if __name__ == "__main__":
    import tkinter as tk

    root = tk.Tk()

    inputVar = tk.StringVar()

    inputLabel = tk.Label(root, anchor=tk.W, text="Hex: ")
    inputEntry = tk.Entry(root, textvariable=inputVar)

    actualLabel = tk.Label(root, text="Actual Color")
    approxLabel = tk.Label(root, text="Approx Color")

    approxHexLabel = tk.Label(root, anchor=tk.W, text="Approx: ")
    noteLabel = tk.Label(root, anchor=tk.W, text="Note: ")
    velLabel = tk.Label(root, anchor=tk.W, text="Vel: ")

    approxHexVar = tk.StringVar()
    noteVar = tk.StringVar()
    velVar = tk.StringVar()

    approxHexDisp = tk.Label(root, textvariable=approxHexVar)
    noteDisp = tk.Label(root, textvariable=noteVar)
    velDisp = tk.Label(root, textvariable=velVar)

    inputLabel.grid(row=0, column=0)
    inputEntry.grid(row=0, column=1)
    actualLabel.grid(row=1, column=0, columnspan=2)
    approxLabel.grid(row=2, column=0, columnspan=2)
    approxHexLabel.grid(row=3, column=0)
    approxHexDisp.grid(row=3, column=1)
    noteLabel.grid(row=4, column=0)
    noteDisp.grid(row=4, column=1)
    velLabel.grid(row=5, column=0)
    velDisp.grid(row=5, column=1)

    def update(ignore):
        hex = inputVar.get()
        note, vel = rgb_to_note(int(hex.lstrip("#"), base=16))
        noteVar.set(note)
        velVar.set(vel)
        approxHex = note_to_rgb(note, vel)
        approxHexVar.set(approxHex)

        actualHex = hex if hex.startswith("#") else "#"+hex
        actualLabel.configure(bg = actualHex)
        approxLabel.configure(bg = "#"+approxHex)

    inputEntry.bind("<Return>", update)

    root.mainloop()
