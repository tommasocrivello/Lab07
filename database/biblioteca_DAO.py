from database.DB_connect import DBConnect
from model.biblioteca_DTO import Biblioteca

"""
    Biblioteca DAO
    Gestisce le operazioni di accesso al database relative alle biblioteche (Effettua le Query).
"""

class BibliotecaDAO:
    def __init__(self):
        pass

    # TODO
    def get_biblioteche(self):
        db = DBConnect()
        cnx = db.get_connection()
        result = []
        if cnx is not None:
            cursor = cnx.cursor()
            # 1. Chiediamo tutte le colonne, non solo il nome
            cursor.execute("SELECT * FROM biblioteca")

            for row in cursor:
                # 2. Spacchettiamo la tupla e istanziamo l'oggetto DTO
                bibl = Biblioteca(*row)
                result.append(bibl)

            cursor.close()
            cnx.close()
            return result
        else:
            print("Could not connect")
            return None