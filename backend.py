import sqlite3

class Database():
    def __init__(self):
        con = sqlite3.connect("Image-Repository.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS images(id INTEGER AUTO_INCREMENT, name TEXT, img BLOB, PRIMARY KEY(id))")
        con.commit()
        con.close()

    def insert(self, filename, image):
        #print(filename, image)
        con = sqlite3.connect("Image-Repository.db")
        cur = con.cursor()
        cur.execute("INSERT INTO images(name, img) VALUES(?,?)", (filename, sqlite3.Binary(image)))
        con.commit()
        con.close()

    def view(self):
        con = sqlite3.connect("Image-Repository.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM images")
        rows = cur.fetchall()
        con.close()
        return rows