import math as mt

class MD5():
    def __init__(self,message):
        self.message=message
        self.s=self.generate_s()
        self.k=self.generate_k()

    def generate_s(self):
        return [7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
                5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
                4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
                6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21]
        
    def generate_k(self):
        return [int(abs(pow(2,32)*mt.sin(i+1))) for i in range(64)]
    
    def rotate_left(self,number,shift,size=32):
        return ((number<<shift)|(number>>size-shift))
    
    def adjust_message(self):
        adjusted_message=bytearray(self.message,"ascii")
        length=(len(adjusted_message)*8)
        adjusted_message.append(0x80)
        while (len(adjusted_message)*8)%512!=448:
            adjusted_message.append(0x00)
        adjusted_message+=length.to_bytes(8,"little")
        return adjusted_message

    def hash(self):
        adjusted_message=self.adjust_message()
        blocks=[adjusted_message[i:i+64] for i in range(0,len(adjusted_message),64)]
        
        a0,b0,c0,d0=0x67452301,0xefcdab89,0x98badcfe,0x10325476
        for block in blocks:
            A,B,C,D=a0,b0,c0,d0
            for i in range(64):
                F,G=0,0
                if i<16:
                    F=(B&C)|(~B&D)
                    G=i
                elif i>=16 and i<32:
                    F=(D&B)|(~D&C)
                    G=(5*i+1)%16
                elif i>=32 and i<48:
                    F=B^C^D
                    G=(3*i+5)%16
                else:
                    F=C^(B|~D)
                    G=(7*i)%16
                F=(F+A+self.k[i]+int.from_bytes(block[G*4:G*4+4],"little"))&0xFFFFFFFF
                A,D,C=D,C,B
                B=(B+self.rotate_left(F,self.s[i]))&0xFFFFFFFF

            a0=a0+A
            b0=b0+B
            c0=c0+C
            d0=d0+D
        
        return sum(buffer_content<<(32*i) for i,buffer_content in enumerate([a0,b0,c0,d0])).to_bytes(16,'little').hex()

# md5=MD5("Hello, World!")
# print(md5.hash())        