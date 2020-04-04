from functools import partial
import socket
import json
import tkinter as tk

root = tk.Tk()

entries = {}
colorvars = {}
buttons = {}

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("10.0.1.170", 9000))

def sendColor(port):
    sock.send(json.dumps({"port":port, "color":colorvars[port].get(), "delay":0}).encode("utf-8"))

for port in range(9001, 9007):
    colorvars[port] = tk.StringVar()
    entries[port] = tk.Entry(root, textvariable=colorvars[port])
    buttons[port] = tk.Button(root, text="SEND", command=partial(sendColor, port))

for i, entry in enumerate(entries.values()):
    entry.grid(row=0, column=i)

for i, button in enumerate(buttons.values()):
    button.grid(row=1, column=i)

root.mainloop()
