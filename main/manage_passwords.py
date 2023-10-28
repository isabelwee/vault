from connect_db import connect_to_db
import sql_queries
import sys


def get_db_masterpwd():
    db = connect_to_db()
    cur = db.cursor()

    cur.execute(sql_queries.db_get_row(), ['~'])
    account = cur.fetchall()
    cur.close()

    return account[0][4]