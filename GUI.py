import sys
from PyQt6.QtWidgets import (
    QApplication,QWidget,QHBoxLayout,QFrame,QVBoxLayout,
    QLabel,QPushButton,QTextEdit,QComboBox
)

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
        self.setGeometry(300,300,800,600)

        self.methods={
            "Playfair Cipher": Playfair,
            "Vigenere Cipher": Vigenere,
            "Polybius": Polybius,
            "Row Column Transposition": Transposition,
            "DES": DES,
            "AES": AES,
            "RSA": RSA,
            "Diffie-Hellman": DH,
            "MD5": MD5,
            "SHA-256": SHA256
        }

        self.setup_ui()

    def setup_ui(self):
        self.main=QHBoxLayout(self)

        self.left_frame=QFrame()
        self.left_frame.setStyleSheet("background-color: #2E3B4E; padding: 10px;")
        self.left_section=QVBoxLayout(self.left_frame)

        self.right_frame=QFrame()
        self.right_frame.setStyleSheet("background-color: #1A1F2B; padding: 10px;")
        self.right_section=QVBoxLayout(self.right_frame)

        self.encryption_dropdown=QComboBox()
        self.encryption_dropdown.addItems(self.methods.keys())
        self.encryption_dropdown.currentIndexChanged.connect(self.updateKeyPlaceHolder)

        self.encrypt_button=self.make_button("Encrypt",self.start_encrypt)
        self.decrypt_button=self.make_button("Decrypt",self.start_decrypt)
        self.show_matrix_button = self.make_button("Show Matrix", self.show_matrix)

        self.left_section.addWidget(QLabel("Select Encryption Method:"))
        self.left_section.addWidget(self.encryption_dropdown)
        self.left_section.addWidget(self.encrypt_button)
        self.left_section.addWidget(self.decrypt_button)
        self.right_section.addWidget(QLabel("Matrix Display:"))
        self.left_section.addWidget(self.show_matrix_button)

        self.key_area=self.make_text_area("Enter Key (Optional)...",height=60)
        self.key_area2=self.make_text_area("Enter Key 2 (Optional)...",height=60)
        self.key_area2.setVisible(False)

        self.text_area=self.make_text_area("Enter Text To Encrypt ...")
        self.result_area=self.make_text_area("Result Here ...",read_only=True)
        self.matrix_area=self.make_text_area("Matrix Output ...", read_only=True)

        self.right_section.addWidget(self.key_area)
        self.right_section.addWidget(self.key_area2)
        self.right_section.addWidget(self.text_area)
        self.right_section.addWidget(self.result_area)
        self.right_section.addWidget(self.matrix_area)

        self.main.addWidget(self.left_frame,1)
        self.main.addWidget(self.right_frame,2)

    def make_text_area(self,placeholder,height=None,read_only=False):
        area=QTextEdit()
        area.setPlaceholderText(placeholder)
        area.setReadOnly(read_only)
        area.setStyleSheet("""
            QTextEdit {
                background-color: #2C2F3A;
                color: white;
                border: 1px solid #5BC0BE;
                border-radius: 10px;
            }
            QTextEdit[readOnly="true"] {
                background-color: #1F232F;
            }
        """)
        if height:
            area.setFixedHeight(height)
        return area

    def make_button(self,text,handler):
        button=QPushButton(text)
        button.clicked.connect(handler)
        button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #5BC0BE;
                padding: 10px;
                border-radius: 5px;
                border: none;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3A9D9A;
            }
        """)
        return button

    def start_encrypt(self):
        method_name=self.encryption_dropdown.currentText()
        text=self.text_area.toPlainText()
        key=self.key_area.toPlainText()

        cls=self.methods.get(method_name)
        res=""

        if method_name in ["MD5","SHA-256"]:
            res=cls(text).hash()
        elif method_name=="RSA":
            p=int(self.key_area.toPlainText())
            q=int(self.key_area2.toPlainText())
            self.rsa_instance=cls(text,p,q)
            res=self.rsa_instance.encrypt()
        else:
            res=cls(text,key).encrypt()
        
        if isinstance(res, list):
            res = ", ".join(map(str, res))

        self.result_area.setPlainText(res)

    def start_decrypt(self):
        method_name=self.encryption_dropdown.currentText()
        text=self.text_area.toPlainText()
        key=self.key_area.toPlainText()

        cls=self.methods.get(method_name)
        res=""

        if method_name=="RSA":
            text_list=list(map(int,text.strip().split(",")))
            res=self.rsa_instance.decrypt(text_list)
        else:
            res=cls(text,key).decrypt(text)

        self.result_area.setPlainText(res)

    def show_matrix(self):
        method_name=self.encryption_dropdown.currentText()
        text=self.text_area.toPlainText()
        key=self.key_area.toPlainText()

        cls=self.methods.get(method_name)
        matrix=cls(text,key).grid
        formatted="\n".join([" ".join(row) for row in matrix])
        self.matrix_area.setPlainText(formatted)

    def updateKeyPlaceHolder(self):
        method_name=self.encryption_dropdown.currentText()

        self.key_area.setVisible(True)
        self.key_area2.setVisible(False)
        self.matrix_area.setVisible(False)
        self.decrypt_button.setVisible(True)
        self.show_matrix_button.setVisible(False)

        if method_name in ("SHA-256","MD5"):
            self.key_area.setVisible(False)
            self.decrypt_button.setVisible(False)
        elif method_name=="RSA":
            self.key_area2.setVisible(True)
            self.key_area.setPlaceholderText("Enter P ...")
            self.key_area2.setPlaceholderText("Enter Q ...")
        elif method_name=="Diffie-Hellman":
            self.key_area2.setVisible(True)
            self.key_area.setPlaceholderText("Enter Base ...")
            self.key_area2.setPlaceholderText("Enter Modulus ...")
        elif method_name=="AES":
            self.key_area.setPlaceholderText("Private Key (16/24/32 chars)...")
        elif method_name=="DES":
            self.key_area.setPlaceholderText("Enter Private Key ...")
        elif method_name in ("Playfair Cipher","Polybius"):
            self.show_matrix_button.setVisible(True)
            self.matrix_area.setVisible(True)
            self.key_area.setPlaceholderText("Enter Key (Optional)...")
        else:
            self.key_area.setPlaceholderText("Enter Key (Default Is Key)...")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CryptoX()
    window.show()
    sys.exit(app.exec())