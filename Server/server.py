import socket
import os
from datetime import datetime
import time

BACKUP_FREQUENCY = 20 #seconds
BUFFER_SIZE = 4096
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

try:
    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serversock.bind((SERVER_HOST, SERVER_PORT))

    serversock.listen(5)
    print(f"Listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        clientsock, clientaddr = serversock.accept()
        print(f"Connected to {clientaddr[0]}:{clientaddr[1]}")

        filename = clientsock.recv(BUFFER_SIZE).decode()
        filename = os.path.basename(filename)
        clientsock.close()

        while True:
            clientsock, clientaddr = serversock.accept()
            filesize = clientsock.recv(BUFFER_SIZE).decode()
            print(f"Taking backup from {clientaddr[0]}:{clientaddr[1]}")
            clientsock.sendall("ok".encode())

            readbytes = clientsock.recv(int(filesize))
            with open(filename, 'wb') as f:
                f.write(readbytes)
                
            currtime = datetime.now().strftime("%H:%M:%S")
            print(f"Created backup at {currtime}")
            clientsock.sendall(f"Created backup at {currtime}".encode())
            clientsock.close()
            time.sleep(BACKUP_FREQUENCY-2)

    clientsock.close()
    print("Connection to client closed. \n")

except Exception as exception:
    print(f"Error: {exception}")
finally:
    clientsock.close()
    serversock.close()
