class Polybius():
    def __init__(self,message,key):
        self.message=message
        self.key=self.remove_duplicate(key)
        self.grid=self.create_grid()

    def remove_duplicate(self,key):
        key=key.replace("j","i")+"abcdefghiklmnopqrstuvwxyz"
        return "".join(dict.fromkeys(key))
    
    def create_grid(self):
        return [[k for k in self.key[i:i+5]] for i in range(0,25,5)]
    
    def find_location(self,char):
        for i in range(0,5):
            for j in range(0,5):
                if self.grid[i][j]==char:
                    return ((i+1)*10)+(j+1)
                
    def encrypt(self):
        encrypted_message=""
        for i in range(len(self.message)):
            encrypted_message+=str(self.find_location(self.message[i]))
        return encrypted_message
    
    def decrypt(self,encrypted_message):
        message=""
        for i in range(0,len(encrypted_message),2):
            location=int(encrypted_message[i:i+2])
            x,y=int(location/10),location%10
            message+=self.grid[x-1][y-1]
        return message
    
pb=Polybius("helloworld","key")
print()
print(pb.encrypt())
print(pb.decrypt(pb.encrypt()))