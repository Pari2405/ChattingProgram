from socket import *
import threading

HOST ='127.0.0.1'
PORT = 10000
ADDR = (HOST, PORT)

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(ADDR)
print ('bind')

serverSocket. listen(100)
print('listen')

clientSocket, addr_info = serverSocket.accept()
print ('accept')
print('--client information--')
print(clientSocket)

def work(clientSocket):
    while True:
        data = clientSocket.recv(8)
        data = data.decode()
        prefix = data[:2]
        length = int(prefix)
        data = data[2:]
        length -= int(len(data))

        while length > 0:
            temp = clientSocket.recv(8).decode()
            data += temp
            length -= int(len(temp))

        if not data:
            break
        print('recieve data:', data)

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
serverSocket.close()
print('close')