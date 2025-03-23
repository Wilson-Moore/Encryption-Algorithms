import random as rd
import math as mt

class RSA:
    def __init__(self,message):
        self.message=message
        self.public_key,self.private_key=self.generate_keys()

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
    
    def mod_inverse(self,e,phi):
        for d in range(3,phi):
            if (d*e)%phi==1:
                return d
            
    def generate_keys(self):
        p=self.generate_prime(1000,2000)
        q=self.generate_prime(1000,2000)
        while p==q:
            q=self.generate_prime(1000,2000)
        n=p*q
        phi=(p-1)*(q-1)
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

# rsa=RSA("Hello, World!")
# print(f"Public Key: {rsa.public_key}")
# print(f"Private Key: {rsa.private_key}")
# print(f"Message: {rsa.message}")
# print(f"Encrypted Message: {rsa.encrypt()}")
# print(f"decrypted Message: {rsa.decrypt(rsa.encrypt())}")