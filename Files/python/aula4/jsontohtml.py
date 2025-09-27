
import re
import json

file = open('novo_dicionario_medico.json', 'r', encoding="utf-8")
textjson = file.read()
json_obj = json.loads(textjson)

html = open('small_book.html', 'r', encoding='utf8')
linhas = html.read().splitlines()
html_new = open('livro_anotado_new.html', 'w', encoding='utf8')
for line in linhas:
    line.strip("!.?,()")
    for key in json_obj:
        key.strip("!.?,()")
        print(key)
        a = re.search(r'\b' + key + r'\b', line, re.IGNORECASE)
        if a != None:
            line = line.lower()
            expression = "<a data-toggle='tooltip' href='' title='"+ json_obj.get(key) +"'>" + key + "'> </a>"
            line = re.sub(r'\b' + key + r'\b', expression, line)
    html_new.write(line + "\n")
html.close()
html_new.close()
file.close()


