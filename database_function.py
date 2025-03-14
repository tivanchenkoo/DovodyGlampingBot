import aiosqlite
import calendar
from datetime import datetime, timedelta
import sqlite3
import json
DB_NAME = 'sqlite.db'


def generate_month_booking():
    year_data = {}
    year = datetime.now().year
    for month in range(13):
        month_name = calendar.month_name
        if month_name[month]:
            day_in_month = calendar.monthrange(year=year, month=month)
            month_dates = {}
            for date in range(day_in_month[1] + 1):
                if date:
                    month_dates[date] = False
            year_data[month_name[month]] = month_dates

    return year_data

#                   REMOVE DATABASE
# with sqlite3.connect(DB_NAME) as connection:
#     sqlite_request = """DROP TABLE glamps """
#     connection.execute(sqlite_request)
#     connection.commit()
    #   CREATE DATABASE AGAIN
# with sqlite3.connect(DB_NAME) as connection:
#     sqlite_request = """CREATE TABLE IF NOT EXISTS glamps (
#     id integer PRIMARY KEY,
#     image blob NOT NULL,
#     desc text NOT NULL,
#     price integer NOT NULL,
#     size text NOT NULL,
#     squares real NOT NULL,
#     rent_calendar text NOT NULL
#     );"""
#     connection.execute(sqlite_request)


# #                   SET_NEW_VAL
# with open('forest-2-optimized.jpg', 'rb') as image_connection:
#     image = image_connection.read()
# with sqlite3.connect(DB_NAME) as connection:
#     sqlite_request = """INSERT INTO glamps (image, desc, price, size, squares, rent_calendar) VALUES(?, ?, ?, ?, ?, ?);"""
#     connection.execute(sqlite_request, (image, """Глемпінг біля лісу "Форест"

# лемпінг у мальовничому куточку лісу, де можна насолоджуватися краєвидами, свіжим повітрям і атмосферою спокою.""", 150,  "12,4 х 10,7 м", 133.0, json.dumps(generate_month_booking())))
#     connection.commit()

#                   SET_EXAMPLE_VAL2
# with open('glampphoto.webp', 'rb') as image_connection:
#     image = image_connection.read()
# with sqlite3.connect(DB_NAME) as connection:
#     sqlite_request = """INSERT INTO glamps (image, desc, price, size, rent_calendar) VALUES(?, ?, ?, ?, ?);"""
#     connection.execute(sqlite_request, (image, """Глемпінг у лісі "Лісова казка"

# Цей затишний глемпінг розташований серед густого лісу, подалі від міської метушні, і дарує ідеальний баланс між природою та комфортом.""", 100, 55, json.dumps(generate_month_booking())))
#     connection.commit()



async def get_data_from_database():
    async with aiosqlite.connect(DB_NAME) as sqlite_connection:
        sqlite_request = """SELECT * FROM glamps"""
        cursor = await sqlite_connection.execute(sqlite_request)
        data = await cursor.fetchall()
        return data