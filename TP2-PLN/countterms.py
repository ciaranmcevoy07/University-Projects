import re
import json

file = open('Final2.json', 'r', encoding="utf-8")
dic = json.load(file)

count = 0
for i in dic.keys():
    count = count +1

print(count)