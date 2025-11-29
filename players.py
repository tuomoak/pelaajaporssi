import db

def add_player(firstname, surname, defence_positions, batting_roles, profile, user_id):
        
    name=firstname + str(" ") + surname
  
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

    for def_position in defence_positions:
       eng_def_position, fi_def_position = def_position.split("|")
       fi_defence_positions.append(fi_def_position)
       columns += ", " + str(eng_def_position)
       column_places +=  ",?" 
       values.append(1)
       sql = """
        INSERT INTO player_def_roles (player_id, role_name_eng, role_name_fi, role_value)
        VALUES (?, ?, ?, 1);
        """
       db.execute(sql,[new_id, str(eng_def_position), str(fi_def_position)])
      
    for batting_role in batting_roles:
       eng_batting_role, fi_batting_role = batting_role.split("|")
       fi_batting_roles.append(fi_batting_role)
       columns += ", " + str(eng_batting_role)
       column_places +=  ",?"
       values.append(1)
       sql = """
        INSERT INTO player_bat_roles (player_id, role_name_eng, role_name_fi, role_value)
        VALUES (?, ?, ?, 1);
        """
       db.execute(sql,[new_id, str(eng_batting_role), str(fi_batting_role)])

    #db.execute(f"INSERT INTO players ({columns}) VALUES ({column_places})",values)

    return fi_defence_positions, fi_batting_roles

def get_players():
    sql = """
        SELECT name, id FROM players ORDER BY id DESC
          """
    
    return db.query(sql)


def get_player(player_id):
        
        sql = """
                SELECT id, name, profile, user_id
                FROM players
                WHERE id = ?;
              """

        player_info = db.query(sql, [player_id])[0]
                
        
        sql = """
                SELECT role_name_fi
                FROM player_def_roles
                WHERE player_id = ?;
              """
        
        def_roles = db.query(sql, [player_id])


        sql = """
                SELECT role_name_fi
                FROM player_bat_roles
                WHERE player_id = ?;
              """
        
        bat_roles = db.query(sql, [player_id])

        return player_info, def_roles, bat_roles
        #return db.query(sql, [player_id])[0]  