from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

class myAES:

    def encrypt(self, plaintext, key):
        cipher = AES.new(key, AES.MODE_CBC)
        iv = cipher.iv
        ciphertextBytes = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
        return base64.b64encode(iv + ciphertextBytes).decode('utf-8')
        
