import telebot
from api_key import API_KEY
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, WMonthTelegramCalendar,  LSTEP
import datetime
from database_function import get_data_from_database
from calenar import generate_month_selector, generate_date_selector, generate_callback_month_selector
import json
import calendar

bot = telebot.TeleBot(API_KEY)

current_date = datetime.datetime.today().strftime('%Y-%m-%d').split('-')


rent_request = {
    'come': None,
    'leave': None,
    'glamp_id': None,
}

glamp_messages_id = []

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
    bd_resp = get_data_from_database()
    for glamp in bd_resp:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(
            text='Забронювати', callback_data=f"rent_{glamp[0]}"))
        photo_message = bot.send_photo(message.chat.id, glamp[1], caption=f"""{glamp[2]}
Ціна : {glamp[3]}$
Розмір : {glamp[4]}кв. м.""", reply_markup=markup)
        glamp_messages_id.append(photo_message.id)


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


@bot.callback_query_handler(lambda query: query.data.startswith('rent_'))
def rent_handler(callback: CallbackQuery):
    rent_request['glamp_id'] = callback.data.split('_')[1]
    for id in glamp_messages_id:
        try:
            bot.delete_message(callback.from_user.id, id)
        except Exception:
            pass
    bot.send_message(callback.from_user.id,
                     'Оберіть дату заїзду',
                     reply_markup=generate_month_selector())


@bot.message_handler(commands=["faq"])
def faq_handler(message):
    markup = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton("❔ Правила скасування", callback_data="rules")
    btn2 = InlineKeyboardButton('🛠 Що взяти із собою?', callback_data="things")
    btn3 = InlineKeyboardButton("🐶 Можна з вихованцями?", callback_data="pets")
    markup.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id,
                     "Найчастіші питання:", reply_markup=markup)


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

@bot.callback_query_handler(func=lambda query: query.data.startswith('date_') or query.data.startswith('date2_'))
def calendar_handler(callback: CallbackQuery):
    month = callback.data.split('_')[1]
    date = callback.data.split('_')[2]
    if callback.data.startswith('date_'):
        rent_request['come'] = datetime.date(datetime.datetime.now(
        ).year, list(calendar.month_name).index(month), int(date))
    if callback.data.startswith('date2_'):
        rent_request['leave'] = datetime.date(datetime.datetime.now(
        ).year, list(calendar.month_name).index(month), int(date))
    bot.delete_message(callback.from_user.id, callback.message.id)
    if callback.data.startswith('date_'):
        bot.send_message(callback.from_user.id, 'Оберіть дату заїзду',
                         reply_markup=generate_callback_month_selector(month, date))
    elif callback.data.startswith('date2_'):
        bot.send_message(callback.from_user.id,
                         f"Ви замовили глемп від {rent_request['come']} до {rent_request['leave']}")


@bot.callback_query_handler(func=lambda query: query.data == '1' or query.data == '2' or query.data == '3' or query.data == '4' or query.data == '5')
def number_handler(callback: CallbackQuery):
    bot.send_message(callback.from_user.id, f"""Повідомлення: "Вибрано: А-фрейм «Лісовий»
Дата: {rent_request['come']} - {rent_request['leave']}
Гості: {callback.data}
Вартість: 100$
Підтверджуєте броню?
""")


@bot.callback_query_handler(func=lambda query: query.data.startswith('calendar_') or query.data.startswith('calendar2_'))
def month_selector_handler(callback: CallbackQuery):
    bot.delete_message(callback.from_user.id, callback.message.id)
    if callback.data.startswith('calendar_'):
        bot.send_message(callback.from_user.id, "choose date", reply_markup=generate_date_selector(
            callback.data.split('_')[1], rent_request['glamp_id']))
    elif callback.data.startswith('calendar2_'):
        bot.send_message(callback.from_user.id, "choose date", reply_markup=generate_date_selector(
            callback.data.split('_')[1], rent_request['glamp_id'], callback.data.split('_')[2], callback.data.split('_')[3]))


@bot.callback_query_handler(lambda query: query.data == "rules")
def rules_callback_handler(callback: CallbackQuery):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton('⬅️  Назад', callback_data='back_to_faq'))
    bot.delete_message(callback.from_user.id, callback.message.id)
    bot.send_message(callback.from_user.id,
                     "Правила скасування:Ви можете скасувати ваше бронювання з повним поверненням коштів до 14 днів,після вже частинно", reply_markup=markup)

@bot.callback_query_handler(lambda query: query.data == 'back_to_faq')
def faq_handler(callback: CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=1)
    bot.delete_message(callback.from_user.id, callback.message.id)
    btn1 = InlineKeyboardButton("❔ Правила скасування", callback_data="rules")
    btn2 = InlineKeyboardButton('🛠 Що взяти із собою?', callback_data="things")
    btn3 = InlineKeyboardButton("🐶 Можна з вихованцями?", callback_data="pets")
    markup.add(btn1, btn2, btn3)
    bot.send_message(callback.from_user.id,
                     "Найчастіші питання:", reply_markup=markup)

@bot.callback_query_handler(lambda query: query.data == "things")
def things_callback_handler(callback):
    bot.delete_message(callback.from_user.id, callback.message.id)
    bot.send_message(callback.from_user.id,
                     "Що взяти із собою?-Радимо вам взяти із собою одяг,взуття та засоби гігієни")


@bot.callback_query_handler(lambda query: query.data == "pets")
def pets_callback_handler(callback):
    bot.delete_message(callback.from_user.id, callback.message.id)
    bot.send_message(callback.from_user.id, "Можна з вихованцями?-Так можна")


bot.infinity_polling()
