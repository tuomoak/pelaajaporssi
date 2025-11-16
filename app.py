from flask import Flask
from flask import redirect, render_template, request
import db

app = Flask(__name__)

@app.route("/")
def index():
    message = "Pelaajapörssi on pesäpalloaiheinen sivusto, joka on tarkoitettu seuraaville:"
    words = ["Joukkuetta etsiville", "Pelaajia etsiville"]
    return render_template("index.html", message=message, items=words)

@app.route("/add_player")
def add_player():
    return render_template("add_player.html")

@app.route("/result", methods=["POST"])
def result():
    firstname = request.form["firstname"]
    surname = request.form["surname"]
    outfield_positions = request.form.getlist("outfield_position")
    infield_roles = request.form.getlist("infield_role")
    profile = request.form["profile"]

    name=firstname + str(" ") + surname
  
    columns = "NAME, PROFILE"
    column_places = "?,?"
    
    values = [name, profile]

    for of_position in outfield_positions:
       columns += ", " + str(of_position)
       column_places +=  ",?" 
       values.append(1)
      
    for infield_role in infield_roles:
       columns += ", " + str(infield_role)
       column_places +=  ",?"
       values.append(1)

    db.execute(f"INSERT INTO players ({columns}) VALUES ({column_places})",values)
        
    return render_template("result.html", name=firstname + str(" ") + surname, outfield_positions=outfield_positions, infield_roles=infield_roles, profile=profile)

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