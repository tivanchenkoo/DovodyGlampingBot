from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from database_function import get_data_from_database
import calendar
import json


def generate_month_selector():
    markup = InlineKeyboardMarkup(row_width=3)
    callback_month = calendar.month_name
    ukr_month = ['Січ', 'Лют', 'Бер', 'Квіт', 'Трав',
                 'Чер', 'Лип', 'Серп', 'Вер', 'Жов', 'Лист', 'Груд']
    buttons = []
    for i in range(13):
        if callback_month[i]:
            buttons.append(InlineKeyboardButton(
                text=ukr_month[i - 1], callback_data=f"calendar_{callback_month[i]}"))
    for i in range(0, len(buttons), 3):
        markup.add(*buttons[i:i+3])
    print('no month err')
    return markup


def generate_callback_month_selector(start_month, start_date):
    markup = InlineKeyboardMarkup(row_width=3)
    callback_month = calendar.month_name
    _, days_in_start_month = calendar.monthrange(
        datetime.now().year, list(callback_month).index(start_month))
    ukr_month = ['Січ', 'Лют', 'Бер', 'Квіт', 'Трав',
                 'Чер', 'Лип', 'Серп', 'Вер', 'Жов', 'Лист', 'Груд']
    buttons = []
    for i in range(13):
        if int(start_date) >= days_in_start_month:
            if callback_month[i]:
                if i >= list(callback_month).index(start_month) + 1:
                    buttons.append(InlineKeyboardButton(
                        text=ukr_month[i - 1], callback_data=f"calendar2_{callback_month[i]}_{start_month}_{start_date}"))
        else:
            if callback_month[i]:
                if i >= list(callback_month).index(start_month):
                    buttons.append(InlineKeyboardButton(
                        text=ukr_month[i - 1], callback_data=f"calendar2_{callback_month[i]}_{start_month}_{start_date}"))

    for i in range(0, len(buttons), 3):
        markup.add(*buttons[i:i+3])
    return markup


async def generate_date_selector(month, glamp_id, start_month=None, start_date=None):
    markup = InlineKeyboardMarkup(row_width=7)
    dates_json = await get_data_from_database()
    dates = json.loads(dates_json[int(glamp_id)- 1][6])[month]
    top_buttons = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Нд']
    top_inline_buttons = [InlineKeyboardButton(
        button, callback_data='ignore') for button in top_buttons]
    markup.add(* top_inline_buttons)
    month_num = list(calendar.month_name).index(month)
    week_first_day, days_in_month = calendar.monthrange(
        datetime.now().year, month_num)
    empty_btn = InlineKeyboardButton(' ', callback_data='ignore')
    if start_month != month and not start_date:
        buttons = [InlineKeyboardButton(
            date, callback_data=f"date_{month}_{date}") if not dates[date] else InlineKeyboardButton(
            '❌', callback_data='ignore') for date in dates.keys()]
    elif start_month != month and start_date:
        buttons = [InlineKeyboardButton(
            date, callback_data=f"date2_{month}_{date}") if not dates[date] else InlineKeyboardButton(
            '❌', callback_data='ignore') for date in dates.keys()]
    elif start_month == month:
        buttons = [InlineKeyboardButton(
            date, callback_data=f"date2_{month}_{date}") if not dates[date] else InlineKeyboardButton(
            '❌', callback_data='ignore') for date in dates.keys()]
        for i in range(int(start_date)):
            buttons[i] = empty_btn
    for i in range(week_first_day):
        buttons.insert(0, empty_btn)
    for i in range(0, len(dates) + week_first_day, 7):
        try:
            if buttons[i+7]:
                markup.add(*buttons[i:i + 7])
        except IndexError:
            try:
                if buttons[i + 7]:
                    markup.add(*buttons[i:i + 7])
            except:
                for day in range(int(
                        (len(dates) + week_first_day) / 7 + 1) * 7 - (len(dates) + week_first_day)):
                    buttons.append(empty_btn)
                markup.add(*buttons[i:i + 7])

    return markup
