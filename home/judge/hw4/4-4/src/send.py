#!/usr/bin/env python3
from sys import argv
import requests, json, traceback
from parse import parse
import time

url = 'http://ca.nasa.nycu:4444'
# url = 'http://localhost:44444'
if len(argv) > 2:
    url = argv[2]

headers = {
    'X-Forwarded-For': '192.168.69.69',
    'User-Agent': 'Mozilla/5.0'
}

q = open(argv[1]).read()
a = json.load(open(argv[1].replace('xml','json')))
j = json.dumps({ 'q': q, 'a': a })
if len(argv) > 3:
    j = json.dumps(a)
res = requests.post(url, headers={ 'Content-Type': 'application/json', **headers }, data=j)
print(res, res.text, time.time())

