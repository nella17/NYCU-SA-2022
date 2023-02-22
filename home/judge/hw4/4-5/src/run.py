#!/usr/bin/env python3
from sys import argv
import requests, json, traceback

url = argv[1]
u = lambda p: url + p

print(f'url: {url}')

try:
    secretKey = requests.post(u('/json'), headers={ 'Content-type': 'application/json' }, data=json.dumps({ "keyword":"give_me_secret_key" })).json()['secretKey']
    print(secretKey)

    secretFile = requests.post(u('/urlencoded'), data={ 'secretKey': secretKey }).content
    print(secretFile)

    secretPart = requests.post(u('/multipart'), files={ 'secretFile': secretFile }).text
    print(secretPart)
except:
    print(traceback.format_exc())
