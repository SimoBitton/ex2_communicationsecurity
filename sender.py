import base64
import socket
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.serialization import load_pem_public_key


def create_symmetric_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=str.encode(salt),
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(str.encode(password)))
    f = Fernet(key)
    return f


def main():
    X = input()
    file_name = "messages" + X + ".txt"
    file = open(file_name, 'r')
    for line in file.readlines():
        message, path, round1, password, salt, destination_ip, destination_port = line.split()
        symmetric_key = create_symmetric_key(password, salt)
        data = symmetric_key.encrypt(str.encode(message))
        msg = socket.inet_aton(destination_ip) + int(destination_port).to_bytes(2, 'big') + data
        print(msg)
        number_of_servers = path.split(',')
        ips_file = open("ips.txt", 'r')
        ips_ports = ips_file.readlines()
        public_key_file_name = "pk" + str(number_of_servers[::-1][0]) + ".pem"
        public_key_file = open(public_key_file_name, 'r')
        public_key = load_pem_public_key(public_key_file.read().encode())
        msg = public_key.encrypt(msg, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))
        print(msg)
        for i in number_of_servers[::-1][1:]:
            public_key_file_name = "pk" + str(i) + ".pem"
            public_key_file = open(public_key_file_name, 'r')
            public_key = load_pem_public_key(public_key_file.read().encode())
            ip_port = ips_ports[int(i) - 2].split()
            ip = socket.inet_aton(ip_port[0])
            port = int(ip_port[1]).to_bytes(2, 'big')
            msg = public_key.encrypt(ip + port + msg, padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            ))
            print(msg)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        first_ip_port = ips_ports[int(number_of_servers[0])-1].split()
        print(first_ip_port)
        s.connect((first_ip_port[0], int(first_ip_port[1])))
        s.send(msg)
        s.close()


if __name__ == '__main__':
    main()
