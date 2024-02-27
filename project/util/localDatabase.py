import sqlite3
import uuid

class LocalDatabase():
    def __init__(self):
        self.create_Tables()

    def get_Database(self):
        db = sqlite3.connect("databases/LocalData.db")
        return db

    def generate_Client_ID(self, name):
        client_id = str(uuid.uuid4())  # Generate a UUID and convert it to string
        db = self.get_Database()
        c = db.cursor()
        # Check if a record with the same name already exists
        c.execute('''SELECT * FROM ClientData WHERE name = ?''', (name,))
        existing_record = c.fetchone()

        # If no record with the same name exists, insert the new record
        if existing_record is None:
            c.execute("INSERT INTO ClientData (name, clientID) VALUES (?,?)", (name, client_id))
            print("Record inserted successfully.")
        else:
            print("A record with the same name already exists.")

        db.commit()
        db.close()

        return True

    def retrieve_clientID(self, name):
        db = self.get_Database()
        c = db.cursor()
        c.execute("SELECT clientID FROM clientData WHERE name = ?", (name,))
        result = c.fetchone()
        db.close()
        return str(result[0])

    def create_Tables(self):
        db = self.get_Database()
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS ClientData 
        (id INTEGER PRIMARY KEY, name TEXT, clientID TEXT);""")

        db.commit()
        db.close()