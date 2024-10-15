import socket
import threading

HOST = '127.0.0.1'  
PORT = 8080

clients = []

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def client_handler(client_socket):
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            print(f"Received: {message.decode()}")  # Print received message
            broadcast(message, client_socket)
        except:
            break
    client_socket.close()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f'Server listening on {HOST}:{PORT}')

    while True:
        client_socket, addr = server.accept()
        print(f'Accepted connection from {addr[0]}:{addr[1]}')
        clients.append(client_socket)
        client_thread = threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()

if __name__ == '__main__':
    main()