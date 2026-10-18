

TARGET = [
    0xFC, 0xFC, 0xF4, 0xD6, 0xF7, 0xAA, 0xEF, 0xEA, 0xEF, 0xF0,
    0xB6, 0xCC, 0x93, 0x8E, 0xB2, 0x12, 0xBB, 0x0C, 0x9E, 0xFC,
    0x42, 0xE9, 0x26, 0xD9, 0xDB, 0x08,
]


def solve() -> str:

    flag_chars = []
    for i, t in enumerate(TARGET):
        c = t ^ ((i * 7) & 0xFF)
        c = c ^ 0xFF
        c = (c - i) & 0xFF
        c = c ^ 0x42
        flag_chars.append(chr(c))
    return ''.join(flag_chars)


def main():
    flag = solve()
    print(f"Flag: {flag}")


    ok = True
    for i, t in enumerate(TARGET):
        c = ord(flag[i])
        c = c ^ 0x42
        c = (c + i) & 0xFF
        c = (~c) & 0xFF
        c = c ^ ((i * 7) & 0xFF)
        ok = ok and (c == t)
    print(f"验证: {'通过' if ok else '失败'}")


if __name__ == '__main__':
    main()
