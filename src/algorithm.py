import math
import sys
def RSA(p, q):
    phi = (p - 1) * (q - 1)
    n = p*q
    e = coprime(phi)
    d = comod(e, phi)
    return (e, n), (d, n)

def coprime(phi):
    e = 2
    while math.gcd(e, phi) != 1:
        e+=1
    return e

def comod(e, phi):
    d = int(phi / e)
    
    while (d * e) % phi != 1:
        d+=1
    return d

def encrypt_RSA(value, e, n):
    value = list(value)
    encoded_values = [ord(c) for c in value]
    encrypted_values = [v**e % n for v in encoded_values]
    converted_values = [chr(v) for v in encrypted_values]
    print(str(converted_values))
    return "".join(converted_values)

def decrypt_RSA(value, d, n):
    value = list(value)
    encoded_values = [ord(c) for c in value]
    decrypted_values = [v**d % n for v in encoded_values]
    byte_values = [chr(v) for v in decrypted_values]
    return "".join(byte_values)

# public, private = RSA(13, 17)
# print(public, private)

# encrypted = encrypt_RSA(155, public[0], public[1])

# print("Encrypted value: ", encrypted)
# print("Decrypted with private key to: ", decrypt_RSA(encrypted, private[0], private[1]))