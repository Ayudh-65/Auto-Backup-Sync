import socket
import os
import time
import sys

BUFFER_SIZE = 4096
PORT = 5000

def sendBackup():
    clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsock.connect((host, PORT))

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

host = input("Enter your server's IPv4 Address:")
filename = input("Relative or absolute path of file to backup:")
backup_frequency = int(input("Your required backup frequency in seconds:")) #seconds

try:
    filesize = os.path.getsize(filename)
except Exception as e:
    print("Error accessing file:", e)
    sys.exit()

try:
    clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsock.connect((host, PORT))
    clientsock.sendall(f"{filename}".encode("utf-8"))
    clientsock.close()

    while True:
        sendBackup()
        time.sleep(backup_frequency)

except Exception as exception:
    print(f"Error: {exception}")

finally:
    clientsock.close()
    print("Connection to the server is closed.")