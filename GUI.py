from PyQt6.QtWidgets import (
    QApplication, QWidget, QHBoxLayout, QFrame, QVBoxLayout, QLabel, QPushButton, QTextEdit, QComboBox
)
import sys

from Classic.Substition.Playfair import Playfair
from Classic.Substition.Vigenere import Vigenere
from Classic.Permutation.Polybius import Polybius
from Classic.Permutation.Transposition import Transposition

from Modern.SecretKey.DES import DES
from Modern.SecretKey.AES import AES
from Modern.PublicKey.RSA import RSA
from Modern.PublicKey.DH import DH
from Modern.Hashing.MD5 import MD5
from Modern.Hashing.SHA256 import SHA256

class CryptoX(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CryptoX")
        self.setGeometry(100, 100, 600, 400)

        self.main = QHBoxLayout(self)

        # Left Section 
        self.left_frame = QFrame()
        self.left_section = QVBoxLayout()
        self.left_frame.setLayout(self.left_section)
        self.left_frame.setStyleSheet("background-color: #677E8A; padding: 10px;")

        # Right Section
        self.right_frame = QFrame()
        self.right_section = QVBoxLayout()
        self.right_frame.setLayout(self.right_section)
        self.right_frame.setStyleSheet("background-color: #0E1D21; padding: 10px;")

        # Drop Down Menu For Select A Method
        self.left_section.addWidget(QLabel("Select Encryption Method:"))
        self.encryption_dropdown = QComboBox()
        self.encryption_dropdown.addItems(["Playfair Cipher", "Vigenère Cipher",
                                            "Row Column Transposition", "Polybius",
                                            "DES", "AES",
                                            "MD5", "SHA-256",
                                            "Diffie-Hellman", "RSA"])
        self.left_section.addWidget(self.encryption_dropdown)
        self.encryption_dropdown.currentIndexChanged.connect(self.updateKeyPlaceHolder)
        # A Button To Perform Encryption
        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.clicked.connect(self.start_encrypt)
        self.left_section.addWidget(self.encrypt_button)
        self.encrypt_button.setStyleSheet("""
                            QPushButton {
                            color: white;
                            border: none;
                            padding: 10px;
                            border-radius: 5px;
                            border: 1px solid #fff;
                            }
                            QPushButton:hover {
                            background-color: #ffa586;
                            border: 1px solid #ffa586;
                            }
                            """)
        
        # A Button To Perform Decryption
        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.clicked.connect(self.start_decrypt)
        self.left_section.addWidget(self.decrypt_button)
        self.decrypt_button.setStyleSheet("""
                            QPushButton {
                            color: white;
                            border: none;
                            padding: 10px;
                            border-radius: 5px;
                            border: 0.5px solid #fff;
                            }
                            QPushButton:hover {
                            background-color: #ffa586;
                            border: 0.5px solid #ffa586;
                            }
                            """)
        
        # Key Input Field
        self.key_area = QTextEdit()
        self.key_area.setPlaceholderText("Enter Key ( Optionnel ) ...")
        self.key_area.setStyleSheet("border: 1px solid #ABAFB5; border-radius: 10px;")
        self.key_area.setFixedHeight(60)
        self.right_section.addWidget(self.key_area)

        self.key_area2 = QTextEdit()
        self.key_area2.setPlaceholderText("Enter Key ( Optionnel ) ...")
        self.key_area2.setStyleSheet("border: 1px solid #ABAFB5; border-radius: 10px;")
        self.key_area2.setFixedHeight(60)
        self.right_section.addWidget(self.key_area2)
        self.key_area2.setVisible(False)
        
        # Text Input Field
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Enter Text To Encrypt ...")
        self.text_area.setStyleSheet("border: 1px solid #ABAFB5; border-radius: 10px;")
        self.right_section.addWidget(self.text_area)
        
        # Text Output Field
        self.result_area = QTextEdit()
        self.result_area.setPlaceholderText("Result Here ...")
        self.result_area.setReadOnly(True)
        self.result_area.setStyleSheet("border: 1px solid #ABAFB5; border-radius: 10px;")
        self.right_section.addWidget(self.result_area)

        # Place The Sections
        self.main.addWidget(self.left_frame, 1)
        self.main.addWidget(self.right_frame, 2)

    def start_encrypt(self):
        method = self.encryption_dropdown.currentText()
        text = self.text_area.toPlainText()
        key = self.key_area.toPlainText()

        if method == "Playfair Cipher":
            playfaire = Playfair(text, key)
            res = playfaire.encrypt()
        elif method == "Vigenère Cipher":
            vigenere = Vigenere(text, key)
            res = vigenere.encrypt()
        elif method == "Polybius":
            polybius = Polybius(text, key)
            res = polybius.encrypt()
        elif method == "Row Column Transposition":
            transposition = Transposition(text, key)
            res = transposition.encrypt()
        elif method == "DES":
            des = DES(text, key)
            res = des.encrypt()
        elif method == "AES":
            aes = AES(text, key)
            res = aes.encrypt()
        elif method == "RSA":
            rsa = RSA(text)
            res = rsa.encrypt()
        elif method == "MD5":
            md5 = MD5(text)
            res = md5.hash()
        elif method == "SHA-256":
            sha = SHA256(text)
            res = sha.hash()
        else : 
            res = "Selected method not implemented."

        self.result_area.setPlainText(res)
        self.text_area.setPlaceholderText("Enter Text To Encrypt")
                    
    def start_decrypt(self):
        method = self.encryption_dropdown.currentText()
        text = self.text_area.toPlainText()
        key = self.key_area.toPlainText()

        if method == "Playfair Cipher":
            playfaire = Playfair(text, key)
            res = playfaire.decrypt(text)
        elif method == "Vigenère Cipher":
            vigenere = Vigenere(text, key)
            res = vigenere.decrypt(text)
        elif method == "Polybius":
            polybius = Polybius(text, key)
            res = polybius.decrypt(text)
        elif method == "Row Column Transposition":
            transposition = Transposition(text, key)
            res = transposition.decrypt(text)
        elif method == "DES":
            des = DES(text, key)
            res = des.decrypt(text)
        elif method == "AES":
            aes = AES(text, key)
            res = aes.decrypt(text)
        elif method == "RSA":
            rsa = RSA(text)
            res = rsa.decrypt(text)
        else : 
            res = "Selected method not implemented."

        self.result_area.setPlainText(res)
        self.text_area.setPlaceholderText("Enter Text To Decrypt")

    def updateKeyPlaceHolder(self):
        method = self.encryption_dropdown.currentText()
        if method in ("Playfair Cipher", "Polybius") :
            self.key_area.setPlaceholderText("Enter Key ( Optionnel ) ...")
        elif method in ("Vigenère Cipher","Row Column Transposition") :
            self.key_area.setPlaceholderText("Enter Key ( Key By Default ) ...")
        elif method in ("SHA-256", "MD5"):
            self.decrypt_button.setVisible(False)
            self.key_area.setVisible(False)
        elif method in ("RSA", "Diffie-Hellman"):
            self.key_area2.setVisible(True)
            self.key_area.setPlaceholderText("Enter The Private Key ...")
            self.key_area2.setPlaceholderText("Enter The Public Key ( Optionnel ) ...")
        elif method == "DES":
            self.key_area.setPlaceholderText("Enter The Private Key ...")
        elif method == "AES":
            self.key_area.setPlaceholderText("Enter The Private Key ( Length 16 24 32 Characters Space Included )...")

# Run the application
app = QApplication(sys.argv)
window = CryptoX()
window.show()
sys.exit(app.exec())