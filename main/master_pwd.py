from bcrypt import hashpw, checkpw, gensalt

def get_hashed_masterpwd(plaintext_pwd):
    return hashpw(plaintext_pwd, gensalt())

def is_masterpwd(plaintext, hashed):
    return checkpw(plaintext, hashed)