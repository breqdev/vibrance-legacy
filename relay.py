import socket
import select
import subprocess
import atexit
import time
import json
import threading
from multiprocessing.dummy import Pool as ThreadPool
from flask import Flask, request

app = Flask(__name__)


ports = list(range(9001, 9007))
colors = {str(port): "000" for port in ports}
servers = []
port_of_server = {}
clients = []
port_of_client = {}
lastMessage = {}
websockify_procs = []

for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port+100))
    sock.listen(16)
    servers.append(sock)
    port_of_server[sock] = port

def shutdownServerSocks():
    for sock in servers:
        sock.close()
atexit.register(shutdownServerSocks)

for port in ports:
    # Start the websockify
    websockify_procs.append(subprocess.Popen(["websockify", str(port), f"localhost:{port+100}"]))

def shutdownWebsockifys():
    for proc in websockify_procs:
        proc.terminate()
atexit.register(shutdownWebsockifys)

# Dealing with clients
def removeClient(client):
    client.close()
    clients.remove(client)
    del lastMessage[client]

def handleIncomingLoop():
    print("Starting handle incoming connections thread")
    while True:
        read_servers = select.select(servers, [], [], 0.1)[0]
        for sock in read_servers:
            # New client
            port = port_of_server[sock]
            new_client, addr = sock.accept()
            clients.append(new_client)
            port_of_client[new_client] = port
            lastMessage[new_client] = time.time()
            print(f"New client from {addr} on port {port}")

def handleAcknowledgeLoop():
    print("Starting handle acknowledge thread")
    while True:
        read_clients = select.select(clients, [], [], 0.1)[0]
        for sock in read_clients:
            # New message from client
            try:
                data = sock.recv(1024)
                if data:
                    message = data.decode()
                    # print(f"Received {message} from {sock.getpeername()}")
                    lastMessage[sock] = time.time()
            except Exception as e:
                print(f"Failure reading message from {sock.getpeername()}:", e)

def handleCheckAliveLoop():
    print("Starting handle check alive thread")
    while True:
        for client in clients:
            if time.time() - lastMessage[client] > 10:
                removeClient(client)
                try:
                    print(f"Terminating dead client {client.getpeername()}")
                except:
                    print("Terminating dead client")
        time.sleep(10)

def wrapLoop(loopfunc):
    def wrapped():
        while True:
            try:
                loopfunc()
            except BaseException as e:
                print(f"Exception in thread {loopfunc}", e)
            else:
                print(f"Thread {loopfunc} exited, restarting")
    return wrapped

def runBackgroundProcesses():
    handleIncomingProcess = threading.Thread(target=wrapLoop(handleIncomingLoop))
    handleAcknowledgeProcess = threading.Thread(target=wrapLoop(handleAcknowledgeLoop))
    handleCheckAliveProcess = threading.Thread(target=wrapLoop(handleCheckAliveLoop))

    handleIncomingProcess.start()
    handleAcknowledgeProcess.start()
    handleCheckAliveProcess.start()


def broadcastToClient(client):
    port = port_of_client[client]
    try:
        #print(f"Sending to client {client.getpeername()} in port {port}")
        client.send(json.dumps(["#"+colors[str(port)], 0]).encode("utf-8"))
    except Exception as e:
        print(f"Failed send to {port} client:", e, "terminating client")
        removeClient(client)

def broadcastToClients():
    print("Broadcasting update...")
    pool = ThreadPool(16)
    pool.map(broadcastToClient, clients)
    pool.close()
    pool.join()
    print(f"Broadcast update to {len(clients)} clients")

@app.route("/", methods=["GET", "POST"])
def index():
    global colors
    if request.method == "GET":
        return "Relay"
    elif request.method == "POST":
        colors = request.json
        for client in clients:
            broadcastToClient(client)
        return "OK"

runBackgroundProcesses()

app.run(host="0.0.0.0", port=9100)
