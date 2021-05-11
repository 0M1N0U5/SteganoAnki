import re
from hashlib import sha1

def codificarFlds(Lista_Entrada):
    return '\x1f'.join(Lista_Entrada)

def decodificarFlds(String_Entrada):
    return String_Entrada.split('\x1f')

#Adaptación de:
#https://github.com/weihautin/anki/blob/8f73d3ad55c298f38c56bc88e0bd62aa9a9828dc/anki/utils.py#L278
def calcularCSUM(data):
    reStyle = re.compile("(?s)<style.*?>.*?</style>")
    reScript = re.compile("(?s)<script.*?>.*?</script>")
    reTag = re.compile("<.*?>")
    reEnts = re.compile("&#?\w+;")
    reMedia = re.compile("<img[^>]+src=[\"']?([^\"'>]+)[\"']?[^>]*>")
    ####
    s = reMedia.sub(" \\1 ", data)
    s = reStyle.sub("", s)
    s = reScript.sub("", s)
    s = reTag.sub("", s)
    ####
    html = s.replace("&nbsp;", " ")
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    s = reEnts.sub(fixup, html)
    ####
    return int(sha1(s.encode("utf-8")).hexdigest()[:8], 16)
