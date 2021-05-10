import utils

password = "antonio"

secret = [5, 6, 7, 8, 1, 0]
print("ORIGINAL:", secret)
print("MEZCLA:", utils.randomArray(secret.copy(), password))
mixedSecret = utils.randomArray(secret.copy(), password)
print("SECRET END")

indices = [0, 1, 2, 3, 4, 5]
print("INDICES:", indices)
print("INDICES MEZCLA:", utils.randomArray(indices.copy(), password))

mixedIndices = utils.randomArray(indices.copy(), password)

originalVector = {}
for i in range(len(mixedIndices)):
    originalVector[mixedIndices[i]] = mixedSecret[i]

import collections
originalVector = collections.OrderedDict(sorted(originalVector.items()))
print(list(originalVector.values()))