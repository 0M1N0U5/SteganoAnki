from numpy import *
import utils

MAX_CAPACITY = 3 #hex values

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
    result=utils.randomArray(solutionArray.copy(),password)
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
    return int(secretFinal)

#Main function to decode the flag and discover its secret
def decode(flagHidden,password):
    #First, we check its colour
    color=utils.calculateMod8(int(flagHidden))
    #We take out the padding (two last digits out)
    flagHidden = str(flagHidden)
    secretComputed=flagHidden[:len(flagHidden)-2]
    
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
        operation= (digit1+digit2) % 16
        secretHex += f'{operation:0>1x}'
        cont=cont+2
    return secretHex

def estimate():
    global MAX_CAPACITY
    return MAX_CAPACITY


#for i in range(16):
#    calculateRandomCombination(i)    