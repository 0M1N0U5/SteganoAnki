from typing import NamedTuple
from numpy import can_cast
from lib.ankiwrapper import AnkiWrapper
import os
import pathlib
import lib.stegoImage as stegoImage
import lib.stegoFlags as stegoFlags
import re
import lib.utils as utils
from lib.dataManager import DataBuffer 
import json
import os

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
    total = 0
    for index, row in mazo.iterrows():
        resultadoAnalisis = analizarCard(rutaBase, row.name, row.flds, estimate)
        if len(resultadoAnalisis) != 0:
            for p in resultadoAnalisis:
                total += p["estimacion"]
            lista.append(resultadoAnalisis)
    return lista, total

def modificarNombre(nombreImagen):
    index = nombreImagen.rfind(".")
    return nombreImagen[:index] + "_.png"

def analizarCard(rutaBase, index, campoFlds, estimacionReal=False): #Por ahora solo imagenes
    global USE_IMAGES
    Objetos_carta = utils.processCardText(campoFlds)
    respuesta = []
    if USE_IMAGES:
        for i in Objetos_carta['images']:
            estimacion = -1
            if estimacionReal:
                print("Estimando "+ i+"...")
                estimacion = stegoImage.estimate(rutaBase + i)
            image = {"name": i, "estimacion": estimacion, "index": index}
            respuesta.append(image)
    return respuesta

def decodeDeck(nameDeck, password):
    media = getDeckMediaInformation(nameDeck, False)
    media = getDeckMetadataInformation(nameDeck, media)
    aw = AnkiWrapper.getInstance()
    data = readDataFromDeck(aw.rutaBase, password, media)
    return data

def encodeDeck(nameDeck, data, password, media=False):
    if not media:
        media = getDeckMediaInformation(nameDeck, False)
        media = getDeckMetadataInformation(nameDeck, media)
    aw = AnkiWrapper.getInstance()
    rutaBase = aw.rutaBase
    #pendingUpdates = { "imagesUpdates" : [], "flagsUpdates" : [] }
    updates = dumpDataToDeck(rutaBase, data, password, media)
    if updates:
        if updates["imagesUpdates"]:            
            aw.updateRowsNotes(updates["imagesUpdates"])
        if updates["flagsUpdates"]:
            aw.guardarFlagsMazo(nameDeck, updates["flagsUpdates"])
        return True
    else:
        return False

def estimateDeck(nameDeck, output=False):
    media = getDeckMediaInformation(nameDeck, True)
    media = getDeckMetadataInformation(nameDeck, media)
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
    imagenes, total = buscarImagenesMazo(aw.rutaBase, deck, estimate)
    media["media"] = imagenes
    media["total"] = total
    return media

def getDeckMetadataInformation(nameDeck, media):
    global USE_FLAGS
    if USE_FLAGS:
        aw = AnkiWrapper.getInstance()
        media["flags"] = aw.getFlagsDeck(nameDeck)
        media["total"] += len(media["flags"])
    return media

def readDataFromDeck(rutaBase, password, media):
    global USE_IMAGES
    global USE_FLAGS
    if USE_FLAGS:
        flags = media["flags"]
    media = media["media"]
    data = []
    exit = False
    for card in media:
        if USE_IMAGES:
            for photo in card:
                readData = stegoImage.decode(rutaBase + photo["name"], password)
                if(readData and len(readData)> 0):
                    print("Leido", photo["name"])
                    data.append(readData)
                else:
                    exit = True
                if exit: 
                    break
            if exit: 
                break
    
    if USE_FLAGS:
        readData = stegoFlags.decode(flags, password)
        if readData and len(readData) > 0:
            print("Leidos flags")
            data.append(readData)
            
    return ''.join(data)

def dumpDataToDeck(rutaBase, data, password, media):
    global USE_IMAGES
    global USE_FLAGS
    total = media["total"]
    if USE_FLAGS:
        flags = media["flags"]
    media = media["media"]
    globalDataLength = len(data)
    print("Espacio necesario: ",globalDataLength)
    print("Espacio disponible:", total)
    if total < globalDataLength:
        print("Este mazo no tiene capacidad suficiente")
        exit(0)
    else:
        print("Ok, escribiendo.")
    processedDataLength = 0
    dataReader = DataBuffer(data)
    end = False
    pendingUpdates = { "imagesUpdates" : [], "flagsUpdates" : [] }
    for card in media:
        if USE_IMAGES:
            for photo in card:
                if photo["estimacion"] < 0:
                    print("Estimando: ", photo["name"])
                    photo["estimacion"] = stegoImage.estimate(rutaBase + photo["name"])
                readData = dataReader.getNext(photo["estimacion"])
                readDataLength = readData[1]
                processedDataLength += readDataLength
                readData = readData[0]
                print("readDatalength...: ", readDataLength, len(readData))
                if readDataLength < photo["estimacion"]:
                    end = True
                if readDataLength > 0:
                    print("Escribiendo:", photo['name'])
                    result = codificar(rutaBase, photo["index"], photo["name"], readData, password)
                    if result:
                        pendingUpdates["imagesUpdates"].append(result)
                    else:
                        print("photo problem detected:", photo["name"], "index:", photo["index"])
                        dataReader.goBack(readDataLength)
                        processedDataLength -= readDataLength
                        end = False
                if end:
                    break
        if end:
            break

    if USE_FLAGS and processedDataLength < globalDataLength and flags:
        readData = dataReader.getNext(len(flags))
        readDataLength = readData[1]
        processedDataLength += readDataLength
        readData = readData[0]
        if readDataLength < len(flags):
            tmpFlags = flags[:readDataLength]
            newFlags = stegoFlags.encode(tmpFlags, readData, password)
        else:
            newFlags = stegoFlags.encode(flags, readData, password)
            
        if newFlags and len(newFlags) < len(flags):
            newFlags = newFlags + flags[readDataLength:]

        if newFlags:
            pendingUpdates["flagsUpdates"] = newFlags
        else:
            print("flag problem detected:", flags, "->", newFlags)
            dataReader.goBack(readDataLength)
            processedDataLength -= readDataLength
        
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
                return f.read().hex()
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
    outputKey = "output"

    aw = AnkiWrapper.getInstance()
    if not aw.deckExiste(args[nameDeckKey]):
        print("ERROR. Deck selecionado no existe.")
        print("Decks disponibles:")
        print(aw.getDecks())

    coverKey = "cover"
    if args[coverKey] == '0' or args[coverKey] == '2':
        USE_IMAGES = True
    if args[coverKey] == '1' or args[coverKey] == '2':
        USE_FLAGS = True

    if args[opModeKey] == opModes[0]:
        #Modo encode
        data = args[dataKey]
        password = args[passwordKey]
        nameDeck = args[nameDeckKey]
        data = prepareData(data)
        media = prepareMedia(args[mediaKey])
        if encodeDeck(nameDeck, data, password, media):
            print("Info saved correctly")
        else:
            print("All data could not be written")
            print("Use estimate function to know about limits of this deck")         
    elif args[opModeKey] == opModes[1]:
        #Modo decode
        password = args[passwordKey]
        nameDeck = args[nameDeckKey]
        output = args[outputKey]
        data = decodeDeck(nameDeck, password)
        if data and len(data) > 0:
            if output:
                try:
                    with open(output, 'wb') as f:
                        f.write(bytearray.fromhex(data))
                        f.flush()
                except Exception as e:     
                    print("Output file could not be written ->", output)
                    print("Check file permissions.")
            else:
                print(data)
    elif args[opModeKey] == opModes[2]:
        #modo estimate
        nameDeck = args[nameDeckKey]
        outputMedia = False
        if args[outputMediaKey]:
            outputMedia = args[outputMediaKey]
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
