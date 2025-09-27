import re
import json

def limpa(text):
    text = re.sub(r"\n", " ", text)
    return text.strip()

file = open('dicionario_medico.xml', "r", encoding="utf-8")
text = file.read()
text = re.sub(r"</?page.*>", "", text)
text = re.sub(r"</?text.*?>", "", text)
lista = re.findall(r"<b>(.*)</b>([^<]*)", text)
lista = [(designacao, limpa(descricao))for designacao, descricao in lista]
dicionario = {}
print(lista)
dicionario = dict(lista)
out = open('novo_dicionario_medico.json', 'w', encoding="utf-8")
json.dump(dicionario, out, ensure_ascii=False, indent=4)
out.close()
