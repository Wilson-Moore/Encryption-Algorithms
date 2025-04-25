import random as rd
import math as mt

class RSA:
    def __init__(self,message,p,q):
        self.message=message
        self.p=p
        self.q=q
        self.public_key,self.private_key=self.generate_keys()
    
    def mod_inverse(self,e,phi):
        return pow(e,-1,phi)
            
    def generate_keys(self):
        n=self.p*self.q
        phi=(self.p-1)*(self.q-1)
        e=rd.randint(3,phi-1)
        while mt.gcd(e,phi)!=1:
            e=rd.randint(3,phi-1)
        d=self.mod_inverse(e,phi)
        return ((e,n),(d,n))
    
    def encrypt(self):
        e,n=self.public_key
        return [pow(ord(char),e,n) for char in self.message]
    
    def decrypt(self,encrypted_message):
        d,n=self.private_key
        return "".join([chr(pow(char,d,n)) for char in encrypted_message])