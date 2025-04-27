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

def save_file(path, data):
    with open(path, 'wb') as f:
        f.write(data)

def work(clientSocket):
    while True:
        data = clientSocket.recv(4096)
        prefix = data[:10].decode()
        length = int(prefix)
        header = data[10:14].decode()
        length -= 4
        length -= int(len(data))
        data = data[14:]

        while length > 0:
            temp = clientSocket.recv(4096)
            data += temp
            length -= int(len(temp))

        if not data:
            break

        if header[0] == 'f':
            type = header[1:]
            path = 'for_server/file.' + type
            save_file(path, data)
        else:
            print (data)

worker = threading.Thread(target=work, args=(clientSocket, ))
worker.start()


while True:
    message = input()
    length = len(message)
    prefix = format(length, '10d')
    print(prefix)
    message = prefix + message
    clientSocket.send(message.encode())

clientSocket.close()
serverSocket.close()
print('close')