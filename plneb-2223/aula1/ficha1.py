import re

def numerosPares(array):
    listapares =[]
    for i in array:
        if i % 2 == 0:
            listapares.append(i)
    return listapares


def nomeFicheiroInverso(nf):
    inverso = nf[::-1]
    print(inverso)


def occurrenciasf(b):
    file = open(b, 'r')
    content = file.read()
    lista = content.split(" ")
    dict={}
    counter = 0
    for i in lista:
        for keys in dict.keys():
            if i == keys:
                dict[i] += 1
                counter += 1
                break
        if counter == 0:
            dict.update({i:1})
    maioresvalores = sorted(dict.items(), key=lambda x:x[1], reverse=True,)[:10]
    return maioresvalores

def limparstring(arg):
    str = arg.lower()
    a = re.sub("[áàãâ]", "a",str)
    o = re.sub("[õôòó]", "o", a)
    c = re.sub("ç", "c", o)
    i = re.sub("[íìî]", "i", c)
    e = re.sub("[éèê]", "e", i)
    u = re.sub("[úùû]", "u", e)
    lista = re.split(", |,|:| |\n", u)
    string = ' '.join(lista)
    return string

def removerpotunacaointroduzida(arg, pontuacoes, sub):
    str = arg.lower()
    form = "["+pontuacoes+"]"
    a = re.sub(form, sub,str)
    lista = re.split(", |,|:| |\n", a)
    string = ' '.join(lista)
    return string

def reverse(a):
    inverso = a[::-1]
    return inverso

def numerodeA(a):
    lista = []
    contador = 0
    for i in a:
        lista.append(i)
    for o in lista:
        if o == "a" or o =="A":
            contador += 1
    return contador

def numerodevogais(a):
    b= a.lower()
    lista = []
    contador = 0
    for i in b:
        lista.append(i)
    for o in lista:
        if o == "a" or o == "e" or o == "i" or o == "o" or o == "u":
            contador += 1
    return contador

def upper(a):
    b = a.upper()
    return b

def lower(a):
    b = a.lower()
    return b
                
nome = input("Introduz Nome:")
print(nome.upper())
a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
b = input("Nome de Ficheiro:")
print(numerosPares(a))
nomeFicheiroInverso(b)
print(occurrenciasf(b))
texto = input("Introduza uma texto:")
print(limparstring(texto))
pontuacao = input("Introduza caracteres a limpar:")
sub = input("Substituir caracteres com:")
print(removerpotunacaointroduzida(texto, pontuacao, sub))
print(reverse(texto))
print(numerodeA(texto))
print(numerodevogais(texto))
print(upper(texto))
print(lower(texto))
