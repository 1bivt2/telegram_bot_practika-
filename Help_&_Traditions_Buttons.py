# telegram_bot_practika-
import time
from colorama import init
from telebot.types import WebAppInfo
from telebot.types import InputMediaPhoto

# Инициализация colorama для цветного вывода в консоль
init()
from colorama import Fore, Back, Style
import telebot
from telebot import types

# Конфигурация бота
TOKEN = '7965556897:AAGxa9SvRQRh1STvmqSEBQCxvw3hXAp6cPk'
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')


def handle_back_button(message):
    """Обработчик кнопки возврата в главное меню"""
    try:
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    main(message)


# =======================================================================
# ОСНОВНОЕ МЕНЮ
# =======================================================================
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


# =======================================================================
# ОБРАБОТЧИКИ CALLBACK-ЗАПРОСОВ (ГЛАВНОЕ МЕНЮ)
# =======================================================================
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    """Единый обработчик кнопок главного меню"""
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

    elif call.data == 'schedule':
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

    elif call.data == 'traditions':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_pamytniki = types.KeyboardButton('🗿 Памятники')
        btn_krik = types.KeyboardButton('📣 Кричалки')
        btn_korpysa = types.KeyboardButton('🏛️ Корпуса')
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.row( btn_pamytniki, btn_krik)
        markup.row(btn_korpysa)
        markup.row(btn_back)

        bot.send_message(
            call.message.chat.id,
            "<b>🏫 Традиции МАДИ</b>\n\n",
            reply_markup=markup
        )

    elif call.data == 'help':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')
        btn_contacts=types.KeyboardButton('📞 Контакты')
        btn_swyaz=types.KeyboardButton('✉️ Обратная связь')
        markup.row( btn_contacts, btn_swyaz)
        markup.row(btn_back)
        bot.send_message(
            call.message.chat.id,
            "<b>🆘 Помощь</b>\n\n",
            reply_markup=markup
        )

    elif call.message.text == '🔙 Возврат в главное меню':
        handle_back_button(call.message)



# =======================================================================
# ОБРАБОТЧИКИ ТЕКСТОВЫХ СООБЩЕНИЙ (REPLY-КНОПКИ)
# =======================================================================
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
    if message.text == '📞 Контакты':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.row(btn_back)
        contacts_text = (
            "📋 <b>Контакты МАДИ</b>\n\n"
            "👮‍♂️ Дежурный: 8 (499) 155-01-00\n"
            "🎓 Приёмная комиссия: 8 (499) 346-01-69\n"
            "🗂️ Отдел контроля и делопроизводства: 8 (499) 346-01-68 доб. 1200\n\n"
            "🌐 Все контакты: https://madi.ru/voip.html"
        )

        bot.send_message(
            message.chat.id,
            contacts_text,
            reply_markup=markup,
            parse_mode='HTML'
        )
    if message.text == '✉️ Обратная связь':
        feedback_text = (
            "📧 По всем вопросам пишите на почту:\n"
            "<a href=\"mailto:feedback@madi.ru\">feedback@madi.ru</a>\n\n"
            "🕒 Мы отвечаем в течение 7 рабочих дней.\n\n"
            "Спасибо за ваши вопросы и предложения — мы всегда рады обратной связи!\n\n"
            "Ваши отзывы помогают нам улучшать качество обучения и сервис МАДИ.\n"
            "Каждое ваше сообщение важено и будет передано в соответствующий отдел."
        )
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        kb.add(types.KeyboardButton('🔙 Возврат в главное меню'))
        bot.send_message(
            message.chat.id,
            feedback_text,
            reply_markup=kb,
            parse_mode='HTML'
        )

    if message.text == '🗿 Памятники':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.row(
            types.KeyboardButton('Студенту и учителю'),
            types.KeyboardButton('Воинам Мадийцам')
        )
        markup.row(
            types.KeyboardButton('ГАЗ-АА "Полуторка"'),
        )
        markup.row(types.KeyboardButton('🔙 Возврат в главное меню'))

        bot.send_message(message.chat.id, "Выберите памятник:", reply_markup=markup)
        # Следующий ввод — в objects_monuments
        bot.register_next_step_handler(message, objects_monuments)
        return  
      
    if message.text == '🏛️ Корпуса':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.row(
            types.KeyboardButton('🏛️ Главный корпус'),
            types.KeyboardButton('🏬 Новый корпус')
        )
        markup.row(
            types.KeyboardButton('🔬 Лабораторный корпус'),
        )
        markup.row(types.KeyboardButton('🔙 Возврат в главное меню'))

        bot.send_message(message.chat.id, "Выберите корпуса:", reply_markup=markup)
        # Следующий ввод — в objects_monuments
        bot.register_next_step_handler(message, objects_corpuses)
        return 
    if message.text == '📣 Кричалки':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.row(btn_back)

        chant_text = (
            "ОЛЕ! ОЛА!\n"
            "ВПЕРЕД МАДИ МОСКВА\n"
            "АВТОДОРОЖНЫЙ\n"
            "АВТОДОРОЖНЫЙ\n"
            "АВТОДОРОЖНЫЙ НАВСЕГДА!\n\n"
            "МАДИ ЭТО Я!\n"
            "МАДИ ЭТО МЫ!\n"
            "МАДИ ЭТО ЛУЧШИЕ ЛЮДИ СТРАНЫ!\n\n"
            "Кто сегодня в зале главный?\n"
            "М-А-Д-И — самый славный!\n"
            "Шумим, горим, идём вперёд —\n"
            "Только МАДИ не подведёт!\n\n"
            "Кто шумит и побеждает?\n"
            "Это МАДИ, каждый знает!\n"
            "Руки вверх, держим строй —\n"
            "МАДИ — в сердце, МАДИ — бой!\n\n"
            "Эй, Москва, держись!\n"
            "МАДИ — врывается ввысь!"
        )

        bot.send_message(
            message.chat.id,
            chant_text,
            reply_markup=markup
        )
        bot.register_next_step_handler(message, objects_text)

    elif message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)






# =======================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ТЕКСТОВЫМ ГИДОМ
# =======================================================================
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


# =======================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ВИДЕО-ГИДОМ
# =======================================================================
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



#РАЗДЕЛЫ ПОД КАЖДЫЙ ФРАГМЕНТ КОДА(ПИШЕМ ВНУТРИ "=" ДЛЯ УДОБСТВА ЧТЕНИЯ)




#========================================================================
#РАСПИСАНИЕ (Разработчики: Кирилл Тихов, Владимир Панфилов)
#========================================================================


#========================================================================
#НАВИГАЦИЯ(Разработчики: Резник Игорь, Цапкова Елизавета)
#========================================================================


#========================================================================
#СТУДЕНЧЕССКАЯ ЖИЗНЬ(Разработчики: Резник Игорь, Цапкова Елизавета)
#========================================================================


#========================================================================
#ТРАДИЦИИ(Разработчик: Полиенко Даниил)
#========================================================================
def objects_monuments(message):
    text = message.text

    # 1) Сначала ловим «Назад»
     # Обработка выбора «Студенту и учителю»
    if text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == 'Студенту и учителю':
        reply = (
            "В начале 2010-х на территории МАДИ напротив друг друга были установлены две\n"
    "жанровые ростовые скульптуры — «Студент» и «Учитель».\n\n"

    "«Студент» изображает юношу, поставившего ногу на автомобильное колесо и устремившего\n"
    "взгляд в сторону памятника автомобилю ГАЗ-АА «Полуторка», одному из самых\n"
    "знаменитых грузовиков в истории СССР.\n\n"

    "Напротив него стоит «Учитель» с учебником в руках, увлечённо читающий лекцию по\n"
    "автомобилестроению — символизируя процесс передачи знаний и опыта от поколения к поколению.\n\n"

    "Эти скульптуры олицетворяют неразрывную связь между студентами и преподавателями\n"
    "МАДИ, подчёркивая важность практического мастерства и научного поиска в формировании\n"
    "будущих инженеров."
        )
        media = [
            InputMediaPhoto(open('3.jpg', 'rb'), caption=reply),
            InputMediaPhoto(open('4.jpg', 'rb'))
        ]
        bot.send_media_group(message.chat.id, media)
        # закрываем файлы
        media[0].media.close()
        media[1].media.close()

    if message.text == 'Воинам Мадийцам':
        caption = (
            "Это памятник преподавателям и студентам МАДИ, погибшим в годы Великой "
            "Отечественной войны. Сложно представить, но тот облик, в котором мы "
            "видим памятник сегодня, он обрел лишь в 1992 году. Торжественное "
            "открытие состоялось 8 мая, в канун Дня Победы.\n\n"
            "К созданию монумента был привлечен "
            "известный московский скульптор Яков Николаевич Купреянов.\n\n"
            "На памятнике можно различить композицию из трех фигур бойцов, установленную "
            "на цилиндрической стеле. В середине стелы расположен барельеф с изображением "
            "фрагментов моста через реку, солдат, толкающих автомобиль, полуторки с бойцами "
            "в кузове и девушки-регулировщицы. А над барельефом выгравирована надпись: "
            "«В память мадийцам, павшим в боях за Родину». \n\n"
            "Этот монумент — символ бессмертной памяти о великом подвиге, совершенном всем "
            "советским народом и в том числе студентами и преподавателями МАДИ. Возложение "
            "мадийцами цветов к памятнику — одна из главных традиций не только памятных мероприятий "
            "ко Дню Победы, но и всех университетских торжеств."
        )
        with open('5.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=caption)
            



    if message.text == 'ГАЗ-АА "Полуторка"':
        caption = (
            "Во дворе МАДИ установлена знаменитая «полуторка»\n\n"
        "ГАЗ-АА \"Полуторка\" – это первый массовый грузовой автомобиль СССР. "
        "Выпускалась эта замечательная машина с 1932 по 1950 годы.\n\n"
        "«Полуторка» стала настоящей спасительницей в годы Великой Отечественной войны. "
        "Автомобиль, установленный у входа в здание Московского автодорожного института, "
        "один из тех, в котором перевозили людей и грузы по знаменитой «Дороге жизни». "
        "На кузове автомобиля можно увидеть многочисленные следы от пуль...\n\n"
        "Автомобиль подняли со дна Ладожского озера и восстановили в 2012 году. "
        "Подарен институту Ассоциацией международных автомобильных перевозчиков."
        )
        with open('6.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo, caption=caption)

    # После успешной отправки любого контента — заново показываем то же меню
    # чтобы пользователь мог выбрать другой памятник или вернуться
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(
        types.KeyboardButton('Студенту и учителю'),
        types.KeyboardButton('Воинам Мадийцам')
    )
    markup.row(
        types.KeyboardButton('ГАЗ-АА "Полуторка"'),
    )
    markup.row(types.KeyboardButton('🔙 Возврат в главное меню'))

    bot.send_message(message.chat.id, "Можно выбрать ещё или вернуться:", reply_markup=markup)
    bot.register_next_step_handler(message, objects_monuments)

#========================================================================
#ПОМОЩЬ(Разработчик: Полиенко Даниил)
#========================================================================
def objects_corpuses(message):
    text = message.text

    # Назад
    if text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return

    # Корпуса
    if text == '🏛️ Главный корпус':
        caption=(
    "Адрес: Ленинградский просп., 64, Москва\n"
    "Год постройки: 1957\n\n"

    "Это здание создали специально для МАДИ, но выглядеть оно могло совсем по-другому. "
    "Из-за затянувшегося строительства проект пересматривали несколько раз.\n\n"

    "В 1939 году для института начали возводить дом на Ленинградском проспекте по проекту "
    "А.Э. Зильберта и А.М. Алхазова, однако работы остановили на время войны: институт "
    "эвакуировали в Узбекистан, а часть студентов ушли добровольцами на фронт. "
    "В память об этом в 1966 году перед зданием установили памятник погибшим в Великой "
    "Отечественной войне воинам-автомобилистам работы Я.Н. Купреянова.\n\n"

    "Для завершения здания с многочисленными колоннами потребовалось значительное финансирование, "
    "поэтому работы окончили лишь в 1957 году. При этом декор фасада едва не стал жертвой "
    "указа Хрущева о борьбе с излишествами: от украшения скульптурными группами и горельефами "
    "пришлось отказаться.")
        with open('7.jpg', 'rb') as photo:
            bot.send_photo(
            message.chat.id,
            photo,
            caption=caption,
            parse_mode='HTML' 
        )
    elif text == '🏬 Новый корпус':
        caption = (
        "Адрес: Ленинградский просп., 64, строение 2, Москва\n"
        "Год постройки: 1977\n\n"
        "В 1977 году с северной стороны к главному зданию был пристроен новый десятиэтажный "
        "лабораторный учебный корпус по проекту А. М. Алхазова.\n\n"
        )
        with open('8.jpg', 'rb') as photo:
            bot.send_photo(
            message.chat.id,
            photo,
            caption=caption,
            parse_mode='HTML'
            )
    elif text == '🔬 Лабораторный корпус':
    # Собираем подпись с абзацами
        caption = (
        "Адрес: Ленинградский просп., 64, строение 3, Москва\n"
        "Год постройки: 2009\n\n"
        "В корпусе расположены современные лаборатории для практических занятий, "
        "просторные аудитории и учебные мастерские, что значительно расширило "
        "возможности практического обучения студентов МАДИ."
        )
    # Отправляем фото с подписью
        with open('9.jpg', 'rb') as photo:
            bot.send_photo(
            message.chat.id,
            photo,
            caption=caption,
            parse_mode='HTML'
            )
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите корпус из списка.")

    # Показываем меню корпусов заново
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.row(
        types.KeyboardButton('🏛️ Главный корпус'),
        types.KeyboardButton('🏬 Новый корпус')
    )
    markup.row(
        types.KeyboardButton('🔬 Лабораторный корпус')
    )
    markup.row(types.KeyboardButton('🔙 Возврат в главное меню'))
    bot.send_message(
        message.chat.id,
        "Можно выбрать ещё или вернуться:",
        reply_markup=markup
    )
    bot.register_next_step_handler(message, objects_corpuses)


# =======================================================================
# ЗАПУСК БОТА
# =======================================================================


if __name__ == '__main__':
    print('Бот запущен и готов к работе! 🚀')
    bot.polling(none_stop=True)
