from socket import *
import threading

HOST = '127.0.0.1'
PORT = 10000
ADDR = (HOST, PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect(ADDR)

def work(conn):
    while True:
        data = conn.recv(8)
        data = data.decode()
        prefix = data[:2]
        length = int(prefix)
        data = data[2:]
        length -= int(len(data))

        while length > 0:
            temp = conn.recv(8).decode()
            data += temp
            length -= int(len(temp))

        if not data:
            break
        else:
            print(data)

worker = threading.Thread(target=work, args=(clientSocket, ))
worker.start()

while True:
    message = input()
    length = len(message)
    prefix = format(length, '02d')
    print(prefix)
    message = prefix + message
    clientSocket.send(message.encode())

clientSocket.close()
print('client disconnected')