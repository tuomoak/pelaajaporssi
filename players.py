import db

def add_player(columns, column_places, values):
    db.execute(f"INSERT INTO players ({columns}) VALUES ({column_places})",values)



