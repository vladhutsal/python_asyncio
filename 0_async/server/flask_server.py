from flask import Flask
from flask import request
import time

app = Flask(__name__)

HOST = '0.0.0.0'
PORT = 5588

USERS = dict()  # user_addr: request count
FIRST_PART: str
SECOND_PART: str


@app.route("/one")
def one():
    user_addr = request.remote_addr
    if not USERS.get(user_addr, None):
        USERS[user_addr] = 1
    else:
        USERS[user_addr] += 1
        time.sleep(1)
        USERS[user_addr] -= 1

    if USERS[user_addr] == 3:
        return 'Concurency is about handling many things simultaneously'
    return ']@h@)qtu7{(8&zj&h8q;pan!==[,mf'
    


@app.route("/two")
def two():
    user_addr = request.remote_addr
    if not USERS.get(user_addr, None):
        USERS[user_addr] = 1
    else:
        USERS[user_addr] += 1
        time.sleep(1)
        USERS[user_addr] -= 1

    if USERS[user_addr] == 3:
        return 'Concurency is about handling many things simultaneously'
    return ')g4&*fm_-/h2+;7%;])%!b46y::]dg'


@app.route("/three")
def three():
    user_addr = request.remote_addr
    if not USERS.get(user_addr, None):
        USERS[user_addr] = 1
    else:
        USERS[user_addr] += 1
        time.sleep(1)
        USERS[user_addr] -= 1

    if USERS[user_addr] == 3:
        return 'Concurency is about handling many things simultaneously'
    return 'h(x5hrb5.w7n;b2u_f8}ar%(wufq_j'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5588)