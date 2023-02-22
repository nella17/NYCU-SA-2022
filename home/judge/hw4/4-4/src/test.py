#!/usr/bin/env python3
from sys import argv
import requests, json, traceback
from parse import parse
import time

url = 'http://ca.nasa.nycu:4444'

headers = {
    'X-Forwarded-For': '192.168.69.69',
    'User-Agent': 'Mozilla/5.0'
}

while True:
    q = requests.get(url, headers=headers).text
    a = parse(q, False)
    j = json.dumps({ 'q': q, 'a': a })
    res = requests.post(url, headers={ 'Content-Type': 'application/json', **headers }, data=j)
    print(res, res.text, time.time())
    if res.status_code != 200:
        print(q)
        print(a)
        break

# root = ET.fromstring(xml)
# root = ET.fromstring(xml)
# print(root)
# print(root.findall('.'))
