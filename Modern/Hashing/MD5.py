class MD5():
    def __init__(self,message):
        self.message=message
        self.s=self.generate_s()
        self.k=self.generate_k()

    def generate_s(self):
        return [7,12,17,22]*4+[5,9,14,20]*4+[4,11,16,23]*4+[6,10,15,21]*4
        
    def generate_k(self):
        return [0xd76aa478,0xe8c7b756,0x242070db,0xc1bdceee,0xf57c0faf,0x4787c62a,0xa8304613,0xfd469501,
                0x698098d8,0x8b44f7af,0xffff5bb1,0x895cd7be,0x6b901122,0xfd987193,0xa679438e,0x49b40821,
                0xf61e2562,0xc040b340,0x265e5a51,0xe9b6c7aa,0xd62f105d,0x02441453,0xd8a1e681,0xe7d3fbc8,
                0x21e1cde6,0xc33707d6,0xf4d50d87,0x455a14ed,0xa9e3e905,0xfcefa3f8,0x676f02d9,0x8d2a4c8a,
                0xfffa3942,0x8771f681,0x6d9d6122,0xfde5380c,0xa4beea44,0x4bdecfa9,0xf6bb4b60,0xbebfbc70,
                0x289b7ec6,0xeaa127fa,0xd4ef3085,0x04881d05,0xd9d4d039,0xe6db99e5,0x1fa27cf8,0xc4ac5665,
                0xf4292244,0x432aff97,0xab9423a7,0xfc93a039,0x655b59c3,0x8f0ccc92,0xffeff47d,0x85845dd1,
                0x6fa87e4f,0xfe2ce6e0,0xa3014314,0x4e0811a1,0xf7537e82,0xbd3af235,0x2ad7d2bb,0xeb86d391]
    
    def rotate_left(self,number,shift,size=32):
        return ((number<<shift)|(number>>(size-shift)))&0xFFFFFFFF
    
    def adjust_message(self):
        adjusted_message=bytearray(self.message,"utf-8")
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

            a0=a0+A&0xFFFFFFFF
            b0=b0+B&0xFFFFFFFF
            c0=c0+C&0xFFFFFFFF
            d0=d0+D&0xFFFFFFFF
        
        return sum(buffer_content<<(32*i) for i,buffer_content in enumerate([a0,b0,c0,d0])).to_bytes(16,'little').hex()       