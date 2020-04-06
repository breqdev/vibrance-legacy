import socket
import select
import subprocess
import atexit
import time
import json
import threading
import traceback
import ssl
from multiprocessing.dummy import Pool as ThreadPool

cert = "../certs/fullchain.pem"
key  = "../certs/privkey.pem"

enable_ssl = True

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

for port in ports:
    # Start the websockify
    if enable_ssl:
        websockify_procs.append(subprocess.Popen(["websockify", str(port),
                                                  f"localhost:{port+100}",
                                                  f"--cert={cert}",
                                                  f"--key={key}"]))
    else:
        websockify_procs.append(subprocess.Popen(["websockify", str(port),
                                                  f"localhost:{port+100}"]))

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
    except KeyError:
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
        try:
            read_clients = select.select(clients, [], [], 0)[0]
        except ValueError:
            continue
        for sock in read_clients:
            # New message from client
            try:
                data = sock.recv(1024)
                if data:
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

broadcastPool = ThreadPool(32)

def broadcastToClient(client):
    global colors
    port = client.getsockname()[1]-100
    try:
        client.send(json.dumps(["#"+colors[str(port)], 0]).encode("utf-8"))
    except Exception as e:
        print(f"Failed send to {port} client")
        traceback.print_exc()
        removeClient(client)

def broadcastToClients():
    ts = time.time()
    broadcastPool.map(broadcastToClient, clients)
    print(f"Broadcast update to {len(clients)} clients in {int((time.time()-ts)*1000)} ms")

### Command Server
if enable_ssl:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(cert, key)
    cserver_sock_unwrapped = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cserver_sock_unwrapped.bind(("0.0.0.0", 9100))
    cserver_sock_unwrapped.listen(16)
    cserver_sock = context.wrap_socket(cserver_sock_unwrapped, server_side=True)
else:
    cserver_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cserver_sock.bind(("0.0.0.0", 9100))
    cserver_sock.listen(16)

cclients = []

def runCServer():
    global colors
    while True:
        read_server = select.select([cserver_sock], [], [], 0)[0]
        if cserver_sock in read_server:
            # New Command Client
            new_client, addr = cserver_sock.accept()
            cclients.append(new_client)
            print(f"New command client from {addr}")
        read_clients = select.select(cclients, [], [], 0)[0]
        for client in read_clients:
            print("New data")
            try:
                data = client.recv(1024)
                if not data:
                    print("Socket closed")
                    cclients.remove(client)
                    try:
                        client.close()
                    except Exception:
                        pass
            except Exception as e:
                print("Error reading from command client, removing")
                traceback.print_exc()
                cclients.remove(client)
                try:
                    client.close()
                except Exception:
                    pass
            try:
                line = data.decode().split("\n")[0]
                colors = json.loads(line)
            except Exception as e:
                print("Unable to decode message")
                traceback.print_exc()
            else:
                print(colors)
                broadcastToClients()
                client.send(b"OK")



runBackgroundProcesses()

while True:
    try:
        runCServer()
    except Exception as e:
        print("Error in Command Server:")
        traceback.print_exc()
