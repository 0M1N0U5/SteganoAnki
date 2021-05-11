import stegoFlags
import utils


def Prueba():
    #Main code to run the previous functions
    secret = "paco"
    print("")
    password="14"
    color=1
    print("INFO: First we hide the secret inside the flag.")
    secretHex = utils.stringToHex(secret)
    print(secret, "->", secretHex)
    secretFinal=stegoFlags.encode(color, secretHex, password)
    print(secretFinal)
    print("INFO: Now, we reveal the secret hidden inside the flag.")
    decodedSecret = stegoFlags.decode(secretFinal,password)
    print(decodedSecret, "->", utils.hexToString(decodedSecret))

    print("INFO: Now, we lets try splitting the data")
    maxValues =stegoFlags.estimate()
    for i in range(0, len(secretHex), maxValues):
        values = secretHex[0+i:i+maxValues]
        splittedSecret = stegoFlags.encode(color, values, password)
        print(values, "->", splittedSecret)

Prueba()