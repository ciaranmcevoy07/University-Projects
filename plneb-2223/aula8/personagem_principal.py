import spacy
import re
from collections import Counter
import sys

file = open("Books/harry_potter_pedra_filosofal.txt", 'r', encoding='utf8')
book = file.read()

nlp = spacy.load('pt_core_news_lg')
av = nlp(book)

counter = Counter()

names = []
locations = []

for s in av.sents:
    for ent in s.ents:
        if ent[0].ent_type_ == "PER":
            names.append(ent)
        if ent[0].ent_type_ == "LOC":
            locations.append(ent.text)

localizacoes = Counter(locations)
personagens = Counter(names)
print(f"Main Characters: f{personagens.most_common(10)}")
print(f"Main Places: f{localizacoes.most_common(10)}")