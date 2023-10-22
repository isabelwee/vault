
def get_row():
    return """SELECT * FROM vault WHERE app_name = %s"""

def insert_row():
    return """INSERT INTO vault (app_name, username, user_email, password) VALUES (%s, %s, %s, %s)"""

def insert_row_no_username():
    return """INSERT INTO vault (app_name, user_email, password) VALUES (%s, %s, %s)"""