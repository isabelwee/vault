import psycopg2
import sys


def connect_to_db():
    try:
        db = psycopg2.connct(dbname="VaultDB")
    except psycopg2.Error as err:
        print("DB error: ", err)
    except Exception as err:
        print("Internal Error: ", err)
        raise err
    finally:
        if db is not None:
            db.close()
    sys.exit(0)
