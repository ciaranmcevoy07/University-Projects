from deep_translator import GoogleTranslator
import json
import re

dict = open('novo_dicionario_medico.json', encoding="utf-8")
json_medico_pt = json.load(dict)

file1 = open('termos_traduzidos.txt', 'r', encoding="utf-8")
termos1 = file1.read().splitlines()
file2 = open('novos_termos_traduzidos.txt', 'w', encoding="utf-8")
for i in termos1:
    new_string = re.sub(r"\s@\s", "@", i)
    file2.write(new_string+'\n')
file2.close()
file1.close()


