# import socket module
from socket import *
import sys  
import datetime  

serverSocket = socket(AF_INET, SOCK_STREAM)

# Prepare a server socket
serverPort = 6789
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

while True:
    # Establishing the socket connection
    print(f"'\nServer Started...{datetime.datetime.now()}")
    print(f"Run the project on the following URL: http://127.0.0.1:{serverPort}")
    connectionSocket, addr = serverSocket.accept()
    print(f"[CLIENT CONNECTED] {addr} at {datetime.datetime.now()}")

    try:
        # Receiving request
        message = connectionSocket.recv(1024).decode()
        if not message:
            print("[WARNING] Empty request received.")
            connectionSocket.close()
            continue

        # Parse request line: e.g., "GET /HelloWorld.html HTTP/1.1"
        filename = message.split()[1]
        f = open(filename[1:], 'rb')

        # Read file contents
        outputdata = f.read()
        f.close()

        # Log file found
        print(f"[FILE FOUND] '{filename[1:]}' served successfully at {datetime.datetime.now()}")

        # Send one HTTP header line into socket
        header = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(outputdata)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        connectionSocket.send(header.encode())

        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i:i+1])

        connectionSocket.send("\r\n".encode())
        connectionSocket.close()

    except IOError:
        # Log 404 not found
        print(f"[404 NOT FOUND] '{filename[1:]}' requested by {addr} at {datetime.datetime.now()}")

        body = (
            "<html><head><title>404 Not Found</title></head>"
            "<body><h1>404 Not Found</h1><p>The requested file was not found.</p></body></html>"
        ).encode()
        header = (
            "HTTP/1.1 404 Not Found\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(body)}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        connectionSocket.send(header.encode())
        connectionSocket.send(body)
        connectionSocket.close()

# Clean up
serverSocket.close()
sys.exit()
