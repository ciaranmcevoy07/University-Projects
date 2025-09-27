import re

file= open('python\dicionario_medico.txt', 'r', encoding="utf8")
text = file.read()
text = re.sub(r"\f", "", text)
new_text = re.sub(r'(\n\n.+)\n\n(.+)', r'\1', text)
entries = re.findall(r'\n\n(.+)((?:\n.+)+)', new_text)
new_entries = [(designation, description.strip()) for designation, description in entries]
print(new_entries[10])
file.close()

'''--------------------------------------------------------------------------'''
html = open('python\dicionario_medico.html', 'w', encoding='utf8')
header = '''<html>
<head>
<meta charset='utf-8'/>
</head>
<style>
table, td {
  border:1px solid black;
}
</style>
<body>
<table>
'''
body = ''
for designation, description in new_entries:
    body += '<tr>' + '<td>'+ designation+'</td>'
    body += '<td>'+ description+'</td>'+'</tr>'

footer = '''</table>
</body>
</html>'''

html.write(header+body+footer)
html.close()
