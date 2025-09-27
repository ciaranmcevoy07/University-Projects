import json
import re

file = open('Final.json', 'r', encoding="utf-8")
final = json.load(file)

file2 = open('mdsaude.json', 'r', encoding="utf-8")
mdsaude = json.load(file2)

new_dict = final


for key, termo in mdsaude.items:
    
    ag = mdsaude[termo]
    termo = termo.lower()
    if termo in new_dict:
            new_dict[termo]["ag_desc"] = [ag]
    elif termo not in new_dict:
        new_dict[termo] = {"ag_desc": [ag]}