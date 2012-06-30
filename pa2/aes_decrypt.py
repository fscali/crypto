#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-
from Crypto.Cipher import AES;
import sys;
import re;
import math;

key_cbc="140b41b22a29beb4061bda66b6747e14";
key_ctr="36f18357be4dbd77f050515c73fcf9f2";

#note: both ciphertexts are 64 bytes length (in fact both are 128 characters long and 2 characters form a byte)
ciphertext_cbc1="4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81";
ciphertext_cbc2="5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253";

#these have variable length
ciphertext_ctr1="69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329";
ciphertext_ctr2="770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451";

cbc_array=[ciphertext_cbc1, ciphertext_cbc2];
ctr_array=[ciphertext_ctr1, ciphertext_ctr2];


def decrypt_cbc(ciphertext):
    ciphertext_array=[ciphertext[l:l+32] for l in range(0,len(ciphertext),32)];
    cipher=AES.new(key_cbc.decode('hex'), AES.MODE_ECB); #the key is expected as byte string
    aux = "";
    for i in range(0,int(len(ciphertext)/32)-1): #for each block
        left_operand  = ciphertext_array[i]; #the first time here there is iv        
        right_operand = ciphertext_array[i+1];
        block = decrypt_cbc_block(cipher, left_operand, right_operand);
        aux += block;

    # we have to remove "padding" number of bytes as specified by cbc mode
    padding = int(aux[-2:],16); #the padding is indicated in the last byte 
    decrypted_hex = aux[0:-(2*padding)]; #drop the indicated number of bytes

    print("".join([chr(int(decrypted_hex[l:l+2],16)) for l in range(0,len(decrypted_hex),2) ]) );


def decrypt_cbc_block(cipher,left_operand, right_operand):
    right_string="".join( [chr(int(right_operand[l:l+2],16)) for l in range(0,len(right_operand),2)]);
    right_decrypted =  cipher.decrypt(right_string).encode('hex');
    block_decrypted = int(left_operand,16) ^ int(right_decrypted,16);
    return re.sub('L','',hex(block_decrypted)[2:]);

cbc_decrypted=[decrypt_cbc(x) for x in cbc_array];


def decrypt_ctr(ciphertext):
    iv=ciphertext[:32];
    cipher=AES.new(key_ctr.decode('hex'),AES.MODE_ECB);
    top=int(math.ceil(len(ciphertext)/32));
    aux = "";
    for i in range(0,top):
        iv_string="".join( [chr(int(iv[l:l+2], 16)) for l in range(0,len(iv),2)]);
        iv_encrypted=cipher.encrypt(iv_string).encode('hex');
        block_size=min(32,len(ciphertext[(i+1)*32:])); #no padding, gotta verify how many bytes have remained 
        iv_encrypted_substr=iv_encrypted[0:block_size]; 
        mi_int=re.sub('L', '',hex(int(iv_encrypted_substr,16) ^  int(ciphertext[(i+1)*32:(i+1)*32+block_size],16))[2:]);
        aux += "".join([chr(int(mi_int[l:l+2],16)) for l in range(0,len(mi_int),2)]);
        iv_int=int(iv,16);
        iv_int=iv_int+1;
        iv=re.sub('L','',hex(iv_int)[2:]);
    print(aux);
        
ctr_decrypted=[decrypt_ctr(x) for x in ctr_array];


