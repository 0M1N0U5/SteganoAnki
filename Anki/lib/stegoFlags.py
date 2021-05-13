import lib.utils as utils

def encodeFlag(x,flag):
    x = utils.intToBin(int(x,16))
    y = utils.binToInt(x)
    y += 1
    return y*8+flag

def decodeFlag(num):
    resultado = num//8
    return f'{resultado-1:0>1X}'

def encode(flags, data, password):
    if(len(flags) != len(data)):
        print("Error stegoFlags, la longitud del data no coincide con la cantidad de flags")
        return False
    else:
        data = utils.splitIntoChars(data)
        data = utils.randomArray(data, password)
        print(data)
        newFlags = []
        for index, d in enumerate(data):
            newFlags.append(encodeFlag(d, flags[index]))

        return newFlags

def decode(flags, password):
    data = []
    for f in flags:
        if f >= 8:
            data.append(decodeFlag(f))
    else:
        data = utils.inverseRandomArray(data, password)
        return ''.join(data).lower()

def estimate():
    return 1

def example():
    data = "abcd0123"
    flags = [0,1,2,3,0,1,2,3]
    passsword = "password123"
    newFlags = encode(flags, data, passsword)
    moduleFlags = [n % 8 for n in newFlags]
    print(newFlags)
    print(moduleFlags)
    # moduleFlags == flags
    newData = decode(newFlags, passsword)
    print(newData)