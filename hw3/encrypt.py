#!/usr/local/bin/python3.7
#coding=utf-8
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import struct
############# ECB CBC ##############

MODE=AES.MODE_ECB
def ECB_encrypt(img_data,key,mode=MODE):
    """ Args: imag_data(bytes)，key(bytes) """
    cipher=[]
    padded_data = padding(img_data)
    for i in range(0,len(padded_data),16):
        block=padded_data[i:i+16]
        ecb_cipher = AES.new(key,mode)
        encrypt_data = ecb_cipher.encrypt(block)
        cipher.extend(encrypt_data)
    return cipher

def CBC_encrypt(img_data,key,init_iv,mode=MODE):
    """ Args: imag_data(bytes)，key(bytes), iv(bytes) """
    cipher=[]
    padded_data = padding(img_data)
    cipher_iv = b''+init_iv
    for i in range(0,len(padded_data),16):
        block=padded_data[i:i+16]
        
        #iv
        bin_iv = byte_to_bit(cipher_iv[i:i+16])
        bin_block = byte_to_bit(block)
        
        # xor
        xor_encoder = bit_to_byte(xor(bin_iv,bin_block,128))
        
        #cipher
        ecb_cipher = AES.new(key,mode)
        encrypt_data = ecb_cipher.encrypt(xor_encoder)
        #print(len(encrypt_data))
        cipher_iv+=encrypt_data
        cipher.extend(encrypt_data)
    return cipher

def CBC_encrypt(img_data,key,init_iv,mode=MODE):
    """ Args: imag_data(bytes)，key(bytes), iv(bytes) """
    cipher=[]
    padded_data = padding(img_data)
    cipher_iv = b''+init_iv
    for i in range(0,len(padded_data),16):
        block=padded_data[i:i+16]
        
        #iv
        bin_iv = byte_to_bit(cipher_iv[i:i+16])
        bin_block = byte_to_bit(block)
        
        # xor
        xor_encoder = bit_to_byte(xor(bin_iv,bin_block,128))
        
        #cipher
        ecb_cipher = AES.new(key,mode)
        encrypt_data = ecb_cipher.encrypt(xor_encoder)
        #print(len(encrypt_data))
        cipher_iv+=encrypt_data
        cipher.extend(encrypt_data)
    return cipher

def process_image(filename,key,method):
         # Opens image and converts it to RGB format for PIL
     img = Image.open(filename)
     img_data = img.tobytes()
     iv = get_random_bytes(16)

     filename_out = "img_encrypted"
     img_format = "ppm"
    # save orignal length of image data
     original_length = len(img_data)
     if method =="ECB":
        new_img_data = convert_to_RGB(ECB_encrypt(img_data,key)[:original_length])
     elif method =="CBC":
        new_img_data = convert_to_RGB(CBC_encrypt(img_data,key,iv)[:original_length])
    # save encrypt image

     new_img = Image.new(img.mode, img.size)
     new_img.putdata(new_img_data)
     new_img.save(filename_out+"."+img_format, img_format)
     new_img.show()

############ Utility function ###############
def string_to_byte(s):
    return s.encode('ASCII')

def xor(x,y,length_of_xor,is_bin=False):
    result = ""
    for i in range(0,length_of_xor):
        if ((x[i] == '0' and y[i] == '1') or (x[i] == '1' and y[i] == '0')):
            result += "1"
        else:
            result += "0"
    if is_bin:
        result=result[2:]
    return result

def byte_to_bit(s):
    result = ""
    for i in range(0,len(s)):
        b_bytes = bin(s[i])[2:-1]
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

def convert_to_RGB(img_data):
    """
    Args:
        img_data:input data must be bytes.
    """
    r, g, b = tuple(map(lambda d: [img_data[i] for i in range(0,len(img_data)) if i % 3 == d], [0,1,2]))
    pixels = tuple(zip(r,g,b))
    return pixels

def convert_to_ppm(filename,form):
    length_of_form=len(form)
    ppmPicture = "mypppm"+filename[:-length_of_form-1]+".ppm"
    im = Image.open(filename)
    im.save(ppmPicture)

def test():
    # # xor test
    # print('################ xor ####################')
    # x=bin(20)
    # y=bin(24)
    # #print(x,y)
    # print(xor(x,y,5,is_bin=True))

    # #byte_to_bit
    # print('################ byte to bit ####################')
    # s='adsasadasdsasd'.encode('ASCII')
    # print(s)
    # print(bytes_to_bit(s))

    # print('################ bit to byte ####################')
    # test_bin=bin(300222555222000000020000)
    # print(test_bin)
    # print(bit_to_byte(test_bin))

    # print('################ padding and unpadding ####################')
    # img_test=b'\x12'
    # a=padding(img_test)
    # print(a)
    # print(unpadding(a))
    # print('################ ECB ####################')
    # key= "0123456789abcdef"
    # bytes_key = string_to_byte(key)
    # img_data=b"\x10\x20\x30\x40\x50\x60\x70\x80\x10\x20\x30\x40\x50\x60\x70\x80"
    # print(img_data)
    # encrypt_data=ECB_encrypt(img_data,bytes_key)
    # print(encrypt_data)
    # print('################ convert ECB ####################')
    # filename='A.png'
    # convert_to_ppm(filename,'png')
    #filename="asadaads.png"

    filename = "./mypppmA.ppm"
    key = get_random_bytes(16)
    METHOD = "CBC"
    process_image(filename,key,METHOD)

############ Main ###############
test()

