import random as rd

class DH():
    def __init__(self,base,modulus):
        self.base=base
        self.modulus=modulus
        self.private_key=rd.randint(2,self.modulus-2)

    def generate_public_key(self):
        return pow(self.base,self.private_key,self.modulus)
    
    def generate_secret_key(self,public_key):
        return pow(public_key,self.private_key,self.modulus)