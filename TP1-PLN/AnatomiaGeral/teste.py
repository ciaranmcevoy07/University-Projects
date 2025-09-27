import json
import re
lista = []
i = open('primeiroteste', 'r', encoding="utf-8")
f = open ('anatomia_geral.json', 'r', encoding="utf-8")
lines = i.read().splitlines()
json_medico_pt = json.load(f)
for j in lines:
    if j not in json_medico_pt.keys():
        lista.append(j)


print(lista)

