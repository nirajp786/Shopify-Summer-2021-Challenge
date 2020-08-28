import sqlite3

class Database():
    def __init__(self):
        con = sqlite3.connect("Image-Repository.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS images(id INTEGER AUTO_INCREMENT PRIMARY KEY, name STRING, img BLOB)")
        con.commit()
        con.close()

    def insert(self, filename, image):
        con = sqlite3.connect("Image-Repository.db")
        cur = con.cursor()
        cur.execute("INSERT INTO images(name, img) VALUES(?,?)", filename, image)
        con.commit()
        con.close()

    def view(self):
        con = sqlite3.connect("Image-Repository.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM Image-Repository")
        rows = cur.fetchall()
        con.close()
        return rows