import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config 
import secrets

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
    check_csrf()
    firstname = request.form["firstname"]
    surname = request.form["surname"]
    defence_positions = request.form.getlist("defence_position")
    batting_roles = request.form.getlist("batting_role")
    profile = request.form["profile"]
    user_id = session["user_id"]

    name=firstname + str(" ") + surname
  
    columns = "NAME, PROFILE, user_id"
    column_places = "?,?,?"
    
    values = [name, profile,user_id]

    fi_defence_positions = []
    fi_batting_roles = []

    for def_position in defence_positions:
       eng_def_position, fin_def_position = def_position.split("|")
       fi_defence_positions.append(fin_def_position)
       columns += ", " + str(eng_def_position)
       column_places +=  ",?" 
       values.append(1)
      
    for batting_role in batting_roles:
       eng_batting_role, fi_batting_role = batting_role.split("|")
       fi_batting_roles.append(fi_batting_role)
       columns += ", " + str(eng_batting_role)
       column_places +=  ",?"
       values.append(1)

    db.execute(f"INSERT INTO players ({columns}) VALUES ({column_places})",values)
        
    return render_template("result.html", name=firstname + str(" ") + surname, defence_positions=fi_defence_positions, batting_roles=fi_batting_roles, profile=profile)

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
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register") 
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")
            
    flash(f'Tunnuksen luonti onnistui. Tunnuksesi on: {username}')
    return redirect("/")

redirect("/register")

@app.route("/login", methods=["POST"])
def login():

    try:
        username = request.form["username"]
        password = request.form["password"]
        

        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            return redirect("/")
        else:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/")
    
    except:
            flash("VIRHE: väärä tunnus tai salasana")
            return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    del session["user_id"]
    return redirect("/")


def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)