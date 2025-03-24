import random as rd
import math as mt

class DH():
    def __init__(self,message):
        self.message=message
        self.prime=self.generate_prime(1000,2000)
        self.private_key=rd.randint(2,self.prime-1)
        self.public_key1,self.public_key2=self.generate_public_keys()
        self.full_key=self.generate_full_key()
        
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
    
    def calculate_public_key(self,generator):
        return pow(generator,self.private_key,self.prime)

    def generate_public_keys(self):
        generator=rd.randint(2,self.prime-1)
        public_key1=self.calculate_public_key(generator)
        generator=rd.randint(2,self.prime-1)
        public_key2=self.calculate_public_key(generator)
        return public_key1,public_key2

    def generate_partial_key(self):
        return pow(self.public_key1,self.private_key,self.public_key2)

    def generate_full_key(self):
        return pow(self.generate_partial_key(),self.private_key,self.public_key2)
    
    def encrypt(self):
        encrypted_message=""
        for char in self.message:
            encrypted_message+=chr(ord(char)+self.full_key)
        return encrypted_message
    
    def decrypt(self, encrypted_message):
        message=""
        for c in encrypted_message:
            message += chr(ord(c)-self.full_key)
        return message

# dh=DH("Hello, World!")
# print(dh.encrypt())
# print(dh.decrypt(dh.encrypt()))