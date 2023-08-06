# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 23:25:49 2022

@author: anugrahshrivastava
"""
from cryptography.fernet import Fernet

class Encryptor():

    def key_create(self):
        key = Fernet.generate_key()
        return key

    def key_write(self, key, key_name):
        with open(key_name, 'wb') as mykey:
            mykey.write(key)

    def key_load(self, key_name):
        with open(key_name, 'rb') as mykey:
            key = mykey.read()
        return key
    
    def encrypt_text(self, key, text):
        f = Fernet(key)
        return str(f.encrypt(text))
    
    def decrypt_text(self, key, text):
        f = Fernet(key)
        return f.decrypt(bytes(text, encoding='utf8')).decode("utf-8") 

    def file_encrypt(self, key, original_file, encrypted_file):
        
        f = Fernet(key)

        with open(original_file, 'rb') as file:
            original = file.read()

        encrypted = f.encrypt(original)

        with open (encrypted_file, 'wb') as file:
            file.write(encrypted)

    def file_decrypt(self, key, encrypted_file):
        
        f = Fernet(key)

        with open(encrypted_file, 'rb') as file:
            encrypted = file.read()

        decrypted = f.decrypt(encrypted)
        return decrypted
            
'''
e = Encryptor()
e.file_encrypt(e.key_load('mykey.key'), 'db_config_dev.txt', 'enc_db_config.txt')
'''