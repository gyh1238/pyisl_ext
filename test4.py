import urllib.request
import json
import time
import base64

url= "http://192.168.186.128:26657/status?"
# json_url = urllib.request.urlopen(url)
# json_text = json_url.read().decode('utf-8')
# status_json = json.loads(json_text)
# print(r.status_code)
# print(r.text)
# print(status_json)

block_height = 0
block_height_old = 0

# while True:
#     json_url = urllib.request.urlopen(url)
#     json_text = json_url.read().decode('utf-8')
#     status_json = json.loads(json_text)
#     block_height_old = block_height
#     block_height = status_json['result']['sync_info']['latest_block_height']
#     if block_height != block_height_old:
#         latest_block_hash = status_json['result']['sync_info']['latest_block_hash']
#         print(block_height)
#         print(latest_block_hash)
#     time.sleep(1)

# name_base64_str = 'CosBCogBChwvY29zbW9zLmJhbmsudjFiZXRhMS5Nc2dTZW5kEmgKLWNvc21vczE2M2NqdDc2aGg0ZjRhNmR6cmF3bWxsNDRhbHNqcjhkYXN5cTR6dxItY29zbW9zMXA3bTdnZzh4Z3k1MDcwaDl0ZWg3dnU0NDB6enQyZG5sank3Z3dwGggKA2xlbxIBMRJYClAKRgofL2Nvc21vcy5jcnlwdG8uc2VjcDI1NmsxLlB1YktleRIjCiECFu+2w0LaaarffuBmHJRu1xm07mqnqxzhc8p2eBI3UVkSBAoCCAEYARIEEMCaDBpAYJrWMY/sGrI7XvK4SyRqhzeIq+kQE5zEIoBiEKYvWeQ/y1j0tHk0GUzktZyXhOJ/T89qh9XyT9KGruyzbwM29w=='
name_base64_str = 'CqoBCogBChwvY29zbW9zLmJhbmsudjFiZXRhMS5Nc2dTZW5kEmgKLWNvc21vczE2M2NqdDc2aGg0ZjRhNmR6cmF3bWxsNDRhbHNqcjhkYXN5cTR6dxItY29zbW9zMWM2OWpoMzNxenN4MHd0YWxuM3pzMnAzbG44NjlmYWNteHQwOGowGggKA2xlbxIBMRIdTElDUyBpcyBiZXN0IGxhYiBpbiB0aGUgd29ybGQSWApQCkYKHy9jb3Ntb3MuY3J5cHRvLnNlY3AyNTZrMS5QdWJLZXkSIwohAhbvtsNC2mmq337gZhyUbtcZtO5qp6sc4XPKdngSN1FZEgQKAggBGAgSBBDAmgwaQIW8C51aP7/qZDF9kZFkYi6XrmH7PfGX/AOropXFv9SEE5JDQttzsh5VAToeSuOq7YcOOPSN7rl13/8pNLSDcAA='
name_bytes = base64.b64decode(name_base64_str)
name = name_bytes.decode('euc-kr', errors = 'ignore')

print(name_bytes)
print(name)