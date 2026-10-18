import socket as sk, re, sys

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
M_HEX = "1234567890abcdef1234567890abcdef"

def go(host, port):
    s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    s.settimeout(10)
    s.connect((host, port))

    def r():
        d = b""
        while True:
            try:
                c = s.recv(4096)
                if not c: break
                d += c
                if d.count(b"\n") >= 2 and b"> " in d: break
            except: break
        return d.decode(errors="replace")

    def sig(msg):
        s.send(f"sign {msg}\n".encode())
        resp = r()
        rv = int(re.search(r"r\s*=\s*(\d+)", resp).group(1))
        sv = int(re.search(r"s\s*=\s*(\d+)", resp).group(1))
        return rv, sv

    print(r())

    r1, s1 = sig(M_HEX)
    r2, s2 = sig(f"-{M_HEX}")

    print(f"r1={r1}\nr2={r2}")
    assert r1 == r2, "nonce reuse failed"

    z1 = int(M_HEX, 16) % N
    z2 = (-int(M_HEX, 16)) % N
    k = ((z1 - z2) % N) * pow((s1 - s2) % N, -1, N) % N
    d = ((s1 * k - z1) % N) * pow(r1, -1, N) % N

    s.send(f"submit {hex(d)[2:]}\n".encode())
    resp = b""
    try:
        s.settimeout(3)
        while True:
            c = s.recv(4096)
            if not c: break
            resp += c
    except: pass
    print(resp.decode().strip())
    s.close()

if __name__ == "__main__":
    go(sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1",
       int(sys.argv[2]) if len(sys.argv) > 2 else 54890)
