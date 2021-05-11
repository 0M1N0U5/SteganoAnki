from ankiwrapper import AnkiWrapper
import os
import pathlib
import stegoImage
import re
import utils

def decodificar(nombreImagen, password):
    aw = AnkiWrapper.getInstance()
    return stegoImage.decode(aw.rutaBase+nombreImagen, password)


def codificar(index, nombreImagen, mensaje, password, mensajeOriginal):
    aw = AnkiWrapper.getInstance()
    rutaBase = aw.rutaBase
    nuevoNombreImagen = modificarNombre(nombreImagen)

    stegoImage.encode(rutaBase+nombreImagen, mensaje, password, rutaBase+nuevoNombreImagen) 
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



def inicio(mensaje, password, nombreMazo):
    print("hola")

def main():
    nombreMazo = "Mazo_Gonzalo"
    aw = AnkiWrapper()
    mazo = aw.getNotesFromDeck(nombreMazo)
    buscarImagenesMazo(mazo)
    
def buscarImagenesMazo(mazo):
    print(type(mazo))
    for index, row in mazo.iterrows():
        print("-")
        print(row.flds)



def calcularTamanyoNecesario(mensaje):
    print("voy a calcular tamañyo")
    taman = utils.stringToHex(mensaje)
    print(len(taman))



######
#Pruebas... luego borrar!
######
def Prueba_Calcular_Foto_LOqueAguantaxd():
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

def Prueba_Codificar_Y_Descodificar():
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


main()