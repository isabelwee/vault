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
    
    return pwd

def write_key():
    key = get_random_bytes(32)
    with open("key.key", "wb") as f:
        f.write(key)

def get_key():
    with open("key.key", "rb") as f:
        key = f.read()
        return key


def encrypt_password(plaintext):
    key = get_key()
    iv = get_random_bytes(AES.block_size)

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_bytes = plaintext.encode('utf-8')

    # pad password to be a multiple of 16 bytes
    padding_len = AES.block_size - len(plaintext_bytes) % AES.block_size
    padded_password = plaintext_bytes + bytes([padding_len] * padding_len)

    ciphertext = cipher.encrypt(padded_password)
    encrypted_password = b64encode(iv + ciphertext).decode('utf-8')

    return encrypted_password


def decrypt_password(encrypted_pwd):
    key = get_key()
    encrypted_data = b64decode(encrypted_pwd)

    # extract the IV and ciphertext
    iv = encrypted_data[:AES.block_size]
    ciphertext = encrypted_data[AES.block_size:]

    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted = cipher.decrypt(ciphertext)

    # unpad the password
    padding_len = decrypted[-1]
    decrypted = decrypted[:-padding_len]

    return decrypted.decode()