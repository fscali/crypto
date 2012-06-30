#!/usr/bin/env python3
# -*- coding: iso-8859-15 -*-
import re;
import sys;
ciphertext1="315c4eeaa8b5f8aaf9174145bf43e1784b8fa00dc71d885a804e5ee9fa40b16349c146fb778cdf2d3aff021dfff5b403b510d0d0455468aeb98622b137dae857553ccd8883a7bc37520e06e515d22c954eba5025b8cc57ee59418ce7dc6bc41556bdb36bbca3e8774301fbcaa3b83b220809560987815f65286764703de0f3d524400a19b159610b11ef3e";

ciphertext2="234c02ecbbfbafa3ed18510abd11fa724fcda2018a1a8342cf064bbde548b12b07df44ba7191d9606ef4081ffde5ad46a5069d9f7f543bedb9c861bf29c7e205132eda9382b0bc2c5c4b45f919cf3a9f1cb74151f6d551f4480c82b2cb24cc5b028aa76eb7b4ab24171ab3cdadb8356f";

ciphertext3="32510ba9a7b2bba9b8005d43a304b5714cc0bb0c8a34884dd91304b8ad40b62b07df44ba6e9d8a2368e51d04e0e7b207b70b9b8261112bacb6c866a232dfe257527dc29398f5f3251a0d47e503c66e935de81230b59b7afb5f41afa8d661cb";

ciphertext4="32510ba9aab2a8a4fd06414fb517b5605cc0aa0dc91a8908c2064ba8ad5ea06a029056f47a8ad3306ef5021eafe1ac01a81197847a5c68a1b78769a37bc8f4575432c198ccb4ef63590256e305cd3a9544ee4160ead45aef520489e7da7d835402bca670bda8eb775200b8dabbba246b130f040d8ec6447e2c767f3d30ed81ea2e4c1404e1315a1010e7229be6636aaa";

ciphertext5="3f561ba9adb4b6ebec54424ba317b564418fac0dd35f8c08d31a1fe9e24fe56808c213f17c81d9607cee021dafe1e001b21ade877a5e68bea88d61b93ac5ee0d562e8e9582f5ef375f0a4ae20ed86e935de81230b59b73fb4302cd95d770c65b40aaa065f2a5e33a5a0bb5dcaba43722130f042f8ec85b7c2070";

ciphertext6="32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd2061bbde24eb76a19d84aba34d8de287be84d07e7e9a30ee714979c7e1123a8bd9822a33ecaf512472e8e8f8db3f9635c1949e640c621854eba0d79eccf52ff111284b4cc61d11902aebc66f2b2e436434eacc0aba938220b084800c2ca4e693522643573b2c4ce35050b0cf774201f0fe52ac9f26d71b6cf61a711cc229f77ace7aa88a2f19983122b11be87a59c355d25f8e4";

ciphertext7="32510bfbacfbb9befd54415da243e1695ecabd58c519cd4bd90f1fa6ea5ba47b01c909ba7696cf606ef40c04afe1ac0aa8148dd066592ded9f8774b529c7ea125d298e8883f5e9305f4b44f915cb2bd05af51373fd9b4af511039fa2d96f83414aaaf261bda2e97b170fb5cce2a53e675c154c0d9681596934777e2275b381ce2e40582afe67650b13e72287ff2270abcf73bb028932836fbdecfecee0a3b894473c1bbeb6b4913a536ce4f9b13f1efff71ea313c8661dd9a4ce";

ciphertext8="315c4eeaa8b5f8bffd11155ea506b56041c6a00c8a08854dd21a4bbde54ce56801d943ba708b8a3574f40c00fff9e00fa1439fd0654327a3bfc860b92f89ee04132ecb9298f5fd2d5e4b45e40ecc3b9d59e9417df7c95bba410e9aa2ca24c5474da2f276baa3ac325918b2daada43d6712150441c2e04f6565517f317da9d3";

ciphertext9="271946f9bbb2aeadec111841a81abc300ecaa01bd8069d5cc91005e9fe4aad6e04d513e96d99de2569bc5e50eeeca709b50a8a987f4264edb6896fb537d0a716132ddc938fb0f836480e06ed0fcd6e9759f40462f9cf57f4564186a2c1778f1543efa270bda5e933421cbe88a4a52222190f471e9bd15f652b653b7071aec59a2705081ffe72651d08f822c9ed6d76e48b63ab15d0208573a7eef027";

ciphertext10="466d06ece998b7a2fb1d464fed2ced7641ddaa3cc31c9941cf110abbf409ed39598005b3399ccfafb61d0315fca0a314be138a9f32503bedac8067f03adbf3575c3b8edc9ba7f537530541ab0f9f3cd04ff50d66f1d559ba520e89a2cb2a83";

targetCipherText="32510ba9babebbbefd001547a810e67149caee11d945cd7fc81a05e9f85aac650e9052ba6a8cd8257bf14d13e6f0a803b54fde9e77472dbff89d71b57bddef121336cb85ccb8f3315f4b52e301d16e9f52f904";


def strxor(a, b):     # xor two strings of different lengths
    if len(a) > len(b):
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a[:len(b)], b)])
    else:
        return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b[:len(a)])])

myList=[ciphertext1,
        ciphertext2,ciphertext3,ciphertext4,ciphertext5,ciphertext6,ciphertext7,ciphertext8,ciphertext9,ciphertext10,targetCipherText];

'''the targetCipherText is the shortest, so we can trim the other cipher texts
to its same length (that is 83)'''

myList=list(map(lambda x: x[:len(targetCipherText)], myList));

guesses=[];
''' Here I treat each of the 11 cipher texts as the master, that is the one to
xor with all the others'''
for c in range(0,len(myList)):
    myXorList=[];
    splitted_c=[myList[c][l:l+2] for l in range(0,len(myList[c]),2)];

    for i in range(0,len(myList)):
        if (i != c): #do not xor the cipher text with itself
            splitted_i=[myList[i][l:l+2] for l in range(0,len(myList[i]),2)];
            aux ="".join([chr(int(x,16) ^ int(y,16)) for (x,y) in zip(splitted_i, splitted_c)]);
            myXorList.append(aux);


        '''Now I have to find some interesting pattern. I know that when a
        space is xored with an alphabetic character, I receive the same
        character with inverted case; I try to use this property to retrieve
        as much text as I can'''
        xorDict={};
        for i in range(0,len(myXorList)): #for each xored text
            aux=re.sub('[^\w ]',"#",myXorList[i]);
            stringWithSpaces=re.sub('\w',' ', aux);
            stringWithChars=re.sub('[^\w]',"#",myXorList[i]);
            xorDict[i]=[stringWithSpaces, stringWithChars]; 
            '''build two helper strings: one that is useful to find spaces and
            the other to find alphabetic characters'''

        guess="";
        for j in range(0,83): #loop for each character
            counter={};
            for i in range(0,len(myXorList)):
                '''consider spaces first and see if it's reasonable that in
                this position there is a space'''
                ch=xorDict[i][0][j]; 
                

                if(counter.__contains__(ch)):
                    counter[ch]=counter[ch]+1;
                else:
                    counter[ch]=1;
            if (counter.__contains__(' ') and counter.__contains__('#')):
                if (counter[' '] > counter['#']):
                    guess+=" "; #I guess a space
                else:
                    '''otherwise look for alphabetic characters'''
                    counter = {};
                    for i in range(0,len(myXorList)):
                        ch=xorDict[i][1][j];
                        if (counter.__contains__(ch)):
                            counter[ch]=counter[ch]+1;
                        else:
                            counter[ch]=1;
                    maxOccurrences=0;
                    chosenChar="#";
                    for k,v in counter.items():
                        if (re.match('[A-Za-z]',k) and v > maxOccurrences):
                            maxOccurrences= v;
                            chosenChar=k;
                    guess+=chosenChar;
            else:
                guess+="#";

    '''swapcase because I get inverted char case'''
    guesses.append(guess.swapcase());

'''now I try to recover the original key, building some guesses from the
various samples'''
keyguesses=[];
for i in range(0,len(guesses)):
    keyguess = "";
    for j in range(0,83):
        ordP=ord(guesses[i][j]);
        ordC=int(myList[i][2*j:2*(j+1)],16);
        keyguess+=str(hex(ordP ^ ordC)[2:]).zfill(2);
    keyguesses.append(keyguess);

'''then I try to interpolate the key as best as possible, taking for each
character the couplet that is most common among all the guessed keys'''
builtKey='';
for i in range(0,83):
    dictCouplets={};
    for kg in keyguesses:
        couple=kg[2*i:2*(i+1)];
        if (dictCouplets.__contains__(couple)):
            dictCouplets[couple]=dictCouplets[couple]+1;
        else:
            dictCouplets[couple]=1;
    maxOccurrences=0;
    chosenCouple="00";
    for k,v in dictCouplets.items():
        if (v > maxOccurrences):
            maxOccurrences=v;
            chosenCouple=k;
    builtKey+=chosenCouple;

print(builtKey); #interpolated key

for i in range(0,len(myList)):

    myguess='';
    for j in range(0,83):
        ordKG=int(builtKey[2*j:2*(j+1)],16);
        ordC=int(myList[i][2*j:2*(j+1)],16);
        myguess+=chr(ordKG ^ ordC);
    print(myguess);

'''
The last print is our target cipher text; the output is:

The secuet message is: Whtn using aa~tream cipher, never use the key more
than once


so there is some error but it's easy to recover and finally we have the
solution:


The secret message is: When using a stream cipher, never use the key more than
once

'''








