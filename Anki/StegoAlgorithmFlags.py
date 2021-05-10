from numpy import *
import utils
import collections

def calculateMod8(number):
    remainder=number%8
    return remainder

def HexToString(s):
    result=bytes.fromhex(s)
    return result

def inverseRandomArray (secret,password):
    #print("ORIGINAL:", secret)
    #print("MIX:", utils.randomArray(secret.copy(), password))
    mixedSecret = utils.randomArray(secret.copy(), password)
    #print("SECRET END")
    count=0
    indices=[]
    while count!=len(secret):
        indices.append(count)
        count=count+1
    #print("INDEXES:", indices)
    #print("INDEXES MIX:", utils.randomArray(indices.copy(), password))
    mixedIndices = utils.randomArray(indices.copy(), password)
    originalVector = {}
    for i in range(len(mixedIndices)):
        originalVector[mixedIndices[i]] = mixedSecret[i]
    originalVector = collections.OrderedDict(sorted(originalVector.items()))
    return list(originalVector.values())

def calculateRandomCombination(number):
    possibleCombinations=[]
    #This limitation is necessary so that each digit has two digits that adds it up
    for i in range(9):
        for l in range(9):
            if i+l==number:
                possibleCombinations.append(str(i)+str(l))
    #print("All possible combinations: ")
    #for x in possibleCombinations:
        #print(str(x))
    
    size=len(possibleCombinations)
    if size==1:
        cont=0
    else:
        cont=random.randint(0, size-1)
    combination=""
    #We choose a combination in random way
    combination=str(possibleCombinations[cont])
    #print("Total number of combinations: "+ str(size))
    #print("Combination selected: "+combination)
    return combination

#Main function to encode the secret in a flag
def encodeFlags(secret,password,color):
    print("ENCODE FLAGS")
    print("Secret: "+secret)
    solution=""
    secretHex=utils.stringToHex(secret)
    print("Secret in Hex: "+str(secretHex))
    for x in secretHex:
        realNumber=int(x,16)
        solution=solution+str(calculateRandomCombination(realNumber))
    print("Secret computed: "+solution)
        
    solutionArray=[]
    for x in solution:
        solutionArray.append(x)
    result=[]
    #We modify the order according to its password in a pseudorandom way
    result=inverseRandomArray(solutionArray.copy(),password)
    secretComputed=""
    for x in result:
        secretComputed=secretComputed+x


    print("This is your secret: "+secretComputed)
    #Time to hide secret!
    #Now we add the padding, so it is equal to the color given (the cover). It will have two digits.
    myColor=calculateMod8(int(secretComputed))
    secretFinal=""
    done=False
    while done==False:
        digit1=random.randint(0, 9)
        digit2=random.randint(0, 9)
        padding=str(digit1)+str(digit2)
        secretFinal=secretComputed+str(padding)
        if calculateMod8(int(secretFinal))==color:
            done=True
    print("Secret undercover: "+secretFinal)
    return secretFinal

#Main function to decode the flag and discover its secret
def decodeFlags(flagHidden,password):
    print("DECODE FLAGS")
    print("Secret undercover: "+flagHidden)
    #First, we check its colour
    color=calculateMod8(int(flagHidden))
    print("Color: "+str(color))
    secretComputed=flagHidden[:len(flagHidden)-2]
    #We take out the padding (two last digits out)
    print("This is your secret: "+secretComputed)
    #Conversion of string in a list
    listSecret=[]
    for x in secretComputed:
        listSecret.append(x)
    #Now we do the random disorder again
    realSecretArray=inverseRandomArray(listSecret,password)
    realSecret=""
    for x in realSecretArray:
        realSecret=realSecret+x
    print("Secret computed: "+realSecret)
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
    print("Secret in Hex: "+secretHex)
    secret=HexToString(secretHex).decode("utf-8") 
    print("Secret: "+ str(secret))
    return secret

#Main code to run the previous functions
print("What secret do you want to hide in the flags?")
secret = input()
print("INFO: Good secret ;). Let's have fun!")
print("")
flagHidden=""
password="14"
color=1
print("")
print("INFO: First we hide the secret inside the flag.")
secretFinal=encodeFlags(secret,password,color)
print("")
print("INFO: Now, we reveal the secret hidden inside the flag.")
flagHidden=secretFinal
decodeFlags(flagHidden,password)



 


