import json
import re
import spacy

file = open('Juntos.json', 'r', encoding="utf-8")
final = json.load(file)

file2 = open('mdsaude.json', 'r', encoding="utf-8")
Doenca = json.load(file2)

file3 = open("Ossos.json", "r", encoding="utf-8")
Ossos = json.load(file3)

nlp = spacy.load('pt_core_news_lg')
new_dict = final

for termo in Doenca:
    d = Doenca[termo]
    termo = termo.lower()
    if termo in new_dict:
        new_dict[termo]["Categoria"] = ["Doenca"]

for termo in Ossos:
    desc = new_dict.get(termo, "")
    termo_doc = nlp(termo)
    termo_lemma = " ".join([token.lemma_ for token in termo_doc])
    termo_lemma = termo_lemma.lower()

    if termo_lemma in new_dict:
        new_dict[termo_lemma]["Categoria"] = ["Osso"]


with(open("ComCategoria.json", "w", encoding="utf-8") as Final):
    json.dump(new_dict, Final, indent=4, ensure_ascii=False)