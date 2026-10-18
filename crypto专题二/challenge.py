from hashlib import sha256 as H
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
g = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
x = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
k = 0x9e3779b97f4a7c15f398e0a2d9d8a8e7
y, r = pow(g, x, p), pow(g, k, p)
h1, s1 = (v := int(H(b'msg1').hexdigest(), 16)), (k + x * v) % (p - 1)
h2, s2 = (v := int(H(b'msg2').hexdigest(), 16)), (k + x * v) % (p - 1)
print(f'p={p}\ng={g}\ny={y}\nr={r}\nh1={h1}\ns1={s1}\nh2={h2}\ns2={s2}')
