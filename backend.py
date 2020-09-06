import psycopg2
import datetime
class Database():
    connection_details = ""
    def __init__(self):
        con = psycopg2.connect(self.connection_details)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS images(id SERIAL PRIMARY KEY, name TEXT, img BYTEA, date_time DATE default NULL)")
        con.commit()
        con.close()

    def insert(self, filename, image):
        #print(filename, image)
        dt = datetime.datetime.date(datetime.datetime.now())
        con = psycopg2.connect(self.connection_details)
        cur = con.cursor()
        #cur.execute("INSERT INTO images VALUES (NULL,?,?)", (filename, image))
        cur.execute("INSERT INTO images(name, img, date_time) VALUES(%s,%s, %s)", (filename, image, dt))
        con.commit()
        con.close()

    def view(self):
        con = psycopg2.connect(self.connection_details)
        cur = con.cursor()
        cur.execute("SELECT * FROM images")
        rows = cur.fetchall()
        con.close()
        return rows
    
    def delete(self, id):
        con = psycopg2.connect(self.connection_details)
        cur = con.cursor()
        cur.execute("DELETE FROM images WHERE id=%s", (id,))
        con.commit()
        con.close()
        
    def update(self, id, image):
        con = psycopg2.connect(self.connection_details)
        cur = con.cursor()
        cur.execute("UPDATE images SET img = %s WHERE id = %s", (image, id))
        con.commit()
        con.close()