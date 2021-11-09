import socket

s_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s_sock.bind(('localhost', 5000))
s_sock.listen(5)

while True:
    print('waiting for client')
    c_sock, addr = s_sock.accept()
    print(f'{addr} connected')

    while True:
        print('waiting for the message')
        req = c_sock.recv(4096)
        print('recieved')

        if not req:
            break
        else:
            print(req.encode())
