import db

def get_all_classes():
    sql = "SELECT title, value FROM classes ORDER BY id"
    result = db.query(sql)

    classes = {}
    for title, value in result:
        classes[title] = []
    for title, value in result:
        classes[title].append(value)

    return classes

def get_all_roles():
    sql = "SELECT title, value FROM roles ORDER BY id"
    result = db.query(sql)

    roles = {}
    for title, value in result:
        roles[title] = []
    for title, value in result:
        roles[title].append(value)

    return roles

def get_all_ideas():
    sql = "SELECT title, value FROM ideas ORDER BY id"
    result = db.query(sql)

    ideas = {}
    for title, value in result:
        ideas[title] = []
    for title, value in result:
        ideas[title].append(value)

    return ideas

def get_all_contacts():
    sql = "SELECT title, value FROM contacts ORDER BY id"
    result = db.query(sql)

    contacts = {}
    for title, value in result:
        contacts[title] = []
    for title, value in result:
        contacts[title].append(value)

    return contacts

def add_player(name, profile, user_id, classes, roles):
    sql = "INSERT INTO players (NAME, PROFILE, user_id) VALUES (?, ?, ?);"
    db.execute(sql, [name, profile, user_id])

    ### If first player, goes to except
    try:
        last_id = int(db.last_insert_id())
    except:
        last_id = 0

    ### classes
    for title, value in classes:
        sql = "INSERT INTO player_classes (player_id, title, value) VALUES (?, ?, ?);"
        db.execute(sql, [last_id, title, value])

    ### roles
    for role_type, role_name in roles:
        sql = """
            INSERT INTO player_roles (player_id, role_type, role_name, role_value)
            VALUES (?, ?, ?, 1);
            """
        db.execute(sql, [last_id, role_type, role_name])

    return last_id

def get_players():
    sql = """
        SELECT players.id, players.name, player_classes.value 
        FROM players 
        LEFT JOIN player_classes ON player_classes.player_id = players.id
        ORDER BY players.id DESC"""

    return db.query(sql)

def get_classes(player_id):
    sql = "SELECT title, value FROM player_classes WHERE player_id = ?;"
    return db.query(sql, [player_id])

def get_player_ideas(player_id):
    sql = """SELECT pi.id, pi.title, pi.value, pi.user_id, pi.contact_type, u.username
             FROM player_ideas AS pi
             LEFT JOIN users as u ON u.id = pi.user_id
            WHERE player_id = ?;"""

    return db.query(sql, [player_id])

def get_idea(idea_id):
    sql = """
            SELECT pi.id, pi.title, pi.value, pi.user_id, pi.contact_type, u.username
            FROM player_ideas AS pi
            LEFT JOIN users as u ON u.id = pi.user_id
            WHERE pi.id = ?;"""

    return db.query(sql, [idea_id])

def remove_idea(idea_id):
    sql = "DELETE FROM player_ideas WHERE id = ?"
    db.execute(sql, [idea_id])

def get_roles(player_id):
    sql = "SELECT role_type, role_name FROM player_roles WHERE player_id = ?;"

    return db.query(sql, [player_id])

def get_player(player_id):

    sql = """SELECT pl.id, pl.name, pl.profile, pl.user_id, u.username, pr.role_name, pr.role_type
            FROM players AS pl
            LEFT JOIN users AS u ON u.id = pl.user_id
            LEFT JOIN player_roles AS pr ON pr.player_id = pl.id AND pr.role_value = 1
            WHERE pl.id = ? ;"""

    ### if no player with player_id, goes to except
    try:
        player_info = db.query(sql, [player_id])
        #user_id = player_info['user_id']
    except:
        player_info = None

    result = player_info

    return result if result else None

def update_player(player_id, name, profile, classes, roles):

    sql = """UPDATE players SET name = ?,
                                profile = ?
                                WHERE id = ?"""

    db.execute(sql, [name, profile, player_id])

    ### remove old classes
    sql = "DELETE FROM player_classes WHERE player_id = ?"
    db.execute(sql, [player_id])

    ### remove old roles
    sql = "DELETE FROM player_roles WHERE player_id = ?"
    db.execute(sql, [player_id])

    #### updates classes
    for title, value in classes:
        sql = "INSERT INTO player_classes (player_id, title, value) VALUES (?, ?, ?);"
        db.execute(sql, [player_id, title, value])

    ### update roles
    for role_type, role_name in roles:
        sql = """INSERT INTO player_roles (player_id, role_type, role_name, role_value)
                VALUES (?, ?, ?, 1);"""
        db.execute(sql, [player_id, role_type, role_name])

def remove_player(player_id):
    ### remove classes and role
    sql = "DELETE FROM player_classes WHERE player_id = ?"
    db.execute(sql, [player_id])

    sql = "DELETE FROM player_roles WHERE player_id = ?"
    db.execute(sql, [player_id])

    ###remove ideas
    sql = "DELETE FROM player_ideas WHERE player_id = ?"
    db.execute(sql, [player_id])

    ### remove player
    sql = "DELETE FROM players WHERE id = ?"
    db.execute(sql, [player_id])

def suggest_idea(player_id, ideas, contacts, user_id):

    for title, value in contacts:
        contact_type = value

    for title, value in ideas:
        sql = """INSERT INTO player_ideas (player_id, title, value, contact_type, user_id)
                VALUES (?, ?, ?, ?,?);
                """
        db.execute(sql, [player_id, title, value, contact_type, user_id])

def find_players(query):

    sql = """
        SELECT players.id, players.name, player_classes.value
        FROM players 
        LEFT JOIN player_classes ON player_classes.player_id = players.id
        WHERE name LIKE ? or profile like ?
        """
    like = "%" + query + "%"
    return db.query(sql, [like, like])
