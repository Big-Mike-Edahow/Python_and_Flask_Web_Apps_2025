# init_db.py

import sqlite3

conn = sqlite3.connect("./data/database.db")

with open("schema.sql") as f:
    conn.executescript(f.read())

curs = conn.cursor()

curs.execute("INSERT INTO notes (content) VALUES (?)", ('# The First Note',))
curs.execute("INSERT INTO notes (content) VALUES (?)", ('_Another note_',))
curs.execute("INSERT INTO notes (content) VALUES (?)", ('Visit [this page](https://www.digitalocean.com/community/tutorials) for more tutorials.',))

conn.commit()
conn.close()