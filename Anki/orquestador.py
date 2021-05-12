from typing import NamedTuple
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

def buscarImagenesMazo(rutaBase, mazo, estimate=False):
    lista = []
    for index, row in mazo.iterrows():
        resultadoAnalisis = analizarCard(rutaBase, row.name, row.flds, estimate)
        if len(resultadoAnalisis) != 0:
            lista.append(resultadoAnalisis)
    return lista

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

def decodeDeck(nameDeck, password):
    media = getDeckMediaInformation(nameDeck, False)
    aw = AnkiWrapper.getInstance()
    data = readDataFromMedia(aw.rutaBase, password, media)
    return data

def encodeDeck(nameDeck, data, password, estimate):
    media = getDeckMediaInformation(nameDeck, estimate)
    if estimate:
        manageEstimateMedia(media)
    else:
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
    return buscarImagenesMazo(aw.rutaBase, deck, estimate)

def readDataFromMedia(rutaBase, password, media):
    data = []
    exit = False
    for card in media:
        for photo in card:
            readData = stegoImage.decode(rutaBase + photo["name"], password)
            if(readData and len(readData)> 0):
                data.append(readData)
            else:
                exit = True
            if exit: 
                break
        if exit: 
            break
    return ''.join(data)

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

def main():
    estimate = False
    nameDeck = "PORRO"
    data = utils.stringToHex("datos")
    password = "password"
    print("Ocultando", data, "en mazo", nameDeck)
    encodeDeck(nameDeck, data, password, estimate)
    print("Leyendo data del mazo", nameDeck)
    data = decodeDeck(nameDeck, password)
    print("Data recuperada:", data)
    print("Data recuperada:",utils.hexToString(data))

main()