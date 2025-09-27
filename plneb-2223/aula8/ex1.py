import spacy
import re

document = "Na opinião do ex-avançado, que representou clubes como Tottenham, Fulham ou Aston Villa, o jogador do Al Nassr ainda tem muito para dar, apesar dos 38 anos de idade... mas não ao serviço dos blues, onde as questões têm outra dimensão.Não, não me parece. Ele tem sido fantástico, mas... Não está acabado, mas penso que seria outro problema, e não precisam disso. Penso que ele ainda seria capaz de marcar golos, começou por afirmar o agora comentador desportivo."

nlp = spacy.load("pt_core_news_lg")
av = nlp(document)

dic= {}
for s in av.sents:
    print(f'#{s}')
    for ent in s.ents:
        print(f'@ {ent}')
    
for w in s:
    '''print(f'w {w.text} | lema {w.lemma_} | POS {w.pos_} | tag: {w.tag_} |dep: {w.dep_}')'''
    if w.pos_ == "VERB":
        if w.pos_ not in dic:
            dic[w.pos_] = 1
        else:
            dic[w.pos_] += 1
for key in dic:
    print(f'verb: {key} | count: {dic[key]}')