from flask import Flask, render_template


app = Flask(__name__)
app.debug = False
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/egua")
def egua():
    return render_template('egua.html')

@app.route("/elefante")
def elefante():
    return render_template('elefante.html')

@app.route("/engenharia")
def engenharia():
    return render_template('engenharia.html')

app.run(host="localhost", port=3000, debug=True)
