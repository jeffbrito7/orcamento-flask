import sqlite3

conn = sqlite3.connect("C:/Users/CPU JEFF/orcamento_web.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM pagador")
for row in cursor.fetchall():
    print(row)

conn.close()