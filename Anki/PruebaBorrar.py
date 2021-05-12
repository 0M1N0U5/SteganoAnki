from ankiwrapper import AnkiWrapper
import utils
import stegoFlags

def calcularRequisitosMensaje(mensaje):
    capacidadMaxima = stegoFlags.estimate()
    return len(mensaje)/capacidadMaxima

def main():
    aw = AnkiWrapper()
    nombreMazo = "Gonzalo"
    flags = aw.devolverFlagsMazo(nombreMazo)
    print(flags)
    mensaje = utils.stringToHex("ho")
    password = "password"
    rowsNecesarias = int(calcularRequisitosMensaje(mensaje))+1
    listaMensaje = [mensaje[start:start+1] for start in range(0, len(mensaje), 1)]
    print(listaMensaje)

    if flags.size < rowsNecesarias:
        print("ERROR: Mensaje demasiado grande para el mazo")
    else:
        for i in range(0,len(listaMensaje)):
            print("FLag:",flags.iloc[i])
            nuevaFlag = stegoFlags.encode(flags.iloc[i],listaMensaje[i],password)
            if not nuevaFlag:
                print("Ya existe un mensaje codificado!")
                exit(0)
            flags.iloc[i] = stegoFlags.encode(flags.iloc[i],listaMensaje[i],password)
        
        aw.guardarFlagsMazo(nombreMazo, flags)
        print(aw.cardsRaw)

    



def luego(flags):
    Necesarios = 3
    for i in range(0,Necesarios):
        flags.iloc[i] = ModuloSofia(flags.iloc[i])

    print("Resultado")
    print(flags)

    aw.guardarFlagsMazo("PORRO", flags)

main()