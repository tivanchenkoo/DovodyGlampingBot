import calendar
from datetime import datetime, timedelta
import sqlite3
from osmodule_text import data
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
                month_dates[date] = False
            year_data[month_name[month]] = month_dates

    return year_data


# {'february' : {
#     '1' : True,
#     '2' : False,
#     '3' : True,
# }}
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
#     size integer NOT NULL,
#     rent_calendar text NOT NULL
#     );"""
#     connection.execute(sqlite_request)


#                   SET_NEW_VAL
# with open('glampphoto2.jpg', 'rb') as image_connection:
#     image = image_connection.read()
# with sqlite3.connect(DB_NAME) as connection:
#     sqlite_request = """INSERT INTO glamps (image, desc, price, size, rent_calendar) VALUES(?, ?, ?, ?, ?);"""
#     connection.execute(sqlite_request, (image, """Глемпінг біля річки "Лісова казка"

# Цей затишний глемпінг розташований біля бушуючої річки, подалі від міста і усіх забот. Незабуваємий досвід для тебе і твоїх друзів або родини!""", 150, 40, json.dumps(generate_month_booking())))
#     connection.commit()


def get_data_from_database():
    with sqlite3.connect(DB_NAME) as sqlite_connection:
        sqlite_request = """SELECT * FROM glamps"""
        cursor = sqlite_connection.execute(sqlite_request)
        return cursor.fetchall()
