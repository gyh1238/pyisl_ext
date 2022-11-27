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
        print("client: ", recvData.decode('utf-8'))

port = 25001

serverSock = socket(AF_INET, SOCK_STREAM)
serverSock.bind(('', port))
serverSock.listen(1)

print("%d port waiting for connection..."%port)

connectionSock, addr = serverSock.accept()

print('Connection from ',str(addr))

sender = threading.Thread(target=send, args=(connectionSock,))
receiver = threading.Thread(target=receive, args=(connectionSock,))
# target: 실제로 쓰레드가 실행할 함수
# args: 그 함수에게 전달할 인자 - 튜플같이 iterable한 변수만 입력가능! but 인자가
# 하나면 튜플이 아닌 var로 인식하기에 (soc,)로 입력해야 함

sender.start()
receiver.start()
# start()로 생성되었던 쓰레드가 실행됨, 전부 수행하면 소멸함
# -> 소멸하지 않게 하기위해 while True를 send, receive 함수에 넣음
# 그치만 이 프로세스가 종료되면 분신과 같은 쓰레드 역시 소멸

while True:
    time.sleep(1)
    pass

# 그냥 pass하면 쉬지않고 코드를 실행함 -> 1초씩 쉬어가며 반복하도록

connectionSock.close()
serverSock.close()