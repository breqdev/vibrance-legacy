import socket
import json

class Controller:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("cloud.itsw.es", 9000))
        self.buffer = []

    def setColor(self, port, color, delay=0):
        self.buffer.append((json.dumps({
            "port":port, "color":color, "delay":delay
            })+"\n").encode("utf-8"))

    def write(self):
        self.sock.send(b"".join(self.buffer))
        self.buffer = []
