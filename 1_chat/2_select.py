from select import select
import socket


HOST = '0.0.0.0'
PORT = 5588

# list of sockets, which fileno() file descriptors we should monitor for events
client_sockets = []

def start_server() -> socket.socket:
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_sock.bind((HOST, PORT))
    serv_sock.listen(5)
    print(f'server started. host = {HOST}, port = {PORT}')
    return serv_sock


def accept_conn(serv_sock: socket.socket):
    client_sock, addr = serv_sock.accept()      # will block until somebody connects
    print(f'{addr} connected\n')
    client_sockets.append(client_sock)


def echo_message(client_sock: socket.socket):
    recieved_data = client_sock.recv(4096)      # will block until all data is recieved
    if recieved_data:
        print('recieved message, echoing')
        echo_msg = get_echo_response(recieved_data)
        client_sock.send(echo_msg)          # will block if write buffer is full
    else:
        print(f'{client_sock.getsockname()}  disconnected\n')
        flush_socket(client_sock)


def run(serv_sock: socket.socket):
    print('chat init')
    while True:
        print('waiting for events')
        ready_to_read_list, _, _ = select(client_sockets, [], [])   # will block while waiting for events
        for sock_ready_to_read in ready_to_read_list:
            if sock_ready_to_read is serv_sock:
                accept_conn(sock_ready_to_read)
            else:
                echo_message(sock_ready_to_read)


def flush_socket(client_sock: socket.socket):
    client_sock.close()
    filtered = filter(lambda sock: sock is client_sock, client_sockets)
    to_remove = next(filtered)
    client_sockets.remove(to_remove)


def get_echo_response(data: bytes) -> bytes:
    str_data = data.decode('UTF-8')
    return f'echo message: {str_data}\n'.encode('UTF-8')


if __name__ == '__main__':
    server_sock = start_server()
    client_sockets.append(server_sock)
    run(server_sock)
