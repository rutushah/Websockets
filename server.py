import socket 
import threading

HEADER = 64
PORT = 5050
# SERVER = "192.168.1.110"

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        # Read exactly HEADER bytes
        header = bytearray()
        while len(header) < HEADER:
            chunk = conn.recv(HEADER - len(header))
            if not chunk:
                connected = False
                break
            header.extend(chunk)
        if not connected:
            break

        msg_length_str = bytes(header).decode(FORMAT).strip()
        if not msg_length_str:
            break

        try:
            msg_length = int(msg_length_str)
        except ValueError:
            print(f"[{addr}] Bad header (not an int): {msg_length_str!r}")
            break

        # Read exactly msg_length bytes
        body = bytearray()
        while len(body) < msg_length:
            chunk = conn.recv(msg_length - len(body))  # FIX: recv (not rec)
            if not chunk:
                connected = False
                break
            body.extend(chunk)
        if not connected:
            break

        msg = bytes(body).decode(FORMAT)
        if msg == DISCONNECT_MESSAGE:
            connected = False

        print(f"[{addr}]  {msg}")

    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Service is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn,addr))
        thread.start()
        print("[ACTIVE CONNECTIONS] " + str(threading.active_count() - 1))

print("[STARTING] server is starting...")
start()
