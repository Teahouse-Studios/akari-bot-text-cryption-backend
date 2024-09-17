# random generate key and tweaks for the encryption and decryption

import random

def random_string(length: int) -> str:
    return ''.join(random.choices("0123456789ABCDEF", k=length))

key = random_string(32)
tweak = random_string(14)
print(f"Key: {key}")
print(f"Tweak: {tweak}")