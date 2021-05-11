from numpy import can_cast
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


def analizarCard(index, campoFlds, estimacionReal=False): #Por ahora solo imagenes
    aw = AnkiWrapper.getInstance()
    Objetos_carta = utils.processCardText(campoFlds)
    respuesta = []
    for i in Objetos_carta['images']:
        print("Realizando estimación a la imagen: " +i+"...")
        estimacion = stegoImage.estimate(aw.rutaBase + i) #¡¡¡Cuello de botella!!!
        print("...Terminada la estimación!")
        #estimacion = stegoImage.estimate(aw.rutaBase + i) if estimacionReal else 500 
        respuesta.append({i: [estimacion, index]})
    return respuesta


def inicio(mensaje, password, nombreMazo):
    print("hola")

def main():
    nombreMazo = "Gonzalo"
    mensaje = utils.stringToHex("Hola, este es un mensaje:)")
    aw = AnkiWrapper()
    mazo = aw.getNotesFromDeck(nombreMazo)
    print(mazo)
    print("---")
    print("Calcular")
    resultado = buscarImagenesMazo(mazo)
    print(resultado)
    print(len(resultado))
    sizeMensaje = len(mensaje)
    for i in resultado:
        for x in i:
            for key in x:
                print(key)
    #Mirar 
    
def buscarImagenesMazo(mazo):
    lista = []
    for index, row in mazo.iterrows():
        resultadoAnalisis = analizarCard(row.name, row.flds)
        if len(resultadoAnalisis) != 0:
            lista.append(resultadoAnalisis)
    return lista


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