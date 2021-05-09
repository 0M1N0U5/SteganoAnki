import hashlib
from random import randrange
import random
import statistics
import numpy
import secrets
from base64 import urlsafe_b64encode as b64e, urlsafe_b64decode as b64d
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()
iterations = 100_000

def _derive_key(password: bytes, salt: bytes, iterations: int = iterations) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return b64e(kdf.derive(password))

def password_encrypt(message: bytes, password: str, iterations: int = iterations) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(password.encode(), salt, iterations)
    return b64e(
        b'%b%b%b' % (
            salt,
            iterations.to_bytes(4, 'big'),
            b64d(Fernet(key).encrypt(message)),
        )
    )

def password_decrypt(token: bytes, password: str) -> bytes:
    decoded = b64d(token)
    salt, iter, token = decoded[:16], decoded[16:20], b64e(decoded[20:])
    iterations = int.from_bytes(iter, 'big')
    key = _derive_key(password.encode(), salt, iterations)
    return Fernet(key).decrypt(token)

def stringToBin(text):
    return ''.join(format(ord(char), '08b') for char in text)

def stringToHex(text):
    return text.encode('utf-8').hex()

def intToBin(x):
    return '{0:b}'.format(x)

supportedExtensionsMap = {
    "defaultExt" : "png",
    "defaultType" : "PNG",
    "png" : "PNG"
    #"jpg" : "JPEG"
}

def isSupported(extension):
    if extension.lower() in supportedExtensionsMap.keys():
        return True
    else:
        print("Extension |", extension, "| not supported. PNG will be used.")
        return False

def manageExtension(extension, outputFile):
    if extension is None or extension == "" or not isSupported(extension):
        outputFile["ext"] = supportedExtensionsMap["defaultExt"]
        outputFile["type"] = supportedExtensionsMap["defaultType"]
        return False

    outputFile["ext"] = extension
    outputFile["type"] = supportedExtensionsMap[extension]
    return True
    

def manageOutputFileName(outputFileName):
    outputFile = {}

    if outputFileName is None or type(outputFileName) != str or outputFileName == "":
        outputFile["name"] = "secret"
        outputFile["ext"] = supportedExtensionsMap["defaultExt"]
        outputFile["type"] = supportedExtensionsMap["defaultType"]
        return outputFile

    if "." in outputFileName:
        splited = outputFileName.split(".")
        extension = splited[-1]
        if manageExtension(extension, outputFile):
            outputFile["name"] = ''.join(splited[:-1])
        else:
            outputFile["name"] = outputFileName
    else:
        outputFile["name"] = outputFileName
        outputFile["ext"] = supportedExtensionsMap["defaultExt"]
        outputFile["type"] = supportedExtensionsMap["defaultType"]
    
    if outputFile["name"].endswith("."):
        outputFile["name"] = outputFile["name"] + outputFile["ext"]
    else:
        outputFile["name"] = outputFile["name"] + "." + outputFile["ext"]

    return outputFile

def sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

def ofuscate(data):
    #print("Ofuscate:", data)
    return data

def deofuscate(data):
    #print("Deofuscate:", data)
    return data


def randomSplit(toSplit, size):
    splited = {}
    for i in range(size):
        splited[i] = 0
    
    while toSplit > 0:
        pos = randrange(size)
        splited[pos] = splited[pos]+1
        toSplit = toSplit-1

    return splited

def getVectorValue(vector):
    return sum([x % 10 for x in vector])

vectorsMap = { 
    "0" : [], "1" : [], "2" : [], "3" : [], "4" : [], "5" : [], "6" : [], "7" : [], "8" : [], "9" : [], "10" : [], "11" : [], "12" : [], "13" : [], "14" : [], "15" : []
}

def getVectorsList(target):
    vectors = vectorsMap[str(target)]
    if not vectors:
        for i in range(9):
            for l in range(9):
                for z in range(9):
                    v = [i, l, z]
                    vectorValue = getVectorValue(v)
                    if vectorValue < 16:
                        vectorsMap[str(vectorValue)].append(v)
        vectors = vectorsMap[str(target)]
    return vectors

kDTreeMap = {
    "0" : None, "1" : None, "2" : None, "3" : None, "4" : None, "5" : None, "6" : None, "7" : None, "8" : None, "9" : None, "10" : None, "11" : None, "12" : None, "13" : None, "14" : None, "15" : None
}

from scipy import spatial
def getVectorFromKdTree(target, vector):
    kdtree = kDTreeMap[str(target)]
    vectors = getVectorsList(target)    
    if kdtree is None:
        kdtree = spatial.KDTree(vectors)
        kDTreeMap[str(target)] = kdtree

    return vectors[kdtree.query(vector)[1]]

def getBestVector(initVector, size, targetValue):
    v = getVectorFromKdTree(targetValue, initVector)
    finalVector = initVector.copy()
    for i in range(size):
        finalVector[i] = finalVector[i] - finalVector[i] % 10 + v[i]
        diffPosition = abs(finalVector[i] - initVector[i])

        if diffPosition > 5:
            if(finalVector[i] > initVector[i]):
                finalVector[i] -= 10
            else:
                finalVector[i] += 10

        while finalVector[i] > 255:
            finalVector[i] -= 10

        while finalVector[i] < 0:
            finalVector[i] += 10

    if not isValidPixel(finalVector):
        max_pos = 0
        min_pos = 0
        last_max = -1
        last_min = 256
        for i in range(size):
            if finalVector[i] > last_max:
                last_max = finalVector[i]
                max_pos = i
            if finalVector[i] < last_min:
                last_min = finalVector[i]
                min_pos = i

        action = 1
        while not isValidPixel(finalVector):
            if finalVector[max_pos] + 5 < 256 and finalVector[min_pos] - 5 > -1:
                finalVector[max_pos] +=5
                finalVector[min_pos] -=5
            else:
                if action == 1:
                    if finalVector[max_pos] + 10 < 256:
                        finalVector[max_pos] +=10
                    action = -1
                else:
                    if finalVector[min_pos] - 10 > -1:
                        finalVector[min_pos] -=10
                    action = 1
    return finalVector

def getBestVectorR(initVector, size, targetValue):
    initVector = initVector.copy()
    actualValue = getVectorValue(initVector)
    while actualValue != targetValue:
        initVector[randrange(size)] += 1
        actualValue = getVectorValue(initVector)

    for i in range(size):
        while initVector[i] > 255:
            initVector[i] -= 10

        while initVector[i] < 0:
            initVector[i] += 10

    return initVector

def randomPositions(width, height, password):
    pos = { "x": 0, "y": 0}
    positions = []

    for x in range(0, width):
        for y in range(0, height):
            pos["x"] = x
            pos["y"] = y
            positions.append(pos.copy())
    
    seed = sha256(password)
    for i in range(10000):
        seed = sha256(seed + password)
    
    random.seed(seed)
    random.shuffle(positions)
    return positions

def getSTDev(vector):
    return statistics.stdev(vector)

def getMean(vector):
    return numpy.mean(vector)

def isValidPixel(pixel):
    return getSTDev(pixel) > 10 or getMean(pixel) < 100