#!/usr/bin/python
import sys
import string
# Input: plaintext needs to be lowercase
# Input: Ciphertext needs to be uppercase
# Input: Key needs to be uppercase
class caeser_cipher(object):
    def __init__(self,key,plaintext):
        self.key=''
        self.plaintext=''

    def caeser_cipher_encrypt(self):
        EncryptText = ""
        # transverse the plain text
        for ch in plaintext:
            # Encrypt lowercase characters in plain text
            if (ch.islower()):
                EncryptText += chr((ord(ch) - 97 + key) % 26 + 97)
            # Encrypt uppercase characters in plain text
            elif (ch.isupper()):
                EncryptText += chr((ord(ch) - 65 + key) % 26 + 65)
            # Encrypt other characters in plain text
            else:
                EncryptText+=ch
        return EncryptText.upper()
# #check the above function

# playfair cipher
# 1.fill in letters of keyword(sans duplicates)
# 2.fill rests of matrix with other letters
# 3.plaintext is encrypted two letters at a time
#   1)if a pair is a repeated letter,insert filler like 'X'
#   2)if both letter fall in same row,replace each with letter to right
#     (wrapping back to start from end)
#   3)if both letters fall in the same column,replace each with the letter
#     below it(wrapping to top from bottom)
#   4)otherwise each letter is replaced by the letter in the same row and
#     in the column of the other letter of the pair

key_table=['','','','','']
# using alphabet without j
alphbet='ABCDEFGHIKLMNOPQRSTUVWXYZ'
def __init__(self,key,plaintext):
    self.key=''
    self.plaintext=''

# delete duplicate letter
def del_duplicates(key):
    # alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    final_key=''
    for i in key:
        if not i in final_key:
            if (i=='j'):
                i='i'
            final_key += i
    return final_key.upper()

def fill_matrix(key):
    j=0
    # Delete duplicate letters
    new_key = del_duplicates(key)
    # create new alphabet
    for ch in alphbet:
        if not ch in new_key:
            new_key+=ch
    # create the new matrix with new alphabet
    for i in range(len(new_key)):
        key_table[j] += new_key[i]
        if 0==(i+1)%5:
            j+=1

def Get_Index(ch):
    for i in range(len(key_table)):
        for j in range(len(key_table)):
            if ch==key_table[i][j]:
                return i,j

def playfair_cipher_encrypt(key_table,plaintext):
    EncryptText = ''
    _plaintext=plaintext
    i=0
    if len(plaintext)%2!=0:
        _plaintext+='X'

    for s in range(0,len(plaintext)+1,2):
        if s<len(plaintext)-1:
            if plaintext[s] == plaintext[s+1]:
                _plaintext=_plaintext[:s+1]+'X'+_plaintext[s+2:]

    _plaintext.upper()
    _plaintext_list = list(_plaintext)
    while i<len(_plaintext):
        if _plaintext[i].isalpha():
            j=i+1
            while j<len(_plaintext):
                if _plaintext[i].upper():
                    if _plaintext[i].upper()=='J':
                        x=Get_Index('I')
                    else:
                        x=Get_Index(_plaintext[i].upper())
                    if _plaintext[j].upper()=='J':
                        y=Get_Index('I')
                    else:
                        y=Get_Index(_plaintext[j].upper())

                    if  x[0]==y[0]: # if in the same row
                        EncryptText += key_table[x[0]][(x[1]+1)%5] + key_table[y[0]][(y[1]+1)%5]
                    elif x[1]==y[1]: # if in the same cloumn
                        EncryptText += key_table[(x[0]+1)%5][x[1]] + key_table[(y[0]+1)%5][y[1]]
                    else: # if not in the same row or cloumn
                        EncryptText += key_table[x[0]][y[1]] + key_table[y[0]][x[1]]
                    break
                j+=1
            i=j+1
            continue
        else:
            EncryptText+=_plaintext[i]
        i+=1
    return EncryptText.upper()

# key='COMP'

#print(key_table)
#plaintext='doyourbestandthenletgo'
# fill_matrix(key)
# print(playfair_cipher_encrypt(key_table,plaintext))


# Vernam proposed the autokey system
#create vernam table
class vernam_cipher(object):
    alphbet=string.ascii_uppercase
    def __init__(self,key,plaintext):
        self.key=''
        self.plaintext=''

    def vernam_encrypt(self,key,plaintext):
        # create the key
        Encrypttext=''
        i=0
        for ch in plaintext:
            if len(key)<len(plaintext):
                key += ch
            ch=ch.upper()
            x=ord(ch)-65
            key=key.upper()
            y=ord(key[i])-65
            i+=1
            ch_index=x^y
            Encrypttext += chr(ch_index+65)
        return Encrypttext.upper()

# key = 'TEC'
# plaintext = 'helloworld'
# #helloworld
# #TEChellowo
# #UAJMKDFFDN
# print(plaintext)
# print(vernam_cipher(key,plaintext))

class row_cipher(object):
    alphbet=string.ascii_uppercase
    def __init__(self,key,plaintext):
        self.key=''
        self.plaintext=''

    def row_encrypt(self):
        # create the matric table
        m=len(key)
        if len(plaintext)%len(key)!=0:
            n=int(len(plaintext)/len(key))+1
        else:
            n=int(len(plaintext)/len(key))
        o=m*n-len(plaintext)
        row_matric=[['' for i in range(m)] for j in range(n)]

        # create key map and row text
        key_map={}
        for i,k in enumerate(key):
            key_map[ord(k)-ord('0')]=i

        row_text = plaintext
        text = []
        seg_num = int (len(row_text)/len(key))+1
        for i in range(len(key)):
            text.append("")

        for i,c in enumerate(row_text):
            text[i % len(key)] += c.upper()
        # Encryption
        Encrypttext=''
        for _key in key_map.keys():
            Encrypttext+=text[key_map.get(_key)]
        return Encrypttext.upper()

class rail_fence_cipher(object):
    def __init__(self,key,plaintext):
        self.key=''
        self.plaintext=''

    def rail_fence_encrypt(self):
        Encrypttext=''
        matrix=[["" for x in range(len(plaintext))] for y in range(key)]
        increment = 1
        x = 0
        y = 0
        for ch in plaintext:
            if x + increment < 0 or x + increment >= len(matrix):
                increment = increment*-1

            matrix[x][y]=ch

            x += increment
            y += 1

        for list in matrix:
            Encrypttext += "".join(list)

        return Encrypttext.upper()

# main block
cml = sys.argv[1]
key = sys.argv[2]
plaintext = sys.argv[3]

# it's work
if(cml=='caesar'):
    key=int(key)
    cipher=caeser_cipher(key,plaintext)
    print(cipher.caeser_cipher_encrypt())

# it's work
elif(cml=='playfair'):
    
    fill_matrix(key)
    print(playfair_cipher_encrypt(key_table,plaintext))

# it's work
elif(cml=='vernam'):
    key=str(key)
    cipher=vernam_cipher(key,plaintext)
    print(cipher.vernam_encrypt(key,plaintext))

# it's work
elif(cml=='row'):

    key=str(key)
    cipher=row_cipher(key,plaintext)
    print(cipher.row_encrypt())

# it's work
elif(cml=='rail_fence'):

    key=int(key)
    cipher=rail_fence_cipher(key,plaintext)
    print(cipher.rail_fence_encrypt())

else:
    print('please enter the ture method,such as caesar,playfair,vernam,row,rail_fence.')