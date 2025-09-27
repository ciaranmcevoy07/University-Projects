import json, re
file = open('json_desc_pt_en.json', 'r', encoding="utf-8")
json_obj = json.load(file)

livro = open('LIVRO-Doenças-do-Aparelho-Digestivo.txt', 'r', encoding="utf-8")
text = livro.read()
blacklist = {"e", "de", "são"}

nova_lista = json_obj.keys() - blacklist
nova_lista.remove("L+")
nova_lista.add("L\+")
'''
for line in linhas:
    for key in nova_lista:
        exp1 = r"\b" + key + r"\b"
        a = re.search(exp1, line, re.IGNORECASE)
        if a:
            line = line.lower()
            expression = f"<a href='' data-toggle='tooltip' title='{json_obj.get(key)}'>{key}</a>"
            exp2 = r"\b" + key + r"\b"
            line = re.sub(exp2, expression, line)
    html_new.write(line + "\n")
'''
expressao = r"\b(" + "|".join(nova_lista) + r")\b"

def anotaTermo(match):
    """
    O input da função é automaticamente inserido, mas ele é um objeto do tipo match,
    no qual o termo de índice 0 é toda a expressão encontrada, o índice 1 o 1º grupo, índice 2 o 2º, etc.
    """
    termo=match[1]
    return f"<a href='' data-toggle='tooltip' title='{json_obj.get(termo)}'>{termo}</a>"

text = re.sub(expressao, anotaTermo, text, flags=re.I)
text = re.sub(r"\f", "<hr>", text)
text = re.sub(r"\n", "<br>", text)

header = """
<html>
<head>
<meta charset='uft-8' />
</head>
<body>
"""

body = ""
body += text

footer = """
</body>
</html>
"""
livro.close()
html = open("livro_anotado_traduzido.html", "w", encoding="utf-8")
html.write(header+body+footer)
file.close()



