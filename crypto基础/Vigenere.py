TEXT_LIST = (
    ' !"#$%&\'()*+,-./0123456789:;<=>?@'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`'
    'abcdefghijklmnopqrstuvwxyz{|}~\t\n'
)
ALPHABET_SIZE = 97
KEY = [17, 41, 33, 89, 94, 60, 80, 13, 72, 79, 18, 65, 50, 20,
       6, 36, 39, 56, 7, 65, 51, 14, 22, 90, 67, 43, 17, 82, 48]


def modinv(a: int) -> int:
    return pow(a, -1, ALPHABET_SIZE)


def decrypt(cipher: str, key: list) -> str:
    out = []
    for i, ch in enumerate(cipher):
        if ch not in TEXT_LIST:
            out.append(ch)
            continue
        c_idx = TEXT_LIST.index(ch)
        inv = modinv(key[i % len(key)])
        p_idx = (c_idx * inv) % ALPHABET_SIZE
        out.append(TEXT_LIST[p_idx])
    return ''.join(out)


def score_column(cipher_col: str, k: int) -> int:
    inv = modinv(k)
    score = 0
    for ch in cipher_col:
        if ch not in TEXT_LIST:
            continue
        p_idx = (TEXT_LIST.index(ch) * inv) % ALPHABET_SIZE
        p_ch = TEXT_LIST[p_idx]
        if p_ch == ' ' or ('a' <= p_ch <= 'z') or ('A' <= p_ch <= 'Z'):
            score += 1
    return score


def find_key_length(cipher: str, lo: int = 15, hi: int = 30) -> int:
    best_len, best_score = 0, -1
    for L in range(lo, hi + 1):
        total = 0
        for col in range(L):
            group = cipher[col::L]
            total += max(score_column(group, k) for k in range(1, 97))
        avg = total / L
        if avg > best_score:
            best_score, best_len = avg, L
    return best_len


def crack_key(cipher: str, key_len: int) -> list:
    key = []
    for col in range(key_len):
        group = cipher[col::key_len]
        best_k = max(range(1, 97), key=lambda k: score_column(group, k))
        key.append(best_k)
    return key


def main():
    import os
    base = r'D:\python\1'

    with open(os.path.join(base, 'cipher.txt'), 'r', encoding='utf-8') as f:
        cipher = f.read()

    plaintext = decrypt(cipher, KEY)

    with open(os.path.join(base, 'decrypted_best.txt'), 'w', encoding='utf-8') as f:
        f.write(plaintext)

    print(plaintext)

    idx = plaintext.find('AAA{')
    if idx >= 0:
        end = plaintext.find('}', idx)
        if end >= 0:
            print(f"\n{plaintext[idx:end + 1]}")


if __name__ == '__main__':
    main()
