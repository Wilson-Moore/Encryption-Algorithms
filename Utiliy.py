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