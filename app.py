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

def valid_roles(type, role):

    valid_roles = players.get_all_roles()

    if type not in valid_roles:
        abort(403)
    if role not in valid_roles[type]:
        abort(403)

def valid_class(type, value):

    valid_classes = players.get_all_classes()
    
    if type not in valid_classes:
        abort(403)
    if value not in valid_classes[type]:
        abort(403)

def valid_ideas(type, value):

    valid_ideas = players.get_all_ideas()

    if type not in valid_ideas:
        abort(403)
    if value not in valid_ideas[type]:
        abort(403)

def valid_contacts(type, value):

    valid_contacts = players.get_all_contacts()

    if type not in valid_contacts:
        abort(403)
    if value not in valid_contacts[type]:
        abort(403)

@app.route("/add_player")
def add_player():
    require_login()
    classes = players.get_all_classes()
    roles = players.get_all_roles()
    return render_template("add_player.html", classes=classes, roles = roles)

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
    profile = request.form["profile"]
    user_id = session["user_id"]
    
    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            classes.append((parts[0],parts[1]))
            valid_class(parts[0], parts[1])

    roles = []
    for entry in request.form.getlist("roles"):
        if entry:
            parts = entry.split(":")
            roles.append((parts[0],parts[1]))
            
            ### checks is input valid
            valid_roles(parts[0], parts[1])

    if len(name) == 0:
        abort(403)

    if len(name) > 50 or len(profile) > 300:
        abort(403)
    
    player_id = players.add_player(name, profile, user_id, classes, roles)
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
        all_classes = players.get_all_classes()
        player_classes = players.get_classes(player_id)
        
        all_roles = players.get_all_roles()
        player_roles = players.get_roles(player_id)

        ### collects selected info
        selected = set()
        if player_classes:
            for entry in player_classes:
                selected.add(entry[1])
        if player_roles: 
            for role in player_roles:
                selected.add(role[1])

        return render_template("/edit_player.html", player=player[0], classes = all_classes, roles = all_roles, selected = selected)

@app.route("/update_player", methods=["POST"])
def update_player():
    require_login()
    check_csrf()
    player_id = request.form["player_id"]
    name = request.form["name"]
    profile = request.form["profile"]

    player = players.get_player(player_id)

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            parts = entry.split(":")
            ### checks is input valid
            valid_class(parts[0], parts[1])

            classes.append((parts[0],parts[1]))

    roles = []
    for entry in request.form.getlist("roles"):
        if entry:
            parts = entry.split(":")
            ### check if input valid
            valid_roles(parts[0], parts[1])

            roles.append((parts[0],parts[1]))
               
    if len(name) == 0:
        abort(403)

    if len(name) > 50 or len(profile) > 300:
        abort(403)

    if not player[0]:
        abort(404)

    if player[0]['user_id'] != session['user_id']:
        abort(403)

    players.update_player(player_id, name, profile, classes, roles)
    flash("Pelaajan muokatut tiedot")

    return redirect("/player/" + str(player_id))

@app.route("/suggest_idea", methods=["POST"])
def suggest_idea():
    require_login()
    check_csrf()
    player_id = request.form["player_id"]
    ideas = request.form["ideas"]
    user_id = session['user_id']

    max_limit = 3


    if len(users.get_player_ideas(user_id, player_id)) >= max_limit:
        flash(f'Sama käyttäjä voi lähettää pelaajalle vain {max_limit} ehdotusta.')
        return redirect("/player/" + str(player_id))

    ideas = []
    for entry in request.form.getlist("ideas"):
        if entry:
            parts = entry.split(":")

            ### checks is input valid
            valid_ideas(parts[0], parts[1])

            ideas.append((parts[0],parts[1]))

    contacts = []
    for entry in request.form.getlist("contact"):
        if entry:
            parts = entry.split(":")

            ### checks is input valid
            valid_contacts(parts[0], parts[1])

            contacts.append((parts[0],parts[1]))

    players.suggest_idea(player_id, ideas, contacts, user_id)
    flash("Pelaajalle lähetty idea")

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
        all_roles = players.get_all_roles()
        ideas = players.get_all_ideas()
        contacts = players.get_all_contacts()
        player_ideas = players.get_ideas(player_id)

        return render_template("/show_player.html", player=player[0], user = player[1], classes = classes, roles=player[2], all_roles = all_roles, ideas=ideas, player_ideas = player_ideas, contacts=contacts)

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