from flask import Flask, render_template, request
import json
import spacy
import re
from collections import Counter
import sys
app = Flask(__name__)

file = open("Final.json", "r", encoding="utf-8")
file2 = open("mdsaude.json", "r", encoding="utf-8")

db = json.load(file) 
file.close()

db_md = json.load(file2)
file2.close()

@app.route("/")
def home():
    return render_template("home.html", title="Welcome!!!")

@app.route("/terms")
def terms():
    return render_template("terms.html", designations=db.keys())

@app.route("/term/<t>")
def term(t):
    return render_template("term.html", designation = t, value= db.get(t,"None"))

@app.route("/mdsaude")
def terms_mdsaude():
    return render_template("mdsaude.html", designations=db_md.keys())

@app.route("/mdsaude/<t>")
def term_mdsaude(t):
    return render_template("term_mdsaude.html", designation = t, value= db_md.get(t,"None"))

@app.route("/categorias")
def categorias():
    listaossos = []
    listadoencas = []

    text = request.args.get("text")
    for i, j in db.items():
        if "Categoria" in j:
            match = re.search('Doenca', str(db[i]["Categoria"]))
            match2 = re.search('Osso', str(db[i]["Categoria"]))
            if match:
                print(i)
                listadoencas.append(i)
            elif match2:
                listaossos.append(i)
    t = []  # Default assignment
    
    if text == "Doencas":
        t = listadoencas
    elif text == "Ossos":
        t = listaossos
    
    return render_template("categorias.html", t=t)

@app.route("/symptoms")
def symptoms():
    text = request.args.get("text")
    
    if not text:
        return render_template("symptoms.html", matched=[])
    listtext = []
    nlp = spacy.load('pt_core_news_lg')
    listtext = re.split(r',\s|;\s|,|;', text)
    new_text = nlp(text)
    normalized_text = " ".join([token.lemma_ for token in new_text])
    lista = []
    for k, v in db_md.items():
        if "Sintomas" in v:
            sintomas = db_md[k]["Sintomas"]
            st = nlp(sintomas)
            normalized_sintomas = " ".join([tokensint.lemma_ for tokensint in st])
            score = new_text.similarity(st)
            for i in listtext:
                text = nlp(i)
                normalized_text = " ".join([token.lemma_ for token in text])
                match = re.search(normalized_text, normalized_sintomas, re.I)
                if score > 0.65 or match:
                    if k not in lista:
                        lista.append(k)
    

    return render_template("symptoms.html", matched=lista)

@app.route("/table")
def table():
    lista = []
    for designation, description in db.items():
        lista.append((designation,description))
    return render_template("table.html", lista=lista)

@app.route("/terms/search")
def search():
    text = request.args.get("text")
    lista = []
    if text:
        for designation, description in db.items():
            if re.search(text,designation,flags=re.I): 
                lista.append((designation,description))
    return render_template("search.html",matched = lista)

@app.route("/term", methods=["POST"])
def addTerm():
    print(request.form)
    designation = request.form["designation"]
    description = request.form["description"]
    english = request.form["english"]
    spanish = request.form["spanish"]

    if designation not in db:
        info_message = "Term Added correctly"
    else:
        info_message = "Term Updated correctly!"

    db[designation] = {"desc":description, "ENG":english, "ES":spanish}
    file_save = open("Final.json", "w", encoding="utf-8")
    json.dump(db,file_save, ensure_ascii=False, indent=4)
    file_save.close()

    return render_template("terms.html", designations=db.keys(), message = info_message)



@app.route("/term/<designation>", methods=["DELETE"])
def deleteTerm(designation):
    desc = db[designation]
    if designation in db:
        print(designation)
        del db[designation]
        print(db.get(designation))
        file_save = open("Final.json","w")
        json.dump(db,file_save, ensure_ascii=False, indent=4)
        file_save.close()
        
    return {designation: {"desc":desc}}

app.run(host="localhost", port=3000, debug=True)
