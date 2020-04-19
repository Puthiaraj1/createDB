import sqlite3

conn = sqlite3.connect("contacts.sqlite")
select_sql = "SELECT * FROM contacts WHERE name = ?"
name = input("Plese enter the name")

select_cursor = conn.cursor()

for row in select_cursor.execute(select_sql, (name,)):
    print(row)

select_cursor.close()

conn.close()