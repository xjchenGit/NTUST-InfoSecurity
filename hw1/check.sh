#!/bin/sh
PLAINTEXT='doyourbestandthenletgo'

./Decrypt.py caesar 5 `./Encrypt.py caesar 5 $PLAINTEXT`
./Decrypt.py playfair COMP  `./Encrypt.py playfair COMP $PLAINTEXT`
./Decrypt.py vernam TEC  `./Encrypt.py vernam TEC $PLAINTEXT`
./Decrypt.py row 45362178 `./Encrypt.py row 45362178 $PLAINTEXT`
./Decrypt.py rail_fence 4 `./Encrypt.py rail_fence 4 $PLAINTEXT`