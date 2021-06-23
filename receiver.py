import socket
from sender import create_symmetric_key
from datetime import datetime


def main():
    password = input()
    salt = input()
    port = input()
    symmetric_key = create_symmetric_key(password, salt)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", int(port)))
    server.listen(5)
    client_socket, _ = server.accept()
    data = client_socket.recv(8192)
    decrypted_data = symmetric_key.decrypt(data).decode()
    print(decrypted_data, end=" ")
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)

if __name__ == '__main__':
    main()
