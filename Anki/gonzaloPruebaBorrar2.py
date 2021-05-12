from ankiwrapper import AnkiWrapper
import stegoFlags

aw = AnkiWrapper()

flags = aw.devolverFlagsMazo("PORRO")

print(flags)

def ModuloSofia(flag):
    return 3

Necesarios = 3
for i in range(0,Necesarios):

    flags.iloc[i] = ModuloSofia(flags.iloc[i])

print("Resultado")
print(flags)

aw.guardarFlagsMazo("PORRO", flags)
