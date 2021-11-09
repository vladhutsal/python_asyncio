from select import select
import socket

to_monitor = []

def start_server():
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_sock.bind(('localhost', 5000))
    serv_sock.listen()
    return serv_sock


def accept_conn(serv_sock):
    client_sock, addr = serv_sock.accept()
    print(f'{addr} connected')
    to_monitor.append(client_sock)


def send_msg(client_sock: socket.socket):
    req = client_sock.recv(4096)
    if req:
        resp = 'your message was recieved\n'.encode()
        client_sock.send(resp)  # will block if write buffer is full
    else:
        client_sock.close()


def run(serv_sock: socket.socket):
    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])
        for sock in ready_to_read:
            if sock is serv_sock:
                accept_conn(sock)
            else:
                send_msg(sock)


if __name__ == '__main__':
    server_sock = start_server()
    to_monitor.append(server_sock)
    run(server_sock)
