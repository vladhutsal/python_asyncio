import socket
from socket import socket as Sock
import loop

from logger import logger


clients = set()

def handler_start_server():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('localhost', 5588))
    server_sock.setblocking(0)
    server_sock.listen(100)
    return server_sock


def handler_accept_connection(server_sock: Sock):
    while True:
        yield 'read', server_sock
        c_soc, addr = server_sock.accept()  # (read) blocks while waiting for new connection
        logger.info(f'{addr} connected')
        clients.add(c_soc)
        task = handler_recieve_message(c_soc)
        loop.add_task(task)


def handler_recieve_message(client_sock: Sock):
    while True:
        yield 'read', client_sock
        msg = client_sock.recv(4096)   # (read) blocks while waiting for new client message
        addr = client_sock.getpeername()
        logger.info(f'Recieving message from {addr}')
        logger.info(msg.decode('UTF-8'))

        if not msg:
            clients.discard(client_sock)
            client_sock.close()
            break
        
        for client in clients:
            if client != client_sock:
                task = handler_send_message(client, msg)
                loop.add_task(task)


def handler_send_message(client_sock: Sock, msg: bytes):
    yield 'write', client_sock
    addr = client_sock.getpeername()
    logger.info(f'sending message to {addr}')
    client_sock.send(msg)


if __name__ == '__main__':
    server_sock = handler_start_server()
    connection_task = handler_accept_connection(server_sock)

    loop.add_task(connection_task)
    loop.start_event_loop()
