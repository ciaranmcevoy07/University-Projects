import re
#EX1
line1 = "hello world"
line2 = "goodbye world"
line3 = "hi, hello there"
def ex11():
    a = re.match(r"^hello", line1)
    b = re.match(r"^hello", line2)
    c = re.match(r"^hello", line3)
    return a,b,c

def ex12():
    a = re.search(r"hello", line1)
    b = re.search(r"hello", line2)
    c = re.search(r"hello", line3)
    return a,b,c

def ex13():
    line = "Hello there! Uh, hi, hello, it's me... Heyyy, hello? HELLO!"
    a = re.findall(r"[Hh][Ee][Ll][Ll][Oo]", line)
    return a

def ex14():
    a = re.sub(r'[Hh][Ee][Ll][Ll][Oo]', '*YEP*', "Hello there! Uh, hi, hello, it's me... Heyyy, hello? HELLO!")
    return a

def ex15():
    a = re.split(',',"bananas, laranjas, maçãs, uvas, melancias, cerejas, kiwis, etc.")
    return a

#EX2
def palavra_magica(frase):
    a = re.search(r"(por favor)\p{P}+$", frase)
    return a


#EX3
def narcissismo(linha):
    a = re.findall(r"\b(eu)\b", linha)
    return len(a)

#EX4
def troca_de_curso(linha, novo_curso):
    a = re.sub("LEI", novo_curso, linha)
    return a

#EX5
def soma_string(linha):
    a = re.split(',', linha)
    soma=0
    for i in a:
        b = int(i)
        soma+=b
    return soma 

#EX6
def pronomes(frase):
    a = re.compile(r'\b(eu|tu|ele|ela)\b',re.IGNORECASE)
    b = re.findall(a, frase)
    return b

#EX7
def variavel_valida(frase):
    if re.match(r'^[a-zA-Z]', frase) != None:
        if re.match(r'[^a-zA-Z0-9_]', frase) == None:
            return 'Nao Valida'
        else:
            return 'Valida'
    else:
        return 'Nao Valida'
        
#EX8
def inteiros(frase):
    a = re.split(', |,| ', frase)
    lista=[]
    print(a)
    for i in a:
        if re.match(r'(-)*[0-9]+', i) != None:
            lista.append(i)
    return lista

#EX9
def underscores(frase):
    a = re.sub(r'( )+', '_', frase)
    return a

#EX10
def codigos_postais(lista):
    return list(re.split(r"-", codigo) for codigo in lista)

print(ex11())
print(ex12())
print(ex13())
print(ex14())
print(ex15())
#palavra_magica("Posso ir à casa de banho, por favor?")
#print(palavra_magica("Preciso de um favor."))
print(narcissismo("Eu não sei se eu quero continuar a ser eu. Por outro lado, eu ser eu é uma parte importante de quem EU sou."))
print(troca_de_curso("LEI é o melhor curso! Adoro LEI! Gostar de LEI devia ser uma lei.", input("Introduza um novo curso:")))
print(soma_string("4,-6,2,3,8,-3,0,2,-5,1"))
print(pronomes(input("Introduza uma frase:")))
print(variavel_valida(input("Introduza uma frase:")))
print(inteiros(input("Introduza uma frase:")))
print(underscores(input("Introduza uma frase:")))
print(codigos_postais([
    "4700-000",
    "1234-567",
    "8541-543",
    "4123-974",
    "9481-025"
]))