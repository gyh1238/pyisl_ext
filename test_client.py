from socket import *
import threading
import time


def send(sock):
    while True:
        sendingData = input('enter message: ')
        sock.send(sendingData.encode('utf-8'))


def receive(sock):
    while True:
        recvData = sock.recv(1024)
        print("server: ", recvData.decode('utf-8'))


ip = '127.0.0.1'
port = 25001

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect((ip, port))

print('connection has been made!')

sender = threading.Thread(target=send, args=(clientSock,))
receiver = threading.Thread(target=receive, args=(clientSock,))

sender.start()
receiver.start()

while True:
    time.sleep(1)
    pass

clientSock.close()