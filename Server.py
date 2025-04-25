import socket
import threading

HOST='0.0.0.0'
PORT=5555

clients = []

def broadcast(message,sender_socket):
    for client in clients:
        if client!=sender_socket:
            try:
                client.sendall(message)
            except:
                clients.remove(client)
                client.close()

def handle_client(client_socket,address):
    print(f"[+] New connection from {address}")
    while True:
        try:
            message=client_socket.recv(4096)
            if not message:
                break
            broadcast(message,client_socket)
        except:
            break

    print(f"[-] Connection closed: {address}")
    clients.remove(client_socket)
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST,PORT))
    server.listen()
    print(f"[*] Server listening on {HOST}:{PORT}")

    while True:
        client_socket,addr=server.accept()
        clients.append(client_socket)
        thread=threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__=="__main__":
    start_server()