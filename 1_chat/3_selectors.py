import selectors
import socket
from socket import socket as sock

selector = selectors.DefaultSelector()


def start_server():
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_sock.bind(('localhost', 5000))
    serv_sock.listen()

    selector.register(fileobj=serv_sock, events=selectors.EVENT_READ, data=accept_conn)


def accept_conn(serv_sock: sock):
    client_sock, addr = serv_sock.accept()
    print(f'{addr} connected')

    selector.register(fileobj=client_sock, events=selectors.EVENT_READ, data=send_msg)


def send_msg(client_sock: sock):
    req = client_sock.recv(4096)
    if req:
        resp = 'hello world\n'.encode()
        client_sock.send(resp)
    else:
        selector.unregister(client_sock)
        client_sock.close()


def run():
    while True:
        events = selector.select()

        for key, _ in events:
            callback = key.data
            sock = key.fileobj
            callback(sock)


if __name__ == '__main__':
    start_server()
    run()
