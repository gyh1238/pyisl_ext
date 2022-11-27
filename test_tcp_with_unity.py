import socket
import time
import urllib.request
import json
import base64

url= "http://192.168.186.128:26657/status?"
url2 = "http://129.154.218.224:26657/block?height="
# json_url = urllib.request.urlopen(url)
# json_text = json_url.read().decode('utf-8')
# status_json = json.loads(json_text)

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

    url2 = "http://129.154.218.224:26657/block?height="
    block_height = "691594"
    url2 = url2 + block_height
    json_url2 = urllib.request.urlopen(url2)
    json_text2 = json_url2.read().decode('utf-8')
    status_json2 = json.loads(json_text2)
    tx_data2 = status_json2['result']['block']['data']['txs']
    print(tx_data2)
    if tx_data2:
        name_bytes = base64.b64decode(name_base64_str)
        name = name_bytes.decode('utf-32')
    block_height = block_height + str(tx_data2)
    sock.sendall(block_height.encode("UTF-8"))  # Converting string to Byte, and sending it to C#
    receivedData = sock.recv(1024).decode("UTF-8")  # receiveing data in Byte fron C#, and converting it to String
    print(receivedData)