import sqlite3

db = sqlite3.connect("contacts.sqlite")
new_email = "newemail@update.com"
name = input("Plese enter the name")

#update_sql = "UPDATE contacts set email = '{}' where name = '{}'".format(new_email, name)
update_sql = "UPDATE contacts set email = ? where name = ?"

update_cursor = db.cursor()
update_cursor.execute(update_sql,(new_email, name))
print("{} rows updated".format(update_cursor.rowcount))

update_cursor.connection.commit()
update_cursor.close()

for name, phone, email in db.execute("SELECT * FROM contacts"):
    print(name)
    print(phone)
    print(email)
    print("-" * 30)

db.close()