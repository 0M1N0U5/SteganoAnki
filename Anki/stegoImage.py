import utils
from PIL import Image
import statistics
import random
import traceback

MAX_WIDTH = 3840
MAX_HEIGHT = 2160
PRE_HEADER_SIZE = 3 #bytes
HEADER_SIZE = 3 #bytes
COLOR_SIZE = 3

# 7E 90 00 -> 3 bytes -> data covered in image
def encode(imagePath, hexdata, password, outputFileName):
    outputFileNameObj = utils.manageOutputFileName(outputFileName)
    outputFileName = outputFileNameObj["name"]

    data = hexdata
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
                preHeader = utils.calculatePreHeader(password)
                header = f'{dataLength:0>6X}'
                dataLength += (HEADER_SIZE * 2)
                dataLength += (PRE_HEADER_SIZE * 2)
                data = preHeader + header + data
                if(dataLength < width * height):
                    positions = utils.randomPositions(width, height, password)
                    for position in positions:
                        if(i < dataLength):
                            x = position["x"]
                            y = position["y"]
                            pixel = list(img.getpixel((x, y)))
                            if utils.isValidPixel(pixel):
                                newPixel = utils.getBestVector(pixel, int(data[i], 16))
                                #print(int(data[i], 16), x, y, pixel, "->", newPixel)
                                img.putpixel((x, y), tuple(newPixel))
                                i += 1
                        else:
                            break
                    if i < dataLength:
                        print("All data could not be written")
                        print("Use estimate function to know about limits of this photo")
                        return False
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

def estimate(imagePath):
    global MAX_WIDTH
    global MAX_HEIGHT
    global HEADER_SIZE
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
        total -= (HEADER_SIZE * 2)
        total -= (PRE_HEADER_SIZE * 2)
    return total


def decode(imagePath, password):
    global HEADER_SIZE
    global COLOR_SIZE
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
                preheader = []
                header = []
                data = []
                dataLength = -1
                for position in positions:
                    x = position["x"]
                    y = position["y"]
                    pixel = list(img.getpixel((x, y)))

                    preHeaderStart = 0
                    preHeaderEnd = PRE_HEADER_SIZE*2
                    headerStart = PRE_HEADER_SIZE*2
                    headerEnd = (PRE_HEADER_SIZE*2)+(HEADER_SIZE*2)

                    if utils.isValidPixel(pixel):
                        #print(x, y, pixel)
                        value = 0
                        for c in range(COLOR_SIZE):
                            value += pixel[c] % 10

                        if i>=preHeaderStart and i<preHeaderEnd:
                            #leyendo preheader
                            preheader.append(f'{value:0>1x}')
                            if i+1 == preHeaderEnd:
                                #cerrar preheader
                                preheader = ''.join(preheader)
                                calculatedPreHeader = utils.calculatePreHeader(password)
                                if preheader != calculatedPreHeader:
                                    print("ERROR: All data could not be read. PREHEADER")
                                    return False
                        elif i>=headerStart and i<headerEnd:
                            #leyendo header
                            header.append(f'{value:0>1x}')
                            if i+1 == headerEnd:
                                #cerrar header
                                header = ''.join(header)
                                dataLength = int(header, 16) + len(header) + len(preheader)

                        elif i>= headerEnd:
                            data.append(f'{value:0>1x}')
                        i += 1
                    if i == dataLength:
                        break
                if(i < dataLength):
                    print("ERROR: All data could not be read.")
                    return False
                return ''.join(data)
    except Exception as e:
            print(f'\n[-]Exception occured: {e}')
            print(e)
            traceback.print_exc()
            return False


