import math as mt

class Transposition:
    def __init__(self,message,key):
        self.message=message
        self.key=key.lower() if key else "Key"

    def encrypt(self):
        message_length=len(self.message)
        message_list=list(self.message)
        key_list=sorted((char,i) for i,char in enumerate(self.key))

        column=len(self.key)
        row=int(mt.ceil(message_length/column))

        fill_empty=int((row*column)-message_length)
        message_list.extend("#"*fill_empty)
        matrix=[message_list[i:i+column] for i in range(0,len(message_list),column)]

        encrypted_message,index="",0
        
        for _ in range(column):
            current_index=key_list[index][1]
            encrypted_message+="".join([row[current_index] for row in matrix])
            index+=1
        return encrypted_message
    
    def decrypt(self,encrypted_message):
        message_index=0
        message_length=len(encrypted_message)
        message_list=list(encrypted_message)

        column=len(self.key)
        row=int(mt.ceil(message_length/column))

        key_list=sorted((char,i) for i,char in enumerate(self.key))

        decrypted_message=[]
        for _ in range(row):
            decrypted_message+=[[None]*column]

        message,index="",0

        for _ in range(column):
            current_index=key_list[index][1]
            for i in range(row):
                decrypted_message[i][current_index]=message_list[message_index]
                message_index+=1
            index+=1

        message="".join(sum(decrypted_message,[]))
        empty_count=message.count("#")
        
        return message[:-empty_count]
