import controller
import json
import readline
import os
import atexit

histfile = os.path.join(os.path.expanduser("~"), ".vibrance_history")
try:
    readline.read_history_file(histfile)
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length(1000)
except FileNotFoundError:
    pass

atexit.register(readline.write_history_file, histfile)

ctrl = controller.Controller("cloud.itsw.es")

while True:
    i = input("Messages> ")
    ctrl.messages = json.loads(i)
    ctrl.write()
