import imageStego
import utils

maxSize = imageStego.estimate("gonzalo-madrid-25.png")
print("maxSize:", maxSize)

print("Codificando imagen")
mensaje = "PacoPaco"
print("Data: ", utils.stringToHex(mensaje))
imageStego.encode("gonzalo-madrid.jpg", mensaje, "password123", "gonzalo-madrid-JPG.png")
print("Imagen codificada")

data = imageStego.decode("gonzalo-madrid-JPG.png", "password123")
print("Data: ", data)
print("Imagen decodificada")