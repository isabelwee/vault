from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

class myAES:
    iv = get_random_bytes(16)

    def encrypt(self, plaintext, key):
        cipher = AES.new(key, AES.MODE_CBC, self.iv)
        ciphertextBytes = cipher.encrypt(pad(plaintext.encode('utf-8'), AES.block_size))
        return base64.b64encode(self.iv + ciphertextBytes).decode('utf-8')
        
