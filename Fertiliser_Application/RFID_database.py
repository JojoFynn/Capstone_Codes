import sqlite3

connection = sqlite3.connect("RFID_database.db")
cursor = connection.cursor()

try:
    create_fertiliser_table = """CREATE TABLE IF NOT EXISTS fertiliser_data(
    rfid_code TEXT PRIMARY KEY,
    voucher_code TEXT NOT NULL, 
	manufacturer_name TEXT NOT NULL,
	start_location TEXT NOT NULL,
	destination_location TEXT NOT NULL
    )"""

    create_administrator_table = """CREATE TABLE IF NOT EXISTS administrator(
        admin_email TEXT NOT NULL,
        admin_password INTEGER PRIMARY KEY
    )"""
    cursor.execute(create_fertiliser_table)
    connection.commit()
    cursor.execute(create_administrator_table)
    connection.commit()

except connection.Error as error:
    print("debug print", error)
finally:
    if connection:
        connection.close()


def insert_list_data(mlist, sql):
    connection = sqlite3.connect("RFID_database.db")
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, mlist)
        connection.commit()
        print("commited")
    except connection.Error as error:
        print(error)
    finally:
        connection.close()


administrator = [("jojofynnmensah@gmail.com", "1234678"),
                 ("capstone@ashesi.com", "12345"),
                 ]
# insert_list_data(intern,sql)
sql1 = """ INSERT INTO administrator(admin_email,admin_password)VALUES(?,?)"""
insert_list_data(administrator, sql1)
