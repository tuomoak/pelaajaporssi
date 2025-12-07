import db

def add_player(name, defence_positions, batting_roles, profile, user_id, classes):
        
    columns = "NAME, PROFILE, user_id"
    column_places = "?,?,?"
    
    values = [name, profile,user_id]

    fi_defence_positions = []
    fi_batting_roles = []

    db.execute(f"INSERT INTO players ({columns}) VALUES ({column_places})",values)
    
    try:
        last_id = int(db.last_insert_id())
    except:
        last_id = 0
            
    new_id = last_id

    ### classes
    for title, value in classes:
        sql = "INSERT INTO player_classes (player_id, title, value) VALUES (?, ?, ?);"
        db.execute(sql,[new_id, title, value])

    for def_position in defence_positions:
       eng_def_position, fi_def_position = def_position.split("|")
       sql = """
        INSERT INTO player_def_roles (player_id, role_name_eng, role_name_fi, role_value)
        VALUES (?, ?, ?, 1);
        """
       db.execute(sql,[new_id, str(eng_def_position), str(fi_def_position)])
      
    for batting_role in batting_roles:
       eng_batting_role, fi_batting_role = batting_role.split("|")
       sql = """
        INSERT INTO player_bat_roles (player_id, role_name_eng, role_name_fi, role_value)
        VALUES (?, ?, ?, 1);
        """
       db.execute(sql,[new_id, str(eng_batting_role), str(fi_batting_role)])

    return last_id

def get_players():
    sql = """
        SELECT name, id FROM players ORDER BY id DESC
          """
    
    return db.query(sql)

def get_classes(player_id):
    sql = "SELECT title, value FROM player_classes WHERE player_id = ?;"

    return db.query(sql, [player_id])

def get_player(player_id):
        
        sql = """
                SELECT id, name, profile, user_id
                FROM players
                WHERE id = ?;
              """

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
        
        try:
            user_info = db.query(sql, [user_id])[0]
        except:
            user_info = None
        
        ### defence_roles
        sql = """
                SELECT role_name_eng, role_name_fi
                FROM player_def_roles
                WHERE player_id = ? AND role_value = 1;
              """
        
        def_roles = db.query(sql, [player_id])

        ### bat_roles
        sql = """
                SELECT role_name_eng, role_name_fi
                FROM player_bat_roles
                WHERE player_id = ? AND role_value = 1;
              """
        
        bat_roles = db.query(sql, [player_id])

        ### result
        result = player_info, def_roles, bat_roles, user_info

        return result if result else None

def update_player(player_id, name, defence_positions, batting_roles, profile, classes):

    sql = """UPDATE players SET name = ?,
                                profile = ?
                                WHERE id = ?"""
    
    db.execute(sql, [name, profile, player_id])


    ### remove old classes
    sql = """DELETE FROM player_classes
                                WHERE player_id = ?"""
    db.execute(sql, [player_id])

    #### removes old def roles
    sql = """DELETE FROM player_def_roles
                            WHERE player_id = ?"""
    db.execute(sql, [player_id])
 
    ### removes old bat roles
    sql = """DELETE FROM player_bat_roles
                            WHERE player_id = ?"""

    db.execute(sql, [player_id])

    #### updates classes, def and bat roles
    for title, value in classes:
        sql = "INSERT INTO player_classes (player_id, title, value) VALUES (?, ?, ?);"
        db.execute(sql,[player_id, title, value])

    for def_position in defence_positions:
       eng_def_position, fi_def_position = def_position.split("|")
       sql = """INSERT INTO player_def_roles (player_id, role_name_eng, role_name_fi, role_value)
                VALUES (?, ?, ?, 1);"""
       db.execute(sql,[player_id, str(eng_def_position), str(fi_def_position)])
      
    for batting_role in batting_roles:
       eng_batting_role, fi_batting_role = batting_role.split("|")
       sql = """INSERT INTO player_bat_roles (player_id, role_name_eng, role_name_fi, role_value)
                VALUES (?, ?, ?, 1);"""
       db.execute(sql,[player_id, str(eng_batting_role), str(fi_batting_role)])

def remove_player(player_id):

    sql = "DELETE FROM player_classes WHERE player_id = ?"
    
    db.execute(sql, [player_id])

    sql = "DELETE FROM player_bat_roles WHERE player_id = ?"
    
    db.execute(sql, [player_id])

    sql = "DELETE FROM player_def_roles WHERE player_id = ?"
    
    db.execute(sql, [player_id])

    sql = "DELETE FROM players WHERE id = ?"
    
    db.execute(sql, [player_id])

def find_players(query):

    sql = """
        SELECT id, name FROM players WHERE name LIKE ? or profile like ?
          """
    like = "%" + query + "%"
    return db.query(sql,[like, like])