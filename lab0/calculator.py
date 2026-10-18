import socket

HOST = "10.214.160.13"
PORT = 11002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

def recv_one_line(socket):
    buf = b""
    while True:
        data = socket.recv(1)
        if data == b'\n':
            return buf
        buf += data

def recv_one_question(socket):
    buf = b""
    while True:
        data = socket.recv(1)
        if data == b'=':
            return buf
        buf += data

for _ in range(7):
    recv_one_line(s)

for _ in range(10):
    question = recv_one_question(s)
    q_str = question.decode('utf-8')
    answer = eval(q_str)
    s.send(f"{answer}\n".encode('utf-8'))
    recv_one_line(s)
    recv_one_line(s)

recv_one_line(s)
flag = recv_one_line(s)

print("\n Flag:", flag.decode('utf-8'))
s.close()