import stegoImage
import utils
from datetime import datetime

maxSize = stegoImage.estimate("gonzalo-madrid-25.png")
print("maxSize:", maxSize)

print(datetime.now().strftime("%H:%M:%S"))
hilos=8
print("Testing de hilos", hilos)
print(datetime.now().strftime("%H:%M:%S"))
stegoImage.drawMask("gonzalo-madrid.jpg", "gonzalo-madrid_mask.png", hilos)
print(datetime.now().strftime("%H:%M:%S"))

#print("Codificando imagen")
mensaje = "PacoPaco"
print("Codificando datos:", utils.stringToHex(mensaje))
print(datetime.now().strftime("%H:%M:%S"))
stegoImage.encode("gonzalo-madrid.jpg", utils.stringToHex(mensaje), "password123", "gonzalo-madrid-JPG.png")
print(datetime.now().strftime("%H:%M:%S"))
print("Imagen codificada")
data = stegoImage.decode("gonzalo-madrid-JPG.png", "password123")
print("Imagen decodificada")
print("Data decodificada:", data)

print("Estimando anki.svg.png")
print(datetime.now().strftime("%H:%M:%S"))
estimate = stegoImage.estimate("anki.svg.png")
print(datetime.now().strftime("%H:%M:%S"))
print(estimate)
print("Codificando datos:", utils.stringToHex(mensaje))
print("Codificando imagen")
print(datetime.now().strftime("%H:%M:%S"))
stegoImage.encode("anki.svg.png", utils.stringToHex(mensaje), "password123", "anki_stego.svg.png")
print(datetime.now().strftime("%H:%M:%S"))
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

print("Estimando youtube")
print(datetime.now().strftime("%H:%M:%S"))
estimate = stegoImage.estimate("youtube.jpg")
print(datetime.now().strftime("%H:%M:%S"))
print(estimate)
info = ""
for  i in range(estimate-1):
    info += "A"

print("Codificando")
print(datetime.now().strftime("%H:%M:%S"))
stegoImage.encode("youtube.jpg", info, "password123", "youtube.png")
print(datetime.now().strftime("%H:%M:%S"))
print("Hecho")
print(datetime.now().strftime("%H:%M:%S"))
stegoImage.decode("youtube.png", "password123")
print(datetime.now().strftime("%H:%M:%S"))
print("Decodificado youtube")

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