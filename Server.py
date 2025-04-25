import socket
import threading
import json
from datetime import datetime

HOST='0.0.0.0'
PORT=5555

clients={}
lock=threading.Lock()

def log_message(sender, recipient, cipher, encrypted_message):
    with open("server_log.txt","a") as f:
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {sender} -> {recipient} [{cipher}]: {encrypted_message}\n")

def broadcast_user_list():
    user_list_msg=json.dumps({"type": "user_list", "users": list(clients.keys())})
    for client in clients.values():
        try:
            client.send(user_list_msg.encode())
        except:
            pass

def handle_client(client_socket, address):
    username=None
    try:
        username=client_socket.recv(1024).decode().strip()
        with lock:
            if username in clients:
                client_socket.send("[ERROR] Username already taken.".encode())
                client_socket.close()
                return
            clients[username]=client_socket
            broadcast_user_list()

        client_socket.send("[INFO] Connected to server.".encode())
        print(f"[+] {username} connected from {address}")

        while True:
            data=client_socket.recv(8192)
            if not data:
                break
            try:
                message_data=json.loads(data.decode())

                msg_type=message_data.get("type", "message")

                if msg_type=="message":
                    sender=message_data["from"]
                    recipient=message_data["to"]
                    cipher=message_data["cipher"]
                    encrypted=message_data["message"]

                    log_message(sender,recipient,cipher,encrypted)

                    with lock:
                        target=clients.get(recipient)
                    if target:
                        target.send(json.dumps(message_data).encode())
                    else:
                        client_socket.send(f"[ERROR] User '{recipient}' not found.".encode())

                elif msg_type=="pubkey":
                    recipient=message_data["to"]
                    with lock:
                        target=clients.get(recipient)
                    if target:
                        target.send(json.dumps(message_data).encode())

            except Exception as e:
                client_socket.send(f"[ERROR] Failed to process message: {e}".encode())
    except Exception as e:
        print(f"[ERROR] Exception: {e}")
    finally:
        if username:
            with lock:
                clients.pop(username,None)
                broadcast_user_list()
            print(f"[-] {username} disconnected")
            client_socket.close()

def start_server():
    server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Server listening on {HOST}:{PORT}")

    while True:
        client_socket,addr=server.accept()
        threading.Thread(target=handle_client,args=(client_socket,addr),daemon=True).start()

if __name__=="__main__":
    start_server()