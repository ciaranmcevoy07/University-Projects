from flask import Flask, render_template
import json

app = Flask(__name__)
app.debug = True
file = open("Final.json", encoding="utf-8")

db = json.load(file)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/terms")
def terms():
    return render_template('terms.html', designations=db.keys())

@app.route("/term/<t>")
def term(t):
    keys = ['desc', 'dmte_desc', 'dtme_desc', 'ENG', 'ES', 'ag_desc', 'escih', 'en']
    if all(key in db[t] for key in keys):
        present_keys = [key for key in keys if key in db[t]]
        present_dict = {key: db[t][key] for key in present_keys}
        return render_template('term.html', designations=t, **present_dict)
    else:
        missing_keys = [key for key in keys if key not in db[t]]
        present_keys = [key for key in keys if key in db[t]]
        present_dict = {key: db[t][key] for key in present_keys}
        return render_template('term.html', designations=t, **present_dict)


app.run(host="localhost", port=3000, debug=True)

