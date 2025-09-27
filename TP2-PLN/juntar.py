import spacy
import re
from collections import Counter
import sys
import json

file = open('Original.json', 'r', encoding="utf-8")
final = json.load(file)
file.close()
file2 = open('mdsaude.json', 'r', encoding="utf-8")
mdsaude = json.load(file2)
file2.close()
file3 = open('doencas.json', 'r', encoding="utf-8")
doencas = json.load(file3)
file3.close()

dictio = final

for key, termo in mdsaude.items():
    key = key.lower()
    if key in dictio:
        for item in termo.keys():
            dictio[key][item] = termo[item]
    else:
        i = 0
        for item in termo.keys():
            if i == 0:
                dictio[key] = {item: termo[item]}
            else:
                dictio[key][item] = termo[item]
            i += 1

for i in doencas:
    for key, termo in i.items():
        key = key.lower()
        if key in dictio:
            for item in termo.keys():
                dictio[key][item] = termo[item]
        else:
            i = 0
            for item in termo.keys():
                if i == 0:
                    dictio[key] = {item: termo[item]}
                else:
                    dictio[key][item] = termo[item]
                i+= 1


file4 = open("Juntos.json", "w", encoding="utf-8")
json.dump(dictio, file4, ensure_ascii=False, indent = 4)
file4.close()