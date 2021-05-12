from typing import NamedTuple
from numpy import can_cast
from ankiwrapper import AnkiWrapper
import os
import pathlib
import stegoImage
import re
import utils
from dataManager import DataBuffer
import json
import os
import binascii

USE_IMAGES = False
USE_FLAGS = False


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
    media = media["media"]
    aw = AnkiWrapper.getInstance()
    data = readDataFromMedia(aw.rutaBase, password, media)
    return data

def encodeDeck(nameDeck, data, password, media=False):
    if not media:
        media = getDeckMediaInformation(nameDeck, False)
    media = media["media"]
    aw = AnkiWrapper.getInstance()
    rutaBase = aw.rutaBase
    updates = dumpDataToMedia(rutaBase, data, password, media)
    if updates:
        aw.updateRowsNotes(updates)
        return True
    else:
        return False

def estimateDeck(nameDeck, output=False):
    media = getDeckMediaInformation(nameDeck, True)
    if output:
        print("Writing media to file", output)
        try:
            with open(output, 'w') as outfile:
                json.dump(media, outfile)
        except Exception as e:
            print("Media file could not be written ->", output)
            print("Check file permissions. Anyway here is you media:")
            print(media)
    else:
        print(media)

def getDeckMediaInformation(nameDeck, estimate=False):
    media = { "nameDeck": nameDeck }
    aw = AnkiWrapper.getInstance()
    deck = aw.getNotesFromDeck(nameDeck)
    imagenes = buscarImagenesMazo(aw.rutaBase, deck, estimate)
    media["media"] = imagenes
    return media

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

def prepareMedia(media):
    try:
        loadedMedia = False
        if os.path.isfile(media):
            with open(media) as json_file:
                loadedMedia = json.load(json_file)
        else:
            loadedMedia = json.load(media)
        return loadedMedia
    except Exception as e:
        return False

def prepareData(data):
    try:
        if os.path.isfile(data):
            with open(data, 'rb') as f:
                content = f.read()
            return binascii.hexlify(content).decode("utf-8")
        else:
            return utils.stringToHex(data)
    except Exception as e:
        return utils.stringToHex(data)

def call(args):
    global USE_IMAGES
    global USE_FLAGS

    USE_IMAGES = False
    USE_FLAGS = False

    opModes = ["enc", "dec", "est"]
    dataKey = "data"
    passwordKey = "password"
    opModeKey = "mode"
    mediaKey = "media"
    nameDeckKey = "nameDeck"
    outputMediaKey = "outputMedia"

    #coverKey = "cover"
    #if args[coverKey] == 0 or args[coverKey] == 2:
    #    USE_IMAGES = True
    #if args[coverKey] == 1 or args[coverKey] == 2:
    #    USE_FLAGS = True

    if args[opModeKey] == opModes[0]:
        #Modo encode
        data = args[dataKey]
        password = args[passwordKey]
        nameDeck = args[nameDeckKey]
        data = prepareData(data)
        media = prepareMedia(args[mediaKey])
        print("nameDeck:", nameDeck)
        print("password:", password)
        print("data:", data)
        print("media:", media)
        if encodeDeck(nameDeck, data, password, media):
            print("Info saved correctly")
        else:
            print("All data could not be written")
            print("Use estimate function to know about limits of this deck")         
    elif args[opModeKey] == opModes[1]:
        #Modo decode
        password = args[passwordKey]
        nameDeck = args[nameDeckKey]
        print("nameDeck:", nameDeck)
        print("password:", password)
        data = decodeDeck(nameDeck, password)
        print(data)
    elif args[opModeKey] == opModes[2]:
        #modo estimate
        nameDeck = args[nameDeckKey]
        outputMedia = False
        if args[outputMediaKey]:
            outputMedia = args[outputMediaKey]
        print("nameDeck:", nameDeck)
        print("outputMedia:", outputMedia)
        estimateDeck(nameDeck, outputMedia)


def test():
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