import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
import db
import config 
import secrets
import players

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

@app.route("/create_player", methods=["POST"])
def create_player():
    check_csrf()
    name = request.form["name"]
    defence_positions = request.form.getlist("defence_position")
    batting_roles = request.form.getlist("batting_role")
    profile = request.form["profile"]
    user_id = session["user_id"]
    
    player_id = players.add_player(name, defence_positions, batting_roles, profile, user_id)
    flash("Uusi pelaaja lisätty.")

    return redirect("/player/" + str(player_id))

@app.route("/edit_player/<int:player_id>")
def edit_player(player_id):
    player = players.get_player(player_id)

    def_list = {row[0] for row in player[1]}
    bat_list = {row[0] for row in player[2]}

    return render_template("/edit_player.html", player=player[0], def_list = def_list, bat_list=bat_list)

@app.route("/update_player", methods=["POST"])
def update_player():
    check_csrf()
    player_id = request.form["player_id"]
    name = request.form["name"]
    defence_positions = request.form.getlist("defence_position")
    batting_roles = request.form.getlist("batting_role")
    profile = request.form["profile"]
    
    players.update_player(player_id, name, defence_positions, batting_roles, profile)
    flash("Pelaajan muokatut tiedot")

    return redirect("/player/" + str(player_id))

@app.route("/teams")
def teams():
    return "Tähän tulee palvelussa olevat joukkueet."

@app.route("/players")
def show_players():

    all_players = players.get_players()
        
    count = len(all_players)
    return render_template("/players.html", count=count, all_players=all_players)

@app.route("/player/<int:player_id>")
def player(player_id):

    player = players.get_player(player_id)

    return render_template("/show_player.html", player=player[0], def_roles=player[1], bat_roles=player[2])

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