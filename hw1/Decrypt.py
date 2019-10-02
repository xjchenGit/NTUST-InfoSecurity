#!/usr/local/bin/python3

import sys
from string import ascii_uppercase as uppercase
from textwrap import wrap
from itertools import cycle
from math import ceil


def die(*args):
    print(*args)
    sys.exit(0)


len(sys.argv) == 4 or die("Usage: ./decrypt.py [cipher] [key] [ciphertext]")

cipher, key, ciphertext = sys.argv[1:]
ciphertext = ciphertext.upper()
key = key.upper()

if cipher == 'caesar':
    key.isnumeric() or die("key should be integer for caesar cipher.")
    key = int(key)
    plaintext = ''.join([chr((ord(c) - 65 - key) % 26 + 65) if c in uppercase else c for c in ciphertext])

elif cipher == 'playfair':
    seen = set()
    key = ''.join([c for c in key + uppercase if c in uppercase and not (c in seen or seen.add(c))])
    key = key.replace('I' if key.rindex('I') > key.rindex('J') else 'J', '')
    key_matrix = wrap(key, 5)
    plaintext = ""
    for (a, b) in zip(ciphertext[::2], ciphertext[1::2]):
        i_a, i_b = key.index(a), key.index(b)
        x_a, y_a = i_a // 5, i_a % 5
        x_b, y_b = i_b // 5, i_b % 5
        if y_a == y_b:
            plaintext += key_matrix[(x_a - 1) % 5][y_a] + key_matrix[(x_b - 1) % 5][y_b]
        elif x_a == x_b:
            plaintext += key_matrix[x_a][(y_a - 1) % 5] + key_matrix[x_b][(y_b - 1) % 5]
        else:
            plaintext += key_matrix[x_a][y_b] + key_matrix[x_b][y_a]

elif cipher == 'vernam':
    xor = lambda c, k: chr(((ord(c) - 65) ^ (ord(k) - 65)) + 65)
    plaintext = ''.join([xor(c, k) for c, k in zip(ciphertext, key)])
    for i, c in enumerate(ciphertext[len(key):]):
        plaintext += xor(c, plaintext[i])

elif cipher == 'row':
    key.isnumeric() or die("key should be integer for row transposition cipher.")
    size = ceil(len(ciphertext) / len(key))
    main_len = size * (len(ciphertext) % len(key))
    ciphertext = wrap(ciphertext[:main_len], size) + wrap(ciphertext[main_len:], size - 1) 
    plaintext = ''.join([''.join([ciphertext[int(k)-1].ljust(3, ' ')[i] for k in key]) for i in range(size)])

elif cipher == 'rail_fence':
    key.isnumeric() or die("key should be integer for row transposition cipher.")
    key = int(key)
    r = list(range(key))
    pattern = cycle(r + r[-2:0:-1])
    indexes = sorted(range(len(ciphertext)), key=lambda i: next(pattern))
    result = [''] * len(ciphertext)
    for i, c in zip(indexes, ciphertext): result[i] = c
    plaintext = ''.join(result)

else:
    die("Unknown cipher:", cipher)

print(plaintext.strip().lower())
