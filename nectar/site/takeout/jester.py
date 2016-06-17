#coding:cp936
import os
import requests
import zlib
import base64
import json
from Crypto.Cipher import AES
from Crypto import Random

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

class AESCipher:
    def __init__(self, key):
        self.key = base64.b64decode(key)

    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return cipher.decrypt(enc[16:])

class Jester:
    def __init__(self):
        self.cipher = AESCipher(os.environ['JESTER_KEY'])

    def query(self, ssid):
        additional_headers = {}
        additional_headers['content-type'] = 'application/json'
        additional_headers['content-encoding'] = 'deflate'
        # 加密
        params = {}
        params['ssid'] = ssid
        compressed = zlib.compress(json.dumps(params))
        request_body = self.cipher.encrypt(compressed)

        endpoint_url = "http://106.75.6.12:9980/v1/sdk-ap/query"
        r = requests.post(endpoint_url, data=request_body,
                          headers=additional_headers)
        return r.json()

