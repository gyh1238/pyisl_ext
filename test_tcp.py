import socket
import time
import urllib.request
import json

url= "http://192.168.186.128:26657/status?"

host, port = "127.0.0.1", 25001
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

startPos = [0, 0, 0] #Vector3   x = 0, y = 0, z = 0
while True:
    time.sleep(1) #sleep 0.5 sec
    json_url = urllib.request.urlopen(url)
    json_text = json_url.read().decode('utf-8')
    status_json = json.loads(json_text)
    block_height = status_json['result']['sync_info']['latest_block_height']
    sock.sendall(block_height.encode("UTF-8"))  # Converting string to Byte, and sending it to C#
    receivedData = sock.recv(1024).decode("UTF-8")  # receiveing data in Byte fron C#, and converting it to String
    print(receivedData)