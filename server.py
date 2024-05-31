import socket
from threading import Thread

clients = []
client_names = {}

def handle_client(client_socket, client_address):
    global clients, client_names
    def log_message(message):
        with open('chat_story.log', 'a', encoding='utf-8') as f:
            f.write(message + '\n')

    try:
        name = client_socket.recv(1024).decode('utf-8')
        client_names[client_socket] = name
        with open('clients.log', 'a', encoding='utf-8') as f:
            f.write(f"{client_address}: {name}\n")
        welcome_message = f"{name} присоединился к чату."
        log_message(welcome_message)
        print(welcome_message)
        broadcast_message(welcome_message, client_socket)
    except Exception as e:
        print(f"Ошибка при получении имени пользователя: {e}")
        client_socket.close()
        clients.remove(client_socket)
        return

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            full_message = f"{name}: {message}"
            log_message(full_message)
            print(full_message)
            broadcast_message(full_message, client_socket)
        except ConnectionResetError:
            break
    client_socket.close()
    clients.remove(client_socket)
    disconnect_message = f"{name} покинул чат."
    log_message(disconnect_message)
    print(disconnect_message)
    broadcast_message(disconnect_message, client_socket)
    del client_names[client_socket]

def broadcast_message(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)
                if client in client_names:
                    del client_names[client]

def start_server(ip='127.0.0.1', port=8080):
    global clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((ip, port))
    server_socket.listen(5)
    print(f"Сервер запущен и слушает на {ip}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)
        print(f"Подключен клиент: {addr}")
        Thread(target=handle_client, args=(client_socket, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()
