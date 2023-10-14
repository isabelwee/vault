
def get_row():
    return """SELECT * FROM vault WHERE app_name = %s"""

def insert_row():
    return """INSERT INTO Vault (app_name, username, user_email, password) VALUES (%s, %s, %s, %s)"""
