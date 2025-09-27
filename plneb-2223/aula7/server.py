from flask import Flask, render_template, request
import json
import re

app = Flask(__name__)
app.debug = True
file = open("novo_dicionario_medico.json", encoding="utf-8")

db = json.load(file)
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/terms")
def egua():
    return render_template('terms.html', designations=db.keys())

@app.route("/term/<t>")
def term(t):
    return render_template('term.html', designations=t, value=db.get(t))

@app.route("/terms/search")
def search():
    text = request.args.get("text")
    lista = []
    if text:
        for designation, description in db.items():
            #if text in description or text in designation:
            if re.search(text, designation, flags=re.I) or re.search(text, description, flags=re.I):
                lista.append((designation,description))
    return render_template('search.html', matched = lista)

@app.route("/term", methods=["POST"])
def addterm():
    print(request.form)
    designation = request.form["designation"]
    description = request.form["description"]
    if designation not in db:
        info_message = "Term added successfully!"
    else:
        info_message = "Term updated correctly!"
    
    db[designation] = description
    file_save = open("novo_dicionario_medico.json", "w", encoding="utf-8")
    json.dump(db,file_save, ensure_ascii=False, indent=4)
    file_save.close()

    return render_template('terms.html', designations=db.keys(), message= info_message)

@app.route("/table")
def table():
    return render_template('table.html')

@app.route("/term/<designation>", methods=["DELETE"])
def deleteterm(designation):
    desc = db[designation]
    if designation in db:
        print(designation)
        del db[designation]
        file_save = open("novo_dicionario_medico.json", "w", encoding="utf-8")
        json.dump(db,file_save, ensure_ascii=False, indent=4)
    return {designation:desc}

app.run(host="localhost", port=3000, debug=True)

