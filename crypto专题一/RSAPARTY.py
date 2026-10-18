import socket as sk, hashlib as hl, string as st, itertools as it
from Crypto.Util.number import *
P = 4101606004956207077610139248107234661363936409291037788329623945052342359189025355857808458327474875872315336042444939304407350365987508146404722456431489

def egcd(a, b):
    if b == 0: return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y

def pow4(t):
    for c in it.product(st.ascii_letters + st.digits, repeat=4):
        if hl.sha256("".join(c).encode()).hexdigest() == t:
            return "".join(c)

def iroot(n):
    x, y = n, (n + 1) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x

def fermat(n):
    a = iroot(n) + 1
    for _ in range(100000):
        b2 = a * a - n
        b = iroot(b2)
        if b * b == b2: return a - b, a + b
        a += 1
    return None

def icbrt(x):
    lo, hi = 0, 1 << (x.bit_length() // 3 + 1)
    while lo < hi:
        mid = (lo + hi) // 2
        if mid ** 3 < x: lo = mid + 1
        else: hi = mid
    return lo if lo ** 3 == x else lo - 1

def crt(rs, ms):
    M = 1
    for m in ms: M *= m
    x = 0
    for r, m in zip(rs, ms):
        Mi = M // m
        x += r * Mi * pow(Mi, -1, m)
    return x % M

def fr(n, e, c1, c2, pad):
    def _(f, g):
        r = [0] * (len(f) + len(g) - 1)
        for i in range(len(f)):
            for j in range(len(g)): r[i+j] = (r[i+j] + f[i]*g[j]) % n
        return r
    def __(f, g):
        f = f[:]
        while len(f) >= len(g):
            c = f[-1] * pow(g[-1], -1, n) % n
            for i in range(len(g)): f[len(f)-len(g)+i] = (f[len(f)-len(g)+i] - c*g[i]) % n
            while f and f[-1] == 0: f.pop()
        return f if f else [0]
    def ___(a, b):
        while b and b != [0]: a, b = b, __(a, b)
        return a
    f1 = [(-c1) % n, 0, 0, 1]
    f2 = [(-c2 + pad**3) % n, (3*pad**2) % n, (3*pad) % n, 1]
    g = ___(f1, f2)
    return (-g[0] * pow(g[1], -1, n)) % n if len(g) == 2 else None

def wiener(n, e):
    a, b = e, n
    cf = []
    while b: cf.append(a // b); a, b = b, a % b
    p0, q0 = 0, 1
    p1, q1 = 1, 0
    for ak in cf:
        p, q = ak * p1 + p0, ak * q1 + q0
        p0, q0, p1, q1 = p1, q1, p, q
        if q == 0 or p == 0: continue
        phi = (e * q - 1) // p
        if (e * q - 1) % p: continue
        s = n - phi + 1
        disc = s * s - 4 * n
        if disc < 0: continue
        t = iroot(disc)
        if t * t == disc and (s + t) & 1 == 0: return q
    return None

def run(ps):
    if "pad" in ps: return fr(ps["n"], ps["e"], ps["c1"], ps["c2"], ps["pad"])
    if "e1" in ps:
        _, a, b = egcd(ps["e1"], ps["e2"])
        c1, c2, n = ps["c1"], ps["c2"], ps["n"]
        if a < 0: c1, a = pow(c1, -1, n), -a
        if b < 0: c2, b = pow(c2, -1, n), -b
        return (pow(c1, a, n) * pow(c2, b, n)) % n
    if "n1" in ps:
        return icbrt(crt([ps["c1"], ps["c2"], ps["c3"]], [ps["n1"], ps["n2"], ps["n3"]]))
    n, e, c = ps["n"], ps["e"], ps["c"]
    pq = fermat(n)
    if pq and pq[0] * pq[1] == n: return pow(c, pow(e, -1, (pq[0]-1)*(pq[1]-1)), n)
    if n % P == 0: return pow(c, pow(e, -1, (P-1)*(n//P-1)), n)
    d = wiener(n, e)
    if d: return pow(c, d, n)

def rdu(s, m):
    d = b""
    while m not in d:
        try:
            c = s.recv(1)
            if not c: break
            d += c
        except: break
    return d.decode(errors="replace")

def go(host, port):
    s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    s.settimeout(60)
    s.connect((host, port))
    buf = rdu(s, b"4 alphanumeric chars): ")
    t = buf.split("== ")[1].split("\n")[0].strip()
    s.send((pow4(t) + "\n").encode())
    rdu(s, b"\n")
    for _ in range(6):
        buf = rdu(s, b"Give me m (hex): ")
        ps = {}
        for l in buf.split("\n"):
            if " = " in l:
                k, v = l.split(" = ", 1)
                try: ps[k.strip()] = int(v.strip())
                except: pass
        m = run(ps)
        s.send((hex(m)[2:] + "\n").encode())
        rdu(s, b"\n")
    try:
        s.settimeout(2)
        buf = b""
        while True:
            try:
                c = s.recv(4096)
                if not c: break
                buf += c
            except: break
        for l in buf.decode(errors="replace").split("\n"):
            if "{" in l: print(l.strip())
    except: pass
    s.close()

if __name__ == "__main__":
    import sys as _s
    go(_s.argv[1] if len(_s.argv) > 1 else "127.0.0.1", int(_s.argv[2]) if len(_s.argv) > 2 else 56187)
