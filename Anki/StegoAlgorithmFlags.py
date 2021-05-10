from numpy import *
import utils

def calculateMod8(number):
    remainder=number%8
    return remainder

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

solution=""
array=[1,2,3,4]

secret="top"
password="14"
color=1

secretHex=utils.stringToHex(secret)

print("Secret in Hex: "+str(secretHex))
for x in secretHex:
    realNumber=int(x,16)
    solution=solution+str(calculateRandomCombination(realNumber))
print("Secret computed: "+solution)
#
solutionArray=[]
for x in solution:
    solutionArray.append(x)

result=[]
#We modify the order according to its password in a pseudorandom way
result=utils.randomArray(solutionArray.copy(),password)
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


 


