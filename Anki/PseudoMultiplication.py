import random

#Script to add pseudorandom positions
#secretOctal="164336700403466254334462564"
secretOctal="1234561"
newSecret=""
count=0

def findNoMark(cadena):
    indice = 0
    for x in cadena:
        if x!= "x":
            return indice
        indice += 1
    return -1

while count!=len(secretOctal):
    #If only one number is left or len=1
    if count==len(secretOctal)-1 or len(secretOctal)==1:
        pos=findNoMark(secretOctal)
        r1=int(secretOctal[pos])
        secretOctal = secretOctal[:pos] + "x" + secretOctal[pos+1:]
        newSecret=newSecret+str(r1)
        print("Operation done!")
        print("Cadena: "+secretOctal)
        #Count of the marks
        count=count+1
    else:
        randomPos1=random.randint(0,len(secretOctal)-1)
        randomPos2=random.randint(0,len(secretOctal)-1)
        #If any is marked, randomize again
        if secretOctal[randomPos1]=="x" or secretOctal[randomPos2]=="x":
            randomPos1=random.randint(0,len(secretOctal)-1)
            randomPos2=random.randint(0,len(secretOctal)-1)
            #If both are the same position, pos2 is randomize again
        elif randomPos1==randomPos2 and secretOctal[randomPos1]!="x" and secretOctal[randomPos2]!="x":
            randomPos2=random.randint(0,len(secretOctal)-1)
        elif randomPos1!=randomPos2 and secretOctal[randomPos1]!="x" and secretOctal[randomPos2]!="x":
            r1=int(secretOctal[randomPos1])*int(secretOctal[randomPos2])
            newSecret=newSecret+str(r1)
            print("Pos1: "+ str(randomPos1))
            print("Num1: "+secretOctal[randomPos1])
            print("Pos2: "+ str(randomPos2))
            print("Num2: "+secretOctal[randomPos2])
            print("Operation done!")
            #We mark the positions already computed only once (maybe numbers repeat)
            secretOctal = secretOctal[:randomPos1] + "x" + secretOctal[randomPos1+1:]
            secretOctal = secretOctal[:randomPos2] + "x" + secretOctal[randomPos2+1:]
            print("Cadena: "+secretOctal)
            #Count of the marks
            count=count+2
            print("Partial solution: "+newSecret)
print("Final solution: "+newSecret)



