import socket
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def read(y):
    private_key_file_name = "sk" + y + ".pem"
    private_key_file = open(private_key_file_name, 'r')
    private_key = load_pem_private_key(private_key_file.read().encode(), password=None)
    ips_file = open("ips.txt", 'r')
    ip_port = ips_file.readlines()[int(y) - 1].split()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip_port[0], int(ip_port[1])))
    server.listen(5)
    # while True:
    client_socket, _ = server.accept()
    data = client_socket.recv(8192)
    decrypted_data = private_key.decrypt(data, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    ))
    client_socket.close()
    print(decrypted_data)
    ip = socket.inet_ntoa(decrypted_data[0:4])
    port = int.from_bytes(decrypted_data[4:6], "big")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("ip, port = ", ip, port)
    s.connect((ip, port))
    s.send(decrypted_data[6:])
    s.close()


def main():
    Y = input()
    read(Y)


if __name__ == '__main__':
    main()
