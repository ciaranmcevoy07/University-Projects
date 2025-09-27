import json
import re

file = open('anatomia_geral.json', 'r', encoding="utf-8")
ag_obj = json.load(file)

file2 = open('CIH.json', 'r', encoding="utf-8")
cih_obj = json.load(file2)

file3 = open('dicionario_termos_medicos_pt_es_en.json', 'r', encoding="utf-8")
dtm_obj = json.load(file3)

file4 = open('Dicionario_de_termos_medicos_e_de_enfermagem.json', 'r', encoding="utf-8")
dtme_obj = json.load(file4)


new_dict = dtm_obj

for termo in dtme_obj:
    desc = dtme_obj[termo]
    termo = termo.lower()
    if termo in new_dict:
        new_dict[termo]["dtme_desc"] =[desc]
    if termo not in dtm_obj:
        new_dict[termo] = {"dtme_desc":[desc]}

for termo in cih_obj:
    escih = cih_obj[termo]
    termo = termo.lower()
    if termo in new_dict:
            new_dict[termo]["escih"] = [escih]
    elif termo not in new_dict:
        new_dict[termo] = {"escih": [escih]}

for termo in ag_obj:
    ag = ag_obj[termo]
    termo = termo.lower()
    if termo in new_dict:
            new_dict[termo]["ag_desc"] = [ag]
    elif termo not in new_dict:
        new_dict[termo] = {"ag_desc": [ag]}

with(open("Final.json", "w", encoding="utf-8") as Final):
    json.dump(new_dict, Final, indent=4, ensure_ascii=False)
