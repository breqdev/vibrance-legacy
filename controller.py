import socket
import json

class Controller:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("cloud.itsw.es", 9000))

    def setColor(self, port, color, delay=0):
        self.sock.send((json.dumps({
            "port":port, "color":color, "delay":delay
            })+"\n").encode("utf-8"))
