from numpy import *
import utils

MAX_CAPACITY = 3 #hex values

def calculateRandomCombination(number):
    possibleCombinations=[]
    #This limitation is necessary so that each digit has two digits that adds it up
    size = 0
    for i in range(9):
        for l in range(9):
            if i+l==number:
                possibleCombinations.append(str(i)+str(l))
                size += 1
    if size==1:
        cont=0
    else:
        cont=random.randint(0, size-1)
    #We choose a combination in random way
    return str(possibleCombinations[cont])

#Main function to encode the secret in a flag
def encode(flag, data, password):
    solution=""
    secretHex=data
    for x in secretHex:
        realNumber=int(x,16)
        solution=solution+str(calculateRandomCombination(realNumber))
        
    solutionArray=[]
    for x in solution:
        solutionArray.append(x)
    result=[]
    #We modify the order according to its password in a pseudorandom way
    result=utils.inverseRandomArray(solutionArray.copy(),password)
    secretComputed=""
    for x in result:
        secretComputed=secretComputed+x
    #Time to hide secret!
    #Now we add the padding, so it is equal to the color given (the cover). It will have two digits.
    myColor=utils.calculateMod8(int(secretComputed))
    secretFinal=""
    done=False
    while done==False:
        digit1=random.randint(0, 9)
        digit2=random.randint(0, 9)
        padding=str(digit1)+str(digit2)
        secretFinal=secretComputed+str(padding)
        if utils.calculateMod8(int(secretFinal))==flag:
            done=True
    return secretFinal

#Main function to decode the flag and discover its secret
def decode(flagHidden,password):
    #First, we check its colour
    color=utils.calculateMod8(int(flagHidden))
    #We take out the padding (two last digits out)
    secretComputed=flagHidden[:len(flagHidden)-2]
    if len(secretComputed) % 2 == 1:
        secretComputed = "0" + secretComputed
    #Conversion of string in a list
    listSecret=[]
    for x in secretComputed:
        listSecret.append(x)
    #Now we do the random disorder again
    realSecretArray=utils.inverseRandomArray(listSecret,password)
    realSecret=""
    for x in realSecretArray:
        realSecret=realSecret+x
    secretHex=""
    cont=0
    #We have to add up its two digits in lineal order
    while cont!=len(realSecret):
        if cont==len(realSecret)-1:
            secretHex=secretHex+realSecret[cont]
        digit1=int(realSecret[cont])
        digit2=int(realSecret[cont+1])
        operation=digit1+digit2
        if operation>9:
            operationHex=hex(operation)
            operation=operationHex[2:]
        secretHex=secretHex+str(operation)
        cont=cont+2
    return secretHex

def estimate():
    global MAX_CAPACITY
    return MAX_CAPACITY
