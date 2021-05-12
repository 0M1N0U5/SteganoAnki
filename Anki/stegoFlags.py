from numpy import *
import random
import utils

MAX_CAPACITY = 1 #hex values

def calculateRandomCombination(number):
    possibleCombinations=[]
    #This limitation is necessary so that each digit has two digits that adds it up
    size = 0
    for i in range(1, 10, 1):
        for l in range(1, 10, 1):
            if (i+l)%16==number:
                #print(str(i)+str(l), "->", (i+l)%16)
                possibleCombinations.append(str(i)+str(l))
                size += 1
    if size==1:
        cont=0
    else:
        cont=random.randint(0, size-1)
    #We choose a combination in random way
    return possibleCombinations[cont]

#Main function to encode the secret in a flag
def encode(flag, data, password):
    #If there is something strange about the flag
    if flag > 10:
        return False

    #Time to hide secret! - We generate a random valid combination
    solutionArray=[]
    for x in data:
        solutionArray += utils.splitIntoChars(calculateRandomCombination(int(x,16)))

    #We modify the order according to its password in a pseudorandom way
    utils.randomArray(solutionArray,password)

    #Now we add the padding, so it is equal to the color given (the cover). It will have two digits.
    paddingNumber = random.randint(10, 92)
    secretFinal = int(''.join(solutionArray)+str(paddingNumber))
    #We check for the correct module for anki
    while secretFinal % 8 != flag:
        secretFinal += 1

    return secretFinal

#Main function to decode the flag and discover its secret
def decode(flagHidden,password):
    #If there is something strange about the flag
    if flagHidden < 10 or len(str(flagHidden)) % 2 != 0 :
        return False

    #We take out the padding (two last digits out)
    secretComputed=str(flagHidden//100)
    
    #Conversion of string in a list
    listSecret= utils.splitIntoChars(secretComputed)

    #Now we do the random disorder again
    realSecretArray=utils.inverseRandomArray(listSecret,password)
    
    #We have to add up its two digits in lineal order
    secretHex=""
    for index, i in enumerate(realSecretArray):
        if index % 2 == 1:
           value = (int(i)+int(realSecretArray[index-1])) % 16
           secretHex += f'{value:0>1x}'

    return secretHex

def estimate():
    global MAX_CAPACITY
    return MAX_CAPACITY


#for i in range(16):
#    calculateRandomCombination(i)    