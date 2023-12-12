import socket
import os
import time
import sys

BUFFER_SIZE = 4096
HOST = '127.0.0.1'
PORT = 5000
BACKUP_FREQUENCY = 20 #seconds

def sendBackup():
    clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsock.connect((HOST, PORT))

    filesize = os.path.getsize(filename)
    clientsock.sendall(str(filesize).encode())

    if clientsock.recv(1024).decode() == "ok":
        print("Updating backup...")
        with open(filename, 'rb') as f:
            readbytes = f.read()
        clientsock.sendall(readbytes)

        confirm = clientsock.recv(BUFFER_SIZE).decode()
        print(confirm)
        clientsock.close()


filename = input("Relative or absolute path of file to backup:")

try:
    filesize = os.path.getsize(filename)
except Exception as e:
    print("Error accessing file:", e)
    sys.exit()

try:
    clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsock.connect((HOST, PORT))
    clientsock.sendall(f"{filename}".encode("utf-8"))
    clientsock.close()

    while True:
        sendBackup()
        time.sleep(BACKUP_FREQUENCY)

except Exception as exception:
    print(f"Error: {exception}")

finally:
    clientsock.close()
    print("Connection to the server is closed.")