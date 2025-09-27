from deep_translator import GoogleTranslator
import json
import re

file = open('novo_dicionario_medico.json', 'r', encoding="utf-8")
json_obj = json.load(file)

txt = open('novos_termos_traduzidos.txt', 'r', encoding="utf-8")
termos1 = txt.read().splitlines()
termos2 = txt.read()

lista = re.findall(r'(.+)(?=@)', termos2)

json_desc_pt_en = open('json_desc_pt_en.json', 'w', encoding="utf-8")

dict = {}
for i in termos1:
    termopt = re.search(r'(.+)(?=@)', i)
    termoeng = re.search(r'(?<=@)(.+)', i)
    if termopt:
        termo_pt = termopt.group()
        if termoeng:
            termo_eng = termoeng.group()
            dict[termo_pt] = {
                "en": termo_eng,
                "desc":json_obj[termo_pt]
                    }

json.dump(dict, json_desc_pt_en, ensure_ascii=False, indent=4)
json_desc_pt_en.close()
file.close()
txt.close()