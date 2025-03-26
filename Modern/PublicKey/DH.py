import random as rd
import math as mt

def is_prime(num):
        if num<2:
            return False
        for i in range(2,int(mt.sqrt(num)+1)):
            if num%i==0:
                return False
        return True
    
def generate_prime(min,max):
    prime=rd.randint(min,max)
    while not is_prime(prime):
        prime=rd.randint(min,max)
    return prime

class DH():
    def __init__(self,base,modulus):
        self.base=base
        self.modulus=modulus
        self.private_key=rd.randint(2,self.modulus-2)

    def generate_public_key(self):
        return pow(self.base,self.private_key,self.modulus)
    
    def generate_secret_key(self,public_key):
        return pow(public_key,self.private_key,self.modulus)

# modulus=generate_prime(1000,2000)
# base=rd.randint(2,modulus-1)
# dh1=DH(base,modulus)
# dh2=DH(base,modulus)
# print(f"DH1 public key {dh1.generate_public_key()},DH2 public key {dh2.generate_public_key()}")
# print(f"DH1 secret key {dh1.generate_secret_key(dh2.generate_public_key())},DH2 secret key {dh2.generate_secret_key(dh1.generate_public_key())}")