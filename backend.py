import psycopg2
import datetime
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'

load_dotenv(dotenv_path=env_path)

class Database():
    connection_details = "dbname="+os.getenv("DBNAME") + " user=" + os.getenv("USER") + " password=" +  os.getenv("PASSWORD") + " host=" + os.getenv("HOST") +  " port=" + os.getenv("PORT")
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