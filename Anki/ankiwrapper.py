from ankipandas import Collection
from ankipandas import AnkiDataFrame
import ankipandas
import UtilesAnki
import pathlib

class AnkiWrapper:
    __instance = None

    @staticmethod 
    def getInstance():
        if AnkiWrapper.__instance == None:
            AnkiWrapper()
        return AnkiWrapper.__instance

    def __init__(self):
        if AnkiWrapper.__instance != None:
            raise Exception("ERROR. Usa getInstance() para no crear otra instancia.")
        else:
            AnkiWrapper.__instance = self
            self.col = Collection()
            self.cards = self.col.cards
            self.notes = self.col.notes
            self.cardsRaw = ankipandas.raw.get_table(self.col.db, "cards")
            self.notesRaw = ankipandas.raw.get_table(self.col.db, "notes")
            self.rutaBase = self.obtenerRutaBase()
    
    def __del__(self):
        self.col.db.close()


    def getDecks(self):
        return self.cards.list_decks()

    def getCardsFromDeck(self, nombreMazo):
        mazoSelecionado = self.cards[self.cards['cdeck'] == nombreMazo]
        mazoSelecionadoRaw = self.cardsRaw[self.cardsRaw.id.isin(mazoSelecionado.cid)]
        return mazoSelecionadoRaw

    def getNotesFromDeck(self, nombreMazo):
        mazoSelecionado = self.cards[self.cards['cdeck'] == nombreMazo]
        idNotas = mazoSelecionado.nid
        notasSelecionadas = self.notesRaw[self.notes.id.isin(idNotas)]
        return notasSelecionadas


    def updateCards(self):
        return ankipandas.raw.set_table(self.col.db,self.cardsRaw,"cards","update")

    def updateNotes(self):
        return ankipandas.raw.set_table(self.col.db,self.notesRaw,"notes","update")


    def updateColCards(self, nombreCol, mazoActualizar):
        self.cardsRaw[nombreCol] = mazoActualizar[nombreCol].combine_first(self.cardsRaw[nombreCol]).astype(type(self.cardsRaw[nombreCol][0]))
        return self.updateCards()
    
    def updateRowNotes(self, index, nuevaEntrada):
        if isinstance(nuevaEntrada, str):
            nuevaRespuestaLista = UtilesAnki.Decodificar_flds(nuevaEntrada)
            nuevaRespuestaCadena = nuevaEntrada
        else:
            nuevaRespuestaCadena = UtilesAnki.Codificar_flds(nuevaEntrada)
            nuevaRespuestaLista = nuevaEntrada
        self.notesRaw.at[index,"flds"] = nuevaRespuestaCadena
        self.notesRaw.at[index, "sfld"] = nuevaRespuestaLista[0]
        self.notesRaw.at[index, "csum"] = UtilesAnki.Calcular_CSUM(nuevaRespuestaLista[0])
        return self.updateNotes()

 
    def obtenerRutaBase(self):
        rutaDB = ankipandas.paths.db_path_input()
        rutaPartes = list(rutaDB.parts)
        rutaPartes[-1] = 'collection.media'
        return str(pathlib.Path(*rutaPartes))+"/"

    

