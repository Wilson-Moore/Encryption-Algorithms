class PlayfairCipher:
    def __init__(self, key, text):
        self.alphabet = "abcdefghiklmnopqrstuvwxyz"
        self.key = key.replace(" ", "").lower() if key else self.alphabet
        self.text = text.replace(" ", "").lower().replace("j", "i")
        self.matrice5x5 = self.matrice()
    def removeDuplicate(self):
        repeated = set()
        not_repeated = []
        for char in self.key:
            if char not in repeated:
                repeated.add(char)
                not_repeated.append(char)

        return "".join(not_repeated)
    def matrice(self):
        key_unique = self.removeDuplicate()
        matrice = list(key_unique)
        for char in self.alphabet:
            if char not in matrice:
                matrice.append(char)

        return [matrice[i:i + 5] for i in range(0, 25, 5)]
    def paires(self):
        paires = []
        i = 0
        while i < len(self.text):
            a = self.text[i]
            if i + 1 < len(self.text):
                b = self.text[i + 1]
                if a == b:
                    b = "x"
                    paires.append((a, b))
                    i += 1
                else:
                    paires.append((a, b))
                    i += 2
            else:
                paires.append((a, "x"))
                i += 1
        return paires
    def readjust_message(self, text):
        i = 0
        while i < len(text) - 2:
            if text[i] == text[i + 2] and text[i + 1] == "x":
                text = text[:i + 1] + text[i + 2:]
            else:
                i += 1
    
        if text and text[-1] == "x":
            text = text[:-1]
    
        return text
    def findPosition(self, char):
        for i, row in enumerate(self.matrice5x5):
            if char in row:
                return i, row.index(char)
        return None
    def playfaireEncrypt(self):
        paires = self.paires()
        c = []
        for a, b in paires:
            rowA, colA = self.findPosition(a)
            rowB, colB = self.findPosition(b)

            if rowA == rowB:
                c.append(self.matrice5x5[rowA][(colA + 1) % 5])
                c.append(self.matrice5x5[rowB][(colB + 1) % 5])

            elif colA == colB:
                c.append(self.matrice5x5[(rowA + 1) % 5][colA])
                c.append(self.matrice5x5[(rowB + 1) % 5][colB])

            else:
                c.append(self.matrice5x5[rowB][colA])
                c.append(self.matrice5x5[rowA][colB])

        return self.readjust_message("".join(c))
    def playfaireDecrypt(self):

        paires = self.paires()
        c = []
        for a, b in paires:
            rowA, colA = self.findPosition(a)
            rowB, colB = self.findPosition(b)

            if rowA == rowB:
                c.append(self.matrice5x5[rowA][(colA - 1) % 5])
                c.append(self.matrice5x5[rowB][(colB - 1) % 5])

            elif colA == colB:
                c.append(self.matrice5x5[(rowA - 1) % 5][colA])
                c.append(self.matrice5x5[(rowB - 1) % 5][colB])

            else:
                c.append(self.matrice5x5[rowB][colA])
                c.append(self.matrice5x5[rowA][colB])

        return self.readjust_message("".join(c))
# pf=Playfair("helloworld","Key")
# print(pf.encrypt())
# print(pf.decrypt(pf.encrypt()))
