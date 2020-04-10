import controller
import json

ctrl = controller.Controller("cloud.itsw.es", "password")

while True:
    i = input("Messages> ")
    ctrl.messages = json.loads(i)
    ctrl.write()
