import sqlite3

dbpath = 'user.sqlite'

connection = sqlite3.connect(dbpath)
cursor = connection.cursor()

try:
    # CREATE
    cursor.execute("DROP TABLE IF EXISTS sample")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, line_id TEXT, building_name TEXT, room_number TEXT, name TEXT)")

except sqlite3.Error as e:
    print('sqlite3.Error occurred:', e.args[0])

connection.commit()
connection.close()