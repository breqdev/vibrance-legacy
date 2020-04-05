import requests
import json

class Controller:
    def __init__(self):
        self.colors = {port: "000" for port in range(9001, 9007)}

    def setColor(self, port, color):
        self.colors[port] = color

    def write(self):
        print(f"Sending JSON object {self.colors}")
        requests.post("http://cloud.itsw.es:9100/", json=self.colors)
