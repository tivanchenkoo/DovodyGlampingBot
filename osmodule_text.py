# import os

# print(os.getcwd()) #Дает путь к текущей дериктории ( род. папка )

# print(os.path.join(os.getcwd(), 'osmodule_text.py')) # Соединяет 2 строки в путь

with open('glampphoto.webp', 'rb') as image_conn:
    data = image_conn.read()
