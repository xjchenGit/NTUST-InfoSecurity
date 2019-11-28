#!/usr/local/bin/python3.7
#coding=utf-8
from Crypto.Cipher import AES
#from Crypto import Random
from PIL import Image
import binascii


def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)


def xor(x,y):
    ans=""
    for i in range(0,128):
        if ((x[i] == '0' and y[i] == '1') or (x[i] == '1' and y[i] == '0')):
            ans += "1" 
        else: 
            ans += "0" 
    ##print(ans)
    return ans
    #return format(int(x, 16) ^ int(y, 16), '032x')

def byte_to_bit(s):
    ans = ""
    #print("leng:",len(s))
    for i in range(0,len(s)):
        ##print(s[i])
        ss = bin(s[i]).replace('0b', '')
        sss = ss.zfill(8)
        ans += sss
    return ans

def bit_to_byte(s):
    ans = b""
   # #print(len(s))
    for i in range(0,len(s),8):
        ss = s[i:i+8]
        sss = int(ss,2)
        #print("sss:",sss)
        ssss = str(hex(sss)).replace('0x', '')
        if len(ssss)<2:
            ssss="0"+ssss
        #print("ssss:",ssss)
        sssss =bytes.fromhex(ssss)
        #print("sssss:",sssss)
        ans+=sssss
    ##print(ans)
    return ans

def shift_key(t,k):
    ans = b""
    kk = ''
    global shift_k
    for i in range(0,len(k),8):
        k1 = k[i:i+8]
        for j in range(0,8):
            kk1 = (t+shift_k)%8
            kk += k1[kk1]
        k2 = int(kk,2)
        k3 = str(hex(k2)).replace('0x', '')
        if len(k3)<2:
            k3="0"+k3
        k4 =bytes.fromhex(k3)
        ans+=k4
    return ans


# encryt with CBC
def encry_to_cbc():
    global key
    global iv
    THIS_MODE = AES.MODE_ECB
    out_cbc = b""
    encrypt_data_cbc = b""
    print("padded:",len(padded_data))
    for i in range(0,len(padded_data),16):
        plaintext = padded_data[i:i+16]
        #print(plaintext)
        if i == 0:
            iv_bit = byte_to_bit(iv)
            in_bit= byte_to_bit(plaintext)
            #print(iv_bit,"\t",in_bit)
            after_xor = xor(iv_bit, in_bit)
        else:
            iv_bit = byte_to_bit(out_cbc)
            in_bit= byte_to_bit(plaintext)
            after_xor = xor(iv_bit, in_bit)
        m = bit_to_byte(after_xor)
        #print("after_xro:",after_xor)
        ecb_cipher = AES.new(key, THIS_MODE)
        out_cbc = ecb_cipher.encrypt(m)
        #print("out_cbc:",out_cbc)
        #print(byte_to_bit(out_cbc))
        encrypt_data_cbc+=out_cbc

    print("encry:",len(encrypt_data_cbc))
    #save file after adding ppm_header P6}\n {width} {height} \n{color} \n
    output_file = open("./CBC_image.ppm", "wb")
    output_file.write(b"\n".join([style, size, color, encrypt_data_cbc]))
    output_file.close()
    im = Image.open('./CBC_image.ppm')
    im.save('./CBC_image.jpg')
    im.show()
 
 # encryt with ECB
def encrypt_to_ecb():
    global key
    encrypt_data_ecb = b""
    THIS_MODE = AES.MODE_ECB
    for i in range(0,len(padded_data),16):
        plaintext = padded_data[i:i+16]
        ##print(plaintext)
        ecb_cipher = AES.new(key, THIS_MODE)
        encrypt_data_ecb+=ecb_cipher.encrypt(plaintext)

    # save file after adding ppm_header P6}\n {width} {height} \n{color} \n
    output_file = open("./ECB_image.ppm", "wb")
    output_file.write(b"\n".join([style, size, color, encrypt_data_ecb]))
    output_file.close()
    im = Image.open('./ECB_image.ppm')
    im.save('./ECB_image.jpg')
    im.show()


# Mode 3
def encry_to_dbu():
    global key
    global iv
    THIS_MODE = AES.MODE_ECB
    out_dbu = b""
    encrypt_data_dbu = b""
    for i in range(0,len(padded_data),16):
        plaintext = padded_data[i:i+16]
        #print(plaintext)
        the_key = shift_key(i,byte_to_bit(key))
        if i == 0:
            dbu_cipher = AES.new(iv, THIS_MODE)
            out_dbu = dbu_cipher.encrypt(plaintext)
        else:
            dbu_cipher = AES.new(out_dbu, THIS_MODE)
            out_dbu = dbu_cipher.encrypt(plaintext)
        iv_bit = byte_to_bit(the_key)
        m_bit = byte_to_bit(out_dbu)
        after_xor = xor(iv_bit,m_bit)
        encrypt_data_dbu += bit_to_byte(after_xor)

    #save file after adding ppm_header P6}\n {width} {height} \n{color} \n
    output_file = open("./DBU_image.ppm", "wb")
    output_file.write(b"\n".join([style, size, color, encrypt_data_dbu]))
    output_file.close()
    im = Image.open('./DBU_image.ppm')
    im.save('./DBU_image.jpg')
    im.show()

# get key&iv
key = 'this is keykeyke'.encode('ASCII')
iv = 'This is an IV123'.encode('ASCII')

# get image
im = Image.open('./A.png')
im.save('./PPM_A.ppm')
input_file = open("./PPM_A.ppm", 'rb')
input_data = input_file.read()
input_file.close()
print("inputex    ",len(input_data))
# get ppm header: {P6}\n {width} {height} \n{color} \n
splits = input_data.split(b"\n", 3)
data_for_encryption = splits[3]
style = splits[0]
size = splits[1]
color = splits[2]
padded_data = pad(data_for_encryption)

# mode3: get shift number
key0 = xor(byte_to_bit(key),byte_to_bit(iv))
shift_k0 = ""
for i in range(0,128,16):
    shift_k0 += key0[i]

shift_k = int(shift_k0,2)%8

# main
a = ""
while a != "4":
    # get input
    a = input("please input a number: \n1.ECB MODE \t2.CBC MODE \t3.MODE DESIGNED BY US \t4.EXIT\n")
    print(a)
    if a == "1":
        encrypt_to_ecb()
    elif a=="2":
        encry_to_cbc()
    elif a=="3":
        encry_to_dbu()
    elif a=="4":
        print("exit!")
    else:
        print("please input the number with the legal form！")



