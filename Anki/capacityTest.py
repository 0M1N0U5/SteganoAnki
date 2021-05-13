import lib.stegoImage as stegoImage
import lib.utils as utils
from datetime import datetime
import numpy
import random
import string

def getRandomString(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def pruebaFoto(name):
    completeName = "media/" + name
    completeOutputStego = "mediaOut/stego_" + name
    completeOutputMask = "mediaOut/mask_" + name
    print("Creando caso de prueba para:", name)
    print(datetime.now().strftime("%H:%M:%S"), "calculando capacidad...")
    capacity = stegoImage.estimate(completeName)
    print(datetime.now().strftime("%H:%M:%S"), "capacidad de", capacity)
    data = numpy.full(capacity, "A")
    data = ''.join(data)
    password = getRandomString(10)
    print(datetime.now().strftime("%H:%M:%S"), "Utilizando password", password)
    print(datetime.now().strftime("%H:%M:%S"), "Escribiendo", capacity, "A's en:", completeOutputStego)
    if stegoImage.encode(completeName, data, password, completeOutputStego):
        print(datetime.now().strftime("%H:%M:%S"), "Datos escritos con éxito. Decodificando")
        nameObj = utils.manageOutputFileName(completeOutputStego)
        decodedData = stegoImage.decode(nameObj["name"], password)
        if numpy.array_equal(data, decodedData):
            print(datetime.now().strftime("%H:%M:%S"), "Data decodificado correctamente")
        else:
            print(datetime.now().strftime("%H:%M:%S"), "El data decodificado no coincide")
    else:
        print(datetime.now().strftime("%H:%M:%S"), "Los datos no se han podido escribir")

    hilos=8
    print(datetime.now().strftime("%H:%M:%S"), "Dibujando mascara en:", completeOutputMask)
    stegoImage.drawMask(completeName, completeOutputMask, hilos)
    print(datetime.now().strftime("%H:%M:%S"), "mascara terminada")

def pruebaFotoMask(name):
    completeName = "media/" + name
    completeOutputStego = "mediaOut/stego_" + name
    completeOutputMask = "mediaOut/mask_" + name
    hilos=8
    print(datetime.now().strftime("%H:%M:%S"), "Dibujando mascara en:", completeOutputMask)
    stegoImage.drawMask(completeName, completeOutputMask, hilos)
    print(datetime.now().strftime("%H:%M:%S"), "mascara terminada")

#pruebaFoto("oso.png")
#pruebaFotoMask("Perro.png")
pruebaFotoMask("oso.png")