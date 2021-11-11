# TODO:
# Now chat exits after the server recieved the client message
# We need to echo 

import socket

HOST = '0.0.0.0'
PORT = 5588

# list of client sockets, connected to server
client_socket: socket.socket
serv_sock: socket.socket

def start_server():
    global serv_sock

    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv_sock.bind((HOST, PORT))
    serv_sock.listen(5)

    print(f'server started. host = {HOST}, port = {PORT}')


def accept_conn():
    global client_socket
    global serv_sock

    print('waiting for connection')
    connected_sock, addr = serv_sock.accept()
    client_socket = connected_sock
    print(f'{addr} connected')


def echo_message():
    global client_socket
    global serv_sock

    recieved_data = client_socket.recv(4096)
    if not recieved_data:
        print('client disconected')
        client_socket.close()
        accept_conn()
        return

    str_data = recieved_data.decode('UTF-8')
    print(f'message from client: {str_data}')
    str_data = recieved_data.decode('UTF-8')
    resp = f'echo message: {str_data}\n'.encode('UTF-8')
    client_socket.send(resp)


if __name__ == '__main__':
    start_server()
    accept_conn()
    # asnwer
    while True:
        echo_message()
