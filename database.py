import sqlite3

DB_NAME = 'sqlite.db'

# with sqlite3.connect(DB_NAME) as connection:
#     sqlite_request = """DROP TABLE glamps """
#     connection.execute(sqlite_request)
#     connection.commit()

# with sqlite3.connect(DB_NAME) as connection:
#     sqlite_request = """CREATE TABLE IF NOT EXISTS glamps (
#     id integer AUTO_INCREMENT,
#     image text NOT NULL,
#     desc text NOT NULL,
#     price integer NOT NULL,
#     size integer NOT NULL
#     );"""
#     connection.execute(sqlite_request)

# with sqlite3.connect(DB_NAME) as connection:
#     sqlite_request = """CREATE TABLE IF NOT EXISTS glamps (
#     id integer PRIMARY KEY,
#     image text NOT NULL,
#     desc text NOT NULL,
#     price integer NOT NULL,
#     size integer NOT NULL
#     );"""
#     connection.execute(sqlite_request)


with sqlite3.connect(DB_NAME) as connection:
    sqlite_request = """INSERT INTO glamps (image, desc, price, size) VALUES(?, ?, ?, ?);"""
    connection.execute(sqlite_request, ('photo.png', """Глемпінг у лісі "Лісова казка"

Цей затишний глемпінг розташований серед густого лісу, подалі від міської метушні, і дарує ідеальний баланс між природою та комфортом.""", 150, 40))
    connection.commit()
