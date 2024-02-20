import sqlite3

class CharacterDatabase():
    def __init__(self):
        self.create_Tables()

    def get_Database(self):
        db = sqlite3.connect("databases/Characters.db")
        return db

    def add_Character(self, name, skin):
        db = self.get_Database()
        c = db.cursor()
        c.execute("SELECT * from Characters WHERE name = ?", (name,))
        if c.fetchone() is not None:
            c.execute("SELECT * from Characters WHERE name = ?", (name,))
            return False
        else:
            c.execute("INSERT INTO Characters (name, skin) VALUES (?,?)", (name, skin))
            db.commit()
            return True

    def retrieve_Character(self, name):
        db = self.get_Database()
        c = db.cursor()
        c.execute("SELECT id FROM Characters WHERE name = ?", (name,))
        user = c.fetchone()
        return user

    def retrieve_Character_Inventory(self, name):
        db = self.get_Database()
        c = db.cursor()
        for row in c.execute("SELECT * FROM inventories WHERE name = ?", (name,)):
            print(row)

    def add_Item(self, char, item):
        db = self.get_Database()
        c = db.cursor()
        c.execute("INSERT INTO Inventories (name, char) VALUES (?)", (item, char))
        db.commit()

    def remove_Item(self, char, item):
        pass
        # db = self.get_Database()
        # c = db.cursor()
        # c.execute('DELETE FROM Characters WHERE name = ?;', (name,))
        # db.commit()

    def retrieve_Character_Names(self):
        db = self.get_Database()
        c = db.cursor()
        c.execute('SELECT name FROM Characters;')
        s_liste = []
        for s in c:
            s_liste.append((s[0]))
        return s_liste

    def delete_Character(self, name):
        db = self.get_Database()
        c = db.cursor()
        c.execute('DELETE FROM Characters WHERE name = ?;', (name,))
        db.commit()

    def create_Tables(self):
        db = self.get_Database()
        c = db.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS Characters 
        (id INTEGER PRIMARY KEY, name TEXT, skin TEXT, inventory TEXT);""")
        c.execute("""CREATE TABLE IF NOT EXISTS Inventories 
        (id INTEGER PRIMARY KEY, name TEXT, char TEXT);""")

        db.commit()