import socket
import select
import json
import time
import os
import shutil
import subprocess

server_socks = {}
clients = {}

for port in range(9001, 9007):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("0.0.0.0", port+100))
    sock.listen(16)
    server_socks[port] = sock
    clients[sock] = [sock]
    # Start the websockify
    subprocess.Popen(["websockify", str(port), f"localhost:{port+100}"])

# Input server
input_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
input_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
input_sock.bind(("0.0.0.0", 9000))
input_sock.listen(16)
input_clients = [input_sock]

def pushColorToClients(port, color, delay):
    print(f"Sending color {color} to clients on port {port} after {delay} sec")
    global clients, server_socks

    server_sock = server_socks[port]

    changeTime = time.time() + delay

    for client in clients[server_sock]:
        if client is not server_sock:
            clientSpecificDelay = (changeTime - time.time()) * 1000
            try:
                print("Sending to client...")
                client.send(json.dumps(["#"+color, clientSpecificDelay]).encode("utf8"))
            except Exception as e:
                print("Failed to send to client", e)
                client.close()
                clients[server_sock].remove(client)


while True:
    # Handle output servers
    for port, server_sock in server_socks.items():
        read_sockets = select.select(clients[server_sock], [], [], 0)[0]

        for sock in read_sockets:
            if sock is server_sock:
                # New client connected
                new_client, addr = server_sock.accept()
                clients[server_sock].append(new_client)
                print(f"New client on port {port}")
            else:
                # Message from existing client
                # Ignore
                pass

    # Handle input servers
    read_sockets = select.select(input_clients, [], [], 0)[0]
    for sock in read_sockets:
        if sock is input_sock:
            # New input client
            new_client, addr = input_sock.accept()
            input_clients.append(new_client)
            print(f"New input client from {addr}")
        else:
            # New message from input client
            try:
                data = sock.recv(1024)
                if data:
                    message = data.decode()
                    print(f"Received {message} from input client")
                    for line in message.partition("\n"):
                        try:
                            obj = json.loads(line)
                            pushColorToClients(obj["port"], obj["color"], obj["delay"])
                        except json.JSONDecodeError:
                            print("Failed to deocde JSON")
            except Exception as e:
                print("Recv failed: "+str(e))
