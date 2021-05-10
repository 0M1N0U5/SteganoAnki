import re
import utils
# ([^\[^\<]+)*(<img src=\"([^\"]+)\">)*(\[sound:([^\]]+)\])*

text = 'Texto1<img src="Jose-madrid.jpg">Texto2<img src="Jose-madrid2.jpg">[sound:ImaTurnItUp1.mp3][sound:ImaTurnItUp2.mp3]<img src="Jose-madrid3.jpg">'
print(utils.processCardText(text))
exit(0)





