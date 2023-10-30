from connect_db import connect_to_db
from cryptography.fernet import Fernet
import sql_queries
import secrets, string, binascii

def get_db_masterpwd():
    db = connect_to_db()
    cur = db.cursor()

    cur.execute(sql_queries.db_get_row(), ['~'])
    account = cur.fetchall()
    cur.close()

    return account[0][3]

# adapted from https://geekflare.com/password-generator-python-code/
def generate_pwd():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    pwd_len = 12
    pwd = ''
    while True:
        for _ in range(pwd_len):
            pwd += ''.join(secrets.choice(alphabet))
        
        if any(char in string.punctuation for char in pwd) and sum(char in string.digits for char in pwd) >= 1:
            break
    
    return pwd.encode()

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    return open("key.key", "rb").read()

def encrypt_password(plaintext):
    key = load_key()
    f = Fernet(key)
    encrypted = f.encrypt(plaintext)

    return encrypted

def decrypt_password(encrypted):
    key = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted)