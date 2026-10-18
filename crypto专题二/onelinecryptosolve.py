import re

MOD = 2**67 - 1

base_flag = "SEKAI{" + "6" * 67 + "}"
base_int = int.from_bytes(base_flag.encode(), 'big')
target = (-base_int) % MOD

bits = [(target >> k) & 1 for k in range(67)]

chars = []
for pos in range(67):
    j = 67 - pos
    k = (8 * j) % 67
    chars.append('7' if bits[k] else '6')

flag = "SEKAI{" + "".join(chars) + "}"
print(f"Flag: {flag}")

assert re.match(r'SEKAI{[67]{67}}$', flag)
flag_int = int.from_bytes(flag.encode(), 'big')
assert flag_int % MOD == 0
print("All assertions passed — Challenge 2 solved!")
