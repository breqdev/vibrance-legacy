import requests
import json

class Controller:
    def __init__(self, relay, username=None, password=None):
        self.colors = {port: "000" for port in range(9001, 9007)}
        self.relay = relay
        if username is not None:
            self.auth = (username, password)
        else:
            self.auth = None

    def setColor(self, port, color):
        self.colors[port] = color

    def write(self):
        print(f"Sending JSON object {self.colors}")
        requests.post(self.relay, json=self.colors, auth=self.auth)
