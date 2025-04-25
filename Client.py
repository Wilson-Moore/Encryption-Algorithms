import sys
import socket
import threading

from PyQt6.QtWidgets import (
    QApplication,QWidget,QVBoxLayout,QTextEdit,
    QLineEdit,QPushButton,QComboBox,QLabel,QHBoxLayout,QCheckBox
)

from Classic.Substition.Playfair import Playfair
from Classic.Substition.Vigenere import Vigenere
from Classic.Permutation.Polybius import Polybius
from Classic.Permutation.Transposition import Transposition
from Modern.SecretKey.DES import DES
from Modern.SecretKey.AES import AES
from Modern.PublicKey.RSA import RSA
from Modern.Hashing.MD5 import MD5
from Modern.Hashing.SHA256 import SHA256

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crypto Chat Client")
        self.setGeometry(100,100,800,500)

        self.methods={
            "Playfair Cipher": Playfair,
            "Vigenère Cipher": Vigenere,
            "Polybius": Polybius,
            "Row Column Transposition": Transposition,
            "DES": DES,
            "AES": AES,
            "RSA": RSA,
            "MD5": MD5,
            "SHA-256": SHA256
        }

        self.build_ui()
        self.setup_network()

    def build_ui(self):
        layout=QVBoxLayout()

        self.chat_box=QTextEdit()
        self.chat_box.setReadOnly(True)
        layout.addWidget(self.chat_box)

        self.encryption_dropdown=QComboBox()
        self.encryption_dropdown.addItems(self.methods.keys())
        layout.addWidget(QLabel("Encryption Method:"))
        layout.addWidget(self.encryption_dropdown)

        self.key_input=QLineEdit()
        self.key_input.setPlaceholderText("Enter Key (or Private Key for RSA: d n)")
        layout.addWidget(QLabel("Key:"))
        layout.addWidget(self.key_input)

        self.auto_decrypt_checkbox=QCheckBox("Auto Decrypt Incoming")
        self.auto_decrypt_checkbox.setChecked(True)
        layout.addWidget(self.auto_decrypt_checkbox)

        input_layout=QHBoxLayout()
        self.message_input=QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")
        input_layout.addWidget(self.message_input)

        self.send_button=QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)
        self.setLayout(layout)

    def setup_network(self):
        self.client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            self.client.connect(('localhost',5555))
            threading.Thread(target=self.receive_messages,daemon=True).start()
            self.chat_box.append("[INFO] Connected to server.")
        except Exception as e:
            self.chat_box.append(f"[ERROR] Could not connect: {e}")

    def encrypt_message(self, text):
        method=self.encryption_dropdown.currentText()
        key=self.key_input.text()
        cls=self.methods[method]

        if method in ("MD5","SHA-256"):
            return cls(text).hash()
        elif method=="RSA":
            try:
                p,q=61,53
                rsa=RSA(text,p,q)
                encrypted=rsa.encrypt()
                return ",".join(map(str,encrypted))
            except Exception as e:
                return f"[ENCRYPTION ERROR] {e}"
        else:
            try:
                return cls(text,key).encrypt()
            except Exception as e:
                return f"[ENCRYPTION ERROR] {e}"

    def send_message(self):
        msg=self.message_input.text()
        if not msg:
            return
        encrypted_msg=self.encrypt_message(msg)
        try:
            self.client.send(encrypted_msg.encode())
        except Exception as e:
            self.chat_box.append(f"[ERROR] Sending failed: {e}")

    def receive_messages(self):
        while True:
            try:
                msg=self.client.recv(4096).decode()
                if not msg:
                    continue

                decrypted_msg=None
                if self.auto_decrypt_checkbox.isChecked():
                    try:
                        method=self.encryption_dropdown.currentText()
                        key=self.key_input.text()
                        cls=self.methods[method]

                        if method in ("MD5", "SHA-256"):
                            decrypted_msg="[No Decryption for Hashing]"
                        elif method=="RSA":
                            d,n=map(int,key.split())
                            rsa=RSA("",1,1)
                            rsa.private_key=(d,n)
                            int_list=list(map(int,msg.strip().split(",")))
                            decrypted_msg=rsa.decrypt(int_list)
                        else:
                            decrypted_msg=cls("",key).decrypt(msg)
                    except Exception as e:
                        decrypted_msg = f"[Decryption failed: {e}]"

                if decrypted_msg:
                    self.chat_box.append(f"[Encrypted] {msg}\n[Decrypted] {decrypted_msg}")
                else:
                    self.chat_box.append(f"[Encrypted] {msg}")
            except Exception as e:
                self.chat_box.append(f"[ERROR] Receiving failed: {e}")
                break

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=ChatClient()
    window.show()
    sys.exit(app.exec())
