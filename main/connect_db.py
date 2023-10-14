#! /usr/bin/env python3
import psycopg2
import sys


def connect_to_db():
    try:
        return psycopg2.connect(dbname="vaultdb")
    except psycopg2.Error as err:
        print("DB error: ", err)
    except Exception as err:
        print("Internal Error: ", err)
        raise err

def close_db(db):
    if db is not None:
        db.close()