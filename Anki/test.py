import re

# ([^\[^\<]+)*(<img src=\"([^\"]+)\">)*(\[sound:([^\]]+)\])*

text = 'Texto1<img src="Jose-madrid.jpg">Texto2<img src="Jose-madrid2.jpg">[sound:ImaTurnItUp1.mp3][sound:ImaTurnItUp2.mp3]<img src="Jose-madrid3.jpg">'
x = re.findall("([^\[^\<]+)*(<img src=\"([^\"]+)\">)*(\[sound:([^\]]+)\])*", text)

images = re.findall("<img src=\"([^\"]+)\">", text)
print(images)
sounds = re.findall("\[sound:([^\]]+)\]", text)
print(sounds)
texts = re.findall("\[sound:([^\]]+)\]", text)
print(texts)

exit(0)




print(x)


fields = { "text" : [], "images" : [], "sounds": [] }

#status = 0 text, status = 1 -> image, status = 2 -> sound
status = 0
for f in x:
    for t in f:
        if t != '':
            print(t)
            print(fields)
        if t.startswith("<img"):
            status = 1
        elif t.startswith("[sound"):
            status = 2
        elif t != '':
            if status == 0:
                fields["text"].append(t)
            elif status == 1:
                fields["images"].append(t)
                status = 0
            elif status == 2:
                fields["sounds"].append(t)
                status = 0

print(fields)


