import socket
import loop

from logger import logger

HOST = '0.0.0.0'
PORT = 5588

clients = set()

def start_server() -> socket.socket:
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((HOST, PORT))
    server_sock.setblocking(0)
    server_sock.listen(100)

    logger.info(f'server started. host = {HOST}, port = {PORT}')
    return server_sock


def handler_accept_connection(server_sock: socket.socket):
    while True:
        yield 'read', server_sock
        c_soc, addr = server_sock.accept()  # (read)
        c_soc.setblocking(0)
        logger.info(f'{addr} connected')
        clients.add(c_soc)
        task = handler_recieve_message(c_soc)
        loop.add_task(task)


def handler_recieve_message(client_sock: socket.socket):
    while True:
        yield 'read', client_sock
        msg = client_sock.recv(4096)   # (read)
        addr = client_sock.getpeername()
        logger.info(f'Recieving message from {addr}')

        if not msg:
            clients.discard(client_sock)
            client_addr = client_sock.getsockname()
            logger.info(f'{client_addr}  disconnected\n')
            client_sock.close()
            break
        
        for client in clients:
            if client != client_sock:
                task = handler_send_message(client, msg)
                loop.add_task(task)


def handler_send_message(client_sock: socket.socket, msg: bytes):
    yield 'write', client_sock
    addr = client_sock.getpeername()
    logger.info(f'sending message to {addr}')
    client_sock.send(msg)   # (write)


if __name__ == '__main__':
    server_sock = start_server()
    connection_task = handler_accept_connection(server_sock)

    loop.add_task(connection_task)
    loop.start_event_loop()
