import orquestador

def main():

    mensaje = "Soy un mensaje super secreto!. Nadie deberia poder leerme..."
    password = "contrasenya_secreta"
    nombreMazo = "Gonzalo"

    orquestador.inicio(mensaje, password, nombreMazo)

if __name__ == "__main__":
    main()