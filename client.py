import socket
from threading import Thread

connection_alive = True

def receive_messages():
    global connection_alive
    while connection_alive:
        try:
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print(data)
            else:
                connection_alive = False
        except (ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError) as error:
            connection_alive = False
            print(error)

try:
    IP = input('Введите IP адрес для подключения (по умолчанию - 127.0.0.1): ') or '127.0.0.1'
    port = int(input('Введите порт для подключения (по умолчанию - 8080): ') or 8080)
    name = input('Введите ваше имя: ').strip()
    if not name:
        print("Имя не может быть пустым!")
        exit()
except ValueError:
    print("Неверно указан порт! Попробуйте еще раз!")
    exit()

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, port))
    client_socket.send(name.encode('utf-8'))
    print(f'Соединение с {IP}:{port} успешно установлено')
except (socket.gaierror, ConnectionRefusedError) as error:
    print(f"Не удается подключиться к {IP}:{port} ({error})!")
    exit()

Thread(target=receive_messages, daemon=True).start()

while connection_alive:
    message = input()
    if message in ['exit', '/stop']:
        client_socket.close()
        break
    client_socket.sendall(message.encode('utf-8'))
