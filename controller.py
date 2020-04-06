import socket
import json

class Controller:
    def __init__(self, relay):
        self.colors = {port: "000" for port in range(9001, 9007)}
        self.relay = relay
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((relay, 9100))

    def setColor(self, port, color):
        self.colors[port] = color

    def write(self):
        self.socket.send((json.dumps(self.colors)+"\n").encode("utf-8"))
