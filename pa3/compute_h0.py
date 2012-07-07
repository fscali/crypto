#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-
import argparse
from Crypto.Hash import SHA256
import binascii

parser=argparse.ArgumentParser(description="Compute hash function h0 for the first 1024 bytes of a binary file");
parser.add_argument('file-to-process',  help='binary file to process');
args=parser.parse_args();
in_file=open(vars(args)['file-to-process'],'rb');
data=in_file.read();
my_array=[data[l:min(len(data),l+1024)] for l in range(0,len(data),1024)];
pad=b'';
for i in range(0,len(my_array)):
    my_block=my_array[-i-1]+pad; #concatenation of the current block plus the  sha from the previous  (following) block
    h=SHA256.new();
    h.update(my_block);
    pad=bytes.fromhex(h.hexdigest());

print(binascii.hexlify(pad));



