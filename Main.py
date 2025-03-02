import telebot
from api_key import API_KEY
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, WMonthTelegramCalendar,  LSTEP
import datetime
from database_function import get_data_from_database


bot = telebot.TeleBot(API_KEY)

current_date = datetime.datetime.today().strftime('%Y-%m-%d').split('-')

rent_request = {
    'come': None,
    'leave': None
}

# --------------------- message_handler ----------------------


@bot.message_handler(commands=['start'])
def reply_start_command(message: Message):
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(
        "🏕 Переглянути доступні А-фрейми", callback_data='seeprojects')
    btn2 = InlineKeyboardButton("📅 Забронювати", callback_data='rent')
    btn3 = InlineKeyboardButton("❓ Допомога", callback_data='help')
    btn4 = InlineKeyboardButton("📞 Контакти", callback_data='contacts')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,
                     """
Привіт! 👋 Я допоможу тобі забронювати затишний А-фрейм у нашому глемпінгу. Вибери дію: """,
                     reply_markup=markup)


@bot.message_handler(commands=['book'])
def photo_resp(message: Message):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Забронювати', callback_data='rent'))
    bd_resp = get_data_from_database()
    for glamp in bd_resp:
        bot.send_photo(message.chat.id, glamp[1], caption=f"""{glamp[2]}
Ціна : {glamp[3]}$
Розмір : {glamp[4]}кв. м.""", reply_markup=markup)


@bot.message_handler(commands=['contacts'])
def contacts_handler(message: Message):
    markup = InlineKeyboardMarkup(row_width=1)
    map_open_btn = InlineKeyboardButton(
        "📍 Відкрити в картах", callback_data=',')
    call_btn = InlineKeyboardButton("📞 Зателефонувати", callback_data=',')
    markup.add(map_open_btn, call_btn)
    bot.send_message(message.chat.id, """
Наша адреса : *адреса для прикладу
Телефон:
""", reply_markup=markup)


@bot.message_handler(commands=['help'])
def contacts_handler(message: Message):
    bot.send_message(message.chat.id, """Ось що я вмію:
/book – Розпочати бронювання
/my_bookings – Мої броні
/cancel – Скасувати броню
/contacts – Контакти та адреса
""")

# @bot.message_handler(commands=['photo'])
# def send_photo(message : Message):
#     bot.send_photo(message.chat.id, )


# @bot.message_handler(commands=['book'])
# def start(message: Message):
#     calendar, step = WMonthTelegramCalendar(calendar_id=1).build()
#     bot.send_message(message.chat.id,
#                      'Оберіть день заїзду',
#                      reply_markup=calendar)

# ------------------------ callback query handler ----------------------


@bot.callback_query_handler(lambda query: query.data == 'rent')
def rent_handler(callback: CallbackQuery):
    calendar, step = WMonthTelegramCalendar(calendar_id=1).build()
    bot.send_message(callback.from_user.id,
                     'Оберіть день заїзду',
                     reply_markup=calendar)


@bot.callback_query_handler(lambda query: query.data == 'investments')
def investments_handler(callback: CallbackQuery):
    bot.send_message(callback.message.chat.id, 'investments')


@bot.callback_query_handler(lambda query: query.data == 'help')
def investments_handler(callback: CallbackQuery):
    bot.send_message(callback.message.chat.id, """Ось що я вмію:
/book – Розпочати бронювання
/my_bookings – Мої броні
/cancel – Скасувати броню
/contacts – Контакти та адреса  
""")


@bot.callback_query_handler(lambda query: query.data == 'seeprojects')
def investments_handler(callback: CallbackQuery):
    bot.send_message(callback.message.chat.id, 'seeprojects')


@bot.callback_query_handler(lambda query: query.data == 'contacts')
def investments_handler(callback: CallbackQuery):
    bot.send_message(callback.message.chat.id, 'contacts')


@bot.callback_query_handler(func=WMonthTelegramCalendar.func(calendar_id=1))
def cal(c: CallbackQuery):
    result, key, step = WMonthTelegramCalendar(calendar_id=1).process(c.data)
    if not result and key:
        bot.edit_message_text("Оберіть день заїзду",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        result_list = str(result).split('-')
        calendar, step = WMonthTelegramCalendar(calendar_id=2, min_date=datetime.date(
            int(result_list[0]), int(result_list[1]), int(result_list[2]) + 1)).build()
        rent_request['come'] = result
        bot.send_message(c.message.chat.id,
                         "Оберіть день виїзду", reply_markup=calendar)


@bot.callback_query_handler(func=WMonthTelegramCalendar.func(calendar_id=2))
def cal(c: CallbackQuery):
    result, key, step = WMonthTelegramCalendar(calendar_id=2).process(c.data)
    if not result and key:
        bot.edit_message_text("Оберіть день виїзду",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        print('yay')
        markup = InlineKeyboardMarkup(row_width=1)
        btn1 = InlineKeyboardButton('1️⃣', callback_data='1')
        btn2 = InlineKeyboardButton('2️⃣', callback_data='2')
        btn3 = InlineKeyboardButton('3️⃣', callback_data='3')
        btn4 = InlineKeyboardButton('4️⃣', callback_data='4')
        btn5 = InlineKeyboardButton('5️⃣', callback_data='5')
        markup.add(btn1, btn2, btn3, btn4, btn5)

        rent_request['leave'] = result
        bot.send_message(c.message.chat.id,
                         f"Скільки гостей проживатиме?", reply_markup=markup)


@bot.callback_query_handler(func=lambda query: query.data == '1' or query.data == '2' or query.data == '3' or query.data == '4' or query.data == '5')
def number_handler(callback: CallbackQuery):
    bot.send_message(callback.from_user.id, f"""Повідомлення: "Вибрано: А-фрейм «Лісовий»
Дата: {rent_request['come']} - {rent_request['leave']}
Гості: {callback.data}
Вартість: 100$
Підтверджуєте броню?
""")


bot.infinity_polling()
