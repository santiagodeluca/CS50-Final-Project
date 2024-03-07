import re
import sqlite3

from flask import Flask, redirect, render_template, request, session, g
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['DEBUG'] = True

app.config['DATABASE'] = 'words.db'

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        session['basic'] = []
        session['moderate'] = []
        session['hard'] = []
        session['impossible'] = []

        db = get_db()
        cursor = db.cursor()
        text = request.form.get("text")
        tmp = re.findall(r'\b\w+\b', text)
        tmp1 = [x.lower() for x in tmp]
        tmpset = set(tmp1)
        word_list = list(tmpset)

        for word in word_list:
            lower = word.lower()
            cursor.execute("SELECT id FROM words WHERE word = (?)", (lower,))
            result = cursor.fetchall()
            if result:
                number = int(result[0][0])

                if number > 0 and number < 9000:
                        session['basic'].append(word)
                elif number > 8999 and number < 25000:
                        session['moderate'].append(word)
                elif number > 24999 and number < 40000:
                        session['hard'].append(word)
                else:
                        print(f'{word}')
                        session['impossible'].append(word)

        return redirect("/learn")

    else:
        return render_template("index.html")

@app.route("/learn", methods=["GET", "POST"])
def learn():
    eas_len = len(session['basic'])
    mod_len = len(session['moderate'])
    har_len = len(session['hard'])
    imp_len = len(session['impossible'])

    return render_template("learn.html", basic_list=session['basic'], moderate_list=session['moderate'], 
                           hard_list=session['hard'], impossible_list=session['impossible'], eas_len=eas_len,
                           mod_len=mod_len, har_len=har_len, imp_len=imp_len)
    

@app.route("/learn/basic")
def learn_basic():
        eas_len = len(session['basic'])
        return render_template("play.html", list=session['basic'], len=eas_len)
@app.route("/learn/moderate")
def learn_moderate():
        mod_len = len(session['moderate'])
        return render_template("play.html", list=session['moderate'], len=mod_len)
@app.route("/learn/hard")
def learn_hard():
        har_len = len(session['hard'])
        return render_template("play.html", list=session['hard'], len=har_len)
@app.route("/learn/impossible")
def learn_impossible():
        imp_len = len(session['impossible'])
        return render_template("play.html", list=session['impossible'], len=imp_len)
        

