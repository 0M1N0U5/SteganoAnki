from ankipandas import Collection
from ankipandas import AnkiDataFrame
import ankipandas
import UtilesAnki
import pathlib
import pandas as pd
import sqlite3
import time

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


    def updateColCards(self, nombreCol, mazoActualizar):#Mirar si se actualiza si no arreglar
        self.cardsRaw[nombreCol] = mazoActualizar[nombreCol].combine_first(self.cardsRaw[nombreCol]).astype(type(self.cardsRaw[nombreCol][0]))
        return self.updateCards()

    def updateRowsNotes(self, lista):
        for i in lista:
            #Actualizar Notas
            antiguoFlds = self.notesRaw.loc[i['index']].flds
            nuevaRespuestaCadena = "."+antiguoFlds.replace(i['name'], i['newName']) 
            nuevaRespuestaLista = UtilesAnki.decodificarFlds(nuevaRespuestaCadena)
            self.notesRaw.at[i['index'],"usn"] = -1
            self.notesRaw.at[i['index'],"flds"] = nuevaRespuestaCadena
            self.notesRaw.at[i['index'], "sfld"] = nuevaRespuestaLista[0]
            self.notesRaw.at[i['index'], "csum"] = UtilesAnki.calcularCsum(nuevaRespuestaLista[0])
        self.updateCards()
        self.updateNotes()
        return self.forzarActualizacion()

    def obtenerRutaBase(self):
        rutaDB = ankipandas.paths.db_path_input()
        rutaPartes = list(rutaDB.parts)
        rutaPartes[-1] = 'collection.media'
        return str(pathlib.Path(*rutaPartes))+"/"

    def forzarActualizacion(self):
        tablaCol = self.getTableCol(self.col.db)
        print(tablaCol)
        tablaCol.at[0, 'mod'] = int(time.time()*1000)
        self.setTable(self.col.db, tablaCol, 'update')
    
#Funciones adaptación de:
#https://github.com/klieret/AnkiPandas/blob/aaa7583c38d9dadf2ff6c4ef13bceef50bbfc99d/ankipandas/raw.py
    def getTableCol(self, db) -> pd.DataFrame:
        df = pd.read_sql_query(
            "SELECT * FROM col", db
        )
        return df

    def consolidateTables(self, df: pd.DataFrame, df_old: pd.DataFrame, mode: str, id_column="id"):

        if not list(df.columns) == list(df_old.columns):
            raise ValueError(
                "Columns do not match: Old: {}, New: {}".format(
                    ", ".join(df_old.columns), ", ".join(df.columns)
                )
            )

        old_indices = set(df_old[id_column])
        new_indices = set(df[id_column])

        # Get indices
        # -----------

        if mode == "update":
            indices = set(old_indices)
        elif mode == "replace":
            indices = set(new_indices)
        else:
            raise ValueError(f"Unknown mode '{mode}'.")

        df = df[df[id_column].isin(indices)]

        # Apply
        # -----

        if mode == "update":
            df_new = df_old.copy()
            df_new.update(df)
        elif mode == "replace":
            df_new = df.copy()
        else:
            raise ValueError(f"Unknown mode '{mode}'.")
        return df_new

    def setTable(self, db: sqlite3.Connection, df: pd.DataFrame, mode: str, id_column="id",) -> None:
        df_old = self.getTableCol(db)
        df_new = self.consolidateTables(
            df=df, df_old=df_old, mode=mode, id_column=id_column
        )
        df_new.to_sql("col", db, if_exists="replace", index=False)


