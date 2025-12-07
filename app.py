import sqlite3
import secrets
from flask import Flask
from flask import redirect, render_template, request, session, flash, abort
import config
import players
import users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    message = "Pelaajapörssi on pesäpalloaiheinen sivusto, joka on tarkoitettu:"
    words = ["Joukkuetta etsiville", "Pelaajia etsiville"]
    return render_template("index.html", message=message, items=words)

def require_login():
    if "user_id" not in session:
        abort(403)

def valid_roles(role):
    valid_roles = ["pitcher|Lukkari","frontfield|Etukenttä", "midfield|Polttolinja", 
                   "baseman|Pesävahti","outfielder|Takakenttä","runner|Etenijä",
                   "advancehitter|Vaihtaja","runhitter|Kotiuttaja",
                   "flyhitter|Kopittaja", "joker|Jokeri"]

    if role not in valid_roles:
        abort(403)

@app.route("/add_player")
def add_player():
    require_login()
    classes = players.get_all_classes()
    return render_template("add_player.html", classes=classes)

@app.route("/find_player")
def find_player():
    require_login()
    query = request.args.get("query")

    if query:
        if len(query) > 100:
            abort(403)
        results = players.find_players(query)
    else:
        query = ""
        results = []
    return render_template("find_player.html", query=query, results=results)

@app.route("/create_player", methods=["POST"])
def create_player():
    require_login()
    check_csrf()
    name = request.form["name"]
    defence_positions = request.form.getlist("defence_position")
    batting_roles = request.form.getlist("batting_role")
    profile = request.form["profile"]
    user_id = session["user_id"]
    
    classes = []
    for entry in request.form.getlist("classes"):
        parts = entry.split(":")
        classes.append((parts[0],parts[1]))

    if len(name) == 0:
        abort(403)

    if len(name) > 50 or len(profile) > 300:
        abort(403)

    for role in defence_positions:
        valid_roles(role)

    for role in batting_roles:
        valid_roles(role)

    player_id = players.add_player(name, defence_positions, batting_roles, profile, user_id, classes)
    flash("Uusi pelaaja lisätty.")

    return redirect("/player/" + str(player_id))

@app.route("/edit_player/<int:player_id>")
def edit_player(player_id):
    require_login()
    player = players.get_player(player_id)

    if not player[0]:
        abort(404)

    if player[0]['user_id'] != session['user_id']:
        abort(403)

    else:
        def_list = {row[0] for row in player[1]}
        bat_list = {row[0] for row in player[2]}

        player_classes = players.get_classes(player_id)
        all_classes = players.get_all_classes()

        selected = {}
        if player_classes:
            selected = {row[1] for row in player_classes}

        return render_template("/edit_player.html", player=player[0], def_list = def_list, bat_list=bat_list, classes = all_classes, selected = selected)

@app.route("/update_player", methods=["POST"])
def update_player():
    require_login()
    check_csrf()
    player_id = request.form["player_id"]
    name = request.form["name"]
    defence_positions = request.form.getlist("defence_position")
    batting_roles = request.form.getlist("batting_role")
    profile = request.form["profile"]

    player = players.get_player(player_id)

    classes = []
    for entry in request.form.getlist("classes"):
        parts = entry.split(":")
        classes.append((parts[0],parts[1]))

    for role in defence_positions:
        valid_roles(role)

    for role in batting_roles:
        valid_roles(role)

    if len(name) == 0:
        abort(403)

    if len(name) > 50 or len(profile) > 300:
        abort(403)

    if not player[0]:
        abort(404)

    if player[0]['user_id'] != session['user_id']:
        abort(403)

    players.update_player(player_id, name, defence_positions, batting_roles, profile, classes)
    flash("Pelaajan muokatut tiedot")

    return redirect("/player/" + str(player_id))


@app.route("/remove_player/<int:player_id>", methods=["GET", "POST"])
def remove_player(player_id):
    require_login()
    player = players.get_player(player_id)

    if not player[0]:
        abort(404)

    if player[0]['user_id'] != session['user_id']:
        abort(403)

    if request.method == "GET":
        player = players.get_player(player_id)
        return render_template("remove_player.html", player=player[0])

    if request.method == "POST":
        check_csrf()
        if "remove" in request.form:
            players.remove_player(player_id)
            flash("Pelaaja poistettu")
            return redirect("/")
        else:
            return redirect("/player/" + str(player_id))


@app.route("/teams")
def teams():
    return "Tähän tulee palvelussa olevat joukkueet."

@app.route("/players")
def show_players():
    require_login()

    all_players = players.get_players()

    count = len(all_players)
    return render_template("/players.html", count=count, all_players=all_players)

@app.route("/player/<int:player_id>")
def player(player_id):

    player = players.get_player(player_id)

    if not player[0]:
        abort(404)
    else:
        classes = players.get_classes(player_id)
        return render_template("/show_player.html", player=player[0], def_roles=player[1], bat_roles=player[2], user = player[3], classes = classes)

@app.route("/user/<int:user_id>")
def user(user_id):

    user = users.get_user(user_id)

    if not user:
        abort(404)
    else:
        users_players = users.get_players(user_id)
        return render_template("/show_user.html", user=user, players = users_players)

@app.route("/team/<int:page_id>")
def team(page_id):
    require_login()
    return "Tämä on joukkueen nro sivu: " + str(page_id)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register_user", methods=["POST"])
def register_user():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: salasanat eivät ole samat")
        return redirect("/register")

    if len(username) == 0:
        flash("Käyttäjätunnus ei voi olla tyhjä")
        return redirect("/register")

    if len(password1) == 0:
        flash("Salasana ei voi olla tyhjä")
        return redirect("/register")

    try:
        users.create_user(username, password1)

    except sqlite3.IntegrityError:
        flash("VIRHE: tunnus on jo varattu")
        return redirect("/register")

    flash(f'Tunnuksen luonti onnistui. Tunnuksesi on: {username}')
    return redirect("/")

redirect("/register")

@app.route("/login", methods=["POST"])
def login():

    username = request.form["username"]
    password = request.form["password"]

    user_id = users.check_login(username, password)

    if user_id:
        session["username"] = username
        session["user_id"] = user_id
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")
    else:
        flash("VIRHE: väärä tunnus tai salasana")
        return redirect("/")

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["username"]
        del session["user_id"]
    return redirect("/")

def check_csrf():
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)