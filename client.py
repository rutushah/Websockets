import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.0.1"
ADDR = (SERVER,PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # FIX: pad the header to exactly 64 bytes (spaces), not b''.
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

send("Hello World!")
send("This is a test message.")
send("Goodbye!")
send(DISCONNECT_MESSAGE)
