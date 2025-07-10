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

        show_schedule_menu(call.message)

    elif call.data == 'select_group':

        ask_for_group_name(call.message)

    elif call.data == 'get_schedule':

        handle_get_schedule(call)

    elif call.data == 'back_to_schedule':

        show_schedule_menu(call.message)

    elif call.data == 'traditions':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_pamytniki = types.KeyboardButton('🗿 Памятники')
        btn_krik = types.KeyboardButton('📣 Кричалки')
        btn_korpysa = types.KeyboardButton('🏛️ Корпуса')
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.row(btn_pamytniki, btn_krik)
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
        btn_contacts = types.KeyboardButton('📞 Контакты')
        btn_swyaz = types.KeyboardButton('✉️ Обратная связь')
        markup.row(btn_contacts, btn_swyaz)
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
        # Добавьте этот код в раздел обработки текстовых сообщений (функцию handle_reply_buttons)

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
        markup.add(btndining1, btndining2)
        markup.add(btndining3_Back)
        bot.send_message(message.chat.id, text, reply_markup=markup)
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


# РАЗДЕЛЫ ПОД КАЖДЫЙ ФРАГМЕНТ КОДА(ПИШЕМ ВНУТРИ "=" ДЛЯ УДОБСТВА ЧТЕНИЯ)


# ========================================================================
# РАСПИСАНИЕ (Разработчики: Кирилл Тихов, Владимир Панфилов)
# ========================================================================

# Для корректной работы требуются следующие условия:
# Google Chrome версии 138 и выше. Посмотреть версию и обновить ее можно тут: chrome://settings/help
# Chromedriver версии как Chrome. После скачивания требуется распаковать и указать
#   путь к chromedriver.exe в self.service. Скачать можно тут: https://googlechromelabs.github.io/chrome-for-testing/
# Также установить библиотеки: selenium и bs4


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


user_data = {}


class MadiScheduleParser:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.service = Service(executable_path=r'C:\chromedriver-win64\chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

    def __del__(self):
        if hasattr(self, 'driver'):
            self.driver.quit()

    def get_groups(self):
        try:
            self.driver.get("https://raspisanie.madi.ru/tplan/r/?task=7")
            time.sleep(2)

            input_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input#groupChoose"))
            )
            input_field.click()
            time.sleep(1)

            groups = self.driver.execute_script("""
                return Array.from(document.querySelectorAll('.comboGroup li:not(.donotshow)'))
                    .map(li => li.textContent.trim());
            """)
            return groups if groups else []

        except Exception as e:
            print(f"Ошибка получения групп: {e}")
            return []

    def select_group(self, group_name):
        try:
            self.driver.get("https://raspisanie.madi.ru/tplan/r/?task=7")
            time.sleep(2)

            input_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input#groupChoose"))
            )
            input_field.click()
            time.sleep(0.5)

            group_element = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, f"//li[contains(., '{group_name}')]"))
            )
            group_element.click()
            time.sleep(2)
            return True

        except Exception as e:
            print(f"Ошибка выбора группы: {e}")
            return False

    def get_weekly_schedule(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table.timetable"))
            )
            time.sleep(2)

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            all_tables = soup.find_all('table', {'class': 'timetable'})

            schedule = {}
            current_day = None

            for table in all_tables:
                for row in table.find_all('tr'):
                    if row.th and row.th.get('colspan'):
                        current_day = row.th.text.strip()
                        schedule[current_day] = []
                        continue

                    if row.find('td') and row.find('td').get_text().strip() == 'Время занятий':
                        continue

                    if current_day and row.find_all('td'):
                        cols = row.find_all('td')
                        if len(cols) >= 6:
                            time_col = cols[0].text.strip()
                            subject = cols[1].text.strip()
                            lesson_type = cols[2].text.strip()
                            frequency = cols[3].text.strip()
                            classroom = cols[4].text.strip()
                            teacher = cols[5].text.strip()

                            if subject and subject != 'Наименование дисциплины':
                                schedule[current_day].append({
                                    'time': time_col,
                                    'subject': subject,
                                    'type': lesson_type,
                                    'frequency': frequency,
                                    'classroom': classroom,
                                    'teacher': teacher
                                })

            return schedule

        except Exception as e:
            print(f"Ошибка парсинга расписания: {e}")
            return None


def format_schedule(schedule, group_name):
    if not schedule:
        return "Расписание не найдено"

    result = []
    days_order = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

    sorted_days = sorted(schedule.keys(),
                         key=lambda x: days_order.index(x) if x in days_order else len(days_order))

    for day in sorted_days:
        classes = schedule[day]
        if not classes:
            continue

        result.append(f"📅 {day} | Группа {group_name}")
        result.append("───────────────────────")

        for cls in classes:
            lesson_type = cls['type'].lower()
            if 'лекц' in lesson_type:
                lesson_type = 'лекция'
            elif 'практ' in lesson_type or 'семин' in lesson_type:
                lesson_type = 'практика'
            elif 'лаб' in lesson_type:
                lesson_type = 'лабораторная'

            frequency = cls['frequency']
            if frequency == 'Еженедельно':
                freq_emoji = '📅'
            elif frequency == 'Числитель':
                freq_emoji = '🔢'
            elif frequency == 'Знаменатель':
                freq_emoji = '🔣'
            elif 'числ' in frequency.lower():
                freq_emoji = '🔢'
            else:
                freq_emoji = '🔄'

            classroom = cls['classroom'].strip() or "не указана"
            teacher = cls['teacher'].strip() or "не указан"

            lesson_str = (
                f"🕒 {cls['time']} | {cls['subject']} ({lesson_type})\n"
                f"📍 Ауд. {classroom} | {teacher} | {freq_emoji} {frequency}"
            )
            result.append(lesson_str)

        if day != sorted_days[-1]:
            result.append("")

    return "\n".join(result)


def create_main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_group = types.KeyboardButton('👥 Выбрать группу')
    btn_schedule = types.KeyboardButton('📅 Получить расписание')
    markup.add(btn_group, btn_schedule)
    return markup


def create_group_selection_menu(groups):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    buttons = [types.KeyboardButton(group) for group in groups[:20]]
    markup.add(*buttons)
    markup.add(types.KeyboardButton('🔙 Назад'))
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Привет! Я бот для расписания МАДИ.\n"
                     "Используй кнопки ниже для навигации:",
                     reply_markup=create_main_menu())


@bot.message_handler(func=lambda message: message.text == '👥 Выбрать группу')
def select_group_menu(message):
    try:
        parser = MadiScheduleParser()
        groups = parser.get_groups()
        del parser

        if not groups:
            bot.send_message(message.chat.id, "⚠️ Не удалось получить список групп. Попробуйте позже.")
            return

        user_data[message.chat.id] = {
            'groups': groups,
            'waiting_for_group': True
        }

        bot.send_message(message.chat.id, "👇 Выберите свою группу из списка:",
                         reply_markup=create_group_selection_menu(groups))

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Произошла ошибка: {str(e)}")


@bot.message_handler(func=lambda message: message.text == '📅 Получить расписание')
def get_schedule_menu(message):
    if message.chat.id not in user_data or 'selected_group' not in user_data[message.chat.id]:
        bot.send_message(message.chat.id, "ℹ️ Сначала выберите группу", reply_markup=create_main_menu())
        return

    send_schedule(message)


@bot.message_handler(func=lambda message: message.text == '🔙 Назад')
def back_to_main_menu(message):
    bot.send_message(message.chat.id, "Главное меню:", reply_markup=create_main_menu())


@bot.message_handler(func=lambda message: message.chat.id in user_data and user_data[message.chat.id].get('waiting_for_group', False))
def handle_group_selection(message):
    try:
        if message.text == '🔙 Назад':
            user_data[message.chat.id]['waiting_for_group'] = False
            bot.send_message(message.chat.id, "Главное меню:", reply_markup=create_main_menu())
            return

        if message.text not in user_data[message.chat.id]['groups']:
            bot.send_message(message.chat.id, "⚠️ Пожалуйста, выберите группу из предложенного списка.")
            return

        user_data[message.chat.id]['selected_group'] = message.text
        user_data[message.chat.id]['waiting_for_group'] = False

        bot.send_message(message.chat.id,
                         f"✅ Группа *{message.text}* сохранена!\n"
                         f"Теперь вы можете получить расписание",
                         reply_markup=create_main_menu(),
                         parse_mode='Markdown')

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Произошла ошибка: {str(e)}")
        if message.chat.id in user_data:
            del user_data[message.chat.id]


def send_schedule(message):
    try:
        if message.chat.id not in user_data or 'selected_group' not in user_data[message.chat.id]:
            return

        group_name = user_data[message.chat.id]['selected_group']
        msg = bot.send_message(message.chat.id, f"⏳ Загружаю расписание для группы *{group_name}*...")

        parser = MadiScheduleParser()
        if parser.select_group(group_name):
            schedule = parser.get_weekly_schedule()
            if schedule:
                formatted = format_schedule(schedule, group_name)
                bot.delete_message(message.chat.id, msg.message_id)

                # Отправляем расписание с inline-кнопками
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('🔄 Обновить расписание', callback_data='get_schedule'))

                max_length = 4000
                parts = [formatted[i:i + max_length] for i in range(0, len(formatted), max_length)]
                for part in parts[:-1]:
                    bot.send_message(message.chat.id, part, parse_mode='Markdown')

                # Последнюю часть отправляем с кнопками
                bot.send_message(
                    message.chat.id,
                    parts[-1],
                    parse_mode='Markdown',
                    reply_markup=markup
                )
            else:
                bot.edit_message_text(
                    "⚠️ Не удалось получить расписание. Попробуйте позже.",
                    message.chat.id,
                    msg.message_id
                )
        else:
            bot.edit_message_text(
                "⚠️ Ошибка при загрузке расписания. Попробуйте позже.",
                message.chat.id,
                msg.message_id
            )
        del parser

    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Произошла ошибка: {str(e)}")


def show_schedule_menu(message):
    """Показывает меню расписания с inline-кнопками"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_group = types.InlineKeyboardButton('👥 Выбрать группу', callback_data='select_group')
    btn_schedule = types.InlineKeyboardButton('📅 Получить расписание', callback_data='get_schedule')
    markup.add(btn_group, btn_schedule)

    schedule_text = """
<b>📅 Расписание МАДИ</b>

Здесь вы можете:
- Выбрать свою учебную группу
- Получить актуальное расписание
- Просмотреть расписание на неделю

Выберите действие:
"""
    try:
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message.message_id,
            text=schedule_text.strip(),
            reply_markup=markup,
            parse_mode='HTML'
        )
    except:
        bot.send_message(
            message.chat.id,
            schedule_text.strip(),
            reply_markup=markup,
            parse_mode='HTML'
        )


def ask_for_group_name(message):
    """Просит пользователя ввести номер группы"""
    msg = bot.send_message(
        message.chat.id,
        "✏️ Введите номер вашей группы:",
        reply_markup=types.ForceReply(selective=True)
    )
    bot.register_next_step_handler(msg, process_group_name)


def process_group_name(message):
    """Обрабатывает введенное название группы"""
    group_name = message.text.strip()

    # Сохраняем группу
    if 'chat.id' not in user_data:
        user_data[message.chat.id] = {}
    user_data[message.chat.id]['selected_group'] = group_name

    # Подтверждаем выбор
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton('👥 Изменить группу', callback_data='select_group'),
        types.InlineKeyboardButton('📅 Получить расписание', callback_data='get_schedule')
    )

    bot.send_message(
        message.chat.id,
        f"✅ Группа <b>{group_name}</b> сохранена!\nТеперь вы можете получить расписание.",
        reply_markup=markup,
        parse_mode='HTML'
    )


def handle_get_schedule(call):
    """Обрабатывает запрос на получение расписания"""
    try:
        if call.message.chat.id not in user_data or 'selected_group' not in user_data[call.message.chat.id]:
            bot.answer_callback_query(
                call.id,
                "ℹ️ Сначала введите номер группы",
                show_alert=True
            )
            return

        group_name = user_data[call.message.chat.id]['selected_group']
        msg = bot.send_message(call.message.chat.id, f"⏳ Ищу расписание для группы {group_name}...")

        parser = MadiScheduleParser()
        if parser.select_group(group_name):
            schedule = parser.get_weekly_schedule()
            if schedule:
                formatted = format_schedule(schedule, group_name)

                # Отправляем расписание с кнопкой обновления
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('🔄 Обновить', callback_data='get_schedule'))

                max_length = 4000
                parts = [formatted[i:i + max_length] for i in range(0, len(formatted), max_length)]
                for part in parts[:-1]:
                    bot.send_message(call.message.chat.id, part, parse_mode='Markdown')

                # Последнюю часть отправляем с кнопкой
                bot.send_message(
                    call.message.chat.id,
                    parts[-1],
                    parse_mode='Markdown',
                    reply_markup=markup
                )
            else:
                bot.send_message(
                    call.message.chat.id,
                    "⚠️ Расписание для указанной группы не найдено",
                    reply_markup=types.InlineKeyboardMarkup().add(
                        types.InlineKeyboardButton('👥 Ввести другую группу', callback_data='select_group')
                    )
                )
        else:
            bot.send_message(
                call.message.chat.id,
                "⚠️ Не удалось загрузить расписание. Попробуйте позже.",
                reply_markup=types.InlineKeyboardMarkup().add(
                    types.InlineKeyboardButton('🔄 Повторить', callback_data='get_schedule')
                )
            )
        del parser

    except Exception as e:
        bot.answer_callback_query(
            call.id,
            f"⚠️ Ошибка: {str(e)}",
            show_alert=True
        )
# ========================================================================
# НАВИГАЦИЯ(Разработчики: Резник Игорь, Цапкова Елизавета)
# ========================================================================


# ========================================================================
# СТУДЕНЧЕССКАЯ ЖИЗНЬ(Разработчики: Резник Игорь, Цапкова Елизавета)
# ========================================================================


# ========================================================================
# ТРАДИЦИИ(Разработчик: Полиенко Даниил)
# ========================================================================


# ========================================================================
# ПОМОЩЬ(Разработчик: Полиенко Даниил)
# ========================================================================


# =======================================================================
# ЗАПУСК БОТА
# =======================================================================


if __name__ == '__main__':
    print('Бот запущен и готов к работе! 🚀')
    bot.polling(none_stop=True)