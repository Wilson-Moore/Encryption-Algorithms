class Playfair():
    def __init__(self,message,key):
        self.message=self.adjust_message(message)
        self.key=self.remove_duplicate(key)
        self.grid=self.create_grid()

    def adjust_message(self,message):
        i=0
        while i<len(message)-1:
            if message[i]==message[i+1]:
                message=message[:i+1]+"x"+message[i+1:]
            i+=1
        if len(message)%2==1:
            message+="x"
        return message
    
    def readjust_message(self,message):
        i=0
        while i<len(message)-2:
            if message[i]==message[i+2] and message[i+1]=="x":
                message=message[:i+1]+message[i+2:]
            i+=1
        if message[-1]=="x":
            message=message[:-1]
        return message

    def remove_duplicate(self,key):
        key=key.replace("j","i")+"abcdefghiklmnopqrstuvwxyz"
        return "".join(dict.fromkeys(key))
    
    def create_grid(self):
        return [[k for k in self.key[i:i+5]] for i in range(0,25,5)]
    
    def find_location(self,char):
        for i in range(0,5):
            for j in range(0,5):
                if self.grid[i][j]==char:
                    return i,j
    
    def encrypt(self):
        encrypted_message=""
        for i in range(0,len(self.message),2):
            digraph=self.message[i:i+2]
            x1,y1=self.find_location(digraph[0])
            x2,y2=self.find_location(digraph[1])
            if x1==x2:
                substitute1=self.grid[x1][(y1+1)%5]
                substitute2=self.grid[x2][(y2+1)%5]
            elif y1==y2:
                substitute1=self.grid[(x1+1)%5][y1]
                substitute2 = self.grid[(x2+1)%5][y2]
            else:
                substitute1=self.grid[x1][y2]
                substitute2=self.grid[x2][y1]
            encrypted_message+=substitute1+substitute2
        return encrypted_message
    
    def decrypt(self,encrypted_message):
        message=""
        for i in range(0,len(encrypted_message),2):
            digraph=encrypted_message[i:i+2]
            x1,y1=self.find_location(digraph[0])
            x2,y2=self.find_location(digraph[1])
            if x1==x2:
                substitute1=self.grid[x1][(y1-1)%5]
                substitute2=self.grid[x2][(y2-1)%5]
            elif y1==y2:
                substitute1=self.grid[(x1-1)%5][y1]
                substitute2 = self.grid[(x2-1)%5][y2]
            else:
                substitute1=self.grid[x1][y2]
                substitute2=self.grid[x2][y1]
            message+=substitute1+substitute2
        return self.readjust_message(message)

# pf=Playfair("helloworld","key")
# print(pf.encrypt())
# print(pf.decrypt(pf.encrypt()))