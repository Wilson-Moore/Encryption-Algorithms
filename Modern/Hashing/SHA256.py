class SHA256():
    def __init__(self,message):
        self.message=message
        self.k=self.generate_k()

    def generate_k(self):
        return [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
                0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
                0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
                0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
                0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
                0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
                0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
                0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2]
    
    def rotate_right(self,number,shift,size=32):
        return (number>>shift)|(number<<size-shift)

    def sigma0(self,number):
        return (self.rotate_right(number,7)^self.rotate_right(number,18)^(number>>3))
    
    def sigma1(self,number):
        return (self.rotate_right(number,17)^self.rotate_right(number,19)^(number>>10))
    
    def capsigma0(self,number):
        return (self.rotate_right(number,2)^self.rotate_right(number,13)^self.rotate_right(number,22))
    
    def capsigma1(self,number):
        return (self.rotate_right(number,6)^self.rotate_right(number,11)^self.rotate_right(number,25))
    
    def ch(self,x,y,z):
        return (x&y)^(~x&z)
    
    def maj(self,x,y,z):
        return (x&y)^(x&z)^(y&z)
    
    def adjust_message(self):
        adjusted_message=bytearray(self.message,"ascii")
        length=len(adjusted_message)*8
        adjusted_message.append(0x80)
        while(len(adjusted_message)*8+64)%512!=0:
            adjusted_message.append(0x00)
        adjusted_message+=length.to_bytes(8,"big")
        return adjusted_message

    def hash(self):
        adjusted_message=self.adjust_message()
        blocks=[adjusted_message[i:i+64] for i in range(0,len(adjusted_message),64)]

        h0,h1,h2,h3,h4,h5,h6,h7=[0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19]

        for block in blocks:
            message_schedule=[]
            for i in range(64):
                if i<=15:
                    message_schedule.append(bytes(block[i*4:(i*4)+4]))
                else:
                    term1=self.sigma1(int.from_bytes(message_schedule[i-2],"big"))
                    term2=int.from_bytes(message_schedule[i-7],"big")
                    term3=self.sigma0(int.from_bytes(message_schedule[i-15],"big"))
                    term4=int.from_bytes(message_schedule[i-16],"big")
                    schedule=((term1+term2+term3+term4)%pow(2,32)).to_bytes(4,"big")
                    message_schedule.append(schedule)
            
            a,b,c,d,e,f,g,h=h0,h1,h2,h3,h4,h5,h6,h7

            for i in range(64):
                t1=((h+self.capsigma1(e)+self.ch(e,f,g)+self.k[i]+int.from_bytes(message_schedule[i],"big"))%pow(2,32))
                t2=(self.capsigma0(a)+self.maj(a,b,c))%pow(2,32)
                h,g,f=g,f,e
                e=(d+t1)%pow(2,32)
                d,c,b=c,b,a
                a=(t1+t2)%pow(2,32)
            
            h0=(h0+a)%pow(2,32)
            h1=(h1+b)%pow(2,32)
            h2=(h2+c)%pow(2,32)
            h3=(h3+d)%pow(2,32)
            h4=(h4+e)%pow(2,32)
            h5=(h5+f)%pow(2,32)
            h6=(h6+g)%pow(2,32)
            h7=(h7+h)%pow(2,32)

        return((h0).to_bytes(4,"big")+(h1).to_bytes(4,"big")+(h2).to_bytes(4,"big")+(h3).to_bytes(4,"big")+
               (h4).to_bytes(4,"big")+(h5).to_bytes(4,"big")+(h6).to_bytes(4,"big")+(h7).to_bytes(4,"big")).hex()
