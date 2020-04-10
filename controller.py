import socket
import json
import ssl

class Controller:
    def __init__(self, relay, password=None, enable_ssl=True):
        self.colors = {port: "000" for port in range(9001, 9007)}
        self.relay = relay
        if enable_ssl:
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            self.context.load_default_certs()
            unwrapped_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket = self.context.wrap_socket(unwrapped_socket, server_hostname=relay)
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((relay, 9100))
        if password:
            self.socket.send(password.encode("utf-8"))
            ret = self.socket.recv(1024)
            if ret == b"OK":
                return
            else:
                raise ValueError("authentication failed")

    def setColor(self, port, color):
        self.colors[port] = color

    def write(self):
        self.socket.send((json.dumps(self.colors)+"\n").encode("utf-8"))
        self.colors = {}
        return self.socket.recv(1024).decode("utf-8")
