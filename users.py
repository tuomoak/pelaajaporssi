import db

def get_user(user_id):
        
        sql = """
                SELECT id, username
                FROM users
                WHERE id = ?;
              """

        try:
            user_info = db.query(sql, [user_id])[0]
        except:
            user_info = None
        
        result = user_info

        return result if result else None

def get_players(user_id):

    sql = """
        SELECT id, name FROM players WHERE user_id = ?
          """
    
    return db.query(sql,[user_id])