from base64 import b64encode, b64decode
from binascii import unhexlify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import random
import os,base64
import requests,os,sys,time,datetime
import pyfiglet,colorama,user_agent
import rich,re
from rich import *
import threading,zlib,marshal,lambda
from colorama import *
salamm3=AES.MODE_CBC
salamm4=AES.block_size
class SalamSource:
    def enc(salamm5):
        salamm22=pad(salamm5.encode(),salamm4)
        salamm=os.urandom(16)
        salamm1=AES.new(salamm,salamm3,salamm)
        salamm2=salamm1.encrypt(salamm22)
        out = b64encode(salamm2).decode('utf-8')
        out1 = b64encode(salamm).decode('utf-8')
        return f'{out1}??{out}'
    def ex(salamm99):
        salamm6= salamm99.split('??')[0]
        salamm7= salamm99.split('??')[1]
        salamm8= pad(salamm7.encode(),salamm4)
        salamm10 = AES.new(b64decode(salamm6),salamm3,b64decode(salamm6))
        exec(unpad(salamm10.decrypt(b64decode(salamm8)),salamm4).decode('utf-8'))


