from numpy import *
import random
import lib.utils as utils
from lib.ankiwrapper import AnkiWrapper

def binToInt(x):
    return int(x,2)  

def main():
    aw = AnkiWrapper()
    flags = aw.getFlagsDeck("Gonzalo")
    print(flags)
    print()
    print(type(flags))

    

def encode(x,flag):
    x = utils.intToBin(int(x,16))
    y = utils.binToInt(x)
    y += 1
    return y*8+flag

def decode(num):
    resultado = num//8
    return f'{resultado-1:0>1X}'


def Mirar():
    for i in range(0,33):
        print(i)

def Prueba():
    h = '0123456789ABCDEF'
    for flag in range(0,5):
        for i in h:
            e = encode(i, flag)
            d = decode(e)
            if i != d or i=='F':
                print("e,d,i",e,d,i)

Prueba()