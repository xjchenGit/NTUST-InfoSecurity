#!/usr/local/bin/python3.7
#coding=utf-8
import sys,io
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
MODE=AES.MODE_ECB

############# ECB CBC DIY##############

def ECB_encrypt(img_data,key,mode=MODE):
    """ Args: imag_data(bytes)，key(bytes) """
    encrypt_data=b""
    for i in range(0,len(img_data),16):
        block=img_data[i:i+16]
        ecb_cipher = AES.new(key,mode)
        encrypt_data += ecb_cipher.encrypt(block)
    return encrypt_data

def CBC_encrypt(img_data,key,init_iv,mode=MODE):
    """ Args: imag_data(bytes)，key(bytes), iv(bytes) """
    cipher = b""
    encrypt_data = b""
    for i in range(0,len(img_data),16):
        #iv & xor
        if i == 0:
            iv_bit = byte_to_bit(init_iv)
        else:
            iv_bit = byte_to_bit(cipher)
        in_bit= byte_to_bit(img_data[i:i+16])
        xor_coder = bit_to_byte(xor(iv_bit, in_bit, 128))

        # encrypt
        ecb_cipher = AES.new(key, mode)
        cipher = ecb_cipher.encrypt(xor_coder)
        encrypt_data+=cipher
    return encrypt_data

def DIY_encrypt(img_data,key,init_iv,mode=MODE):
    """ Args: imag_data(bytes)，key(bytes), iv(bytes) """
    cipher = b''
    encrypt_data = b''
    xor_next_encoder=b''
    for i in range(0,len(img_data),16):
        #iv & xor
        if i == 0:
            iv_bit = byte_to_bit(init_iv)
        else:
            iv_bit = byte_to_bit(xor_next_encoder)
        in_bit= byte_to_bit(img_data[i:i+16])
        xor_coder = bit_to_byte(xor(iv_bit, in_bit, 128))
        # encrypt
        ecb_cipher = AES.new(key, mode)
        cipher = ecb_cipher.encrypt(xor_coder)

        #next_iv
        bin_xor_encoder = byte_to_bit(xor_coder)
        bin_encrypt_data = byte_to_bit(cipher)
        xor_next_encoder = bit_to_byte(xor(bin_xor_encoder, bin_encrypt_data, 128))

        # add encryption to list
        encrypt_data+=cipher
    return encrypt_data

def process_image(filename,key,iv,method):
    # image processing
    filename_out = "_cipher_"
    img_format = "ppm"
    im = Image.open(filename)
    input_file=open(filename,'rb')
    input_data=input_file.read()
    input_file.close()

    # get ppm header: {P6}\n {width} {height} \n{color} \n
    splits = input_data.split(b"\n", 3)
    data_for_encryption = splits[3]
    style = splits[0]
    size = splits[1]
    color = splits[2]
    padded_data = padding(data_for_encryption)

    original_length = len(input_data)
    if method =="ECB":
         new_img_data = ECB_encrypt(padded_data,key)
         print("output:",len(new_img_data))
    elif method =="CBC":
         new_img_data = CBC_encrypt(padded_data,key,iv)
    elif method =="DIY":
         new_img_data = DIY_encrypt(padded_data,key,iv)
         print("output:",len(new_img_data))

    output_file = open('./'+method+filename_out+filename[2:-4]+"."+img_format, "wb")
    output_file.write(b"\n".join([style, size, color, new_img_data]))
    output_file.close()
    im = Image.open('./'+method+filename_out+filename[2:-4]+"."+img_format)
    im.show()

############ Utility function ##############
def string_to_byte(s):
    return s.encode('ASCII')

def xor(x,y,length_of_xor):
    result = ""
    for i in range(0,length_of_xor):
        if ((x[i] == '0' and y[i] == '1') or (x[i] == '1' and y[i] == '0')):
            result += "1"
        else:
            result += "0"
    return result

def byte_to_bit(s):
    result = ""
    for i in range(0,len(s)):
        b_bytes = bin(s[i]).replace('0b','')
        b_bytes = b_bytes.zfill(8)
        result += b_bytes
    return result

def bit_to_byte(b):
    result = b""
    for i in range(0,len(b),8):
        temp_b = b[i:i+8]
        int_b = int(temp_b,2)
        str_b = str(hex(int_b)).replace('0x', '')
        if len(str_b)<2:
            str_b="0"+str_b
        result+=bytes.fromhex(str_b)
    return result

def padding(img_data):
    """ Args: img_data: input data must be bytes."""
    return img_data + b'\x00'*(AES.block_size-len(img_data)%AES.block_size)

def unpadding(img_data):
    """ Args: img_data: input data must be bytes."""
    number_of_padding=(AES.block_size-len(img_data)%AES.block_size)
    return img_data[:-number_of_padding+1]

def convert_to_ppm(filename):
    length_of_form=len(filename.split('.')[1])
    ppmPicture = "PPM_"+filename[:-length_of_form-1]+".ppm"
    im = Image.open(filename)
    im.save(ppmPicture)
    return ppmPicture

############ Main ###############

def main():
    try:
        # argvs
        method = sys.argv[1]
        pic = sys.argv[2]
        str_key = sys.argv[3]
        str_iv = sys.argv[4]

        # pre-processing
        key = string_to_byte(str_key)
        iv = string_to_byte(str_iv)
        pic=convert_to_ppm(pic)
        filename = "./"+pic
    except BaseException:
        print("Command error!\n\n")
        print("Please enter the command in the following format:\
            \n'./encrypt.py command_number Picture_name key iv',\
            \n'./encrypt.py 0 xxxx.png 0123456789abcdef 0123456789abcdef'\n\
            \nCommand Number:\
            \n0:ECB mode\n1:CBC mode\n2:DIY mode")
    else:
        if (method=="0"):
            METHOD = "ECB"
        elif (method=="1"):
            METHOD = "CBC"
        elif (method=="2"):
            METHOD = "DIY"
        process_image(filename,key,iv,METHOD)

if __name__=="__main__":
    main()