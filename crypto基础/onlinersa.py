import sys
from math import gcd
import sympy

sys.set_int_max_str_digits(0)

c = [
    62672938275009705596581242847130514775891540954531116,
    62672938275009705596581242847130514775891540954531116,
    62672938275009705596581242847130514775891540954531116,
    28065112754348826692839224620054962177237340625508142,
    82805428369361023445247061843917815511685788893461488,
    64529102835595887450014112173830620877278761152089439,
    61692909713449333722171394128578104844776919632656810,
]

exponents = [65, 65, 65, 240, 159, 152, 141]

c65  = c[0]
c240 = c[3]
c159 = c[4]
c152 = c[5]
c141 = c[6]


print(f"Exponents: {sorted(set(exponents))}")
print(f"c65  = {c65}")
print(f"c240 = {c240}")
print(f"c159 = {c159}")
print(f"c152 = {c152}")
print(f"c141 = {c141}")


print("Computing D1 = c65^48 - c240^13 ...")
D1 = pow(c65, 48) - pow(c240, 13)
print(f"  D1 has {len(str(D1))} decimal digits")

print("Computing D2 = c240^19 - c152^30 ...")
D2 = pow(c240, 19) - pow(c152, 30)
print(f"  D2 has {len(str(D2))} decimal digits")

n_candidate = gcd(D1, D2)
print(f"\nInitial gcd(D1, D2) = {n_candidate}")

def remove_small_factors(x, limit=1000000):
    while x % 2 == 0:
        x //= 2
    p = 3
    while p * p <= x and p <= limit:
        while x % p == 0:
            x //= p
        p += 2
    return x

n = remove_small_factors(n_candidate)
print(f"n = {n}")
print(f"  ({len(str(n))} decimal digits, {n.bit_length()} bits)")

if sympy.isprime(n):
    print("[OK] n is prime")
else:
    print("[WARN] n is NOT prime")
    for p in range(2, 100000):
        while n % p == 0:
            n //= p
    if sympy.isprime(n):
        print(f"  After factoring: n = {n}")

assert pow(c65, 48, n) == pow(c240, 13, n), "Verification failed!"
print("[OK] c65^48 ≡ c240^13 (mod n)")


def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    return g, y1, x1 - (a // b) * y1

g, a_coeff, b_coeff = extended_gcd(65, 159)
print(f"gcd(65, 159) = {g}")
print(f"{a_coeff}*65 + {b_coeff}*159 = {a_coeff*65 + b_coeff*159}")

m_mod_n = (pow(c65, a_coeff, n) * pow(c159, b_coeff, n)) % n
print(f"\nm mod n = {m_mod_n}")

assert pow(m_mod_n, 65, n) == c65
assert pow(m_mod_n, 159, n) == c159
print("[OK] Verified m_mod_n")


SHIFT = 150
TWO150 = 1 << SHIFT

m_full = None
found = False

for delta in range(0, 100000):
    low_candidate = (m_mod_n + delta * TWO150) % n
    if low_candidate < TWO150:
        high_candidate = n - delta
        if high_candidate <= 0:
            continue
        m_candidate = high_candidate * TWO150 + low_candidate
        if sympy.nextprime(m_candidate >> SHIFT) == n:
            if pow(m_candidate, 65, n) == c65:
                m_full = m_candidate
                found = True
                print(f"Found at delta = {delta}")
                break

if not found:
    p = sympy.prevprime(n)
    while p > n - 100000 and not found:
        delta = n - p
        low_candidate = (m_mod_n + delta * TWO150) % n
        if low_candidate < TWO150:
            m_candidate = p * TWO150 + low_candidate
            if sympy.nextprime(m_candidate >> SHIFT) == n:
                if pow(m_candidate, 65, n) == c65:
                    m_full = m_candidate
                    found = True
                    break
        p = sympy.prevprime(p)

    if not found:
        for q_offset in range(-1000, 1000):
            q = TWO150 + q_offset
            if q <= 0:
                continue
            m_candidate = q * n + m_mod_n
            if sympy.nextprime(m_candidate >> SHIFT) == n:
                if pow(m_candidate, 65, n) == c65:
                    m_full = m_candidate
                    found = True
                    break

if not found:
    print("ERROR: Could not recover m!")
    sys.exit(1)

print(f"m = {m_full}")


flag_bytes = m_full.to_bytes((m_full.bit_length() + 7) // 8, 'big')
flag = flag_bytes.decode('utf-8')
print(f"Flag: {flag}")

for i, (exp, ct) in enumerate(zip(exponents, c)):
    computed = pow(m_full, exp, n)
    status = "OK" if computed == ct else "FAIL"
    print(f"  [{i}] m^{exp} mod n: {status}")

print("\nDone.")
