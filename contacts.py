import sqlite3

db = sqlite3.connect("contacts.sqlite")
db.execute("CREATE TABLE IF NOT EXISTS contacts(name TEXT, phone INTEGER, email TEXT)")
db.execute("INSERT INTO contacts(name, phone, email) VALUES('Raj', 987654, 'email@email.com')")
db.execute("INSERT INTO contacts(name, phone, email) VALUES('Puthia', 76543, 'www@email.com')")

cursor = db.cursor()
cursor.execute("SELECT * FROM contacts")
# print(cursor.fetchall())
print(cursor.fetchone())
print(cursor.fetchone())
print(cursor.fetchone())

for name, phone, email in cursor:
    print(name)
    print(phone)
    print(email)
    print("-" * 30)
cursor.close()
db.commit()

db.close()