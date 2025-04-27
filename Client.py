from socket import *
import threading

HOST = '127.0.0.1'
PORT = 10000
ADDR = (HOST, PORT)

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect(ADDR)

def work(conn):
    while True:
        data = conn.recv(4096)
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

def read_file(path):
    try:
        with open(path, 'rb') as f:
            file = f.read()
        return file
    except FileNotFoundError:
        print ('File not found')
        return None

while True:
    message = input()
    if not message:
        break

    option = 'text '
    if message[0] == '/':
        if message[1:6] == 'file ':
            option = 'file'

    if option == 'file':
        filename = message[6:]
        type = filename.split('.')[-1]
        header = 'f'
        if type == 'jpg':
            header += 'jpg'

        message = read_file(filename)
        if not message:
            continue

    else:
        header = 't___'

    message = header.encode() + message

    length = len(message)
    prefix = format(length, '10d')
    print(prefix)
    message = prefix.encode() + message
    clientSocket.send(message)

clientSocket.close()
print('client disconnected')


#(4587224)(f jpg)(file)
#(578)(t____)(text)