#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import xmltodict
from sys import argv
import re, json

def postprocessor(path, key, value):
    try:
        value = eval(value, { '__builtins__': {} })
    except:
        if value == 'false':
            value = False
        if value == 'true':
            value = True
    return key, value

def parse(q, d = True):
    xml = f'<?xml version="1.0"?><root>{q}</root>'
    if d: print(xml)
    a = xmltodict.parse(xml, postprocessor=postprocessor)['root']
    if d: print(a)
    return a

if __name__ == '__main__':
    q = open(argv[1]).read()
    d = parse(q)
    print(d)
    a = json.load(open(argv[1].replace('xml','json')))
    print(a)
    print(d == a)
