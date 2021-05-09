import utils
from PIL import Image
import statistics
import random
import traceback

MAX_WIDTH = 3840
MAX_HEIGHT = 2160
HEADER_SIZE = 3 #bytes

def encodeSeq(imagePath, text, password, outputFileName):
    outputFileNameObj = utils.manageOutputFileName(outputFileName)
    outputFileName = outputFileNameObj["name"]
    print(outputFileNameObj)

    data = utils.stringToHex(text)
    data = utils.ofuscate(data)
    try:
        with Image.open(imagePath) as img:
            width, height = img.size
            print(img.size)
            i = 0
            dataLength = len(data)
            if(dataLength < width * height):
                for x in range(0, width):
                    for y in range(0, height):
                        if(i < dataLength):
                            pixel = list(img.getpixel((x, y)))
                            newPixel = utils.getBestVector(pixel, len(pixel), int(data[i], 16))
                            #print(int(data[i], 16), " | ", pixel, "->", newPixel)
                            i += 1
                            img.putpixel((x, y), tuple(newPixel))
                img.save(outputFileName, outputFileNameObj["type"])
            else: 
                print("Data demasiado largo:", dataLength, "máximo soportado: ", width * height)
                return False
    except Exception as e:
            print(f'\n[-]Exception occured: {e}')
            return False
    finally:
            return True

def encodeRandomSeq(imagePath, text, password, outputFileName):
    outputFileNameObj = utils.manageOutputFileName(outputFileName)
    outputFileName = outputFileNameObj["name"]
    print(outputFileNameObj)

    data = utils.stringToHex(text)
    data = utils.ofuscate(data)
    try:
        with Image.open(imagePath) as img:
            width, height = img.size
            print(img.size)
            i = 0
            dataLength = len(data)
            if(dataLength < width * height):
                positions = utils.randomPositions(width, height, password)
                for position in positions:
                    if(i < dataLength):
                        x = position["x"]
                        y = position["y"]
                        pixel = list(img.getpixel((x, y)))
                        newPixel = utils.getBestVector(pixel, len(pixel), int(data[i], 16))
                        i += 1
                        img.putpixel((x, y), tuple(newPixel))
                    else:
                        break
                img.save(outputFileName, outputFileNameObj["type"])
            else: 
                print("Data demasiado largo:", dataLength, "máximo soportado: ", width * height)
                return False
    except Exception as e:
            print(f'\n[-]Exception occured: {e}')
            print(e)
            traceback.print_exc()
            return False
    finally:
            return True
# 7E 90 00 -> 3 bytes -> data covered in image
def encode(imagePath, text, password, outputFileName):
    outputFileNameObj = utils.manageOutputFileName(outputFileName)
    outputFileName = outputFileNameObj["name"]

    data = utils.stringToHex(text)
    data = utils.ofuscate(data)
    try:
        with Image.open(imagePath) as img:
            width, height = img.size
            if width > MAX_WIDTH or height > MAX_HEIGHT:
                print(imagePath, "is", width, "x", height)
                print("Max supported resolution is (width x height) -> ("+MAX_WIDTH+" x "+MAX_HEIGHT+") 4k")
                return False
            else:
                i = 0
                dataLength = len(data)
                header = f'{dataLength:0>6X}'
                dataLength += (HEADER_SIZE * 2)
                data = header + data
                if(dataLength < width * height):
                    positions = utils.randomPositions(width, height, password)
                    for position in positions:
                        if(i < dataLength):
                            x = position["x"]
                            y = position["y"]
                            pixel = list(img.getpixel((x, y)))
                            if utils.isValidPixel(pixel):
                                newPixel = utils.getBestVector(pixel, len(pixel), int(data[i], 16))
                                #print(int(data[i], 16), x, y, pixel, "->", newPixel)
                                img.putpixel((x, y), tuple(newPixel))
                                i += 1
                        else:
                            break
                    if i < dataLength:
                        print("All data could not be written")
                        print("Use estimate function to know about limits of this photo")
                        return False
                    img.save(outputFileName, outputFileNameObj["type"], dpi=[300,300], quality=90)
                else: 
                    print("Data demasiado largo:", dataLength, "máximo soportado: ", width * height)
                    return False
    except Exception as e:
            print(f'\n[-]Exception occured: {e}')
            print(e)
            traceback.print_exc()
            return False
    finally:
            return True

def estimate(imagePath):
    global MAX_WIDTH
    global MAX_HEIGHT
    total = 0
    try:
        with Image.open(imagePath) as img:
            width, height = img.size
            if width > MAX_WIDTH or height > MAX_HEIGHT:
                print(imagePath, "is", width, "x", height)
                print("Max supported resolution is (width x height) -> ("+MAX_WIDTH+" x "+MAX_HEIGHT+") 4k")
            else:
                for x in range(0, width):
                    for y in range(0, height):
                        pixel = list(img.getpixel((x, y)))
                        if utils.isValidPixel(pixel):
                            total += 1
    except Exception as e:
            print(f'\n[-]Exception occured: {e}')

    if total > 0:
        total -= HEADER_SIZE
    return total


def decode(imagePath, password):
    try:
        with Image.open(imagePath) as img:
            width, height = img.size
            if width > MAX_WIDTH or height > MAX_HEIGHT:
                print(imagePath, "is", width, "x", height)
                print("Max supported resolution is (width x height) -> ("+MAX_WIDTH+" x "+MAX_HEIGHT+") 4k")
                return False
            else:
                positions = utils.randomPositions(width, height, password)
                i = 0
                header = []
                data = []
                dataLength = 0
                for position in positions:
                    x = position["x"]
                    y = position["y"]
                    pixel = list(img.getpixel((x, y)))
                    if utils.isValidPixel(pixel):
                        #print(x, y, pixel)
                        if i < (HEADER_SIZE * 2):
                            value = 0
                            for c in pixel:
                                value += c % 10
                            header.append(f'{value:0>1X}')
                        if i >= (HEADER_SIZE * 2):
                            if i == (HEADER_SIZE * 2):
                                header = ''.join(header)
                                dataLength = int(header, 16) + len(header)
                            if dataLength > 0:
                                value = 0
                                for c in pixel:
                                    value += c % 10
                                data.append(f'{value:0>1X}')
                        i += 1
                    if i == dataLength:
                        break
                if(i < dataLength):
                    print("ERROR: All data could not be read.")
                    return ''.join([])
                return ''.join(data)
    except Exception as e:
            print(f'\n[-]Exception occured: {e}')
            print(e)
            traceback.print_exc()
            return False


