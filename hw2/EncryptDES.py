#!/usr/bin/python
import sys
# Permutation tables & SBoxes


class DesEncrypt(object):
<<<<<<< HEAD
    # Create 16 subkeys,each of which is 48-bits long
    PC1=(
=======
    # Step1: Create 16 subkeys,each of which is 48-bits long
    PC1 = (
>>>>>>> 7a8ca7b2776e502f0ce79b1b035061504211b3cf
        57, 49, 41, 33, 25, 17, 9,
        1,  58, 50, 42, 34, 26, 18,
        10, 2,  59, 51, 43, 35, 27,
        19, 11, 3,  60, 52, 44, 36,
        63, 55, 47, 39, 31, 23, 15,
        7,  62, 54, 46, 38, 30, 22,
        14, 6,  61, 53, 45, 37, 29,
        21, 13, 5,  28, 20, 12, 4
    )
    PC2 = (
        14, 17, 11, 24, 1,  5,
        3,  28, 15, 6,  21, 10,
        23, 19, 12, 4,  26, 8,
        16, 7,  27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    )
    # Encode each 64-bit block of data
    InitialPermutation = (
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9,  1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    )

    Expansion = (
        32, 1,  2,  3,  4,  5,
        4,  5,  6,  7,  8,  9,
        8,  9,  10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    )

    SBoxes = {
        0: (
            14,  4, 13,  1,  2, 15, 11,  8,  3, 10,  6, 12,  5,  9,  0,  7,
            0, 15,  7,  4, 14,  2, 13,  1, 10,  6, 12, 11,  9,  5,  3,  8,
            4,  1, 14,  8, 13,  6,  2, 11, 15, 12,  9,  7,  3, 10,  5,  0,
            15, 12,  8,  2,  4,  9,  1,  7,  5, 11,  3, 14, 10,  0,  6, 13
        ),
        1: (
            15,  1,  8, 14,  6, 11,  3,  4,  9,  7,  2, 13, 12,  0,  5, 10,
            3, 13,  4,  7, 15,  2,  8, 14, 12,  0,  1, 10,  6,  9, 11,  5,
            0, 14,  7, 11, 10,  4, 13,  1,  5,  8, 12,  6,  9,  3,  2, 15,
            13,  8, 10,  1,  3, 15,  4,  2, 11,  6,  7, 12,  0,  5, 14,  9
        ),
        2: (
            10,  0,  9, 14,  6,  3, 15,  5,  1, 13, 12,  7, 11,  4,  2,  8,
            13,  7,  0,  9,  3,  4,  6, 10,  2,  8,  5, 14, 12, 11, 15,  1,
            13,  6,  4,  9,  8, 15,  3,  0, 11,  1,  2, 12,  5, 10, 14,  7,
            1, 10, 13,  0,  6,  9,  8,  7,  4, 15, 14,  3, 11,  5,  2, 12
        ),
        3: (
            7, 13, 14,  3,  0,  6,  9, 10,  1,  2,  8,  5, 11, 12,  4, 15,
            13,  8, 11,  5,  6, 15,  0,  3,  4,  7,  2, 12,  1, 10, 14,  9,
            10,  6,  9,  0, 12, 11,  7, 13, 15,  1,  3, 14,  5,  2,  8,  4,
            3, 15,  0,  6, 10,  1, 13,  8,  9,  4,  5, 11, 12,  7,  2, 14
        ),
        4: (
            2, 12,  4,  1,  7, 10, 11,  6,  8,  5,  3, 15, 13,  0, 14,  9,
            14, 11,  2, 12,  4,  7, 13,  1,  5,  0, 15, 10,  3,  9,  8,  6,
            4,  2,  1, 11, 10, 13,  7,  8, 15,  9, 12,  5,  6,  3,  0, 14,
            11,  8, 12,  7,  1, 14,  2, 13,  6, 15,  0,  9, 10,  4,  5,  3
        ),
        5: (
            12,  1, 10, 15,  9,  2,  6,  8,  0, 13,  3,  4, 14,  7,  5, 11,
            10, 15,  4,  2,  7, 12,  9,  5,  6,  1, 13, 14,  0, 11,  3,  8,
            9, 14, 15,  5,  2,  8, 12,  3,  7,  0,  4, 10,  1, 13, 11,  6,
            4,  3,  2, 12,  9,  5, 15, 10, 11, 14,  1,  7,  6,  0,  8, 13
        ),
        6: (
            4, 11,  2, 14, 15,  0,  8, 13,  3, 12,  9,  7,  5, 10,  6,  1,
            13,  0, 11,  7,  4,  9,  1, 10, 14,  3,  5, 12,  2, 15,  8,  6,
            1,  4, 11, 13, 12,  3,  7, 14, 10, 15,  6,  8,  0,  5,  9,  2,
            6, 11, 13,  8,  1,  4, 10,  7,  9,  5,  0, 15, 14,  2,  3, 12
        ),
        7: (
            13,  2,  8,  4,  6, 15, 11,  1, 10,  9,  3, 14,  5,  0, 12,  7,
            1, 15, 13,  8, 10,  3,  7,  4, 12,  5,  6, 11,  0, 14,  9,  2,
            7, 11,  4,  1,  9, 12, 14,  2,  0,  6, 10, 13, 15,  3,  5,  8,
            2,  1, 14,  7,  4, 10,  8, 13, 15, 12,  9,  0,  3,  5,  6, 11
        )
    }

    P = (
        16,  7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2,  8, 24, 14, 32, 27,  3,  9,
        19, 13, 30,  6, 22, 11, 4,  25
    )

    FinalPermutation = (
        40,  8, 48, 16, 56, 24, 64, 32,
        39,  7, 47, 15, 55, 23, 63, 31,
        38,  6, 46, 14, 54, 22, 62, 30,
        37,  5, 45, 13, 53, 21, 61, 29,
        36,  4, 44, 12, 52, 20, 60, 28,
        35,  3, 43, 11, 51, 19, 59, 27,
        34,  2, 42, 10, 50, 18, 58, 26,
        33,  1, 41,  9, 49, 17, 57, 25
    )
    # generate round keys
    shift_value = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)

    def __init__(self, key, plaintext):
        self.key = ''
        self.plaintext = ''

    def encrypt(self, key, plaintext):
        # int(self.key)
        # permutate by table PC1
        key = self.permutation(key, 64, 'PC1')
        # split up key in two halves
        # generate the 16 round keys
        C0 = key >> 28
        D0 = key & (2**28-1)

        round_keys = dict.fromkeys(range(0, 17))
        # left-rotation function

        def rotation_function(val, left, right): return \
            ((val & (2**right-1)) >> (right-(left % right))) | \
            (val << left % right) & (2**right-1)
        # # initial rotation
        C0 = rotation_function(C0, 0, 28)
        D0 = rotation_function(D0, 0, 28)
        round_keys[0] = (C0, D0)
        # #create 16 different key pairs
        for i, s_val in enumerate(self.shift_value):
            i += 1
            Ci = rotation_function(round_keys[i-1][0], s_val, 28)
            Di = rotation_function(round_keys[i-1][1], s_val, 28)
            round_keys[i] = (Ci, Di)
        del round_keys[0]
<<<<<<< HEAD
        
        #now form the keys from concatenated CiDi i<=i<=16 and by apllying PC2
        for i,(Ci,Di) in round_keys.items():
=======

        # #now form the keys from concatenated CiDi i<=i<=16 and by apllying PC2
        for i, (Ci, Di) in round_keys.items():
>>>>>>> 7a8ca7b2776e502f0ce79b1b035061504211b3cf
            Keyi = (Ci << 28) + Di
            round_keys[i] = self.permutation(Keyi, 56, 'PC2')  # 56bits->48bits
            # print('K',i,':',bin(round_keys[i]))

        # print(round_keys)

        _plaintext = self.permutation(plaintext, 64, 'InitialPermutation')
        Left0 = _plaintext >> 32
        Right0 = _plaintext & (2**32-1)

        # apply the round function 16 times in following scheme
        # (feistel cipher)
        L_last = Left0
        R_last = Right0

        for i in range(1, 17):
            LeftRound = R_last
            RightRound = L_last ^ self.round_function(R_last, round_keys[i])
            L_last = LeftRound
            R_last = RightRound

        # concatenate reversed
        ciphertext = (RightRound << 32) + LeftRound
        # final permutation
        ciphertext = self.permutation(ciphertext, 64, 'FinalPermutation')
        ciphertext = hex(ciphertext)[:2]+hex(ciphertext)[2:].upper().rstrip("L")
        return ciphertext

    def permutation(self, block, per_len, table):
        _block = bin(block)[2:].zfill(per_len)

        if table == 'PC1':
            _table = self.PC1
        elif table == 'PC2':
            _table = self.PC2
        elif table == 'Expansion':
            _table = self.Expansion
        elif table == 'P':
            _table = self.P
        elif table == 'InitialPermutation':
            _table = self.InitialPermutation
        elif table == 'FinalPermutation':
            _table = self.FinalPermutation

        # print(_table)
        perm = []
        for i in range(len(_table)):
            perm.append(_block[_table[i]-1])
        return int(''.join(perm), 2)

    def round_function(self, Righti, Keyi):
        # expend Righti from 32 to 48 bit using table expansion
        Righti = self.permutation(Righti, 32, 'Expansion')

        # xor with round key
        Righti = Righti ^ Keyi

        # split Righti into 8 groups of 6 bit
        Rightis = [((Righti & (0b111111 << s_val)) >> s_val)
                   for s_val in (42, 36, 30, 24, 18, 12, 6, 0)]

        for i, j in enumerate(Rightis):
            row = ((0b100000 & j) >> 4) + (0b1 & j)
            column = (0b011110 & j) >> 1
            Rightis[i] = self.SBoxes[i][16*row+column]

        Rightis = zip(Rightis, (28, 24, 20, 16, 12, 8, 4, 0))
        Righti = 0

        for j, l_s_val in Rightis:
            Righti += (j << l_s_val)
        # another permutation 32 bit -> 32bit
        Righti = self.permutation(Righti, 32, 'P')

        return Righti


# main block
key = sys.argv[1]
plaintext = sys.argv[2]

key = int(key, 16)
plaintext = int(plaintext, 16)
DESEn = DesEncrypt(key, plaintext)
print(DESEn.encrypt(key, plaintext))
