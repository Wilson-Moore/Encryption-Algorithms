class Vigenere:
    def __init__(self,message,key):
        self.message=message
        self.key=key if key else "Key"
        self.alphabet=self.generate_alphabet()
        self.letters_dictionary=dict(zip(self.alphabet,range(len(self.alphabet))))
        self.index_dictionary=dict(zip(range(len(self.alphabet)),self.alphabet))

    def generate_alphabet(self):
        alphabet="abcdefghijklmnopqrstuvwxyz"
        alphabet+="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        alphabet+=" ,.!?-'"
        return alphabet
    
    def encrypt(self):
        encrypted_message=""
        split_message=[self.message[i:i+len(self.key)] for i in range(0,len(self.message),len(self.key))]
        for split in split_message:
            i=0
            for letter in split:
                num=(self.letters_dictionary[letter]+self.letters_dictionary[self.key[i]])%len(self.alphabet)
                encrypted_message += self.index_dictionary[num]
                i+=1
        return encrypted_message
    
    def decrypt(self,encrypted_message):
        message=""
        split_message=[encrypted_message[i:i+len(self.key)] for i in range(0,len(encrypted_message),len(self.key))]
        for split in split_message:
            i=0
            for letter in split:
                num=(self.letters_dictionary[letter]-self.letters_dictionary[self.key[i]])%len(self.alphabet)
                message+=self.index_dictionary[num]
                i+=1
        return message
    