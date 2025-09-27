import json
import re

file = open('CIH_Bilingual_Medical_Glossary_English_Spanish.xml', 'r', encoding="utf-8")
text = file.read()
file.close()
file1 = open('CIH_Editado.xml', 'w', encoding="utf-8")

'Remove linhas que nao tem fonte="4 ou 5"'
text = re.sub(r'(.*)(font="[0-3|6-9]")(.*)', '', text, flags=re.MULTILINE)
text = re.sub(r'(.*)(font="10")(.*)', '', text, flags=re.MULTILINE)

'Retira linhas que nao tem nada entre > <'
text = re.sub(r'^<text\s.*?>(\s)</text>$', '', text, flags=re.MULTILINE)

'Retira linhas sem nada entre<b> e </b>'
text = re.sub(r'(.*)<b>\s*</b>(.*)', '', text, flags=re.MULTILINE)

'Retira linhas e paragrafos desnecessarios'
text = re.sub(r'(.*)(fontspec)(.*)', '', text, flags=re.MULTILINE)
text = re.sub(r'(.*)(page)(.*)', '', text, flags=re.MULTILINE)
text = re.sub(r'(.*)(pdf2xml)(.*)', '', text, flags=re.MULTILINE)
text = re.sub(r'(.*)(xml)(.*)', '', text, flags=re.MULTILINE)
text = re.sub(r'(.*)(<i>)(.*)', '', text, flags=re.MULTILINE)
text = re.sub(r'(.*)(:)(.*)', '', text, flags=re.MULTILINE)
text = re.sub(r'(.*)(<b>)(.*)', '', text, flags=re.MULTILINE)
text = re.sub(r'(.*)(`)(.*)', '', text, flags=re.MULTILINE)
text = re.sub(r'(.*)>\)(.*)', '', text, flags=re.MULTILINE)
text = re.sub(r'\n\s*\n', '\n', text)
file1.write(text)
file1.close()

'Criar e limpar lista de <b> e espacos adicionais'
file2 = open('CIH_Editado.xml', 'r', encoding="utf-8")
text2 = file2.read().splitlines()
file2.close()

lista = []

for i in text2:
    match = re.search(r"(.*)", i)
    if match:
        new_i = match.group()
        new_i = re.sub(r'<b>|</b>', '', new_i)
        newmatch = re.search(r'(?<=>)(.*)(?=<)', new_i)
        if newmatch:
            new_i = newmatch.group()
            new_i = new_i.strip()
            lista.append(new_i)

'Retira primeiros paragrafos desnecessarios'        
for i in range(16):
    lista.pop(0)
json_file = open('CIH.json', 'w', encoding="utf-8")
dict = {}

'Liga as palavras com traducao correta'
k = 0
while k !=-1:
    string = ''
    nos = 1
    count = 2
    if k+count >= len(lista):
        break
    string = lista[k+1]
    while count != 0:
        if k+count >= len(lista):
            break
        else:
            match = re.search(r"^[()[]|^[a-z]|^(Humana)|^(Salud)|^(Paciente)|^(Estreptococcica)|^(Adquirida)|^(Papanicolau)", lista[k+count])
            match2 = re.search(r'^.*;\s*$', lista[k + count -1])
            if match or match2:
                string  = string + lista[k+count]
                nos = nos +1
                count = count + 1
            else:
                dict[lista[k]] = {
                        "es": string
                        }
                if nos > 1:
                    k = k + count 
                    count = 0
                else:
                    k = k + 2
                    count = 0
v = "Vasectomía"
dict['Vasectomy'] = {
    "es": v
    }
json.dump(dict, json_file, ensure_ascii=False, indent=4)
json_file.close()




        



