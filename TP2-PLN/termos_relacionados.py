import spacy
import re
from collections import Counter
import sys
import json

file = open("Original.json", "r", encoding="utf-8")
final = json.load(file)
file.close()

file = open("mdsaudeOriginal.json", "r", encoding="utf-8")
mdsaude = json.load(file)
file.close()



nlp = spacy.load('pt_core_news_lg')
for i in mdsaude.keys():
    fi = nlp(i)
    text = ""
    for j in final.keys():
        md = nlp(j)
        score = fi.similarity(md)
        if score > 0.8:
            text += j+";"
    mdsaude[i]["relacoes_sim"] = text

for i in mdsaude.keys():
    md = nlp(i)
    if i in mdsaude:
        text = mdsaude[i]["relacoes_sim"]
    else:
        text = ""
    for j in mdsaude.keys():
        md2 = nlp(j)
        score = md.similarity(md2)
        if score > 0.8:
            text += j+";"
    if i in mdsaude:
        mdsaude[i]["relacoes_sim"] = text
    else:
        mdsaude[i] = {"relacoes_sim" :text}
    
file2 = open("mdsaude.json", "w", encoding="utf-8")
json.dump(mdsaude,file2, ensure_ascii=False, indent = 4)
file2.close()



