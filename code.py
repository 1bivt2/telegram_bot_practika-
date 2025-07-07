# telegram_bot_practika-
import time
from colorama import init
from telebot.types import WebAppInfo

# Инициализация colorama для цветного вывода в консоль
init()
from colorama import Fore, Back, Style
import telebot
from telebot import types

# Конфигурация бота
TOKEN = '7428981437:AAH_dXO9neL50DS6zcBnnsi-4Hu4_3-4msY'
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')


def handle_back_button(message):
    """Обработчик кнопки возврата в главное меню"""
    try:
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    main(message)


# ОСНОВНОЕ МЕНЮ
@bot.message_handler(commands=['start'])
def main(message):
    """Главное меню бота с основными разделами"""
    markup = types.InlineKeyboardMarkup()

    # Основные кнопки
    bt1 = types.InlineKeyboardButton('📍 Навигация', callback_data='navigation')
    bt2 = types.InlineKeyboardButton('📅 Расписание', callback_data='schedule')
    bt3 = types.InlineKeyboardButton('🏫Традиции', callback_data='traditions')
    bt4 = types.InlineKeyboardButton('🎓 Студлайф', callback_data='student_life')
    bt5 = types.InlineKeyboardButton('🆘 Помощь', callback_data='help')
    markup.add(bt4, bt2, bt3, bt1, bt5)

    welcome_text = f"""
    <b>🚀 Добро пожаловать в МАДИ-ГИД!</b>

Этот бот — ваш универсальный помощник в университете. Здесь вы можете:

📍 <b>Навигация</b> - найти нужный корпус или аудиторию
📅 <b>Расписание</b> - узнать расписание своей группы
🏫 <b>Традиции</b> - погрузиться в традиции МАДИ
🎓 <b>Студлайф</b> - быть в курсе студенческой жизни
🆘 <b>Помощь</b> - экстренные контакты и инструкции

<i>Выберите нужный раздел:</i>
"""

    bot.send_message(
        message.chat.id,
        welcome_text.strip(),
        reply_markup=markup
    )



# ОБРАБОТЧИКИ CALLBACK-ЗАПРОСОВ (ГЛАВНОЕ МЕНЮ)
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """Обработчик нажатий на кнопки главного меню"""
    if call.data == 'navigation':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        btn_text = types.KeyboardButton('🗒️ Текстовый гид')
        btn_video = types.KeyboardButton('🎬 Видео-гид')
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')

        markup.add(btn_text, btn_video, btn_back)

        bot.send_message(
            call.message.chat.id,
            "<b>📍 Режим навигации</b>\n\nВыберите тип путеводителя:",
            reply_markup=markup
        )

    if call.data == 'schedule':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bt_menu = types.KeyboardButton('🔗 Перейти к расписанию',
                                       web_app=WebAppInfo('https://raspisanie.madi.ru/tplan/'))
        bt_back = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(bt_menu)
        markup.add(bt_back)
        bot.send_message(
            call.message.chat.id,
            "Актуальное расписание для всех групп доступно на официальном сайте МАДИ",
            reply_markup=markup
        )
    # if call.data == 'help':


    elif call.message.text == '🔙 Возврат в главное меню':
        handle_back_button(call.message)


# ОБРАБОТЧИКИ ТЕКСТОВЫХ СООБЩЕНИЙ (REPLY-КНОПКИ)
@bot.message_handler(content_types=['text'])
def handle_reply_buttons(message):
    """Обработчик текстовых сообщений для Reply-кнопок"""
    if message.text == '🗒️ Текстовый гид':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        btn1 = types.KeyboardButton('🏫 Учебные корпуса')
        btn2 = types.KeyboardButton('🍽️ Столовые')
        btn3 = types.KeyboardButton('📖 Библиотека')
        btn4 = types.KeyboardButton('🏛️ Музей')
        btn5 = types.KeyboardButton('🏢 Администрация')
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')

        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5)
        markup.row(btn_back)

        bot.send_message(
            message.chat.id,
            "Медиаконтент в процессе...",
            reply_markup=markup
        )
        bot.register_next_step_handler(message, objects_text)

    if message.text == '🎬 Видео-гид':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        btn1 = types.KeyboardButton('🏫 Учебные корпуса')
        btn2 = types.KeyboardButton('🍽️ Столовые')
        btn3 = types.KeyboardButton('📖 Библиотека')
        btn4 = types.KeyboardButton('🏛️ Музей')
        btn5 = types.KeyboardButton('🏢 Администрация')
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')

        markup.row(btn1, btn2)
        markup.row(btn3, btn4)
        markup.row(btn5)
        markup.row(btn_back)

        bot.send_message(
            message.chat.id,
            "Медиаконтент в процессе...",
            reply_markup=markup
        )
        bot.register_next_step_handler(message, objects_video)

    elif message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)


# ФУНКЦИИ ДЛЯ РАБОТЫ С ТЕКСТОВЫМ ГИДОМ
def objects_text(message):
    """Обработчик объектов для текстового гида"""
    if message.text == '🏫 Учебные корпуса':
        markup = types.ReplyKeyboardMarkup()
        btnKorp1 = types.KeyboardButton('🏛️ Главный корпус')
        btnKorp2 = types.KeyboardButton('🏬 Новый корпус')
        btnKorp3 = types.KeyboardButton('🔬 Лабораторный корпус')
        btnback = types.KeyboardButton('🔙 Возврат в главное меню')

        markup.add(btnKorp1)
        markup.add(btnKorp2, btnKorp3)
        markup.add(btnback)

        text = """<b>🏫 Учебные корпуса МАДИ</b>

Выберите интересующий вас корпус:
"""
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, korp_MADI_text)
    if message.text == '🍽️ Столовые':
        text = """В главном корпусе есть две столовые:
на 2-м этаже — на 120 посадочных мест;
на 4-м этаже — на 130 посадочных мест.
 
madi.ru
Также есть столовая на 70 посадочных мест в лабораторном корпусе. 
"""
        markup = types.ReplyKeyboardMarkup()
        btndining1 = types.KeyboardButton("🏛️ Главный корпус")
        btndining2 = types.KeyboardButton("🔬 Лабораторный корпус")
        btndining3_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btndining1,btndining2)
        markup.add(btndining3_Back)
        bot.send_message(message.chat.id,text,reply_markup=markup)
        # bot.register_next_step_handler(message, dining_rooms)

    elif message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)


def korp_MADI_text(message):
    """Обработчик учебных корпусов (текстовый режим)"""
    if message.text in ['🏛️ Главный корпус', '🏬 Новый корпус', '🔬 Лабораторный корпус']:
        markup = types.ReplyKeyboardMarkup()
        bt_korp_MADI1_back = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(bt_korp_MADI1_back)
        bot.send_message(message.chat.id, 'Контент в процессе', reply_markup=markup)

    elif message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)


# ФУНКЦИИ ДЛЯ РАБОТЫ С ВИДЕО-ГИДОМ
def objects_video(message):
    """Обработчик объектов для видео-гида"""
    if message.text == '🏫 Учебные корпуса':
        markup = types.ReplyKeyboardMarkup()
        btnKorp1 = types.KeyboardButton('🏛️ Главный корпус')
        btnKorp2 = types.KeyboardButton('🏬 Новый корпус')
        btnKorp3 = types.KeyboardButton('🔬 Лабораторный корпус')
        btnback = types.KeyboardButton('🔙 Возврат в главное меню')

        markup.add(btnKorp1)
        markup.add(btnKorp2, btnKorp3)
        markup.add(btnback)

        text = """<b>🏫 Учебные корпуса МАДИ</b>

Выберите интересующий вас корпус:
"""
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, korp_MADI_video)

    elif message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)


def korp_MADI_video(message):
    """Обработчик учебных корпусов (видео-режим)"""
    if message.text in ['🏛️ Главный корпус', '🏬 Новый корпус', '🔬 Лабораторный корпус']:
        markup = types.ReplyKeyboardMarkup()
        bt_korp_MADI1_back = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(bt_korp_MADI1_back)
        bot.send_message(message.chat.id, 'Контент в процессе', reply_markup=markup)

    elif message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)



if __name__ == '__main__':
    print('Бот запущен и готов к работе! 🚀')
    bot.polling(none_stop=True)
