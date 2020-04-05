import socket
import select
import subprocess
import atexit
import time
import json
import threading
import traceback
from multiprocessing.dummy import Pool as ThreadPool
from flask import Flask, request

app = Flask(__name__)


ports = list(range(9001, 9007))
colors = {str(port): "000" for port in ports}
servers = []
clients = []
lastMessage = {}
websockify_procs = []

for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", port+100))
    sock.listen(16)
    servers.append(sock)

def shutdownServerSocks():
    for sock in servers:
        sock.close()
atexit.register(shutdownServerSocks)

for port in ports:
    # Start the websockify
    websockify_procs.append(subprocess.Popen(["websockify", str(port),
                                              f"localhost:{port+100}",
                                              "--cert=../certs/fullchain.pem",
                                              "--key=../certs/privkey.pem"]))

def shutdownWebsockifys():
    for proc in websockify_procs:
        proc.terminate()
atexit.register(shutdownWebsockifys)

# Dealing with clients
def removeClient(client):
    client.close()
    try:
        clients.remove(client)
    except ValueError:
        pass
    try:
        del lastMessage[client]
    except ValueError:
        pass

def handleIncomingLoop():
    print("Starting handle incoming connections thread")
    while True:
        read_servers = select.select(servers, [], [], 0)[0]
        for sock in read_servers:
            # New client
            port = sock.getsockname()[1]-100
            new_client, addr = sock.accept()
            clients.append(new_client)
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
                print("Error receiving message, terminating client")
                traceback.print_exc()
                removeClient(sock)

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
                print(f"Exception in thread {loopfunc}")
                traceback.print_exc()
            else:
                print(f"Thread {loopfunc} exited, restarting")
    return wrapped

def runBackgroundProcesses():
    handleIncomingProcess = threading.Thread(
                                        target=wrapLoop(handleIncomingLoop))
    handleAcknowledgeProcess = threading.Thread(
                                        target=wrapLoop(handleAcknowledgeLoop))
    handleCheckAliveProcess = threading.Thread(
                                        target=wrapLoop(handleCheckAliveLoop))

    handleIncomingProcess.start()
    handleAcknowledgeProcess.start()
    handleCheckAliveProcess.start()


def broadcastToClient(client):
    port = client.getsockname()[1]-100
    try:
        #print(f"Sending to client {client.getpeername()} in port {port}")
        client.send(json.dumps(["#"+colors[str(port)], 0]).encode("utf-8"))
    except Exception as e:
        print(f"Failed send to {port} client; terminating client")
        traceback.print_exc()
        removeClient(client)

def broadcastToClients():
    print("Broadcasting update...")
    pool = ThreadPool(32)
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
