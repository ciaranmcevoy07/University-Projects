import re
import json

ficheiro1 = open(r"XML\dicionario_termos_medicos_pt_es_en.xml", "r",encoding="utf-8")
ficheiro1 = ficheiro1.read()
ficheiro1=re.sub(r"<page.+>", r"", ficheiro1)
ficheiro1=re.sub(r"</page>", r"", ficheiro1)
ficheiro1=re.sub(r'.+font="(20)".+</text>', r"", ficheiro1)
ficheiro1=re.sub(r'.+font="(14)".+</text>', r"", ficheiro1)
ficheiro1=ficheiro1.splitlines()
list1 = []
list2 = []
list3 = []
dic = {}
match = ""


'Começar por 76209 porque é aonde os termos que queremos considerar começam'
for i in range(76209, len(ficheiro1)):
    j = i + 1
    'percorrer a lista até deixarmos de encontrar linhas que não tenham termos (denominados pela font=16)'
    if re.findall(r'font="(16)"[^>]*>(.*?)</text>', ficheiro1[i]):
        if i not in list1:
                'adicionar todos os valores de i a uma lista para não os percorrer outra vez'
                if re.search(r'font="(16|19|20|)"[^>]*>(.*?)</text>', ficheiro1[i]):
                    list1.append(i)
                    search = re.search(r'font="(16)"[^>]*>(.*?)</text>', ficheiro1[i])
                    if search is not None:
                        search = search.group(0)
                        'somar todos os valores de search desde que estes não sejam none ou apenas valores numéricos (da página)'
                        if re.findall(r"<b>\d+</b>", search):
                            ficheiro1[i] = re.sub(r"<b>\d+</b>", "", ficheiro1[i])
                            continue
                        else:
                            search = re.sub(r".*(16|20).*?<b>(.*?)</b>.*", r"\2", str(search))
                            match = match + " " + search
                else:
                    continue
    if re.search(r'^(?!.*<(b|i)>).+<', ficheiro1[i]):
        'Se não for um termo, percorrer as traduções para as adicionar a uma lista'
        for j in range(i,(len(ficheiro1))):
            if j not in list2:
                list2.append(j)
                if re.search(r'^(?!.*<(b|i)>).+<', ficheiro1[j]):
                    match1 = re.search(r'^(?!.*<(b|i)>).+<', ficheiro1[j])
                    match1 = match1.group(0)
                    match1 = re.sub('.+>(.+)<', r"\1", match1)
                    list3.append(match1)
            'quando se encontrar outro termo que comece com bold(logo termo e não tradução)'
            if re.findall(r"<(b)>", ficheiro1[j]):
                if list3 != []:
                    string1 = ""
                    for element in list3:
                        string1 = string1 + " " + element
                        string1 = re.sub(r"- ", r"", string1)
                if match == "":
                    break
                match = re.sub(r"\s(.+)", r"\1", match)
                eng = re.search(r'(?<=U)\s+(.*?)\s*(?=E)', string1)
                es =  re.search(r'(?<=E)(.*)', string1)
                if es and eng:
                    eng = eng.group()
                    es = es.group()
                    es = es.strip()
                    eng = eng.strip()
                    dic[(match)] = {
                        "ENG": eng,
                        "ES": es
                    }
                else:
                    if es:
                        es = es.group()
                        es = es.strip()
                        dic[(match)] = {
                            "ES": es
                        }
                    else:
                        if eng:
                            eng = eng.group()
                            eng = eng.strip()
                            dic[(match)] = {
                                "ENG": eng,
                            }
                match=""
                list3=[]
                break
                '''a lista aonde as traduções são adicionadas é percorrida e juntada ao valor correspondente de match
                por fim retornam-se os valores de match e list3 para empty para percorrer o ciclo outra vez'''
with open(r'JSON\dicionario_termos_medicos_pt_es_en.json', "w", encoding="utf-8") as dici:
    json.dump(dic, dici, ensure_ascii=False, indent=4)