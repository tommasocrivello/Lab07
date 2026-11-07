from database.DB_connect import DBConnect
from model.libro_DTO import Libro

"""
    LIBRO DAO
    Gestisce le operazioni di accesso al database relative ai libri (Effettua le Query).
"""

class LibroDAO:
    def __init__(self):
        pass

    # TODO
    def get_generi(self):
        db = DBConnect()
        cnx = db.get_connection()
        result = []
        if cnx is not None:
            cursor = cnx.cursor()
            # Estraiamo i generi senza doppioni
            cursor.execute("SELECT DISTINCT genere FROM libro")

            for row in cursor:
                result.append(row[0])  # È una singola stringa, non serve spacchettare in un DTO

            cursor.close()
            cnx.close()
            return result
        else:
            print("Could not connect")
            return None

    def get_libri_filtrati(self, genere, id_biblioteca):
        db = DBConnect()
        cnx = db.get_connection()
        result = []
        if cnx is not None:
            cursor = cnx.cursor()

            # La query con COALESCE gestisce i filtri opzionali
            query = """SELECT * 
                       FROM libro 
                       WHERE genere = COALESCE(%s, genere) 
                       AND id_biblioteca = COALESCE(%s, id_biblioteca)"""

            # Eseguiamo la query passando i parametri (che possono essere stringhe, interi o None)
            cursor.execute(query, (genere, id_biblioteca))

            for row in cursor:
                libro = Libro(*row)  # Spacchettiamo la tupla nel DTO Libro
                result.append(libro)

            cursor.close()
            cnx.close()
            return result
        else:
            print("Could not connect")
            return None