import sqlite3
from osmodule_text import data
DB_NAME = 'sqlite.db'

#                   REMOVE DATABASE
# with sqlite3.connect(DB_NAME) as connection:
#     sqlite_request = """DROP TABLE glamps """
#     connection.execute(sqlite_request)
#     connection.commit()

#                   CREATE DATABASE AGAIN
# with sqlite3.connect(DB_NAME) as connection:
#     sqlite_request = """CREATE TABLE IF NOT EXISTS glamps (
#     id integer PRIMARY KEY,
#     image blob NOT NULL,
#     desc text NOT NULL,
#     price integer NOT NULL,
#     size integer NOT NULL
#     );"""
#     connection.execute(sqlite_request)


#                   SET_NEW_VAL
# with open('glampphoto2.jpg', 'rb') as image_connection :
#     image = image_connection.read()
# with sqlite3.connect(DB_NAME) as connection:
#     sqlite_request = """INSERT INTO glamps (image, desc, price, size) VALUES(?, ?, ?, ?);"""
#     connection.execute(sqlite_request, (image, """Глемпінг біля річки "Лісова казка"

# Цей затишний глемпінг розташований біля бушуючої річки, подалі від міста і усіх забот. Незабуваємий досвід для тебе і твоїх друзів або родини!""", 150, 40))
#     connection.commit()


def get_data_from_database():
    with sqlite3.connect(DB_NAME) as sqlite_connection:
        sqlite_request = """SELECT * FROM glamps"""
        cursor = sqlite_connection.execute(sqlite_request)
        return cursor.fetchall()
