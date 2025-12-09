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

def add_player(name, profile, user_id, classes, roles):
        
    columns = "NAME, PROFILE, user_id"
    column_places = "?,?,?"
    values = [name, profile,user_id]
    db.execute(f"INSERT INTO players ({columns}) VALUES ({column_places})",values)
    
    ### If first player, goes to except
    try:
        last_id = int(db.last_insert_id())
    except:
        last_id = 0
            
    ### classes
    for title, value in classes:
        sql = "INSERT INTO player_classes (player_id, title, value) VALUES (?, ?, ?);"
        db.execute(sql,[last_id, title, value])

    ### roles
    for role_type, role_name in roles:
        sql = """
        INSERT INTO player_roles (player_id, role_type, role_name, role_value)
        VALUES (?, ?, ?, 1);
        """
        db.execute(sql,[last_id, role_type, role_name])

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

def get_roles(player_id):
    sql = "SELECT role_type, role_name FROM player_roles WHERE player_id = ?;"

    return db.query(sql, [player_id])

def get_player(player_id):
        
        sql = """
                SELECT id, name, profile, user_id
                FROM players
                WHERE id = ?;
              """
        ### if no player with player_id, goes to except
        try:
            player_info = db.query(sql, [player_id])[0]
            user_id = player_info['user_id']
        except:
            player_info = None

        #### USER INFO
        sql = """
                SELECT id, username
                FROM users
                WHERE id = ?;
              """
        
        ### if no player with user_id, goes to except
        try:
            user_info = db.query(sql, [user_id])[0]
        except:
            user_info = None
        
        ### roles
        sql = """
                SELECT role_type, role_name
                FROM player_roles
                WHERE player_id = ? AND role_value = 1;
              """
        
        roles = db.query(sql, [player_id])

        ### result
        result = player_info, user_info, roles

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
        db.execute(sql,[player_id, title, value])

    ### update roles
    for role_type, role_name in roles:
       sql = """INSERT INTO player_roles (player_id, role_type, role_name, role_value)
                VALUES (?, ?, ?, 1);"""
       db.execute(sql,[player_id, role_type, role_name])
        
def remove_player(player_id):
    ### remove classes and role
    sql = "DELETE FROM player_classes WHERE player_id = ?"
    db.execute(sql, [player_id])

    sql = "DELETE FROM player_roles WHERE player_id = ?"
    db.execute(sql, [player_id])

    ### remove player
    sql = "DELETE FROM players WHERE id = ?"
    db.execute(sql, [player_id])

def find_players(query):

    sql = """
        SELECT players.id, players.name, player_classes.value
        FROM players 

        LEFT JOIN player_classes ON player_classes.player_id = players.id
        WHERE name LIKE ? or profile like ?
        """
    like = "%" + query + "%"
    return db.query(sql,[like, like])