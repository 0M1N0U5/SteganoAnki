from ankiwrapper import AnkiWrapper
import imageStego
import re


def decodificar(RutaImagen, Contrasenya):
    data = imageStego.decode(RutaImagen, Contrasenya)
    print("Data: ", data)
    print("Imagen decodificada")

def Codificar(RutaImagen, Mensaje, Contrasenya):
    maxSize = imageStego.estimate(RutaImagen)
    imageStego.encode(RutaImagen, Mensaje, Contrasenya, RutaImagen)
    print("Imagen codificada")

def Busqueda_multimedia(mazo, tipo):
    resultado = []
    if tipo == "img":
        patron = '<img src="([^"]+)">'
    elif tipo == "mp3":
        patron = '[sound:([^"]+)]'
    elif tipo =="todo":
        patron = '([^\[^\<]+)*(<img src=\"([^\"]+)\">)*(\[sound:([^\]]+)\])*'
    
    for i in mazo.flds:
        r = re.findall(patron,i)
        if r : resultado.extend(r)
    return resultado


def main():
    aw = AnkiWrapper()
    mazo = aw.get_Notes_from_Deck("Gonzalo")
    array_resultado = Busqueda_multimedia(mazo, 'img')
    print(array_resultado)
    rutaImagen = aw.Obtener_ruta_media(array_resultado[3])
    print(rutaImagen)

    Mensaje = "hola este es un mensaje"
    Contrasenya = "halamadrid13"

    Codificar(rutaImagen, Mensaje, Contrasenya)
    decodificar(rutaImagen, Contrasenya)
    



if __name__ == "__main__":
    main()