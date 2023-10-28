
def db_get_row():
    return """SELECT * FROM vault WHERE app_name = %s"""

def db_insert_row():
    return """INSERT INTO vault (app_name, username, user_email, password) VALUES (%s, %s, %s, %s)"""

def db_insert_row_no_username():
    return """INSERT INTO vault (app_name, user_email, password) VALUES (%s, %s, %s)"""

def db_delete_row():
    return """DELETE FROM vault WHERE app_name = %s"""

def db_update_app_name():
    return """UPDATE vault SET app_name = %s WHERE app_name = %s"""

def db_update_username():
    return """UPDATE vault SET username = %s WHERE app_name = %s"""
    
def db_update_email():
    return """UPDATE vault SET email = %s WHERE app_name = %s"""

def db_update_password():
    return """UPDATE vault SET password = %s WHERE app_name = %s"""

