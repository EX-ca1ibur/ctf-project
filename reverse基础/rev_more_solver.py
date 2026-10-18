import struct
import socket
import sys

DELTA = 0x4A537F29
ROUNDS = 111
HOST = '127.0.0.1'
PORT = 64068


def bswap32(x: int) -> int:

    return int.from_bytes(struct.pack('<I', x), 'big')


def tea_decrypt_block(x0: int, x1: int, key: list[int]) -> tuple[int, int]:

    sum_val = (DELTA * ROUNDS) & 0xFFFFFFFF
    for _ in range(ROUNDS):

        f2 = (((x0 << 4) ^ (x0 >> 5)) + x0) & 0xFFFFFFFF
        k_idx2 = (sum_val >> 11) & 3
        x1 = (x1 - (f2 ^ (key[k_idx2] + sum_val))) & 0xFFFFFFFF
        sum_val = (sum_val - DELTA) & 0xFFFFFFFF

        f1 = (((x1 << 4) ^ (x1 >> 5)) + x1) & 0xFFFFFFFF
        x0 = (x0 - (f1 ^ (key[sum_val & 3] + sum_val))) & 0xFFFFFFFF
    return x0, x1


def decrypt(ciphertext: bytes, key_words: list[int]) -> bytes:

    result = b''
    for i in range(0, len(ciphertext), 8):

        x0 = struct.unpack('<I', ciphertext[i:i + 4])[0]
        x1 = struct.unpack('<I', ciphertext[i + 4:i + 8])[0]

        x0_bs = bswap32(x0)
        x1_bs = bswap32(x1)

        d0_bs, d1_bs = tea_decrypt_block(x0_bs, x1_bs, key_words)

        d0 = bswap32(d0_bs)
        d1 = bswap32(d1_bs)

        result += struct.pack('<I', d0) + struct.pack('<I', d1)
    return result


def solve(host: str = HOST, port: int = PORT) -> str:

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    try:
        sock.connect((host, port))
        data = sock.recv(4096)
        sock.close()
    except Exception as e:
        raise ConnectionError(f"无法连接到 {host}:{port}: {e}")

    lines = data.decode('ascii').strip().split('\n')
    if len(lines) < 2:
        raise ValueError(f"服务器返回数据格式错误: {data}")

    key_hex = lines[0].strip()
    ciphertext_hex = lines[1].strip()


    key_raw = bytes.fromhex(key_hex)
    key_words = [bswap32(k) for k in struct.unpack('<IIII', key_raw)]

    ciphertext = bytes.fromhex(ciphertext_hex)
    plaintext = decrypt(ciphertext, key_words)
    plaintext = plaintext.rstrip(b'\x00')

    return plaintext.decode('ascii')


def main():
    if len(sys.argv) >= 3:

        key_hex = sys.argv[1]
        ciphertext_hex = sys.argv[2]

        key_raw = bytes.fromhex(key_hex)
        ciphertext = bytes.fromhex(ciphertext_hex)

        key_words = [bswap32(k) for k in struct.unpack('<IIII', key_raw)]
        plaintext = decrypt(ciphertext, key_words)
        plaintext = plaintext.rstrip(b'\x00')

        print(f"Flag: {plaintext.decode('ascii', errors='replace')}")
    else:

        try:
            flag = solve()
            print(f"Flag: {flag}")
        except Exception as e:
            print(f"错误: {e}")
            print("\n用法: python rev_more_solver.py <key_hex> <ciphertext_hex>")
            sys.exit(1)


if __name__ == '__main__':
    main()
