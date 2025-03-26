import random as rd
import math as mt

class DH():
    def __init__(self,message,key):
        self.message=message
        self.public_key=self.generate_public_key()
        self.private_key=self.generate_private_key(key)
        self.shared_key=self.generate_shared_key()
        
    def is_prime(self,num):
        if num<2:
            return False
        for i in range(2,int(mt.sqrt(num)+1)):
            if num%i==0:
                return False
        return True
    
    def generate_prime(self,min,max):
        prime=rd.randint(min,max)
        while not self.is_prime(prime):
            prime=rd.randint(min,max)
        return prime
    
    def generate_public_key(self):
        modulus=self.generate_prime(1000,2000)
        base=rd.randint(2,modulus-1)
        return (base,modulus)

    def generate_private_key(self,key):
        return sum([ord(char) for char in key])

    def generate_intermidate_key(self):
        base,modulus=self.public_key
        return pow(base,self.private_key,modulus)
    
    def generate_shared_key(self):
        intermidate_key,modulus=self.generate_intermidate_key(),self.public_key[1]
        return pow(intermidate_key,self.private_key,modulus)
    
    def encrypt(self):
        encrypted_message=""
        for char in self.message:
            encrypted_message+=chr(ord(char)+self.shared_key)
        return encrypted_message
    
    def decrypt(self, encrypted_message):
        message=""
        for c in encrypted_message:
            message+=chr((ord(c)-self.shared_key))
        return message

# dh=DH("Hello, World!","key")
# print(dh.encrypt())
# print(dh.decrypt(dh.encrypt()))