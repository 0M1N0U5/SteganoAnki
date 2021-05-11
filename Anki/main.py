from ankiwrapper import AnkiWrapper
import os
import pathlib
import stegoImage
import re
import utils

def decodificar(nombreImagen, contrasenya):
    aw = AnkiWrapper.getInstance()
    return stegoImage.decode(aw.rutaBase+nombreImagen, contrasenya)


def codificar(index, nombreImagen, mensaje, contrasenya, mensajeOriginal):
    aw = AnkiWrapper.getInstance()
    rutaBase = aw.rutaBase
    nuevoNombreImagen = modificarNombre(nombreImagen)

    stegoImage.encode(rutaBase+nombreImagen, mensaje, contrasenya, rutaBase+nuevoNombreImagen) 
    return aw.updateRowNotes(index, mensajeOriginal.replace(nombreImagen, nuevoNombreImagen))

def modificarNombre(nombreImagen):
    index = nombreImagen.rfind(".")
    return nombreImagen[:index] + "_.png"


def analizarCard(card):
    aw = AnkiWrapper.getInstance()
    Objetos_carta = utils.processCardText(card.flds)
    respuesta = []
    for i in Objetos_carta['images']:
        respuesta.append({i: stegoImage.estimate(aw.rutaBase + i)})
    return respuesta

def main():
    aw = AnkiWrapper()
    mazo = aw.getNotesFromDeck("Gonzalo")
    card = mazo.loc[482]
    analisis = analizarCard(card)
    #Decidir con analisis
    nombre = list(analisis[0].keys())[0] #Nombre
    valor = analisis[0][list(analisis[0].keys())[0]] #Valor
    print(nombre)
    print(valor)
    for i in analisis:
        print(list(i.keys())[0]) #NOMBRE
        print(i[list(i.keys())[0]]) #VALOR

    codificar(card.name, nombre, utils.stringToHex("HolaXD"), "password", card.flds)
    decodificar(nombre, "password")
    print(mazo)


if __name__ == "__main__":
    main()