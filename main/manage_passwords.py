from connect_db import connect_to_db
from Crypto.Cipher import AES 
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
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


def encrypt_password(plaintext):
    key = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_EAX)
    encrypted, tag = cipher.encrypt_and_digest(str.encode(plaintext))

    nonce = cipher.nonce
    add_nonce = encrypted + nonce
    
    return b64encode(add_nonce).decode()


def decrypt_password(encrypted):
    
    return 