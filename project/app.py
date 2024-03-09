# Create a webpage that lets the user learn the words in an inputted text
import re
import sqlite3

from flask import Flask, redirect, render_template, request, session, g
from flask_session import Session

# Creating the app
app = Flask(__name__)

# Creating the session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Setting the database
app.config['DATABASE'] = 'words.db'


# Making sure I have access to the database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

# Homepage route
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # Create lists of words
        session['basic'] = []
        session['moderate'] = []
        session['hard'] = []
        session['impossible'] = []

        # Setting up the database
        db = get_db()
        cursor = db.cursor()

        # Getting all the words from the text, using a set to ensure there are no duplicated words
        text = request.form.get("text")
        tmp = re.findall(r'\b\w+\b', text)
        tmp1 = [x.lower() for x in tmp]
        tmpset = set(tmp1)
        word_list = list(tmpset)

        # Categorize words into complexity level
        for word in word_list:
            # Set all words to lowercase since the database is also lowercased
            lower = word.lower()
            cursor.execute("SELECT id FROM words WHERE word = (?)", (lower,))
            result = cursor.fetchall()

            # Categorize words
            if result:
                number = int(result[0][0])

                if number > 0 and number < 9000:
                        session['basic'].append(word)
                elif number > 8999 and number < 25000:
                        session['moderate'].append(word)
                elif number > 24999 and number < 40000:
                        session['hard'].append(word)
                else:
                        session['impossible'].append(word)

        # Once done, redirect to the next page
        return redirect("/learn")

    else:
        return render_template("index.html")

# Picking a level route
@app.route("/learn", methods=["GET", "POST"])
def learn():
    
    eas_len = len(session['basic'])
    mod_len = len(session['moderate'])
    har_len = len(session['hard'])
    imp_len = len(session['impossible'])

    return render_template("learn.html", basic_list=session['basic'], moderate_list=session['moderate'], 
                           hard_list=session['hard'], impossible_list=session['impossible'], eas_len=eas_len,
                           mod_len=mod_len, har_len=har_len, imp_len=imp_len)
    
# The four following routes show the user the choosen level
# Same template is used, the difference is made by what lists are passed in
@app.route("/learn/basic")
def learn_basic():
        lvl1 = 'basic'
        eas_len = len(session['basic'])
        return render_template("play.html", list=session['basic'], len=eas_len, link=lvl1, level='Basic')

@app.route("/learn/moderate")
def learn_moderate():
        lvl2 = 'moderate'
        mod_len = len(session['moderate'])
        return render_template("play.html", list=session['moderate'], len=mod_len, link=lvl2, level='Moderate')

@app.route("/learn/hard")
def learn_hard():
        lvl3 = 'hard'
        har_len = len(session['hard'])
        return render_template("play.html", list=session['hard'], len=har_len, link=lvl3, level='Hard')

@app.route("/learn/impossible")
def learn_impossible():
        lvl4 = 'impossible'
        imp_len = len(session['impossible'])
        return render_template("play.html", list=session['impossible'], len=imp_len, link=lvl4, level='Impossible')

# 'About' route
@app.route("/about")
def about():
        return render_template("about.html")

