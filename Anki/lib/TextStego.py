from lib.ankiwrapper import AnkiWrapper
import lib.UtilesAnki as UtilesAnki

aw = AnkiWrapper()

def Insertar_Caracter_Invisible(Entrada):
    Entrada_texto = Entrada[6]
    Lista_Entrada = UtilesAnki.Decodificar_flds(Entrada_texto)
    Lista_Entrada[0] = "." + Lista_Entrada[0] + "\u200b"
    Lista_Entrada[1] = "\u200b" + Lista_Entrada[1] + "\u200b"
    aw.Update_row_notes(Entrada.name, Lista_Entrada)
    #aw.Update_row_notes()
    #Detectar_Caracter_Invisible(Entrada)

def Detectar_Caracter_Invisible(Entrada):
    Entrada_texto = Entrada[6]
    print()
    print(bytes(Entrada_texto,'utf-8'))
    Lista_Entrada = UtilesAnki.Decodificar_flds(Entrada_texto)
    Prueba = Lista_Entrada[0].find('\u200b')
    print(Prueba)

def Pruebas():
    Entrada_con = "Prueba" + '\u0000'
    Entrada_sin = "Prueba" 
    Comprobar = "Holaaaa2HolaaaaHolaaaaFront9"
    print( bytes(Entrada_con, 'utf-8'))
    print( bytes(Entrada_sin, 'utf-8'))
    print( bytes(Comprobar, 'utf-8'))

def amain():
    mazo = aw.get_Notes_from_Deck("Gonzalo")
    Entrada = mazo.iloc[-3]
    print(Entrada)
    print()
    print(Entrada[6])
    

def main():
    mazo = aw.get_Notes_from_Deck("Gonzalo")
    Entrada = mazo.iloc[-3]
    print(Entrada)
    Insertar_Caracter_Invisible(Entrada)
    print(Entrada)
    Detectar_Caracter_Invisible(Entrada)


"""CREATE TABLE col (
    id              integer primary key,
      -- arbitrary number since there is only one row
    crt             integer not null,
      -- timestamp of the creation date in second. It's correct up to the day. For V1 scheduler, the hour corresponds to starting a new day. By default, new day is 4.
    mod             integer not null,
      -- last modified in milliseconds
    scm             integer not null,
      -- schema mod time: time when "schema" was modified. 
      --   If serner scm is different from the client scm a full-sync is required
    ver             integer not null,
      -- version
    dty             integer not null,
      -- dirty: unused, set to 0
    usn             integer not null,
      -- update sequence number: used for finding diffs when syncing. 
      --   See usn in cards table for more details.
    ls              integer not null,
      -- "last sync time"
    conf            text not null,
      -- json object containing configuration options that are synced
    models          text not null,
      -- json array of json objects containing the models (aka Note types)
    decks           text not null,
      -- json array of json objects containing the deck
    dconf           text not null,
      -- json array of json objects containing the deck options
    tags            text not null
      -- a cache of tags used in the collection (This list is displayed in the browser. Potentially at other place)
);"""

main()
