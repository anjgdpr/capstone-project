import sqlite3

connection = sqlite3.connect("db.sqlite3")
cursor = connection.cursor()

with open('libdata-v6.txt', 'r') as file: 
    no_records = 0
    for row in file: 
        cursor.execute("INSERT INTO books_book VALUES (?,?,?,?,?,?,?,?,?,?)", row.split("\t"))
        connection.commit()
        no_records += 1 

connection.close() 
print('\n {} Records Transferred'.format(no_records))