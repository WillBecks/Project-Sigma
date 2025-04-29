import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host, database, user, password, port=3306):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port  # Specify the port separately
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error while connecting to MySQL: {e}")
            self.connection = None

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")


class GebruikerDAO:
    def __init__(self, db: Database):
        self.db = db

    def create_gebruiker(self, naam, familienaam, email, wachtwoord, straat, postcode, straatnr, gemeente):
        cursor = None  # Initialize cursor here to ensure proper handling of errors
        try:
            if not self.db.connection:  # If connection is None, return early
                print("No database connection")
                return

            cursor = self.db.connection.cursor()
            query = """
                INSERT INTO gebruiker (naam, familienaam, `e-mail`, wachtwoord, straat, postcode, straatnr, gemeente)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (naam, familienaam, email, wachtwoord, straat, postcode, straatnr, gemeente))
            self.db.connection.commit()
            print("Gebruiker toegevoegd.")
        except Error as e:
            print(f"Fout bij toevoegen gebruiker: {e}")
        finally:
            if cursor:
                cursor.close()  # Close cursor only if it was created

    def get_all_gebruikers(self):
        cursor = None
        try:
            if not self.db.connection:
                print("No database connection")
                return []

            cursor = self.db.connection.cursor(dictionary=True)
            query = "SELECT * FROM gebruiker"
            cursor.execute(query)
            return cursor.fetchall()
        except Error as e:
            print(f"Fout bij ophalen gebruikers: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def get_gebruiker_by_id(self, idgebruiker):
        cursor = None
        try:
            if not self.db.connection:
                print("No database connection")
                return None

            cursor = self.db.connection.cursor(dictionary=True)
            query = "SELECT * FROM gebruiker WHERE idgebruiker = %s"
            cursor.execute(query, (idgebruiker,))
            return cursor.fetchone()
        except Error as e:
            print(f"Fout bij ophalen gebruiker: {e}")
            return None
        finally:
            if cursor:
                cursor.close()

    def update_gebruiker(self, idgebruiker, naam, familienaam, email, wachtwoord, straat, postcode, straatnr, gemeente):
        cursor = None
        try:
            if not self.db.connection:
                print("No database connection")
                return

            cursor = self.db.connection.cursor()
            query = """
                UPDATE gebruiker
                SET naam=%s, familienaam=%s, `e-mail`=%s, wachtwoord=%s, straat=%s, postcode=%s, straatnr=%s, gemeente=%s
                WHERE idgebruiker=%s
            """
            cursor.execute(query, (naam, familienaam, email, wachtwoord, straat, postcode, straatnr, gemeente, idgebruiker))
            self.db.connection.commit()
            print("Gebruiker bijgewerkt.")
        except Error as e:
            print(f"Fout bij bijwerken gebruiker: {e}")
        finally:
            if cursor:
                cursor.close()

    def delete_gebruiker(self, idgebruiker):
        cursor = None
        try:
            if not self.db.connection:
                print("No database connection")
                return

            cursor = self.db.connection.cursor()
            query = "DELETE FROM gebruiker WHERE idgebruiker = %s"
            cursor.execute(query, (idgebruiker,))
            self.db.connection.commit()
            print("Gebruiker verwijderd.")
        except Error as e:
            print(f"Fout bij verwijderen gebruiker: {e}")
        finally:
            if cursor:
                cursor.close()


# Voorbeeld gebruik:
if __name__ == "__main__":
    db = Database(host="127.0.0.1", database="mydb", user="root", password="Willem2007")

    gebruiker_dao = GebruikerDAO(db)

    # Voeg een gebruiker toe (voorbeeld)
    gebruiker_dao.create_gebruiker(
        naam="Mauro",
        familienaam="Vilroxk",
        email="maurovilroxk@telenet.be",
        wachtwoord="De hond 007",
        straat="Hondenwijk",
        postcode="3900",
        straatnr="34",
        gemeente="Pelt"
    )

    # Haal alle gebruikers op
    gebruikers = gebruiker_dao.get_all_gebruikers()
    print(gebruikers)

    db.close()
