import re
import json
ficheiro1 = open("XML\Dicionario_de_termos_medicos_e_de_enfermagem_setup.xml", "r", encoding="utf-8")
ficheiro1 = ficheiro1.read().splitlines()
list1=[]
list2=[]
list3=[]
dic = {}
string1 = ""
match=""
'percorrer a lista à procura dos termos, podendo estes conter apenas uma linha ou várias'
for i in range(156, len(ficheiro1)):
    if re.findall(r'font="(10|24)"[^>]*>(.*?)</text>', ficheiro1[i]):
        if i not in list1:
            if re.search(r'font="(10|24)"[^>]*>(.*?)</text>', ficheiro1[i]):
                'adição do termo caso este não esteja na lista de valores de i já percorridos'
                search = re.search(r'font="(10|24)"[^>]*>(.*?)</text>', ficheiro1[i])
                list1.append(i)
                if search is not None:
                    'assegurar que search não é vazio e adicionar valores a adicionar a match os valores de search'
                    search = search.group(0)
                    search = re.sub(r".*(10|24).*?<b>(.*?)</b>.*", r"\2", str(search))
                    match = match + " " + search
                    

    else:
            list2 = []
            for j in range(i, len(ficheiro1)):
                'percorrer o livro à procura de descrições'
                if re.search(r'font="(11|12|19|25|26)"[^>]*>(.*?)</text>', ficheiro1[j]):
                    if j not in list3:
                        list3.append(j)
                        match1 = re.search(r'font="(11|12|19|25|26)"[^>]*>(.*?)</text>', ficheiro1[j])
                        match1 = match1.group(0)
                        'juntar as descrições todas numa só linha e adicionar a list2 e fazer uma limpeza destes'
                        match1 = re.sub(r'font="(11|12|19|25|26)"[^>]*>(.*?)</text>', r"\2", match1)
                        match1 = re.sub(r"<b|i>(.+)</b|i>", r"\1", match1)
                        list2.append(match1)
                if re.findall(r'font="(10|24)"', ficheiro1[j]):
                    'quando no segundo ciclo se encontrar um termo e não uma descrição, percorre a list2 caso esta não seja nula e concatenar todos os elementos da lista, limpando-os'
                    if list2 != []:
                        string1 = ""
                        for element in list2:
                            string1 = string1 + " " + element
                            string1 = re.sub(r"- ", r"", string1)
                            string1 = re.sub(r"(.+)○.+", r"\1", string1)

                    if match =="":
                        break
                    'juntar todos os termos e descrições a um dicionário, fazendo outra limpeza primeiro, assim como retornar os valores de match e list para empty'
                    match = re.sub(r'.*(10|24).*?>(.*?)<.*', r'\2', str(match))
                    print(match)
                    match = str(match).lower()
                    dic[(match)] = string1
                    match=""
                    list2=[]
                    break

'adicionar o último caso ao dicionário uma vez que o ciclo para antes deste'
dic["zumbido"] = "Barulho nos ouvidos, como um tinido, um burburinho ou um rugido. Alguns barulhos nos ouvidos podem aparecer devido a uma causa remediável, como catarro, infecção no ouvido médio ou cera, e desaparecem com a remoção da causa. Um som de vibração no ouvido pode ocorrer com a pressão arterial alta, que pode ser tratada. O zumbido propriamente dito - um distúrbio do nervo da audição -não pode ser curado, exceto algumas vezes em que haja um tumor removível no nervo; podem ser receitados comprimidos para ajudar. O zumbido verdadeiro sempre significa perda permanente da audição e, infelizmente, está se tornando predominante entre os jovens nos cenários modernos, devido à exposição prolongada a barulhos altos. Quando ligado a vertigens e surdez, a condição é conhecida como “Mal de Menière”. (V. Surdez, Vertigens.)"

with open('JSON\Dicionario_de_termos_medicos_e_de_enfermagem.json', "w", encoding="utf-8") as dici:
    json.dump(dic, dici, ensure_ascii=False, indent=4)
