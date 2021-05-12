import json
import binascii
import os

myobject = {"cosa": "algo", "esto": "otracosa", "l":[1,2,3,4]}

with open('data.txt', 'w') as outfile:
    json.dump(myobject, outfile)

with open('data.txt') as json_file:
    data = json.load(json_file)
    print(data)


def prepareData(data):
    try:
        if os.path.isfile(data):
            with open(data, 'rb') as f:
                content = f.read()
            return binascii.hexlify(content)

    except Exception as e:
        return False

print(prepareData("data.txt").decode("utf-8"))