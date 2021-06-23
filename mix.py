import socket


def read(y):
    file_name = "sk" + y + ".pem"
    file = open(file_name, 'r')
    ips_file = open("ips.txt", 'r')
    ip_port = ips_file.readlines()[int(y)-1].split()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(ip_port)
    server.bind((ip_port[0], int(ip_port[1])))
    server.listen(5)
    while True:
        client_socket, client_address = server.accept()
        data = client_socket.recv(100)
        print(data)
        client_socket.close()
        print('Client disconnected')


def main():
    Y = input()
    read(Y)


if __name__ == '__main__':
    main()
