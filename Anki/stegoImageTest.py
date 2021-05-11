import stegoImage
import utils

maxSize = stegoImage.estimate("gonzalo-madrid-25.png")
print("maxSize:", maxSize)

#print("Codificando imagen")
mensaje = "PacoPaco"
print("Codificando datos:", utils.stringToHex(mensaje))
stegoImage.encode("gonzalo-madrid.jpg", utils.stringToHex(mensaje), "password123", "gonzalo-madrid-JPG.png")
print("Imagen codificada")
data = stegoImage.decode("gonzalo-madrid-JPG.png", "password123")
print("Imagen decodificada")
print("Data decodificada:", data)

print("Codificando imagen")
print("Codificando datos:", utils.stringToHex(mensaje))
stegoImage.encode("anki.svg.png", utils.stringToHex(mensaje), "password123", "anki_stego.svg.png")
print("Imagen codificada")
print("Imagen decodificando")
data = stegoImage.decode("anki_stego.svg.png", "password123")
print("Data decodificada:", data)

#print("Dibujando mascara")
#stegoImage.drawMask("anki.svg.png", "anki_mask.svg.png")
#print("Mascara dibujada")

#print("Dibujando mascara")
#stegoImage.drawMask("youtube.jpg", "youtube_mask.png")
#print("Mascara dibujada")

#print("Estimando youtube")
#estimate = stegoImage.estimate("youtube.jpg")
#print(estimate)
#estimate = 643041
#info = ""
#for  i in range(estimate):
#    info += "A"

#print("Codificando")
#stegoImage.encode("youtube.jpg", info, "password123", "youtube.png")
#print("Hecho")

from datetime import datetime
print(datetime.now().strftime("%H:%M:%S"))
hilos=8
print("Testing de hilos", hilos)
print(datetime.now().strftime("%H:%M:%S"))
stegoImage.drawMask("gonzalo-madrid.jpg", "gonzalo-madrid_mask.png", hilos)
print(datetime.now().strftime("%H:%M:%S"))

#hilos=8
#print("Testing de hilos", hilos)
#print(datetime.now().strftime("%H:%M:%S"))
#stegoImage.drawMask("gonzalo-madrid.jpg", "gonzalo-madrid_mask.png", hilos)
#print(datetime.now().strftime("%H:%M:%S"))

#hilos=16
#print("Testing de hilos", hilos)
#print(datetime.now().strftime("%H:%M:%S"))
#stegoImage.drawMask("gonzalo-madrid.jpg", "gonzalo-madrid_mask.png", hilos)
#print(datetime.now().strftime("%H:%M:%S"))