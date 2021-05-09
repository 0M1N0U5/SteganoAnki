from PIL import Image
import utils

#Modification of https://github.com/omnone/pyHide/blob/master/src/pyHide/lsbSteg.py

from PIL import Image
import tkinter as tk
import crypto
import pyAesCrypt
import os

# ============================================================================================

def encodeImage(imagePath, text, password, outputFileName):
    outputFileNameObj = utils.manageOutputFileName(outputFileName)
    outputFileName = outputFileNameObj["name"]

    if os.path.isfile(text):
        encodeFile(imagePath, text, password, outputFileName)
        return

    text = crypto.encryptText(text, password=password)

    try:
        data = stringToBin(text)
        lenData = intToBin(len(data))

        data = format(len(lenData), 'b').zfill(8)+lenData + data

        with Image.open(imagePath) as img:
            width, height = img.size

            i = 0

            for x in range(0, width):
                for y in range(0, height):
                    pixel = list(img.getpixel((x, y)))
                    for n in range(0, 3):
                        if(i < len(data)):
                            pixel[n] = pixel[n] & 0 | int(data[i])
                            i += 1

                    img.putpixel((x, y), tuple(pixel))

            img.save(outputFileName, outputFileNameObj["type"])

    except Exception as e:
            print(f'\n[-]Exception occured: {e}')
            return False
    finally:
            return True


def encodeFile(imagePath, targetFile, password, outputFileName):
    bufferSize = 64 * 1024
    ext = targetFile.split('.')[-1]
    filename = os.path.basename(targetFile)

    pyAesCrypt.encryptFile(targetFile,
                           'temp.'+ext, password, bufferSize)

    with open(outputFileName, 'wb') as out:
        out.write(open('temp.'+ext, 'rb').read() + b'aescrypt,fileextension:'+ext.encode()+b',filename:'+filename.encode())

    os.remove('temp.'+ext)

# ============================================================================================

def decodeImage(imagePath, password):

    try:
        with open(imagePath, 'rb') as f:
            data = f.read().split(b'aescrypt')

        if len(data) > 1:
            return decodeFile(imagePath, password)
    except FileNotFoundError:
        pass

    try:
        extractedBin = []
        with Image.open(imagePath) as img:
            width, height = img.size

            for x in range(0, width):
                for y in range(0, height):
                    pixel = list(img.getpixel((x, y)))
                    for n in range(0, 3):
                        extractedBin.append(pixel[n] & 1)

        len_len = int(''.join([str(i) for i in extractedBin[0:8]]), 2)
        len_data = int(''.join([str(i)
                                for i in extractedBin[8:len_len+8]]), 2)

        binaryMessage = int(''.join([str(extractedBin[i+8+len_len])
                                     for i in range(len_data)]), 2)

        decodedMessage = binaryMessage.to_bytes((binaryMessage.bit_length() + 7) // 8, 'big').decode()

        if password and password != "":
            decodedMessage = crypto.decryptText(decodedMessage, password=password)
            return decodedMessage

    except Exception as e:
        print(f'\n[-]Exception occured: {e}')

def decodeFile(imagePath, password):
    bufferSize = 64 * 1024
    with open(imagePath, 'rb') as f:
        data = f.read().split(b'aescrypt')[0]
        f.seek(0)
        filename = f.read().split(b'filename:')[1].decode()
        ext = filename.split('.')[-1]

        with open('temp.'+ext, 'wb') as f1:
            f1.write(data)

    pyAesCrypt.decryptFile('temp.'+ext,filename, password, bufferSize)
                           
    os.remove('temp.' + ext)
    return filename



encodeImage("gonzalo-madrid.jpg", "textoAEsconder", "password123", "soyGonzalooooo.png")