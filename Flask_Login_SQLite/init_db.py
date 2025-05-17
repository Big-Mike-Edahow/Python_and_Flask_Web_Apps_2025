# init_db.py

import sqlite3

conn = sqlite3.connect("./data/database.db")
curs = conn.cursor()

with open("schema.sql") as f:
    conn.executescript(f.read())

curs.execute("INSERT INTO users(username, password) VALUES('mike', 'foobar')")

conn.commit()
conn.close()
