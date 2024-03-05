import re
import sqlite3

from flask import Flask, redirect, render_template, request, session, g


app = Flask(__name__)
app.config['DEBUG'] = True

app.config['DATABASE'] = 'words.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

basic = []
moderate = []
hard = []
impossible = []

learned = []

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        db = get_db()
        cursor = db.cursor()
        print("hello")
        text = request.form.get("text")
        list = re.findall(r'\b\w+\b', text)

        for word in list:
            lower = word.lower()
            cursor.execute("SELECT id FROM words WHERE word = (?)", (lower,))
            result = cursor.fetchall()
            number = int(result[0][0])

            if number > 0 and number < 9000:
                basic.append(word)
            elif number > 8999 and number < 25000:
                moderate.append(word)
            elif number > 24999 and number < 40000:
                hard.append(word)
            else:
                impossible.append(word)

        return redirect("/learn")

    else:
        return render_template("index.html")

@app.route("/learn", methods=["GET", "POST"])
def learn():
        return render_template("learn.html")
    

@app.route("/learn/easy")
def learn_easy():
        return render_template("play.html", list=basic)
@app.route("/learn/moderate")
def learn_moderate():
        return render_template("play.html", list=moderate)
@app.route("/learn/hard")
def learn_hard():
        return render_template("play.html", list=hard)
@app.route("/learn/impossible")
def learn_impossible():
        return render_template("play.html", list=impossible)
        

