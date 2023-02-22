#!/usr/bin/env python3 
from sys import argv
import requests, json, traceback
from parse import parse
import time

url = argv[1]
path = argv[2]

print(f'url: {url}')

headers = {
    'X-Forwarded-For': '192.168.69.69',
    'User-Agent': 'Mozilla/5.0'
}

q = requests.get(url, headers=headers).text
with open(path, 'w') as f:
    f.write(q)
a = parse(q)
with open(path.replace('xml','json'), 'w') as f:
    f.write(json.dumps(a))
j = json.dumps({ 'q': q, 'a': a })
res = requests.post('http://ca.nasa.nycu:4444', headers={ 'Content-Type': 'application/json', **headers }, data=j)
print(res, res.text)
# time.sleep(60*9)
j = json.dumps(a)
res = requests.post(url, headers={ 'Content-Type': 'application/json', **headers }, data=j)
print(res, res.text)

# root = ET.fromstring(xml)
# root = ET.fromstring(xml)
# print(root)
# print(root.findall('.'))
