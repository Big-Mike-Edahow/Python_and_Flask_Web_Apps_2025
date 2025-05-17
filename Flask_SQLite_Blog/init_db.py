# init_db.py

import sqlite3

conn = sqlite3.connect('./data/database.db')
curs = conn.cursor()

with open('schema.sql') as f:
    conn.executescript(f.read())

curs.execute(
    "INSERT INTO posts (title, author, content) VALUES (?, ?, ?)",
    (
        "Life out on the road",
        "Big Mike",
        "It's quite hot and humid here in Jackson, Tennessee. One strategy that I use to stay cool out on the road is to bring my Chromebook inside the Truckstop, and do a little coding in the comfy air conditioning of the fast food joint. Today I ordered a Diet Coke and a bottle of Dasani, and then proceeded to joyfully hack away."
    )
)

curs.execute(
    "INSERT INTO posts (title, author, content) VALUES (?, ?, ?)",
    (
        "The joy of programming",
        "Mike Jackson",
        "I enjoy programming with Go, Python, SQL, HTML, CSS and JavaScript. I like to use pictures from my travels as content for my web pages and web apps. My adventures as I travel the country make great stories that I can share with friends and family."
    )
)

conn.commit()
conn.close()
