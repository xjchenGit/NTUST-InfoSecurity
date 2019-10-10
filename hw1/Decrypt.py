#!/usr/local/bin/python3

import sys
from string import ascii_uppercase as uppercase
from textwrap import wrap
from itertools import cycle
from math import ceil


def die(*args):
    print(*args)
    sys.exit(0)


len(sys.argv) == 4 or die("Usage: ./Decrypt.py [cipher] [key] [ciphertext]")

cipher, key, ciphertext = sys.argv[1:]
cipher in ['caesar', 'playfair', 'vernam', 'row', 'rail_fence'] or die("Unknown cipher:", cipher)

ciphertext = ciphertext.upper()
key = key.upper()


def caesar(key, ciphertext):
    key.isdigit() or die("key should be integer for caesar cipher.")
    return ''.join([chr((ord(c) - 65 - int(key)) % 26 + 65) if c in uppercase else c for c in ciphertext])


def playfair(key, ciphertext):
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
    return plaintext.rstrip('X')


def vernam(key, ciphertext):
    def xor(c, k): return chr(((ord(c) - 65) ^ (ord(k) - 65)) + 65)
    plaintext = ''.join([xor(c, k) for c, k in zip(ciphertext, key)])
    for i, c in enumerate(ciphertext[len(key):]):
        plaintext += xor(c, plaintext[i])
    return plaintext


def row(key, ciphertext):
    key.isdigit() or die("key should be digits for row transposition cipher.")
    key = list(map(int, key))
    height = ceil(len(ciphertext) / len(key))
    box = height * (len(ciphertext) % len(key) or len(key))
    chunks = sorted([(height, k) if i < box/height else (height-1, k)
                     for i, k in enumerate(key)], key=lambda c: c[1])
    plaintext, pointer = ['']*len(key), 0
    for chunk in chunks:
        plaintext[chunk[1]-1] = ciphertext[pointer:pointer+chunk[0]].ljust(height, " ")
        pointer += chunk[0]
    return ''.join(map(lambda p: ''.join(p), zip(*[plaintext[k-1] for k in key])))


def rail_fence(key, ciphertext):
    key.isdigit() or die("key should be integer for row transposition cipher.")
    r = list(range(int(key)))
    pattern = cycle(r + r[-2:0:-1])
    indexes = sorted(range(len(ciphertext)), key=lambda i: next(pattern))
    result = [''] * len(ciphertext)
    for i, c in zip(indexes, ciphertext):
        result[i] = c
    return ''.join(result)


print(locals()[cipher](key, ciphertext).lower())
