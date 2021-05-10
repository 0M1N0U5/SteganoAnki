import imageStego
import utils

maxSize = imageStego.estimate("gonzalo-madrid-25.png")
print("maxSize:", maxSize)

#print("Codificando imagen")
mensaje = "PacoPaco"
print("Codificando datos:", utils.stringToHex(mensaje))
imageStego.encode("gonzalo-madrid.jpg", utils.stringToHex(mensaje), "password123", "gonzalo-madrid-JPG.png")
print("Imagen codificada")
data = imageStego.decode("gonzalo-madrid-JPG.png", "password123")
print("Imagen decodificada")
print("Data decodificada:", data)

print("Codificando imagen")
print("Codificando datos:", utils.stringToHex(mensaje))
imageStego.encode("anki.svg.png", utils.stringToHex(mensaje), "password123", "anki_stego.svg.png")
print("Imagen codificada")
print("Imagen decodificando")
data = imageStego.decode("anki_stego.svg.png", "password123")
print("Data decodificada:", data)
