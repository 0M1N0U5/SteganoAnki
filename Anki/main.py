from ankiwrapper import AnkiWrapper
import os
import pathlib
import stegoImage
import re
import utils


def decodificar2(RutaImagen, Contrasenya):
    data = stegoImage.decode(RutaImagen, Contrasenya)
    print("Resultado: ", utils.hexToString(data))
    print("Imagen decodificada")
def Codificar2(RutaImagen, Mensaje, Contrasenya, NuevaRutaImagen):
    return  stegoImage.encode(RutaImagen, Mensaje, Contrasenya, NuevaRutaImagen) 

def decodificar(nombreImagen, contrasenya):
    aw = AnkiWrapper.getInstance()
    return stegoImage.decode(aw.ruta_base+nombreImagen, contrasenya)


def codificar(index, nombreImagen, mensaje, contrasenya, mensajeOriginal):
    aw = AnkiWrapper.getInstance()
    rutaBase = aw.ruta_base
    nuevoNombreImagen = modificarNombre(nombreImagen)

    stegoImage.encode(rutaBase+nombreImagen, mensaje, contrasenya, rutaBase+nuevoNombreImagen) 
    return aw.Update_row_notes(index, mensajeOriginal.replace(nombreImagen, nuevoNombreImagen))

def modificarNombre(nombreImagen):
    index = nombreImagen.rfind(".")
    return nombreImagen[:index] + "_.png"


def Prueba1():
    rutaBase = "/Users/gonzalo/Library/Application Support/Anki2/Esteganografia/collection.media/"

    Codificar(rutaBase+"Jose-madrid.png", utils.stringToHex("hola"), "contra", rutaBase+"Jose-madrid_MOD.png") 
    print(decodificar(rutaBase+"Jose-madrid_MOD.png", "contra"))


def analizarCard(card):
    aw = AnkiWrapper.getInstance()
    print(card.flds)
    Objetos_carta = utils.processCardText(card.flds)
    respuesta = []
    for i in Objetos_carta['images']:
        respuesta.append({i: stegoImage.estimate(aw.ruta_base + i)})
    return respuesta

def main():
    aw = AnkiWrapper()
    mazo = aw.get_Notes_from_Deck("Gonzalo")
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


def Prueba_Decodificar():
    aw = AnkiWrapper.getInstance()
    mazo = aw.get_Notes_from_Deck("Gonzalo")
    print(mazo)
    row = mazo.iloc[1]
    print(row)
    Nuevo_mensaje = row[6]

    Objetos_carta = utils.processCardText(row[6])

    RutaImagen = aw.Obtener_ruta_media(Objetos_carta['images'][0])
    NuevaRutaImagen = Modificar_Nombre(RutaImagen)

    print(RutaImagen)
    print(decodificar(RutaImagen, "Contrasenya"))



def PruebaCodificar():
    aw = AnkiWrapper()
    mazo = aw.get_Notes_from_Deck("Gonzalo")
    row = mazo.iloc[1]
    Nuevo_mensaje = row[6]

    Objetos_carta = utils.processCardText(row[6])

    RutaImagen = aw.Obtener_ruta_media(Objetos_carta['images'][0])
    NuevaRutaImagen = Modificar_Nombre(RutaImagen)

    print(Codificar(RutaImagen, utils.stringToHex("Esto es un mensaje:)"), "Contrasenya", str(NuevaRutaImagen)))
    aw.Update_row_notes(row.name, Nuevo_mensaje.replace(Objetos_carta['images'][0],NuevaRutaImagen.name))
    #print(aw.get_Notes_from_Deck("Gonzalo"))


if __name__ == "__main__":
    main()