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
    try:
            ex1 = basic[0]
    except IndexError:
            ex1 = None 
    try:
            ex2 = moderate[0]
    except IndexError:
            ex2 = None 
    try:
            ex3 = hard[0]
    except IndexError:
            ex3 = None 
    try:
            ex4 = impossible[0]
    except IndexError:
            ex4 = None 

    return render_template("learn.html", basic_list=basic, moderate_list=moderate, hard_list=hard, impossible_list=impossible, 
                            basic_word=ex1, moderate_word=ex2, hard_word=ex3, impossible_word=ex4)
    

@app.route("/learn/basic")
def learn_basic():
        eas_len = len(basic)
        return render_template("play.html", list=basic, len=eas_len)
@app.route("/learn/moderate")
def learn_moderate():
        mod_len = len(moderate)
        return render_template("play.html", list=moderate, len=mod_len)
@app.route("/learn/hard")
def learn_hard():
        har_len = len(hard)
        return render_template("play.html", list=hard, len=har_len)
@app.route("/learn/impossible")
def learn_impossible():
        imp_len = len(impossible)
        return render_template("play.html", list=impossible, len=imp_len)
        

