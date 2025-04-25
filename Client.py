import sys
import socket
import threading
import json

from PyQt6.QtWidgets import (
    QApplication,QWidget,QVBoxLayout,QTextEdit,
    QLineEdit,QPushButton,QComboBox,QLabel,QHBoxLayout,
    QCheckBox,QListWidget,QListWidgetItem,QInputDialog
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
from Utiliy import generate_prime

class ChatClient(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Crypto Chat Client")
        self.setGeometry(100,100,600,600)

        self.username=self.ask_username()
        self.rsa_public_keys={}
        self.p=generate_prime(1000,2000)
        self.q=generate_prime(1000,2000)

        self.methods={
            "Playfair Cipher": Playfair,
            "Vigenere Cipher": Vigenere,
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

    def ask_username(self):
        username,ok=QInputDialog.getText(self,"Username","Enter your username:")
        if ok and username:
            return username.strip()
        else:
            sys.exit()

    def build_ui(self):
        layout=QVBoxLayout()

        self.chat_box=QTextEdit()
        self.chat_box.setReadOnly(True)
        layout.addWidget(self.chat_box)

        method_layout=QHBoxLayout()
        self.encryption_dropdown=QComboBox()
        self.encryption_dropdown.addItems(self.methods.keys())
        method_layout.addWidget(QLabel("Encryption:"))
        method_layout.addWidget(self.encryption_dropdown)

        self.key_input=QLineEdit()
        self.key_input.setPlaceholderText("Key or RSA private: d n")
        method_layout.addWidget(QLabel("Key:"))
        method_layout.addWidget(self.key_input)

        self.auto_decrypt_checkbox=QCheckBox("Auto Decrypt")
        self.auto_decrypt_checkbox.setChecked(True)
        method_layout.addWidget(self.auto_decrypt_checkbox)

        layout.addLayout(method_layout)

        hlayout=QHBoxLayout()
        self.to_input=QLineEdit()
        self.to_input.setPlaceholderText("Recipient username")
        hlayout.addWidget(QLabel("To:"))
        hlayout.addWidget(self.to_input)

        self.share_key_button=QPushButton("Share Public Key")
        self.share_key_button.clicked.connect(self.share_public_key)
        hlayout.addWidget(self.share_key_button)

        layout.addLayout(hlayout)

        input_layout=QHBoxLayout()
        self.message_input=QLineEdit()
        self.message_input.setPlaceholderText("Type a message...")
        input_layout.addWidget(self.message_input)

        self.send_button=QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

        self.user_list=QListWidget()
        self.user_list.itemClicked.connect(self.user_selected)
        layout.addWidget(QLabel("Online Users:"))
        layout.addWidget(self.user_list)

        self.setLayout(layout)

    def setup_network(self):
        self.client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(('localhost', 5555))
            self.client.send(self.username.encode())
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            self.chat_box.append(f"[ERROR] Could not connect: {e}")

    def user_selected(self,item):
        self.to_input.setText(item.text())

    def share_public_key(self):
        try:
            rsa=RSA("init",self.p,self.q)
            e,n=rsa.public_key
            d,_=rsa.private_key
            msg={
                "type": "pubkey",
                "from": self.username,
                "to": self.to_input.text().strip(),
                "key": f"{e} {n}"
            }
            self.client.send(json.dumps(msg).encode())
            self.chat_box.append(f"[KEY SHARED] Sent your public key to {msg['to']}")
            self.chat_box.append(f"[YOUR PRIVATE KEY] d: {d}  n: {n} — save this to decrypt!")
            self.key_input.setText(f"{d} {n}")
        except Exception as e:
            self.chat_box.append(f"[ERROR] Failed to share key: {e}")

    def encrypt_message(self,text,recipient):
        method=self.encryption_dropdown.currentText()
        key=self.key_input.text()
        cls=self.methods[method]

        if method in ("MD5","SHA-256"):
            return cls(text).hash()

        elif method=="RSA":
            try:
                e,n=self.rsa_public_keys.get(recipient,(None,None))
                if not e:
                    return "[ERROR] No public key for recipient"
                rsa=RSA(text,self.p,self.q)
                rsa.public_key=(e,n)
                encrypted=rsa.encrypt()
                return ",".join(map(str,encrypted))
            except Exception as e:
                return f"[ENCRYPTION ERROR] {e}"

        else:
            return cls(text,key).encrypt()

    def send_message(self):
        text=self.message_input.text()
        to_user=self.to_input.text().strip()
        if not text or not to_user:
            return
        method=self.encryption_dropdown.currentText()
        encrypted=self.encrypt_message(text, to_user)
        message={
            "type": "message",
            "from": self.username,
            "to": to_user,
            "cipher": method,
            "message": encrypted
        }
        try:
            self.client.send(json.dumps(message).encode())
            self.message_input.clear()
        except Exception as e:
            self.chat_box.append(f"[ERROR] Sending failed: {e}")

    def receive_messages(self):
        while True:
            try:
                data=self.client.recv(8192).decode()
                if not data:
                    continue
                try:
                    msg=json.loads(data)

                    if msg["type"]=="user_list":
                        self.user_list.clear()
                        for user in msg["users"]:
                            if user!=self.username:
                                self.user_list.addItem(QListWidgetItem(user))

                    elif msg["type"]=="pubkey":
                        sender=msg["from"]
                        e,n=map(int,msg["key"].split())
                        self.rsa_public_keys[sender]=(e,n)
                        self.chat_box.append(f"[KEY RECEIVED] {sender}'s public key stored.")

                    elif msg["type"]=="message":
                        encrypted=msg["message"]
                        sender=msg["from"]
                        cipher=msg["cipher"]
                        decrypted="[Unknown]"
                        if self.auto_decrypt_checkbox.isChecked():
                            try:
                                cls=self.methods[cipher]
                                if cipher=="RSA":
                                    d,n=map(int,self.key_input.text().strip().split())
                                    rsa=RSA("",self.p,self.q)
                                    rsa.private_key=(d,n)
                                    int_list=list(map(int,encrypted.split(",")))
                                    decrypted=rsa.decrypt(int_list)
                                elif cipher in ("MD5","SHA-256"):
                                    decrypted="[Hash: No Decryption]"
                                else:
                                    decrypted=cls("",self.key_input.text()).decrypt(encrypted)
                            except Exception as e:
                                decrypted=f"[DECRYPT ERROR] {e}"
                        self.chat_box.append(f"[{sender} -> You]\nEncrypted: {encrypted}\nDecrypted: {decrypted}")

                except json.JSONDecodeError:
                    self.chat_box.append(data)

            except Exception as e:
                self.chat_box.append(f"[ERROR] Receive failed: {e}")
                break

if __name__=="__main__":
    app=QApplication(sys.argv)
    window=ChatClient()
    window.show()
    sys.exit(app.exec())
