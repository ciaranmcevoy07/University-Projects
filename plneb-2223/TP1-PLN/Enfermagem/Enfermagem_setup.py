import re
import json
ficheiro1 = open("\XML\Dicionario_de_termos_medicos_e_de_enfermagem.xml", "r", encoding="utf-8")
ficheiro1 = ficheiro1.read()
'remoção de linhas e de informação irrelevante, assim como passagem de vários \n seguidos para apenas um'
ficheiro1 = re.sub(r'<b>(.+)</b>', r"\1", ficheiro1)
ficheiro1 = re.sub(r'<i>(.+)</i>', r"\1", ficheiro1)
ficheiro1 = re.sub(r'.+font="20".+', "", ficheiro1)
ficheiro1 = re.sub(r'.+font="19".+', "", ficheiro1)
ficheiro1 = re.sub(r'.+font="6".+', "", ficheiro1)
ficheiro1 = re.sub(r'.+font="0".+', "", ficheiro1)
ficheiro1 = re.sub(r'.+font="27".+', "", ficheiro1)
ficheiro1 = re.sub(r'<page.+>', "", ficheiro1)
ficheiro1 = re.sub(r'</page>', "", ficheiro1)
ficheiro1 = re.sub(r'\n+', r"\n", ficheiro1)

f = open("\XML\Dicionario_de_termos_medicos_e_de_enfermagem_setup.xml", "w", encoding="utf-8")
f.write(ficheiro1)
f.close()