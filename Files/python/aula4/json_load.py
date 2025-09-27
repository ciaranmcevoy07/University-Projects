import json

file = open('novo_dicionario_medico.json', encoding="utf-8")
lista = json.load(file)
print(lista)