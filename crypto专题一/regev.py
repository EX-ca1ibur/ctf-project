import sys
sys.path.insert(0, "D:/regev")
from hashlib import sha256
from Crypto.Cipher import AES
import flint
from output import n, m, q, A, b, iv, ct

dim = m + n + 1
M = [[0] * dim for _ in range(dim)]
for i in range(m):
    M[i][i] = q
for i in range(n):
    for j in range(m):
        M[m + i][j] = (-A[j][i]) % q
    M[m + i][m + i] = 1
for j in range(m):
    M[dim - 1][j] = b[j]
M[dim - 1][dim - 1] = 1

L = flint.fmpz_mat([[flint.fmpz(v) for v in r] for r in M]).lll()

for i in range(dim):
    last = int(L[i, dim - 1])
    if abs(last) != 1:
        continue
    row = [int(L[i, j]) for j in range(dim)]
    e, s = row[:m], row[m:m + n]
    if last == -1:
        e, s = [-x for x in e], [-x for x in s]
    if not (all(abs(x) <= 2 for x in e) and all(x in (0, 1) for x in s)):
        continue
    ok = True
    for ii in range(m):
        if (sum(A[ii][jj] * s[jj] for jj in range(n)) + e[ii]) % q != b[ii]:
            ok = False
            break
    if not ok:
        continue
    key = sha256(bytes(s)).digest()
    pt = AES.new(key, AES.MODE_CBC, iv).decrypt(ct)
    print(pt[:-pt[-1]].decode())
    break
