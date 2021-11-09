import socket
import sys

HOST = '0.0.0.0'    # you need to write the server IP here
PORT = 5588


def start_client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(0)
    sock.connect((HOST, PORT))
    return sock


if __name__ == '__main__':
    client_sock = start_client()
    while True:
        client_msg = input('write a message: ')
        if client_msg:
            client_sock.send(client_msg.encode('UTF-8'))
            byte_data = client_sock.recv(1024)
            if not byte_data:
                sys.exit()
            print(byte_data.decode('UTF-8'))
        else:
            client_sock.close()


