from Crypto.Util.number import *
from Crypto.Cipher import AES
from hashlib import md5

def pad(x, length):
    return x + (length - len(x) % length) * b'\x00'

p = 960494008017250155494739990397196249930200062145145133132556398221074529657304218221253517153928380265486339083177542201148993799925721673833333778621388110957986908045712612233794551809
g = 3
c = 104432909313713867727553310098163745147881907436023683892360341201060611877398021767148427983607592721518923076185059576446612113776349611392890056681875737267105739889849963654386118023
ct = b"\xd9\xb5\xdf\xc6\xfc\xf5'C\xb5\x10%\x93\xbe\x98\xc8\x8d\x80\x98\x1d2}\xce\x99wr\xe2\xb7n\xe1{\xf0\xf2"

v = 518
x = 0
gi = pow(g, p - 2, p)
for k in range(v):
    h = c * pow(gi, x, p) % p
    e = (p - 1) // (1 << (k + 1))
    t = pow(h, e, p)
    if t == p - 1:
        x += (1 << k)

key = md5(str(x).encode()).digest()
aes = AES.new(key=key, mode=AES.MODE_ECB)
flag = aes.decrypt(ct).rstrip(b'\x00').decode()
print(flag)
