from numpy import can_cast
from ankiwrapper import AnkiWrapper
import os
import pathlib
import stegoImage
import re
import utils
from dataManager import DataBuffer

def decodificar(rutaBase, nombreImagen, password):
    return stegoImage.decode(rutaBase+nombreImagen, password)

def codificar(rutaBase, index, nombreImagen, mensaje, password):
    nuevoNombreImagen = modificarNombre(nombreImagen)
    result = stegoImage.encode(rutaBase+nombreImagen, mensaje, password, rutaBase+nuevoNombreImagen)
    if result:
        return {"index": index, "name": nombreImagen, "newName": nuevoNombreImagen}
    else:
        return False

def modificarNombre(nombreImagen):
    index = nombreImagen.rfind(".")
    return nombreImagen[:index] + "_.png"


def analizarCard(rutaBase, index, campoFlds, estimacionReal=False): #Por ahora solo imagenes
    Objetos_carta = utils.processCardText(campoFlds)
    respuesta = []
    for i in Objetos_carta['images']:
        estimacion = -1
        if estimacionReal:
            estimacion = stegoImage.estimate(rutaBase + i)
        image = {"name": i, "estimacion": estimacion, "index": index}
        respuesta.append(image)
    return respuesta

def main():
    supossedMain()
    exit(0)
    mocking = True
    mocking = False
    rutaBase = "/home/jose/.local/share/Anki2/Usuario 1/collection.media/"
    resultado = [[{"name": "gonzalo-madrid.jpg", "estimacion" : 91693, "index": 477}], [{"name": "Jose-madrid.jpg", "estimacion": 37653, "index": 478}]]
    data = utils.stringToHex("Esto")
    password = "password123"
    if not mocking:
        aw = AnkiWrapper.getInstance()
        rutaBase = aw.rutaBase
        nombreMazo = "Gonzalo"
        mensaje = utils.stringToHex("Hola, este es un mensaje:)")
        mazo = aw.getNotesFromDeck(nombreMazo)
        print(mazo)
        print("---")
        print("Calcular")
        resultado = buscarImagenesMazo(rutaBase, mazo)
        print(resultado)
        print(len(resultado))
        sizeMensaje = len(mensaje)

    dumpDataToMedia(rutaBase, data, password, resultado)

def supossedMain():
    estimate = False
    nameDeck = "PORRO"
    media = getDeckMediaInformation(nameDeck, estimate) 
    if estimate:
        manageEstimateMedia(media)
    else:
        password = "password"
        data = utils.stringToHex("datos")
        aw = AnkiWrapper.getInstance()
        rutaBase = aw.rutaBase
        updates = dumpDataToMedia(rutaBase, data, password, media)
        if updates:
            aw.updateRowsNotes(updates)
        else:
            print("All data could not be written")
            print("Use estimate function to know about limits of this deck")

def manageEstimateMedia(media):
    print(media)

def getDeckMediaInformation(nameDeck, estimate=False):
    aw = AnkiWrapper.getInstance()
    deck = aw.getNotesFromDeck(nameDeck)
    print(aw.getDecks())
    print("---")
    print(deck)
    return buscarImagenesMazo(aw.rutaBase, deck, estimate)

def dumpDataToMedia(rutaBase, data, password, media):
    globalDataLength = len(data)
    processedDataLength = 0
    dataReader = DataBuffer(data)
    end = False
    pendingUpdates = []
    for card in media:
        for photo in card:
            if photo["estimacion"] < 0:
                print("Estimando: ", photo["name"])
                photo["estimacion"] = stegoImage.estimate(rutaBase + photo["name"])
            readData = dataReader.getNext(photo["estimacion"])
            readDataLength = readData[1]
            processedDataLength += readDataLength
            readData = readData[0]
            if readDataLength < photo["estimacion"]:
                end = True
            if readDataLength > 0:
                print("Escribiendo:", readData)
                result = codificar(rutaBase, photo["index"], photo["name"], data, password)
                if result:
                    pendingUpdates.append(result)
                else:
                    print("photo problem detected: ", photo["name"], "index:", photo["index"])
                    dataReader.goBack(readDataLength)
                    end = False
            if end:
                break
        if end:
            break
            
    if processedDataLength < globalDataLength:
        return False

    return pendingUpdates

    
def buscarImagenesMazo(rutaBase, mazo, estimate=False):
    lista = []
    for index, row in mazo.iterrows():
        resultadoAnalisis = analizarCard(rutaBase, row.name, row.flds, estimate)
        if len(resultadoAnalisis) != 0:
            lista.append(resultadoAnalisis)
    return lista

main()