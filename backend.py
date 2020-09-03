import psycopg2


class Database():
    connection_details = ""
    def __init__(self):
        con = psycopg2.connect(self.connection_details)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS images(id SERIAL PRIMARY KEY, name TEXT, img BYTEA)")
        con.commit()
        con.close()

    def insert(self, filename, image):
        #print(filename, image)
        con = psycopg2.connect(self.connection_details)
        cur = con.cursor()
        #cur.execute("INSERT INTO images VALUES (NULL,?,?)", (filename, image))
        cur.execute("INSERT INTO images(name, img) VALUES(%s,%s)", (filename, image))
        con.commit()
        con.close()

    def view(self):
        con = psycopg2.connect(self.connection_details)
        cur = con.cursor()
        cur.execute("SELECT * FROM images")
        rows = cur.fetchall()
        con.close()
        return rows