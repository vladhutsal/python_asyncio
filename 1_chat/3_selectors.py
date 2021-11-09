import selectors
import socket
from socket import socket as sock

selector = selectors.DefaultSelector()

HOST = '0.0.0.0'
PORT = 5588

def start_server():
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_sock.bind((HOST, PORT))
    serv_sock.listen()
    print(f'server started. host = {HOST}, port = {PORT}')
    selector.register(fileobj=serv_sock, events=selectors.EVENT_READ, data=accept_conn)


def accept_conn(serv_sock: sock):
    client_sock, addr = serv_sock.accept()
    print(f'{addr} connected')

    selector.register(fileobj=client_sock, events=selectors.EVENT_READ, data=echo_message)


def echo_message(client_sock: sock):
    print('recieved message, echoing')
    recieved_data = client_sock.recv(4096)
    if recieved_data:
        response = get_echo_response(recieved_data)
        client_sock.send(response)
    else:
        print(f'{client_sock.getsockname()} left chat')
        selector.unregister(client_sock)
        client_sock.close()


def run():
    print('selectors chat init')
    while True:
        print('waiting for events')
        events = selector.select()      # will block while waiting for events

        for key, _ in events:      # returns SelectorKey - namedtuple(fileobj, fd, events, data)
            callback = key.data
            sock = key.fileobj
            callback(sock)


def get_echo_response(data: bytes) -> bytes:
    str_data = data.decode('UTF-8')
    return f'echo message: {str_data}\n'.encode('UTF-8')


if __name__ == '__main__':
    start_server()
    run()
