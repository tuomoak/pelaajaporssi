import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    message = "Pelaajapörssi on pesäpalloaiheinen sivusto, joka on tarkoitettu:"
    words = ["Joukkuetta etsiville", "Pelaajia etsiville"]
    return render_template("index.html", message=message, items=words)

@app.route("/add_player")
def add_player():
    return render_template("add_player.html")

@app.route("/result", methods=["POST"])
def result():
    firstname = request.form["firstname"]
    surname = request.form["surname"]
    defence_positions = request.form.getlist("defence_position")
    batting_roles = request.form.getlist("batting_role")
    profile = request.form["profile"]

    name=firstname + str(" ") + surname
  
    columns = "NAME, PROFILE"
    column_places = "?,?"
    
    values = [name, profile]

    for def_position in defence_positions:
       columns += ", " + str(def_position)
       column_places +=  ",?" 
       values.append(1)
      
    for batting_role in batting_roles:
       columns += ", " + str(batting_role)
       column_places +=  ",?"
       values.append(1)

    db.execute(f"INSERT INTO players ({columns}) VALUES ({column_places})",values)
        
    return render_template("result.html", name=firstname + str(" ") + surname, defence_positions=defence_positions, batting_roles=batting_roles, profile=profile)

@app.route("/teams")
def teams():
    return "Tähän tulee palvelussa olevat joukkueet."

@app.route("/players")
def players():
    all_players = db.query("SELECT * FROM players")
    count = len(all_players)
    return render_template("/players.html", count=count, all_players=all_players)

@app.route("/player/<int:page_id>")
def player(page_id):
    return "Tämä pelaajan nro sivu: " + str(page_id)

@app.route("/team/<int:page_id>")
def team(page_id):
    return "Tämä on joukkueen nro sivu: " + str(page_id)


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"


@app.route("/login", methods=["POST"])
def login():

    try:
        username = request.form["username"]
        password = request.form["password"]
        

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]
        #password_hash = db.query(sql, [username])[0][0]

    
        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            return redirect("/")
        else:
            return "VIRHE: väärä tunnus tai salasana"
    
    except:
            return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")