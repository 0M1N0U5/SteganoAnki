from ankipandas import Collection
from ankipandas import AnkiDataFrame
import ankipandas
import UtilesAnki

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
            self.cards_Raw = ankipandas.raw.get_table(self.col.db, "cards")
            self.notes_Raw = ankipandas.raw.get_table(self.col.db, "notes")
    
    def __del__(self):
        self.col.db.close()


    def get_Decks(self):
        return self.cards.list_decks()

    def get_Cards_from_Deck(self, NombreMazo):
        Mazo_Selecionado = self.cards[self.cards['cdeck'] == NombreMazo]
        Mazo_Selecionado_Raw = self.cards_Raw[self.cards_Raw.id.isin(Mazo_Selecionado.cid)]
        return Mazo_Selecionado_Raw

    def get_Notes_from_Deck(self, NombreMazo):
        Mazo_Selecionado = self.cards[self.cards['cdeck'] == NombreMazo]
        ID_Notas = Mazo_Selecionado.nid
        Notas_Selecionadas = self.notes_Raw[self.notes.id.isin(ID_Notas)]
        return Notas_Selecionadas


    def Update_cards(self):
        return ankipandas.raw.set_table(self.col.db,self.cards_Raw,"cards","update")

    def Update_notes(self):
        return ankipandas.raw.set_table(self.col.db,self.notes_Raw,"notes","update")


    def Update_col_cards(self, NombreCol, Mazo_Para_Actualizar):
        self.cards_Raw[NombreCol] = Mazo_Para_Actualizar[NombreCol].combine_first(self.cards_Raw[NombreCol]).astype(type(self.cards_Raw[NombreCol][0]))
        return self.Update_cards()
    
    def Update_row_notes(self, index, Nueva_Entrada):
        NuevaRespuesta_Cadena = UtilesAnki.Codificar_flds(Nueva_Entrada)
        self.notes_Raw.at[index,"flds"] = NuevaRespuesta_Cadena
        self.notes_Raw.at[index, "sfld"] = Nueva_Entrada[0]
        self.notes_Raw.at[index, "csum"] = UtilesAnki.Calcular_CSUM(Nueva_Entrada[0])
        return self.Update_notes()

    

    

