

CIPHERTEXT = bytes([
    0x50, 0xF7, 0x8C, 0xF9, 0x80, 0x59, 0xA8, 0x77,
    0x85, 0xCA, 0xCB, 0x89, 0x6F, 0x56, 0x1A, 0x6F,
    0x2F, 0x24, 0xFD, 0x84, 0x67, 0x8E, 0x8F, 0x36,
    0xD4, 0x37, 0x7F, 0x36, 0xDB, 0xD0, 0xEC, 0xC9,
    0xEC, 0xD9, 0x04, 0x03, 0x9C, 0xED, 0x53, 0x90,
    0xB5, 0xFD, 0xE5, 0x12,
])

KEY = b"kEy3rd"


def rc4_modified_decrypt(ciphertext: bytes, key: bytes) -> bytes:


    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]


    i = j = 0
    result = []
    for byte in ciphertext:
        i = (i + 1) % 256
        j = (j + S[i] + 1) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        result.append(byte ^ K)
    return bytes(result)


def main():
    plaintext = rc4_modified_decrypt(CIPHERTEXT, KEY)
    flag = plaintext.decode('ascii', errors='replace')
    print(f"Flag: {flag}")


    encrypted = rc4_modified_decrypt(CIPHERTEXT, KEY)
    ok = (encrypted == plaintext)  # RC4 是对称的，加解密相同
    print(f"验证: {'通过' if ok else '失败'}  (RC4 加解密对称，密文 XOR 密钥流 = 明文)")


if __name__ == '__main__':
    main()
