#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-

import urllib.request 
import urllib.parse 
import sys

TARGET = 'http://crypto-class.appspot.com/po?er='
#--------------------------------------------------------------
# padding oracle
#--------------------------------------------------------------
class PaddingOracle(object):
    def query(self, q):
        target = TARGET + urllib.parse.quote(q)    # Create query URL
        req = urllib.request.Request(target)         # Send HTTP request to server
        try:
            f = urllib.request.urlopen(req)          # Wait for response
            f.close()
            print("200")
            return True
        except urllib.request.HTTPError as e:          
#            print("We got: {code:d}".format(code=e.code))       # Print response code
            if e.code == 404:
                return True # good padding
            return False # bad padding




if __name__ == "__main__":
    originalQuery="f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4"
    couples=[ [originalQuery[l:l+32],originalQuery[l+32:l+64]] for l in range(0,len(originalQuery)-32,32) ]

    po = PaddingOracle()
    totalRes = ""
    for couple in couples:
        helperBlock = couple[0]
        blockToDecrypt = couple[1]
        appGuessed = ""
        appGuessed_hex = ""
        myByte=1
        byteToFoundDict={} #dict used to take reference to the guessed char for previous bytes
        while (myByte < 17):
            pad=(hex(myByte)[2:].zfill(2)) * myByte  #01 or 0202 or 030303 and so on
            if (myByte in  byteToFoundDict.keys()): 
                guess=byteToFoundDict[myByte]+1
            else:
                guess=0

            found = False
            while (guess < 256):
                h_guess_single=(hex(guess)[2:].zfill(2))
                h_guess = h_guess_single+appGuessed_hex
                ''' xor the left block with the pad and the guess '''
                helperModified = (hex( int(helperBlock,16) ^ int(pad,16)  ^  int(h_guess,16))[2:]).zfill(32)
                             
                print("myByte={byte_guessing:d},guess={my_guess:d}".format(byte_guessing=myByte, my_guess=guess))
                resCall = po.query(helperModified+blockToDecrypt)
                if (resCall):
                    print("found " + chr(int(h_guess_single,16)))
                    appGuessed_hex = h_guess_single + appGuessed_hex
                    if (int(h_guess_single,16)>31):
                        appGuessed = chr(int(h_guess_single,16)) + appGuessed
                        print(appGuessed)
                    found = True
                    byteToFoundDict[myByte] = guess
                    break #found the correct guess for the current byte, so  exit from the inner for cycle
                guess = guess + 1
            if (found):
                myByte = myByte + 1
            else:
                print("backtrack")
                myByte = myByte -1
                appGuessed_hex=appGuessed_hex[2:]
                appGuessed=appGuessed[1:]

        totalRes = totalRes + appGuessed
        print(totalRes)

