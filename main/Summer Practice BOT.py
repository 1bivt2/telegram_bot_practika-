import time
from colorama import init
from PIL import Image
import io
from telebot.types import WebAppInfo
from telebot.types import InputMediaPhoto
#РАСПИСАНИЕ
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
# Инициализация colorama для цветного вывода в консоль
init()
from colorama import Fore, Back, Style
import telebot
from telebot import types

# Конфигурация бота
TOKEN = '7428981437:AAH_dXO9neL50DS6zcBnnsi-4Hu4_3-4msY' #- игоря
#TOKEN = '7966778534:AAH2SWtEAV34Ck_4Z1YU-RNMAqMu7FuoqRI'  # - мой
#TOKEN = '8187726226:AAEKveJ4SWsxlWJM4-yi25vSDeBSsTazrdA' #-ТЕСТ
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')


def handle_back_button(message):
    """Обработчик кнопки возврата в главное меню"""
    try:
        # Пытаемся удалить предыдущее сообщение (если есть)
        bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    main(message)


# =======================================================================
# ОСНОВНОЕ МЕНЮ
# =====================================================================

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
        bot.register_next_step_handler(call.message, handle_reply_buttons)
    if call.data == 'student_life':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnlife1 = types.KeyboardButton("🧑🏻‍🏫Профком")
        btnlife2 = types.KeyboardButton("🏃🏻Студактивности")
        btnlife3 = types.KeyboardButton("🎈Мероприятия")
        btnlife4 = types.KeyboardButton("🤑Денежные выплаты")
        btnlife5 = types.KeyboardButton("🚂Поездки")
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btnlife1, btnlife2, btnlife3)
        markup.add(btnlife4, btnlife5)
        markup.add(btn_back)
        bot.send_message(call.message.chat.id, "Выберите интересующий вас раздел:", reply_markup=markup)
        bot.register_next_step_handler(call.message,life)


    elif call.data == 'schedule':

        markup = types.InlineKeyboardMarkup(row_width=1)

        # 1. Кнопка встроенного расписания в боте (автоматический поиск по группе)

        btn_get_schedule = types.InlineKeyboardButton(

            '📅 Расписание в боте',

            callback_data='show_schedule_menu'

        )

        # 2. Кнопка WebApp (ручной поиск на сайте)

        btn_webapp = types.InlineKeyboardButton(

            '🌐 Расписание на сайте МАДИ',

            web_app=WebAppInfo(url="https://raspisanie.madi.ru/tplan/")

        )
        btn_back = types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_main')

        markup.add(btn_get_schedule, btn_webapp, btn_back)

        bot.edit_message_text(

            chat_id=call.message.chat.id,

            message_id=call.message.message_id,

            text=(

                "<b>📅 Выберите способ просмотра расписания</b>\n\n"

                "<b>В боте</b> - автоматический поиск по вашей группе <i>(БЕТА ТЕСТ)</i> 🧑🏻‍💻\n"

                "<b>На сайте</b> - ручной поиск на официальном сайте <i>(СТАБИЛЬНАЯ)</i> ✅"
            ),

            reply_markup=markup,

            parse_mode='HTML'

        )

    elif call.data == 'show_schedule_menu':
          show_schedule_menu(call.message)

    elif call.data == 'select_group':

        ask_for_group_name(call.message)

    elif call.data == 'get_schedule':

        handle_get_schedule(call)

    elif call.data == 'back_to_schedule':

        show_schedule_menu(call.message)
    if call.data == 'traditions':
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

    if call.data == 'help':
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
    elif call.data == 'back_to_main':  # Новый обработчик
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except:
            pass
        main(call.message)
        return


    elif call.message.text == '🔙 Возврат в главное меню':
        handle_back_button(call.message)



# =======================================================================
# ОБРАБОТЧИК ТЕКСТОВЫХ СООБЩЕНИЙ ПРОФКОМ
# =======================================================================
def life(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == '🧑🏻‍🏫Профком':
        text = """<b>👥 Первичная профсоюзная организация студентов МАДИ</b>

<u>📅 Дата основания:</u>
<i>2 июня 1999 года на общем собрании студентов</i>

<u>🎯 Основные направления деятельности:</u>
• <b>Правовая защита</b> интересов студентов
• <b>Помощь</b> в решение конфликтных ситуаций с преподавателями
• <b>Консультационная поддержка</b> по вопросам:
  - Стипендиального обеспечения
  - Проживания в общежитиях
  - Академических вопросов
• <b>Представительство</b> обучающихся в органах управления университетом
• <b>Управление</b> основной частью денежных выплат

<u>🔧 Методы работы:</u>
✔️ <b>Личные консультации</b>
✔️ <b>Онлайн-поддержка</b>
✔️ Работа с правовой системой <b>"Консультант+"</b>
✔️ Привлечение <b>профессиональных юристов</b>

<u>🏆 Ключевые достижения (2009-2014):</u>
• Разработка <b>Положения о стипендиальном обеспечении</b>
• Участие в создании <b>Правил внутреннего распорядка</b>
• Совершенствование <b>Положения о студенческом городке</b>
• Организация <b>волонтерского движения</b>

<u>📜 Разработанные документы:</u>
<code>
1. Положение о ППО студентов МАДИ
2. Правила перевода между формами обучения
3. Нормы проживания в общежитиях
4. Положение о материальной помощи
</code>

<b>📩 Официальная группа:</b> <a href="https://vk.com/ppoomadi">VK</a>
<b>🌐 Официальный сайт:</b> <a href="http://profcommadi.ru/">profcommadi.ru</a>
<b>🗣 Телеграм-канал:</b> <a href="https://t.me/ppomadi">@ppomadi</a>
<b>📞 Контакты:</b> <code>+7 (499) 155-07-46</code>"""

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btn_back)
        photo = open('profkom.jpg', 'rb')
        bot.send_photo(message.chat.id, photo,reply_markup=markup)
        bot.send_message(message.chat.id, text, reply_markup=markup)
    if message.text == "🏃🏻Студактивности":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')
        text = """<b>Студенческая жизнь в Московском автомобильно-дорожном государственном техническом университете (МАДИ)</b>

Студенческая жизнь в МАДИ насыщенная и разнообразная, включающая множество направлений деятельности для самореализации студентов.

<b>🎓 1. Студенческое самоуправление и социальная поддержка</b>
Первичная профсоюзная организация студентов (ППОС) МАДИ занимается защитой прав студентов, организацией культурных мероприятий и курирует деятельность студенческих строительных отрядов. Студенческий совет общежитий решает вопросы проживания и организует мероприятия для жителей кампуса. Активные студенты получают льготные путёвки в санатории, повышенные стипендии и другие поощрения.

<b>🎭 2. Культурно-массовая деятельность</b>
Университет проводит традиционные мероприятия: конкурс "Мисс МАДИ", празднование Татьяниного дня, шоу-программы ко Дню университета и церемонии посвящения в студенты. Работают творческие коллективы: команда КВН "Ближний Свет", театральные студии и танцевальные ансамбли. Ежегодно проходит фестиваль "ФЕСТОС" с конкурсами эстрадного вокала и бардовской песни.

<b>⚽ 3. Спортивная жизнь</b>
В университете действуют секции по различным видам спорта: единоборства (самбо, карате), игровые виды (волейбол, баскетбол, хоккей). Ежегодная спартакиада включает соревнования по 30 видам спорта, в том числе автоспорту и бадминтону. Студенты участвуют в международных турнирах, включая Спартакиаду автомобильно-дорожных вузов СНГ.

<b>🔧 4. Научная и инженерная деятельность</b>
Студенческие строительные отряды МАДИ участвовали в возведении объектов для крупных международных мероприятий. В университете работают инженерные лаборатории и проектные команды, такие как "МАДИ-Дрифт" и "MADI Karting Team". Регулярно проводятся научные конференции с участием студентов из российских и зарубежных вузов.

<b>❤️ 5. Волонтёрская работа</b>
Волонтёрский центр МАДИ организует экологические акции, оказывает помощь социальным учреждениям и участвует в городских программах. Студенческий сервисный отряд "Леон" специализируется на благотворительной деятельности.

<b>🌍 6. Международное сотрудничество</b>
Студенты участвуют в международных экспедициях и научных форумах, университет развивает партнёрские отношения с вузами Монголии и других стран. Для иностранных студентов проводятся специальные олимпиады с возможностью получения бесплатного обучения.

<b>💼 7. Карьерные возможности</b>
Университет сотрудничает с ведущими предприятиями отрасли, предоставляя студентам возможности для стажировок и трудоустройства. Регулярно проводятся дни открытых дверей с экскурсиями по лабораториям и мастер-классами.

<b>🏆 Примеры реализованных проектов:</b>
- В 2025 году университет получил 14,8 миллионов рублей грантовой поддержки
- Традиционный автопробег "Дорога Победы"
- Участие в федеральных программах развития

Для получения дополнительной информации:
🔗 Официальный сайт: <a href="https://madi.ru">madi.ru</a>
🔗 Студактивности МАДИ ссылка на ВК: https://vk.com/university_madi?to=L3VuaXZlcnNpdHlfbWFkaT8-"""
        photo = open('ВР.jpg', 'rb')
        markup.add(btn_back)
        bot.send_photo(message.chat.id, photo,reply_markup=markup)
        bot.send_message(message.chat.id, text, reply_markup=markup)
    if message.text == "🎈Мероприятия":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')
        text = """🎉 Мероприятия и активная жизнь с Профкомом

Студенчество — это время открытий, развития и самореализации!
Профком МАДИ ежегодно проводит мероприятия по самым разным направлениям, где каждый может найти что-то по душе: от спорта и творчества до лидерства и общественной деятельности ✨
🎓 Вузовские мероприятия

Здесь ты можешь заявить о себе, познакомиться с единомышленниками и прокачать свои навыки 💬💪

    🧩 "Просто учись быть первым" — спортивно-интеллектуальная игра для адаптации первокурсников

    🚀 Школа студенческого актива — старт для будущих лидеров

    🏆 Профорг года МАДИ — конкурс, в котором выбирают самого инициативного и активного профорга

    👥 Конкурс на лучшую команду института МАДИ — покажи силу своего коллектива!

📍 Региональные мероприятия

Участвуй и представляй МАДИ на уровне города — заяви о себе в масштабах Москвы!

    🌟 Профорг года г. Москвы

    🏅 Конкурс на лучшее профбюро

    и другие события, где ты можешь проявить лидерские и организационные качества

🌐 Всероссийские мероприятия

Самые масштабные площадки страны ждут твоего участия! Это не только опыт, но и новые друзья со всей России 🇷🇺

    🧠 Студенческий лидер — конкурс для самых активных представителей студенчества

    📚 "Лекториум" — образовательная платформа с интереснейшими лекциями и мастер-классами

    🏕 Форум "ОБЩАГА" — обмен опытом и студенческая тусовка в одном формате

    💼 "СТИПКОМ" — школа стипендиальных комиссий для тех, кто хочет разбираться в системе поддержки студентов

Следи за новостями в группе Профкома обучающихся МАДИ ( https://vk.com/ppoomadi ) и не упусти шанс стать частью яркой студенческой истории! 🌟
"""
        markup.add(btn_back)
        photo = open('МЕРОПРИЯТИЯ.jpg', 'rb')
        bot.send_photo(message.chat.id, photo,reply_markup=markup)
        bot.send_message(message.chat.id, text, reply_markup=markup)
    if message.text == "🤑Денежные выплаты":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')
        text = """<b>💰 Денежные выплаты для студентов МАДИ</b>

    В МАДИ предусмотрено несколько видов материальной поддержки для студентов. Ниже — краткое руководство, куда обращаться и на что рассчитывать 👇

    <u>🤝 Материальная помощь от Профсоюза</u>
    Если ты оказался(-ась) в сложной жизненной ситуации — не оставайся один(-а)! Всегда можно обратиться в профком за разовой материальной помощью. Это может быть связано с:
    • Болезнью
    • Утратой близких
    • Чрезвычайными происшествиями

    👉 <b>Просто напиши в <a href="https://vk.com/ppoomadi">Профком обучающихся МАДИ</a></b> — тебе подскажут, что нужно сделать.

    <u>🎓 Стипендии</u>
    • Размеры стипендий на 2025 год станут известны в сентябре
    • Доступны разные виды:
      - Академические
      - ПГАС
      - От правительства

    🔔 <b>Следи за обновлениями</b>, чтобы ничего не пропустить! Вся информация появится в <a href="https://vk.com/ppoomadi">официальной группе профкома</a>.

    <u>📌 Единовременная материальная поддержка</u>
    • Доступна раз в квартал
    • Может получить каждый студент в затруднительном положении
    • Подробности по срокам и документам в <a href="https://vk.com/ppoomadi">группе ППО МАДИ</a>

    <u>🏙 Материальная поддержка из бюджета города Москвы</u>
    • Выплаты от правительства Москвы
    • Заявки принимаются раз в семестр
    • Выплаты на конкурсной основе — раз в квартал
    • <b>Размер:</b> 3 600 рублей

    💡 <b>Не упусти возможность!</b> Все актуальные даты и инструкции в <a href="https://vk.com/ppoomadi">группе профкома</a>."""
        markup.add(btn_back)
        photo = open('Материальная поддержка Единовр.jpg', 'rb')
        photo1 = open('Поддержка из средств бюджета Москвы.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, reply_markup=markup)
        bot.send_photo(message.chat.id, photo1, reply_markup=markup)
        bot.send_message(message.chat.id, text, reply_markup=markup)
    if message.text == "🚂Поездки":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')
        text = """<b>🚍 Поездки и отдых с Профкомом МАДИ</b>

<i>Студенческая жизнь — это не только учеба, но и новые впечатления, путешествия и восстановление сил.</i> Профком МАДИ регулярно организует экскурсии и оздоровительные поездки для студентов. Рассказываем, что вас ждёт 👇

<u>🏙 Экскурсионные поездки</u>
Каждый учебный год профком организует экскурсии по городам России. Это отличная возможность:
• Увидеть новые места
• Отдохнуть от учёбы
• Провести время с друзьями <b>и завести новые знакомства</b> 🤝

📅 <b>Более подробная информация</b> о направлениях и датах появится в конце августа — начале сентября. Следите за анонсами в <a href="https://vk.com/ppoomadi">группе Профкома</a>!

<u>🏖 Оздоровление</u>
Хочешь перезагрузиться и набраться сил на свежем воздухе?

<b>Летнее оздоровление:</b>
🌊☀️ Ежегодно в августе на побережье Чёрного моря

<b>Зимнее оздоровление:</b>
❄️🏔 Конец января — время тепла и заснеженных пейзажей

👉 <b>Все подробности</b> о месте, условиях участия и подаче заявок будут опубликованы ближе к датам заезда. <i>Не пропусти!</i>

🔔 <b>Если хочешь участвовать</b> — следи за новостями в <a href="https://vk.com/ppoomadi">официальной группе Профкома</a>, где будут появляться:
• Формы регистрации
• Условия участия
• Списки участников"""
        markup.add(btn_back)
        photo = open('ПОЕЗДКИ.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, reply_markup=markup)
        bot.send_message(message.chat.id, text, reply_markup=markup)


    # =======================================================================
# ОБРАБОТЧИКИ ТЕКСТОВЫХ СООБЩЕНИЙ (REPLY-КНОПКИ)
# =======================================================================
@bot.message_handler(content_types=['text'])
def handle_reply_buttons(message):
    """Обработчик текстовых сообщений для Reply-кнопок"""
    # Проверка на кнопку возврата ДО основного кода
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return  # Важно: прерываем выполнение функции

    # Остальной код обработки...
    if message.text == '🗒️ Текстовый гид':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('🍽️ Питание')
        btn2 = types.KeyboardButton('📖 Библиотека')
        btn3 = types.KeyboardButton('👔 Гардероб')
        btn4 = types.KeyboardButton('🎖️ ВУЦ')
        btn5 = types.KeyboardButton('🎭 Актовый зал')
        btn6 = types.KeyboardButton('🎓 ЦадиЛ')
        btn7 = types.KeyboardButton('📜 Музей МАДИ')
        btn8 = types.KeyboardButton('🏃 Физическое воспитание')
        btn9 = types.KeyboardButton('👥 Профком')
        btn10 = types.KeyboardButton('🚪 400 кабинет')
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')

        markup.row(btn1, btn2, btn3, btn4)
        markup.row(btn5, btn6, btn7)
        markup.row(btn8, btn9, btn10)
        markup.row(btn_back)

        response_text = """
        <b>📝 ТЕКСТОВЫЙ ГИД ПО МАДИ</b>
        Здесь вы найдете подробное описание ключевых мест университета. 

        Выберите интересующий вас объект:
        """
        bot.send_message(
            message.chat.id,
            response_text,
            reply_markup=markup
        )
        bot.register_next_step_handler(message, objects_text)

    elif message.text == '🎬 Видео-гид':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('🍽️ Питание')
        btn2 = types.KeyboardButton('📖 Библиотека')
        btn3 = types.KeyboardButton('👔 Гардероб')
        btn4 = types.KeyboardButton('🎖️ ВУЦ')
        btn5 = types.KeyboardButton('🎭 Актовый зал')
        btn6 = types.KeyboardButton('🎓 ЦадиЛ')
        btn7 = types.KeyboardButton('📜 Музей МАДИ')
        btn8 = types.KeyboardButton('🏃 Физическое воспитание')
        btn9 = types.KeyboardButton('👥 Профком')
        btn10 = types.KeyboardButton('🚪 400 кабинет')
        btn_back = types.KeyboardButton('🔙 Возврат в главное меню')

        markup.row(btn1, btn2, btn3, btn4)
        markup.row(btn5, btn6, btn7)
        markup.row(btn8, btn9, btn10)
        markup.row(btn_back)

        response_text = """
        <b>🎥 Видео-гид по МАДИ</b>
        Здесь вы можете посмотреть короткие видео-экскурсии по ключевым местам университета. 

        Выберите интересующий объект:
        """
        bot.send_message(
            message.chat.id,
            response_text,
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

    elif message.text == '👥 Выбрать группу':
        try:
            parser = MadiScheduleParser()
            groups = parser.get_groups()
            del parser

            if not groups:
                error_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                error_markup.add(types.KeyboardButton('🔙 Назад'))
                bot.send_message(
                    message.chat.id,
                    "⚠️ Не удалось загрузить список групп. Попробуйте позже.",
                    reply_markup=error_markup
                )
                return

            # Создаем клавиатуру с группами (максимум 20 групп)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            buttons = [types.KeyboardButton(group) for group in sorted(groups)[:20]]
            markup.add(*buttons)
            markup.add(types.KeyboardButton('🔙 Назад'))

            # Сохраняем данные пользователя
            user_data[message.chat.id] = {
                'groups': groups,
                'waiting_for_group': True,
                'previous_markup': message.reply_markup  # Сохраняем предыдущую клавиатуру
            }

            loading_msg = bot.send_message(
                message.chat.id,
                "⌛️ Загружаю список групп...",
                reply_markup=types.ReplyKeyboardRemove()
            )

            # Удаляем сообщение "Загружаю" и показываем список групп
            bot.delete_message(message.chat.id, loading_msg.message_id)
            bot.send_message(
                message.chat.id,
                "👇 Пожалуйста, выберите вашу группу из списка:",
                reply_markup=markup
            )

        except Exception as e:
            error_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            error_markup.add(types.KeyboardButton('🔙 Назад'))
            bot.send_message(
                message.chat.id,
                f"⚠️ Ошибка при загрузке групп: {str(e)}",
                reply_markup=error_markup
            )
            print(f"Ошибка при выборе группы: {e}")
    elif message.chat.id in user_data and user_data[message.chat.id].get('waiting_for_group', False):
        if message.text == '🔙 Назад':
            # Возвращаемся к предыдущему меню
            user_data[message.chat.id]['waiting_for_group'] = False
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            markup.add(
                types.KeyboardButton('👥 Выбрать группу'),
                types.KeyboardButton('📅 Получить расписание')
            )
            markup.add(types.KeyboardButton('🔙 Возврат в главное меню'))

            bot.send_message(
                message.chat.id,
                "<b>📅 Расписание МАДИ</b>\n\nВыберите действие:",
                reply_markup=markup
            )
            return

        # Проверяем, что выбранная группа есть в списке
        if message.text not in user_data[message.chat.id]['groups']:
            bot.send_message(
                message.chat.id,
                "⚠️ Выбранная группа не найдена. Пожалуйста, выберите группу из списка."
            )
            return

        # Сохраняем выбранную группу
        user_data[message.chat.id].update({
            'selected_group': message.text,
            'waiting_for_group': False
        })

        # Создаем клавиатуру для работы с расписанием
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            types.KeyboardButton('👥 Выбрать группу'),
            types.KeyboardButton('📅 Получить расписание')
        )
        markup.add(types.KeyboardButton('🔙 Возврат в главное меню'))

        # Отправляем подтверждение
        bot.send_message(
            message.chat.id,
            f"✅ Группа <b>{message.text}</b> успешно выбрана!\n"
            "Теперь вы можете получить расписание.",
            reply_markup=markup,
            parse_mode='HTML'
        )
    elif message.text == '📅 Получить расписание':
        if message.chat.id not in user_data or 'selected_group' not in user_data[message.chat.id]:
            bot.send_message(message.chat.id, "ℹ️ Сначала выберите группу")
            return

        send_schedule(message)

    elif message.text == '🔙 Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_group = types.KeyboardButton('👥 Выбрать группу')
        btn_schedule = types.KeyboardButton('📅 Получить расписание')
        btn_back = types.KeyboardButton('🔙 Назад')
        markup.add(btn_group, btn_schedule, btn_back)

        bot.send_message(message.chat.id, "<b>📅 Расписание МАДИ</b>\n\nВыберите действие:", reply_markup=markup)

    elif message.chat.id in user_data and user_data[message.chat.id].get('waiting_for_group', False):
        if message.text == '🔙 Назад':
            user_data[message.chat.id]['waiting_for_group'] = False
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            btn_group = types.KeyboardButton('👥 Выбрать группу')
            btn_schedule = types.KeyboardButton('📅 Получить расписание')
            btn_back = types.KeyboardButton('🔙 Назад')
            markup.add(btn_group, btn_schedule, btn_back)
            bot.send_message(message.chat.id, "<b>📅 Расписание МАДИ</b>\n\nВыберите действие:", reply_markup=markup)
            return

        if message.text not in user_data[message.chat.id]['groups']:
            bot.send_message(message.chat.id, "⚠️ Пожалуйста, выберите группу из предложенного списка.")
            return

        user_data[message.chat.id]['selected_group'] = message.text
        user_data[message.chat.id]['waiting_for_group'] = False

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_group = types.KeyboardButton('👥 Выбрать группу')
        btn_schedule = types.KeyboardButton('📅 Получить расписание')
        btn_back = types.KeyboardButton('🔙 Назад')
        markup.add(btn_group, btn_schedule, btn_back)
        bot.send_message(
            message.chat.id,
            f"✅ Группа {message.text} сохранена!\nТеперь вы можете получить расписание",
            reply_markup=markup
        )
# =======================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ТЕКСТОВЫМ ГИДОМ
# =======================================================================

def objects_text(message):
    """Обработчик объектов для текстового гида"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == '🍽️ Питание':
        text = """Выберите расположение:"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btndining1 = types.KeyboardButton("🏛️ Главный корпус")
        btndining2 = types.KeyboardButton("🔬 Лабораторный корпус")
        btndining_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btndining1, btndining2)
        markup.add(btndining_Back)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, dining_rooms)
    if message.text == '📖 Библиотека':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btndlibrary1 = types.KeyboardButton("🏛️ Главный корпус")
        btndlibrary2 = types.KeyboardButton("🔬 Лабораторный корпус")
        btndlibrary_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btndlibrary1, btndlibrary2)
        markup.add(btndlibrary_Back)
        bot.send_message(message.chat.id, "Выберите куда отправимся", reply_markup=markup)
        bot.register_next_step_handler(message, library_text)

    # ---------------------------------------------------
    # ----Гардероб изначальный вариант----
    # ---------------------------------------------------

    # if message.text == '👔 Гардероб':
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     btndclothes_loc = types.KeyboardButton("Как пройти❓")
    #     btndclothes_Back = types.KeyboardButton("🔙 Возврат в главное меню")
    #     markup.add(btndclothes_loc)
    #     markup.add(btndclothes_Back)
    #     bot.send_message(message.chat.id, "В ожидании информации🤔", reply_markup=markup)

    # ---------------------------------------------------
    # ---------------------------------------------------
    if message.text == '👔 Гардероб':
        text1 = """
            🎬 <b>ТЕКСТОВЫЙ ГИД ДО ГАРДЕРОБА МАДИ</b> 🧥

            Выберите корпус для просмотра видео-экскурсии:

            🏛️ <b>Главный корпус</b> - 2 гардероба
            • 1 этаж ▶️ - основной
            • Подвал ▶️ - дополнительный

            🔬 <b>Лабораторный корпус</b> - мгновенный показ
            """
        text2 = """Выберите интересующий вас корпус:"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_main = types.KeyboardButton("🏛️ Главный корпус")
        btn_lab = types.KeyboardButton("🔬 Лабораторный корпус")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_main, btn_lab)
        markup.add(btn_back)
        bot.send_message(message.chat.id, text1, reply_markup=markup)
        bot.send_message(message.chat.id, text2, reply_markup=markup)
        bot.register_next_step_handler(message, clothes_corpus_text)

    if message.text == '🎖️ ВУЦ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_loc = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc)
        markup.add(btn_back)
        text = """
                <b>🎖️ ВОЕННЫЙ УЧЕБНЫЙ ЦЕНТР(ВУЦ)</b>
                <b>Военный учебный центр</b> является структурным подразделением <b>Московского автомобильно-дорожного государственного технического университета (МАДИ)</b> с момента его основания.
        <b>Требования для участия в конкурсном отборе:</b>
        - Иметь гражданство РФ
        - Обучаться по очной форме обучения
        - Состоять на воинском учёте в Военном комиссариате
        - Иметь уровень физической подготовки, соответствующий Нормативам по физической подготовке
        - Основная специальность должна быть включена в Перечень направлений
        - Возраст не старше 27 лет
        - Не иметь задолженностей по учёбе
        - Годность по состоянию здоровья
        Ссылка для более подробного изучения о <b>ВУЦ МАДИ</b>: https://madi.ru/6421-voennyy-uchebnyy-centr-vuc-informaciya.html
                <u>Нажмите "Как пройти❓", чтобы посмотреть видео-экскурсию до ВУЦ.</u>
                """
        photo = open('вуц .jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption=text,reply_markup=markup)
        bot.register_next_step_handler(message, process_vuc_text)
    if message.text == '🎭 Актовый зал':
        text = """<b>🎭 Актовый зал МАДИ</b>

📍 <b>Местоположение:</b>
🏛 Главный корпус МАДИ
📌 Ленинградский пр-т, 64, <b>ауд. 344 (3 этаж)</b>

📌 <b>Назначение:</b>
✔ Организационные собрания (встречи с первокурсниками, инструктажи)
✔ Дни открытых дверей, конференции
✔ Творческие мероприятия
✔ Торжественные церемонии

🛠 <b>Оснащение:</b>
• Современная мультимедийная система
• Пространство для массовых мероприятий
• Сцена для выступлений

🏛 <b>Историческая справка:</b>
Зал сохранил архитектурные особенности 1950-х годов, сочетая их с современным оснащением.

🔗 <b>Подробнее:</b> <a href="https://madi.ru">madi.ru</a>"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btndclAct_loc = types.KeyboardButton("Как пройти❓")
        btndclAct_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btndclAct_loc)
        markup.add(btndclAct_Back)
        photo = open('актовый зал мади.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)
        bot.register_next_step_handler(message, Act_loc)
    if message.text == '🎓 ЦадиЛ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🏗️ Зал ЦАДИ-Л в МАДИ</b>

📍 <b>Расположение:</b>
🏢 Новый корпус университета
🔍 В структуре <b>Центра автомобильно-дорожного инжиниринга (ЦАДИ)</b>

<b>🎯 Основные функции:</b>

🔹 <b>Учебная деятельность:</b>
• Проведение занятий и семинаров
• Лабораторные работы
• Изучение технологий испытаний мостовых конструкций

🔹 <b>Научные исследования:</b>
• Проекты по импортозамещению
• Реверс-инжиниринг
• Разработка передвижных лабораторий для мониторинга дорог

🔹 <b>Мероприятия:</b>
• Киберспортивный турнир (февраль 2025)
• Научные конференции
• Встречи студенческих организаций

<b>💡 Особенности:</b>
✅ Многофункциональность: обучение + исследования + мероприятия
✅ Современное оборудование для инженерных работ
✅ Техническая база для событий

<b>🌟 Значение:</b>
Интегрирует образовательную, научную и внеучебную деятельность МАДИ"""
        btnL_loc = types.KeyboardButton("Как пройти❓")
        btnL_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btnL_loc)
        markup.add(btnL_Back)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message,tsadi_L_Loc)
    if message.text == '📜 Музей МАДИ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_loc = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc)
        markup.add(btn_back)

        text = """<b>📜 МУЗЕЙ </b>
                ℹ️ <b>ИНФОРМАЦИЯ О МУЗЕЕ МАДИ</b>

                Университет - учреждение, в котором <u>всё подчинено учебному процессу</u>.
                Музейные документы и стенды представляют самую разностороннюю информацию
                о создании и развитии каждого <b>факультета</b> и каждой <b>кафедры</b>. Юные студенты
                с интересом знакомятся с экспозицией музея, а с полотен высоко висящих фотографий
                смотрят глаза тех, чьи силы и талант навсегда стали частью родного <b>МАДИ</b>.

                Музей призван напоминать о том, что <b>инженерное дело</b> является интересным не только само по себе,
                что оно - часть общей культуры, поэтому здесь проходят встречи как с корифеями <i>науки, техники,
                искусства</i> так и с творческой молодежью и артистами. Это общение воспитывает художественный вкус,
                а главное мотивирует стремление к профессионализму, важному в любом деле.

                Здесь вы найдете:

                • Экспозицию об основании университета в <b>1930 году</b>
                • Исторические документы и фотографии
                • Модели первых <b>автомобилей</b> и дорожной техники
                • Интерактивные стенды о развитии транспорта
                • Выставку достижений <b>студентов и преподавателей</b>

                Чтобы ознакомиться более подробнее с <b>музеем МАДИ</b> перейдите по ссылке: https://madi.ru/2380-muzey-o-nas.html
                <u>Чтобы узнать как <i>добраться</i> до музея нажмите кнопку: Как пройти❓</u>"""
        photo = open('Музей.jpg', 'rb')
        bot.send_photo(message.chat.id, photo,reply_markup=markup)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, process_museum_text)

    if message.text == '🏃 Физическое воспитание':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_gym = types.KeyboardButton("🏋️ Спортзал")
        btn_stadium = types.KeyboardButton("🏟️ Стадион")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_gym, btn_stadium)
        markup.add(btn_back)

        text = """<b>🏃 Физическое воспитание в МАДИ</b>

            Выберите объект:
            • 🏋️ <b>Спортзал</b> - расположен в главном корпусе
            • 🏟️ <b>Стадион</b> - спортивный комплекс "Октябрь"
            """
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, process_sport_selection_text)

    if message.text == '👥 Профком':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>👥 ПРОФКОМ СТУДЕНТОВ МАДИ</b>
            Первичная Профсоюзная организация работников Московского автомобильно-дорожного государственного 
            технического университета (МАДИ) Московской городской организации Общероссийского профсоюза образования 
            (ППО РАБОТНИКОВ МАДИ МГО ОБЩЕРОССИЙСКОГО ПРОФСОЮЗА ОБРАЗОВАНИЯ) была образована из объединенной профсоюзной 
            организации МАДИ в 1989 году. Ее руководителем был избран Гурьянов Вячеслав Михайлович, который руководил ею до 2024 года.

            Это выборный орган студенческого самоуправления, который:
            • Защищает права студентов
            • Организует культурные мероприятия
            • Помогает с решением бытовых вопросов
            • Предоставляет материальную поддержку
            • Организует льготные путевки в санатории

            🌐 Официальная группа: https://vk.com/profkom_madi
            📞 Контакты: +7 (499) 155-01-91
            <u>Чтобы узнать как <i>добраться</i> до Профкома нажмите кнопку: Как пройти❓</u>"""

        btn_loc = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc)
        markup.add(btn_back)
        photo = open('профком.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)
        bot.register_next_step_handler(message, process_profcom_text)

    if message.text == '🚪 400 кабинет':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_loc = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc)
        markup.add(btn_back)

        text = """
                    <b>🚪 Лекционная аудитория 400</b>
                    """

        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, process_400_text)
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

def korp_MADI_text(message):
    """Обработчик учебных корпусов (текстовый режим)"""
    if message.text in ['🏛️ Главный корпус', '🏬 Новый корпус', '🔬 Лабораторный корпус']:
        markup = types.ReplyKeyboardMarkup()
        bt_korp_MADI1_back = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(bt_korp_MADI1_back)
        bot.send_message(message.chat.id, 'Контент в процессе', reply_markup=markup)

    elif message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)

# НАЧАЛО РАЗДЕЛА СТОЛОВЫЕ
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
# СТОЛОВЫЕ МАДИ ТЕКСТОВЫЙ ГИД

# ========================================================================
# 3.1.СТОЛОВЫЕ ТЕКСТОВЫЙ ГИД
# ========================================================================
def dining_rooms(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "🏛️ Главный корпус":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_text_buffet_1 = types.KeyboardButton("🍩 1 этаж - буфет")
        btn_text_gl4_table = types.KeyboardButton("🍽️ 4 этаж - столовая")
        btn_text_gl2_table = types.KeyboardButton("🍴 2 этаж - столовая")
        btndining_gl_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_text_buffet_1)
        markup.add(btn_text_gl2_table,btn_text_gl4_table)
        markup.add(btndining_gl_Back)
        text_gl = """<b>🍽️ Питание в МАДИ</b>

<b>🏛️ Главный корпус:</b>
┣ <b>2-й этаж</b> — столовая на 120 мест 🪑 
┣ <b>4-й этаж</b> — столовая на 130 мест 🍽️ 

<b>☕️ Буфеты:</b>
┣ <b>1-й этаж</b> — буфет на 24 места 🍩 

<b>📍 Адрес:</b> Ленинградский проспект, д. 64
<b>🌐 Подробнее:</b> <a href="https://madi.ru">madi.ru</a>"""
        bot.send_message(message.chat.id, text_gl, reply_markup=markup)
        bot.register_next_step_handler(message, diningGl_text)
    if message.text == "🔬 Лабораторный корпус":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        text_lab = """<b>🍽️ Столовые МАДИ</b>

🏛️ <b>Лабораторный корпус:</b>
┗ 1-й этаж — столовая на <b>70</b> посадочных мест 🔬

Куда отправимся❓
"""
        btn_text_buffet = types.KeyboardButton("🔬 1 этаж")
        btndining_gl_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_text_buffet)
        markup.add(btndining_gl_Back)
        bot.send_message(message.chat.id, text_lab, reply_markup=markup)
        bot.register_next_step_handler(message, diningLAB_text)


# ========================================================================
# 3.1.СТОЛОВЫЕ ТЕКСТОВЫЙ ГИД(ОБРАБОТЧИКИ)(ЭТАЖИ)
# ========================================================================

def diningGl_text(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "🍩 1 этаж - буфет":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🍽️ Буфет в главном корпусе МАДИ (2025 год)</b>

📍 <b>Расположение:</b> 1-й этаж главного корпуса
🪑 <b>Вместимость:</b> 24 посадочных места

<b>🍴 Ассортимент:</b>
- Сэндвичи и снеки
- Пирожные и сладости
- Соки и вода
- Горячие напитки (чай, кофе)

<i>Удобное место для быстрого перекуса между занятиями</i>

📌 <b>Адрес:</b> Ленинградский проспект, д. 64
🌐 <b>Подробнее:</b> <a href="https://madi.ru">madi.ru</a>"""
        btn_loc3 = types.KeyboardButton("Как пройти❓")
        btn_Back3 = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc3)
        markup.add(btn_Back3)
        photo = open('Буфет.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)
        bot.register_next_step_handler(message, buffet_1_loc)
    if message.text == "🍽️ 4 этаж - столовая":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🍽️ Питание в университете</b>

На территории университета работают столовые, где можно приобрести полноценные <b>завтраки и обеды</b>.

<b>📍 Столовая в Главном корпусе</b>
- <b>4 этаж</b>, 130 посадочных мест
- <b>Стол заказов</b> – можно заказать еду на вынос
- <b>Телефон для заказов</b>:
  <code>8 (965) 268 99 80</code> (Вера Александровна Горелова)

<b>🎉 Дополнительные услуги</b>
Комбинат питания принимает заказы на:
- Проведение <b>торжественных мероприятий</b>

<b>🌐 Подробнее:</b> <a href="https://madi.ru">madi.ru</a>"""
        btn_loc4 = types.KeyboardButton("Как пройти❓")
        btn_Back4 = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc4)
        markup.add(btn_Back4)
        photo = open('столовая 4 этаж.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)
        bot.register_next_step_handler(message, table4_loc)
    if message.text == "🍴 2 этаж - столовая":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🍽️ Столовые университета</b>

На территории университета работают столовые, где можно приобрести полноценные <b>завтраки и обеды</b>.

<b>📍 Столовая в Главном корпусе</b>
• <b>2 этаж</b>
• <b>120 посадочных мест</b>

<b>🎉 Дополнительные услуги:</b>
Комбинат питания организует:
- Проведение <b>торжественных мероприятий</b>

<b>🌐 Подробнее:</b> <a href="https://madi.ru">madi.ru</a>
"""

        btn_loc1 = types.KeyboardButton("Как пройти❓")
        btn_Back1 = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc1)
        markup.add(btn_Back1)
        photo = open('Столовая 2 этаж.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)
        bot.register_next_step_handler(message,table2_loc)


# ^-----------------------------------------------------------------------
def diningLAB_text(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "🔬 1 этаж":
        text = """<b>🍽️ Столовая в Лабораторном корпусе</b>

В Лабораторном корпусе университета работает уютная столовая, где вы можете:
- Вкусно <b>позавтракать</b>
- Плотно <b>пообедать</b>
- Взять еду <b>с собой</b>

<b>📍 Местоположение:</b>
• <b>1 этаж</b> Лабораторного корпуса
• <b>70 посадочных мест</b>
• Доступно питание на вынос

<b>📌 Особенности:</b>
- Свежие комплексные обеды
- Разнообразная выпечка

<b>🌐 Подробнее:</b> <a href="https://madi.ru">madi.ru</a>
"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_loclab1 = types.KeyboardButton("Как пройти❓")
        btn_Back1 = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loclab1)
        markup.add(btn_Back1)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message,table1_loc_lab)

# ========================================================================
# 3.1.СТОЛОВЫЕ ТЕКСТОВЫЙ ГИД(ОБРАБОТЧИКИ)(МАРШРУТЫ❓)
# ========================================================================
def buffet_1_loc(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>☕ Как найти буфет в Главном корпусе:</b>

1️⃣ <b>Старт:</b>
   🏛 Начните от центрального входа Главного корпуса МАДИ
   ➡️ Поверните <b>направо</b>

2️⃣ <b>Движение по коридору:</b>
   ⬆️ Идите <b>прямо по коридору до конца</b>

3️⃣ <b>Финишный ориентир:</b>
   ➡️ Снова поверните <b>направо</b>
   ← <b>Слева</b> дверь с надписью:
   🥪 <b>"БУФЕТ"</b>"""
        btn_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_Back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(буфет)(изм).png", "rb")),
        ]

        # Отправляем группу медиаэтаж1.0(актовый)(изм размер).png
        bot.send_media_group(message.chat.id, media=media)

        # Затем отправляем текстовое сообщение с разметкой
        bot.send_message(message.chat.id, text, reply_markup=markup)

#-------------------------------------------------------------------------

def table4_loc(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🍽️ Путь в столовую Главного корпуса МАДИ</b>

1️⃣ <b>Старт маршрута:</b>
   🏛 Центральный вход (1 этаж)
   ↗ К <b>правой лестнице</b>

2️⃣ <b>Подъем:</b>
   🔼 На <b>3 этаж</b>
   ↪ На выходе <b>дважды налево</b>

3️⃣ <b>Ключевой ориентир:</b>
   🚗 Идите до <b>экспозиции гоночных авто</b>
   ↖ У авто - <b>налево</b>
   🪜 До лестничной площадки

4️⃣ <b>Финальный рывок:</b>
   ➡️ <b>Направо</b>
   🔼 Подъем <b>на 4 этаж</b>

5️⃣ <b>Пункт назначения:</b>
   🍴 <b>СТОЛОВАЯ</b> прямо перед вами!"""
        btn_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_Back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(столовая2-4)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж3.0.(столовая)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж4.0(столовая)(изм).png", "rb"))
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)

        # Затем отправляем текстовое сообщение с разметкой
        bot.send_message(message.chat.id, text, reply_markup=markup)

#-------------------------------------------------------------------------
def table2_loc(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🍽️ Как найти столовую в Главном корпусе:</b>

1️⃣ <b>Старт:</b>
   🏛 Центральный вход Главного корпуса (1 этаж)
   ↗ Идите к <b>правой лестнице</b>

2️⃣ <b>Подъем:</b>
   🔼 Поднимайтесь <b>на 3 этаж</b>
   ↪ На выходе - <b>дважды налево</b>

3️⃣ <b>Ориентиры:</b>
   🚶‍♂️ Идите прямо до <b>экспозиции гоночных авто</b> 🏎️
   ↖ У авто - <b>налево</b>
   🪜 Затем до лестничной площадки

4️⃣ <b>Спуск:</b>
   ➡ <b>Направо</b> 
   🔽 Спуск <b>на 2 этаж</b>

5️⃣ <b>Финиш:</b>
   🍴 <b>Столовая</b> прямо перед вами!
        """
        btn_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_Back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(столовая2-4)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж3.0.(столовая)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж2.0(столовая)(изм).png", "rb"))
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)

        # Затем отправляем текстовое сообщение с разметкой
        bot.send_message(message.chat.id, text, reply_markup=markup)
    elif message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)

#-------------------------------------------------------------------------
def table1_loc_lab(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🍽️ Путь в столовую лабораторного корпуса 🔬</b>

1️⃣ <b>Начало маршрута:</b>
   🏛 Войдите в <b>главный корпус МАДИ</b>
   ↙ Пройдите к <b>левой лестнице</b>
   🌳 Выйдите во внутренний двор

2️⃣ <b>Переход между корпусами:</b>
   🚶‍♂️ Идите <b>прямо</b> по двору
   ↖ На пешеходном переходе сверните <b>направо</b>
   🏢 Пройдите до лабораторного корпуса

3️⃣ <b>Лабораторный корпус:</b>
   🚪 Центральный вход (1 этаж)
   🚶‍♂️ Идите <b>прямо</b> до следующих дверей
   🚪 Пройдите через них и продолжайте идти <b>прямо</b>

4️⃣ <b>Финиш:</b>
   ➡️ С <b>правой стороны</b> увидите дверь с надписью:
   🍴 <b>"КОМБИНАТ ПИТАНИЯ МАДИ СТОЛОВАЯ"</b>
"""
        btn_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_Back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(столоваяЛаб)(изм).png", "rb")),
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)

        # Затем отправляем текстовое сообщение с разметкой
        bot.send_message(message.chat.id, text, reply_markup=markup)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
# КОНЕЦ РАЗДЕЛА СТОЛОВЫЕ


# НАЧАЛО РАЗДЕЛА БИБЛИОТЕКИ
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
# БИБЛИОТЕКИ МАДИ ТЕКСТОВЫЙ ГИД

# ========================================================================
# 3.1.БИБЛИОТЕКИ ТЕКСТОВЫЙ ГИД
# ========================================================================
def library_text(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "🏛️ Главный корпус":
        text = """<b>📚 Научно-техническая библиотека МАДИ</b>  

        Основана в <b>1930 году</b> и является одной из <b>крупнейших университетских библиотек России</b> с уникальным фондом литературы по <b>автомобильно-дорожной тематике</b>.  

        <b>🔍 Основные задачи библиотеки:</b>  
        ✔ Содействие учебному и научному процессам МАДИ  
        ✔ Формирование и хранение отечественных и зарубежных научных материалов  
        ✔ Библиотечное и справочно-библиографическое обслуживание  
        ✔ Внедрение современных автоматизированных и электронных технологий  

        <b>💻 Электронный каталог</b>  
        Базируется на системе <b>АБИС «Руслан»</b> и содержит <b>свыше 107 тысяч записей</b> (книги, статьи из журналов и сборников).  

        🌐 <b>Доступен онлайн:</b> <a href="https://lib.madi.ru/">перейти в каталог</a>"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btndlib_loc = types.KeyboardButton("Как пройти❓")
        btndlib_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btndlib_loc)
        markup.add(btndlib_Back)
        photo = open('библиотека МАДИ главный корпус.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)
        bot.register_next_step_handler(message, library2_loc)
    if message.text == "🔬 Лабораторный корпус":
        text = """  
        📍 <u>Все перечисленные ниже услуги доступны в Научно-технической библиотеке (НТБ) МАДИ, расположенной на <b>3 этаже учебно-лабораторного корпуса (УЛК)</b></u>  
необходимо иметь <b>студенческий билет</b>.  
        <b>ℹ Дополнительная информация:</b>  
        🌐 Сайт НТБ: <a href="https://lib.madi.ru">lib.madi.ru</a>  
        📍 <b>Основные помещения библиотеки:</b>  
           • Абонемент: <b>ауд. 302л</b> (3 этаж УЛК)  
           • Научный читальный зал: <b>ауд. 142б</b>  
           • Отдел справочно-библиографической работы: <b>ауд. 249</b>  

        <b>📖 Правила пользования:</b>  
        • Студенты самостоятельно выбирают литературу по рекомендациям преподавателей  
        • При отсутствии книг на абонементе - посещайте читальные залы  
        • Все услуги доступны только при наличии студенческого билета  

        <b>💻 Электронные ресурсы (доступ с 3 этажа УЛК):</b>  
        • <b>ПЭБ</b> (Полнотекстовая электронная библиотека) - бесплатный доступ без регистрации  
        • ЭБС <b>«Лань»</b>, <b>«Znanium»</b>, <b>«Book.ru»</b> - регистрация с университетского компьютера  
        • В <b>ауд. 142б</b> доступны:  
          - <b>«Консультант-Плюс»</b>  
          - <b>«ТехЭксперт»</b>"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btndlib1_loc = types.KeyboardButton("Как пройти❓")
        btndlib1_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btndlib1_loc)
        markup.add(btndlib1_Back)
        photo = open('библиотека лаб корпус.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, reply_markup=markup)
        bot.send_message(message.chat.id, text,reply_markup=markup)
        bot.register_next_step_handler(message,library3_lab_loc)



# ========================================================================
# 3.1.БИБИЛОТЕКИ ТЕКСТОВЫЙ ГИД(ОБРАБОТЧИКИ)(МАРШРУТЫ❓)
# ========================================================================

def library2_loc(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🚀 Как найти Научно-техническую библиотеку МАДИ:</b>

1️⃣ <b>Начало пути:</b>
   - Заходим через <b>главный вход 1 этажа Главного корпуса МАДИ</b>
2️⃣ <b>Поднимаемся:</b>
   - Идем по <b>правой лестнице</b> на <b>2 этаж</b>
3️⃣ <b>Ориентируемся:</b>
   - После выхода с лестницы идем <b>прямо</b>
   - С <b>правой стороны</b> увидим две двери
   - Над одной из них будет табличка: <b>"Научно-техническая библиотека МАДИ"</b>"""
        btn_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_Back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(библиоГлав)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж2.0(библиоГлав)(изм).png", "rb"))
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)

        # Затем отправляем текстовое сообщение с разметкой
        bot.send_message(message.chat.id, text, reply_markup=markup)

#--------------------------------------------------------------------------

def library3_lab_loc(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>📚 Пошаговый маршрут до библиотеки МАДИ</b>

1️⃣ <b>Главный корпус:</b>
    ‍🚪 Войдите в <b>главный корпус МАДИ</b>
   ↙ Пройдите к <b>левой лестнице</b>
   🌳 Выйдите во <b>внутренний двор</b>

2️⃣ <b>Переход в лабораторный корпус:</b>
   🚶‍♂️ Идите <b>прямо</b> по двору
   🛑 На пешеходном переходе <b>сверните</b> налево

3️⃣ <b>Лабораторный корпус:</b>
   🚪 Заходим через <b>главный вход 1 этажа</b> лабораторного корпуса
   ➡ Идем <b>налево</b> и <b>прямо</b>
   🪜 С правой стороны увидим <b>вход на лестничную площадку</b>

4️⃣ <b>Путь на 3 этаж:</b>
   🔼 Поднимаемся на <b>3 этаж</b>
    ⬅️Поворачиваем <b>налево</b>
   🚶‍♂️ Идем <b>прямо</b>

5️⃣ <b>Финиш:</b>
   🏛 Прямо перед вами - дверь с надписью <b>"БИБЛИОТЕКА"</b>

<i>💡 Если заблудитесь, спросите дорогу у охраны или студентов старших курсов.</i>"""
        btn_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_Back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(библиоЛаб)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж3.0.(библио)(изм).png", "rb"))
        ]
        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)

        # Затем отправляем текстовое сообщение с разметкой
        bot.send_message(message.chat.id, text, reply_markup=markup)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
# КОНЕЦ РАЗДЕЛА БИБЛИОТЕКИ


# ========================================================================
# АКТОВЫЙ ЗАЛ ТЕКСТОВЫЙ ГИД(ОБРАБОТЧИКИ)(МАРШРУТЫ❓)
# ========================================================================
def Act_loc(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🎭 Как найти Актовый зал МАДИ:</b>

1️⃣ <b>Начало маршрута:</b>
   🏛 Проходим на <b>1 этаж Главного корпуса МАДИ</b>

2️⃣ <b>Подъем:</b>
   ↕️ Идем по <b>лестнице</b> (можно выбрать правую или левую сторону)
   🔼 Поднимаемся на <b>3 этаж</b>

3️⃣ <b>Финиш:</b>
   🚶‍♂️ Идем <b>прямо</b>
   ➡️ <b>Справа</b> увидите дверь с надписью:
   🎭 <b>"АКТОВЫЙ ЗАЛ"</b>"""
        btn_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_Back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(актовый)(изм размер).png", "rb")),
            InputMediaPhoto(open("routes/этаж3.0(актовый)(изм размер).png", "rb"))
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)
        # Затем отправляем текстовое сообщение с разметкой
        bot.send_message(message.chat.id, text, reply_markup=markup)


# ========================================================================
# ЦАДИ-Л ТЕКСТОВЫЙ ГИД(ОБРАБОТЧИКИ)(МАРШРУТЫ❓)
# ========================================================================
def tsadi_L_Loc(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>📍 Как найти зал ЦАДИ-Л в МАДИ:</b>

1️⃣ <b>Начало маршрута:</b>
   🏛 Войдите в <b>главный корпус МАДИ</b>
   ↙ Пройдите к <b>левой лестнице</b>
   🌳 Выйдите во <b>внутренний двор</b>

2️⃣ <b>Переход между корпусами:</b>
   🚶‍♂️ Идите <b>прямо</b> по двору
   ↖ На пешеходном переходе <b>сверните налево</b>
   🏢 Пройдите до <b>Нового корпуса</b>

3️⃣ <b>Новый корпус:</b>
   🚪 Заходим в <b>левую дверь</b>
   🔼 Поднимаемся по лестнице <b>на 2 этаж</b>
   🏫 Находим дверь с надписью <b>"АУДИТОРИЯ ЦАДИ-Л"</b>

4️⃣ <b>Финальный участок:</b>
   ➡️ Заходим и идем <b>направо</b>
   🚶‍♂️ Затем <b>прямо</b> по коридору
   ➡️ Сворачиваем <b>налево</b>

5️⃣ <b>Пункт назначения:</b>
   🏗 Вы в <b>зале ЦАДИ-Л</b>!
"""
        media = [
            InputMediaPhoto(open("routes/этаж1.0(цадил)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж2.0(цадил)(изм).png", "rb"))
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)

        btn_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_Back)
        bot.send_message(message.chat.id, text, reply_markup=markup)


# НАЧАЛО РАЗДЕЛА СТОЛОВЫЕ
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
# СТОЛОВЫЕ МАДИ ВИДЕО ГИД


# =======================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ВИДЕО-ГИДОМ
# =======================================================================
def objects_video(message):
    """Обработчик объектов для видео-гида"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == '🍽️ Питание':
        text = """<b>🎥 ВИДЕО-ГИД ДО СТОЛОВОЙ ИЛИ ДО БУФЕТА</b>"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btndining1 = types.KeyboardButton("🏛️ Главный корпус")
        btndining2 = types.KeyboardButton("🔬 Лабораторный корпус")
        btndining_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btndining1, btndining2)
        markup.add(btndining_Back)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, dining_video_rooms)
    if message.text == '📖 Библиотека':
        text = """<b>🎥 ВИДЕО-ГИД ДО БИБЛИОТЕКИ</b>"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btndlibrary1 = types.KeyboardButton("🏛️ Главный корпус")
        btndlibrary2 = types.KeyboardButton("🔬 Лабораторный корпус")
        btndlibrary_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btndlibrary1, btndlibrary2)
        markup.add(btndlibrary_Back)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, library_video)
    if message.text == '👔 Гардероб':
        text1 = """
            🎬 <b>ВИДЕО-ГИД ПО ГАРДЕРОБАМ МАДИ</b> 🧥

            Выберите корпус для просмотра видео-экскурсии:

            🏛️ <b>Главный корпус</b> - 2 гардероба
            • 1 этаж ▶️ - основной
            • Подвал ▶️ - дополнительный

            🔬 <b>Лабораторный корпус</b> - мгновенный показ
            """
        text2 = """Выберите корпус:"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_main = types.KeyboardButton("🏛️ Главный корпус")
        btn_lab = types.KeyboardButton("🔬 Лабораторный корпус")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_main, btn_lab)
        markup.add(btn_back)
        bot.send_message(message.chat.id, text1, reply_markup=markup)
        bot.send_message(message.chat.id, text2, reply_markup=markup)
        bot.register_next_step_handler(message, clothes_corpus_video)

    if message.text == '🎖️ ВУЦ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_loc = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc)
        markup.add(btn_back)

        text = """
                    <b>🎥 ВИДЕО-ГИД ДО ВОЕННОГО УЧЕБНОГО ЦЕНТРА</b>
                    <b>Военный учебный центр</b> является структурным подразделением <b>Московского автомобильно-дорожного государственного технического университета (МАДИ)</b> с момента его основания.

            <b>Требования для участия в конкурсном отборе:</b>
            - Иметь гражданство РФ
            - Обучаться по очной форме обучения
            - Состоять на воинском учёте в Военном комиссариате
            - Иметь уровень физической подготовки, соответствующий Нормативам по физической подготовке
            - Основная специальность должна быть включена в Перечень направлений
            - Возраст не старше 27 лет
            - Не иметь задолженностей по учёбе
            - Годность по состоянию здоровья

            Ссылка для более подробного изучения о <b>ВУЦ МАДИ</b>: https://madi.ru/6421-voennyy-uchebnyy-centr-vuc-informaciya.html
                    <u>Нажмите "Как пройти❓", чтобы посмотреть видео-экскурсию до ВУЦ.</u>
                    """
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, process_vuc_video)

    if message.text == '🎭 Актовый зал':
        text = """<b>🎥 ВИДЕО-ГИД: Актовый зал МАДИ</b>

📍 <b>Местоположение:</b>
🏛 Главный корпус МАДИ
📌 Ленинградский пр-т, 64, <b>ауд. 344 (3 этаж)</b>

📌 <b>Назначение:</b>
✔ Организационные собрания (встречи с первокурсниками, инструктажи)
✔ Дни открытых дверей, конференции
✔ Творческие мероприятия
✔ Торжественные церемонии

🛠 <b>Оснащение:</b>
• Современная мультимедийная система
• Пространство для массовых мероприятий
• Сцена для выступлений

🏛 <b>Историческая справка:</b>
Зал сохранил архитектурные особенности 1950-х годов, сочетая их с современным оснащением.

🔗 <b>Подробнее:</b> <a href="https://madi.ru">madi.ru</a>

🎥 <em>Хотите увидеть маршрут? Нажмите "Как пройти❓" из меню ⬇️</em>
"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btndclAct_loc = types.KeyboardButton("Как пройти❓")
        btndclAct_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btndclAct_loc)
        markup.add(btndclAct_Back)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message,act_video)
    if message.text == '🎓 ЦадиЛ':
        text = """<b>🎥 ВИДЕО-ГИД: Зал ЦАДИ-Л в МАДИ</b>

📍 <b>Расположение:</b>
🏢 Новый корпус университета
🔧 Часть <b>Центра автомобильно-дорожного инжиниринга (ЦАДИ)</b>

<b>🎯 Основные направления:</b>

🔹 <b>Учебный процесс:</b>
• Семинары и практические занятия
• Лабораторные работы
• Испытания мостовых конструкций

🔹 <b>Научная работа:</b>
• Импортозамещающие технологии
• Реверс-инжиниринг
• Разработка мобильных дорожных лабораторий

🔹 <b>События:</b>
• Киберспортивные турниры
• Научные форумы
• Студенческие мероприятия

<b>💎 Особенности:</b>
• Универсальное пространство для разных задач
• Новейшее инженерное оборудование
• Современная техническая инфраструктура

🎥 <em>Хотите увидеть маршрут? Нажмите "Как пройти❓" из меню ⬇️</em>"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnL_loc = types.KeyboardButton("Как пройти❓")
        btnL_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btnL_loc)
        markup.add(btnL_Back)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message,tsadi_video)
    if message.text == '📜 Музей МАДИ':
        text = """<b>🎥 ВИДЕО-ГИД ДО МУЗЕЯ</b>

                ℹ️ <b>ИНФОРМАЦИЯ О МУЗЕЕ МАДИ</b>

                Университет - учреждение, в котором <u>всё подчинено учебному процессу</u>.
                Музейные документы и стенды представляют самую разностороннюю информацию
                о создании и развитии каждого <b>факультета</b> и каждой <b>кафедры</b>. Юные студенты
                с интересом знакомятся с экспозицией музея, а с полотен высоко висящих фотографий
                смотрят глаза тех, чьи силы и талант навсегда стали частью родного <b>МАДИ</b>.

                Музей призван напоминать о том, что <b>инженерное дело</b> является интересным не только само по себе,
                что оно - часть общей культуры, поэтому здесь проходят встречи как с корифеями <i>науки, техники,
                искусства</i> так и с творческой молодежью и артистами. Это общение воспитывает художественный вкус,
                а главное мотивирует стремление к профессионализму, важному в любом деле.

                Здесь вы найдете:

                • Экспозицию об основании университета в <b>1930 году</b>
                • Исторические документы и фотографии
                • Модели первых <b>автомобилей</b> и дорожной техники
                • Интерактивные стенды о развитии транспорта
                • Выставку достижений <b>студентов и преподавателей</b>

                Чтобы ознакомиться более подробнее с <b>музеем МАДИ</b> перейдите по ссылке: https://madi.ru/2380-muzey-o-nas.html
                <u>Чтобы узнать как <i>добраться</i> до музея нажмите кнопку: Как пройти❓</u>
                """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_play = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_play)
        markup.add(btn_back)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, process_museum_video)

    if message.text == '🏃 Физическое воспитание':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_gym = types.KeyboardButton("🏋️ Спортзал")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_gym)
        markup.add(btn_back)

        text = """<b>🎥 ВИДЕО-ГИД: ФИЗИЧЕСКОЕ ВОСПИТАНИЕ</b>

            Доступен только видео-гид до спортзала.
            Выберите объект:
            """
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, process_sport_selection_video)

    if message.text == '👥 Профком':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🎥 ВИДЕО-ГИД ДО ПРОФКОМА</b>
            Первичная Профсоюзная организация работников Московского автомобильно-дорожного государственного 
            технического университета (МАДИ) Московской городской организации Общероссийского профсоюза образования 
            (ППО РАБОТНИКОВ МАДИ МГО ОБЩЕРОССИЙСКОГО ПРОФСОЮЗА ОБРАЗОВАНИЯ) была образована из объединенной профсоюзной 
            организации МАДИ в 1989 году. Ее руководителем был избран Гурьянов Вячеслав Михайлович, который руководил ею до 2024 года.

            Это выборный орган студенческого самоуправления, который:
            • Защищает права студентов
            • Организует культурные мероприятия
            • Помогает с решением бытовых вопросов
            • Предоставляет материальную поддержку
            • Организует льготные путевки в санатории

            🌐 Официальная группа: https://vk.com/profkom_madi
            📞 Контакты: +7 (499) 155-01-91
            <u>Чтобы узнать как <i>добраться</i> до Профкома нажмите кнопку: Как пройти❓</u>"""

        btn_play = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_play)
        markup.add(btn_back)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, process_profcom_video)

    if message.text == '🚪 400 кабинет':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_play = types.KeyboardButton("Как пройти❓")  # Было "Смотреть видео▶️"
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_play)
        markup.add(btn_back)
        bot.send_message(message.chat.id, "🎥 ВИДЕО-ГИД ДО 400 КАБИНЕТА", reply_markup=markup)
        bot.register_next_step_handler(message, process_400_video)


# ========================================================================
# 3.1.СТОЛОВЫЕ ВИДЕО ГИД
# ========================================================================
def dining_video_rooms(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "🏛️ Главный корпус":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn_text_buffet_1vid = types.KeyboardButton("🍩 1 этаж - буфет")
        btn_text_gl4_tablevid = types.KeyboardButton("🍽️ 4 этаж - столовая")
        btn_text_gl2_tablevid = types.KeyboardButton("🍴 2 этаж - столовая")
        btndining_gl_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_text_buffet_1vid)
        markup.add(btn_text_gl2_tablevid, btn_text_gl4_tablevid)
        markup.add(btndining_gl_Back)
        text_gl = """<b>🍽️ Питание в МАДИ</b>

<b>🏛️ Главный корпус:</b>
┣ <b>2-й этаж</b> — столовая на 120 мест 🪑 
┣ <b>4-й этаж</b> — столовая на 130 мест 🍽️ 

<b>☕️ Буфеты:</b>
┣ <b>1-й этаж</b> — буфет на 24 места 🍩 

<b>📍 Адрес:</b> Ленинградский проспект, д. 64
<b>🌐 Подробнее:</b> <a href="https://madi.ru">madi.ru</a>"""
        bot.send_message(message.chat.id, text_gl, reply_markup=markup)
        bot.register_next_step_handler(message, diningGl_video)
    if message.text == "🔬 Лабораторный корпус":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        text_lab = """<b>🍽️ Столовые МАДИ</b>

    🏛️ <b>Лабораторный корпус:</b>
    ┗ 1-й этаж — столовая на <b>70</b> посадочных мест 🔬

    Куда отправимся❓
    """
        btn_text_buffet = types.KeyboardButton("🔬 1 этаж")
        btndining_gl_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_text_buffet)
        markup.add(btndining_gl_Back)
        bot.send_message(message.chat.id, text_lab, reply_markup=markup)
        bot.register_next_step_handler(message, diningLAB_video)


    # ========================================================================
    # 3.1.СТОЛОВЫЕ ТЕКСТОВЫЙ ГИД(ОБРАБОТЧИКИ)(ЭТАЖИ)
    # ========================================================================


def diningGl_video(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "🍩 1 этаж - буфет":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🎞️ Видео-гид: Буфет в главном корпусе МАДИ (2025 год)</b>

📍 <b>Расположение:</b> 1-й этаж главного корпуса
🪑 <b>Вместимость:</b> 24 посадочных места

<b>🍴 Ассортимент:</b>
- Сэндвичи и снеки
- Пирожные и сладости
- Соки и вода
- Горячие напитки (чай, кофе)

<i>Удобное место для быстрого перекуса между занятиями</i>

📌 <b>Адрес:</b> Ленинградский проспект, д. 64
🌐 <b>Подробнее:</b> <a href="https://madi.ru">madi.ru</a>

<em>Хотите увидеть маршрут? Нажмите "Как пройти❓" из меню ⬇️</em>"""
        btn_loc3 = types.KeyboardButton("Как пройти❓")
        btn_Back3 = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc3)
        markup.add(btn_Back3)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, buffet_1_loc_video)
    if message.text == "🍽️ 4 этаж - столовая":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🎞️ Видео-гид: Питание в университете</b>

На территории университета работают столовые, где можно приобрести полноценные <b>завтраки и обеды</b>.

<b>📍 Столовая в Главном корпусе</b>
- <b>4 этаж</b>, 130 посадочных мест
- <b>Стол заказов</b> – можно заказать еду на вынос
- <b>Телефон для заказов</b>:
  <code>8 (965) 268 99 80</code> (Вера Александровна Горелова)

<b>🎉 Дополнительные услуги</b>
Комбинат питания принимает заказы на:
- Проведение <b>торжественных мероприятий</b>
- Обслуживание <b>конференций и семинаров</b>

<b>🌐 Подробнее:</b> <a href="https://madi.ru">madi.ru</a>

<em>Хотите увидеть маршрут? Нажмите "Как пройти❓" из меню ⬇️</em>"""
        btn_loc4 = types.KeyboardButton("Как пройти❓")
        btn_Back4 = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc4)
        markup.add(btn_Back4)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, table4_loc_video)
    if message.text == "🍴 2 этаж - столовая":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🎞️ Видео-гид: Столовые университета</b>

На территории университета работают столовые, где можно приобрести полноценные <b>завтраки и обеды</b>.

<b>📍 Столовая в Главном корпусе</b>
• <b>2 этаж</b>
• <b>120 посадочных мест</b>

<b>🎉 Дополнительные услуги:</b>
Комбинат питания организует:
- Проведение <b>торжественных мероприятий</b>
- Обслуживание <b>конференций</b>
- Организацию <b>семинаров</b>

<b>🌐 Подробнее:</b> <a href="https://madi.ru">madi.ru</a>

<em>Хотите увидеть маршрут? Нажмите "Как пройти❓" из меню ⬇️</em>
    """

        btn_loc1 = types.KeyboardButton("Как пройти❓")
        btn_Back1 = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc1)
        markup.add(btn_Back1)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, table2_loc_video)

    # ^-----------------------------------------------------------------------




def diningLAB_video(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "🔬 1 этаж":
        text = """<b>🎞️ Видео-гид: Столовая в Лабораторном корпусе</b>

В Лабораторном корпусе университета работает уютная столовая, где вы можете:
- Вкусно <b>позавтракать</b>
- Плотно <b>пообедать</b>
- Взять еду <b>с собой</b>

<b>📍 Местоположение:</b>
• <b>1 этаж</b> Лабораторного корпуса
• <b>70 посадочных мест</b>
• Доступно питание на вынос

<b>📌 Особенности:</b>
- Свежие комплексные обеды
- Разнообразная выпечка

<b>🌐 Подробнее:</b> <a href="https://madi.ru">madi.ru</a>

<em>Хотите увидеть маршрут? Нажмите "Как пройти❓" из меню ⬇️</em>
    """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_loclab1 = types.KeyboardButton("Как пройти❓")
        btn_Back1 = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loclab1)
        markup.add(btn_Back1)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, table1_loc_lab_video)




# ========================================================================
# 3.1.СТОЛОВЫЕ ВИДЕО ГИД(ОБРАБОТЧИКИ)(МАРШРУТЫ❓)
# ========================================================================


def buffet_1_loc_video(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnbuff = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btnbuff)
        # Укажите правильный путь к видеофайлу
        try:
            with open('media/Буфет в главном корпусе.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎞️ 1 этаж - буфет", reply_markup=markup)

def table4_loc_video(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable4 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable4)
        try:
            with open('media/столовая 4 этаж главный корпус.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎞️ 4 этаж - столовая", reply_markup=markup)

def table2_loc_video(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/столовая 2 этаж главный корпус.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎞️ 2 этаж - столовая", reply_markup=markup)

def table1_loc_lab_video(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/Столовая ЛАБ корпус.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎞️ 1 этаж - столовая", reply_markup=markup)
## =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
# КОНЕЦ РАЗДЕЛА СТОЛОВЫЕ


# НАЧАЛО РАЗДЕЛА БИБЛИОТЕКИ
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
# БИБЛИОТЕКИ МАДИ ТЕКСТОВЫЙ ГИД

# ========================================================================
# 3.1.БИБЛИОТЕКИ ТЕКСТОВЫЙ ГИД
# ========================================================================
def library_video(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "🏛️ Главный корпус":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        text = """<b>🎥 ВИДЕО-ГИД: Научно-техническая библиотека МАДИ</b> 

Основана в <b>1930 году</b> и является одной из <b>крупнейших университетских библиотек России</b> с уникальным фондом литературы по <b>автомобильно-дорожной тематике</b>.  

<b>🔍 Основные задачи библиотеки:</b>  
✔ Содействие учебному и научному процессам МАДИ  
✔ Формирование и хранение отечественных и зарубежных научных материалов  
✔ Библиотечное и справочно-библиографическое обслуживание  
✔ Внедрение современных автоматизированных и электронных технологий  

<b>💻 Электронный каталог</b>  
Базируется на системе <b>АБИС «Руслан»</b> и содержит <b>свыше 107 тысяч записей</b> (книги, статьи из журналов и сборников).  

🌐 <b>Доступен онлайн:</b> <a href="https://lib.madi.ru/">перейти в каталог</a>
<em>Хотите увидеть маршрут? Нажмите "Как пройти❓" из меню ⬇️</em>"""

        btndlib1 = types.KeyboardButton("Как пройти❓")
        btndlib_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btndlib1)
        markup.add(btndlib_Back)
        bot.send_message(message.chat.id,text, reply_markup=markup)
        bot.register_next_step_handler(message,library_GL)
    if message.text == "🔬 Лабораторный корпус":
        text = """  
    <b>🎥 ВИДЕО-ГИД: Научно-техническая библиотека МАДИ</b>
📍 <u>Все перечисленные ниже услуги доступны в Научно-технической библиотеке (НТБ) МАДИ, расположенной на <b>3 этаже учебно-лабораторного корпуса (УЛК)</b></u>  

<b>📌 Запись в НТБ и выдача учебников для 1 КУРСА:</b>  
<b>С 9 сентября 2024 г.</b>  
⏰ <b>Часы работы:</b>  
<pre>
Понедельник    10:00 - 15:00  
Вторник        10:00 - 15:00  
Среда          10:00 - 15:00  
Четверг        10:00 - 15:00  
Пятница        10:00 - 15:00  
</pre>  
❗ При себе необходимо иметь <b>студенческий билет</b>.  

<b>ℹ Дополнительная информация:</b>  
🌐 Сайт НТБ: <a href="https://lib.madi.ru">lib.madi.ru</a>  
📍 <b>Основные помещения библиотеки:</b>  
   • Абонемент: <b>ауд. 302л</b> (3 этаж УЛК)  
   • Научный читальный зал: <b>ауд. 142б</b>  
   • Отдел справочно-библиографической работы: <b>ауд. 249</b>  

<b>📖 Правила пользования:</b>  
• Студенты самостоятельно выбирают литературу по рекомендациям преподавателей  
• При отсутствии книг на абонементе - посещайте читальные залы  
• Все услуги доступны только при наличии студенческого билета  

<b>💻 Электронные ресурсы (доступ с 3 этажа УЛК):</b>  
• <b>ПЭБ</b> (Полнотекстовая электронная библиотека) - бесплатный доступ без регистрации  
• ЭБС <b>«Лань»</b>, <b>«Znanium»</b>, <b>«Book.ru»</b> - регистрация с университетского компьютера  
• В <b>ауд. 142б</b> доступны:  
  - <b>«Консультант-Плюс»</b>  
  - <b>«ТехЭксперт»</b>  

<u>🚪 Все помещения библиотеки находятся на 3 этаже учебно-лабораторного корпуса МАДИ.</u>  
<em>Хотите увидеть маршрут? Нажмите "Как пройти❓" из меню ⬇️</em>"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btndlib1 = types.KeyboardButton("Как пройти❓")
        btndlib1_Back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btndlib1)
        markup.add(btndlib1_Back)
        bot.send_message(message.chat.id,text, reply_markup=markup)
        bot.register_next_step_handler(message,library_LAB)


# ========================================================================
# 3.1.БИБЛИОТЕКИ ВИДЕО ГИД(ОБРАБОТЧИКИ)(МАРШРУТЫ❓)
# ========================================================================

def library_GL(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/библиотека главный корпус.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎥 Научно-техническая библиотека МАДИ", reply_markup=markup)

def library_LAB(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/библиотека лабораторный корпус.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎞️ Научно-техническая библиотека МАДИ", reply_markup=markup)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
# КОНЕЦ РАЗДЕЛА БИБЛИОТЕКИ


# НАЧАЛО РАЗДЕЛА ГАРДЕРОБЫ
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
# ГАРДЕРОБЫ МАДИ ТЕКСТОВЫЙ ГИД

# ========================================================================
# 4.1.ГАРДЕРОБЫ ТЕКСТОВЫЙ ГИД
# ========================================================================
# =======================================================================
# ФУНКЦИИ ДЛЯ РАБОТЫ С ТЕКСТОВЫМ ГИДОМ (ГАРДЕРОБЫ)
# =======================================================================

def clothes_corpus_text(message):
    """Выбор корпуса (главный или лабораторный)"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "🏛️ Главный корпус":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_floor1 = types.KeyboardButton("🔼 1 этаж")
        btn_basement = types.KeyboardButton("🔽 Подвал")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_floor1, btn_basement)
        markup.add(btn_back)
        bot.send_message(message.chat.id, "Выберите расположение гардероба:", reply_markup=markup)
        bot.register_next_step_handler(message, clothes_main_text)  # Передаем в clothes_main_text
    elif message.text == "🔬 Лабораторный корпус":
        text = """
        <b>👔 Гардероб в лабораторном корпусе</b>
        """

        photo = open('гардероб лабораторный корпус.jpg', 'rb')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        btn_loc = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc)
        markup.add(btn_back)
        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)
        bot.register_next_step_handler(message, how_to_get_clothes_lab)



def clothes_main_text(message):
    """Обработчик гардеробов в главном корпусе (1 этаж или подвал)"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "🔼 1 этаж":
        text = """
        <b>👔 Гардероб на 1 этаже (главный корпус)</b>
        """

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_loc = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc)
        markup.add(btn_back)
        photo = open('гардероб 1 этаж.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)
        bot.register_next_step_handler(message, how_to_get_clothes_floor1)

    elif message.text == "🔽 Подвал":
        text = """
        <b>👔 Гардероб в подвале (главный корпус)</b>
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_loc = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc)
        markup.add(btn_back)
        photo = open('гардероб подвал.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption=text, reply_markup=markup)
        bot.register_next_step_handler(message, how_to_get_clothes_basement)



def how_to_get_clothes_floor1(message):
    """Маршрут до гардероба на 1 этаже"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        text = """
        👔 <b>ГАРДЕРОБ НА 1 ЭТАЖЕ</b> 🧥

        📍 <b>Подробный маршрут:</b>
        1️⃣ Войдите в <u>Главный корпус МАДИ</u> через центральный вход
        2️⃣ Пройдите прямо по холлу 
        3️⃣ Справа от лестницы будет надпись <b>"ГАРДЕРОБ"</b>

        ✨ <b>Что можно сделать здесь:</b>
        • Сдать верхнюю одежду (пальто, куртки) 
        • Оставить головные уборы 🧢☂️
        • Взять номерок для ваших вещей 🔢
        • Получить помощь у гардеробщика 🤵
        """

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(гардеоб)(изм).png", "rb")),
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)

        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')
        bot.register_next_step_handler(message, how_to_get_clothes_floor1)



def how_to_get_clothes_basement(message):
    """Маршрут до гардероба в подвале"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        text = """
        🔻 <b>ГАРДЕРОБ В ПОДВАЛЕ</b> 🧥

        📍 <b>Подробный маршрут:</b>
        1️⃣ От главного входа поверните <u>направо</u> к лестнице
        2️⃣ Спуститесь на 1 пролёт вниз
        3️⃣ Перед вами будет проход в гардеробную
        4️⃣ Поверните налево — увидите окошко гардероба

        ✨ <b>Что можно сделать здесь:</b>
        • Сдать верхнюю одежду (пальто, куртки) 
        • Оставить головные уборы 🧢☂️
        • Взять номерок для ваших вещей 🔢
        • Получить помощь у гардеробщика 🤵
        """
        """
                try:
                    with open('images/wardrobe_floor1_1.jpg', 'rb') as photo:
                        bot.send_photo(message.chat.id, photo, caption="Главный вход")
                    with open('images/wardrobe_floor1_2.jpg', 'rb') as photo:
                        bot.send_photo(message.chat.id, photo, caption="Указатель к гардеробу")
                except:
                    pass
                """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(гардеоб)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж0.0.(гардероб)(изм).png", "rb"))
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)

        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')
        bot.register_next_step_handler(message, how_to_get_clothes_basement)


def how_to_get_clothes_lab(message):
    """Маршрут до гардероба в лабораторном корпусе"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        text = """
        🔬 <b>ГАРДЕРОБ В ЛАБОРАТОРНОМ КОРПУСЕ</b> 🧪

        📍 <b>Подробный маршрут:</b>
        1️⃣ Войдите в <b>главный корпус МАДИ</b>
        2️⃣ Пройдите к левой лестнице
        3️⃣ Выйдите во внутренний двор
        4️⃣ Идите прямо потом на пешеходном переходе сверните направо и пройдите до лабораторного корпуса
        5️⃣ Гардероб — справа от входа

        ✨ <b>Что можно сделать здесь:</b>
        • Сдать верхнюю одежду (пальто, куртки) 
        • Оставить головные уборы 🧢☂️
        • Взять номерок для ваших вещей 🔢
        • Получить помощь у гардеробщика 🤵
        """
        """
                try:
                    with open('images/wardrobe_floor1_1.jpg', 'rb') as photo:
                        bot.send_photo(message.chat.id, photo, caption="Главный вход")
                    with open('images/wardrobe_floor1_2.jpg', 'rb') as photo:
                        bot.send_photo(message.chat.id, photo, caption="Указатель к гардеробу")
                except:
                    pass
                """

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(гардеробЛаб)(изм).png", "rb"))
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)

        # Затем отправляем текстовое сообщение с разметкой
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')
        bot.register_next_step_handler(message, how_to_get_clothes_lab)


# ========================================================================
# 4.2.ГАРДЕРОБЫ ВИДЕО ГИД (ОБРАБОТЧИКИ)(МАРШРУТЫ❓)
# ========================================================================
def clothes_corpus_video(message):
    """Выбор корпуса (находится в разделе callback-обработчиков)"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    welcome_msg = """
        🎬 <b>ВИДЕО-ГИД ПО ГАРДЕРОБАМ МАДИ</b> 🧥

        Выберите корпус для просмотра видео-экскурсии:

        🏛️ <b>Главный корпус</b> - 2 гардероба
        • 1 этаж ▶️ - основной
        • Подвал ▶️ - дополнительный

        🔬 <b>Лабораторный корпус</b> - мгновенный показ
        """

    if message.text == "🏛️ Главный корпус":
        bot.send_message(
            message.chat.id,
            welcome_msg,
            parse_mode='HTML'
        )

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("1 этаж ▶️")
        btn2 = types.KeyboardButton("Подвал ▶️")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn1, btn2)
        markup.add(btn_back)

        bot.send_message(
            message.chat.id,
            "🎬 Выберите этаж для просмотра видео-гида:",
            reply_markup=markup
        )
        bot.register_next_step_handler(message, clothes_main_video)

    elif message.text == "🔬 Лабораторный корпус":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btnlab = types.KeyboardButton("Как пройти❓")
        btnback = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btnlab)
        markup.add(btnback)
        bot.send_message(
            message.chat.id,
            welcome_msg,
            parse_mode='HTML',reply_markup=markup)
        bot.register_next_step_handler(message,send_lab_video)




def clothes_main_video(message):
    """Обработчик для гардероба в главном корпусе (видео)"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "1 этаж ▶️":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_loc = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc)
        markup.add(btn_back)
        bot.send_message(message.chat.id, "Нажмите 'Как пройти❓' для просмотра видео-гида🎥", reply_markup=markup)
        bot.register_next_step_handler(message, handle_floor1_video)

    elif message.text == "Подвал ▶️":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_loc = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc)
        markup.add(btn_back)
        bot.send_message(message.chat.id, "Нажмите 'Как пройти❓' для просмотра видео-гида🎥", reply_markup=markup)
        bot.register_next_step_handler(message, handle_basement_video)


def handle_floor1_video(message):
    """Обработчик 1 этажа"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    elif message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/Гардероб в главном корпусе.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "1 этаж ▶️ - основной", reply_markup=markup)

def handle_basement_video(message):
    """Обработчик видео для подвала (находится после функций text-гида)"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    elif message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/гардероб в подвале.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "Подвал ▶️ - дополнительный", reply_markup=markup)


#🔬 Видео-гид: Гардероб лабораторного корпуса
def send_lab_video(message):
    """Непосредственная отправка видео (добавить перед запуском бота)"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/гардероб 1 этаж лаб корпус.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎞️ Гардероб лабораторного корпуса", reply_markup=markup)

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
    # КОНЕЦ РАЗДЕЛА ГАРДЕРОБЫ

# =======================================================================
# 5.1 - 5.2. ВУЦ (ТЕКСТОВЫЙ И ВИДЕО ГИД)
# =======================================================================

def process_vuc_text(message):
    """Обработка выбора в текстовом гиде ВУЦ"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        text = """
        🎖️ <b>КАК ДОЙТИ ДО ВОЕННОГО УЧЕБНОГО ЦЕНТРА</b>

        📍 <b>Подробный маршрут:</b>
        1️⃣ Войдите в главный корпус МАДИ через центральный вход
        2️⃣ Пройдите к левой лестничной площадке
        3️⃣ Выйдите через дверь во внутренний двор
        4️⃣ Идите по диагонали влево к большому кирпичному зданию (Новый корпус)
        5️⃣ Войдите в Новый корпус
        6️⃣ После входа будет лестничная площадка
        7️⃣ Поднимитесь на 6 этаж
        8️⃣ Там вы найдёте Военный учебный центр(Весь этаж – это военный учебный центр)
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(вуц)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж6.0(вуц)(изм).png", "rb"))
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)
        bot.send_message(message.chat.id, text, reply_markup=markup)


def process_vuc_video(message):
    """Обработка видео-гида ВУЦ"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/ВУЦ.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎞️ ВУЦ нового корпуса", reply_markup=markup)

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
    # КОНЕЦ РАЗДЕЛА ВУЦ


# =======================================================================
# 6.1 - 6.2. 400 кабинет (ТЕКСТОВЫЙ И ВИДЕО ГИД)
# =======================================================================

def process_400_text(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        text = """
        🚪 <b>ПОДРОБНЫЙ МАРШРУТ ДО 400 КАБИНЕТА</b>

        📍 <b>Пошаговая инструкция:</b>
        1️⃣ Войдите в <b>главный корпус МАДИ</b> через центральный вход
        2️⃣ Поверните направо к лестничной площадке
        3️⃣ Поднимитесь на <b>3 этаж</b>
        4️⃣ От лестницы поверните два раза налево
        5️⃣ Пройдите по коридору до поворота → поверните направо
        6️⃣ Идите прямо до конца коридора → поверните налево и пройдите дальше по коридору
        7️⃣ Слева после двери перед вами будет лестничная площадка → поднимитесь на 1 этаж вверх
        8️⃣ Откройте дверь на 4 этаже → слева вы увидите лекционную аудиторию
        """
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(физ)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж2.0(400)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж3.0(400)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж4.0(400)(изм).png", "rb"))
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)
        bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='HTML')
        bot.register_next_step_handler(message, process_400_text)


# Видео-гид до 400 кабинета
def process_400_video(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/400 кабинет.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎞️ 400 кабинет главного корпуса", reply_markup=markup)


    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
    # КОНЕЦ РАЗДЕЛА 400 кабинет


# =======================================================================
# 7.1 - 7.2. Профком (ТЕКСТОВЫЙ И ВИДЕО ГИД)
# =======================================================================

def process_profcom_text(message):
    """Обработка выбора в текстовом гиде Профкома"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        text = """
        👥 <b>ПОДРОБНЫЙ МАРШРУТ ДО ПРОФКОМА СТУДЕНТОВ</b>

        📍 <b>Пошаговая инструкция:</b>
        1️⃣ Войдите в <b>главный корпус МАДИ</b> через центральный вход
        2️⃣ Пройдите к <b>правой лестнице</b>
        3️⃣ Поднимитесь на <b>3 этаж</b>
        4️⃣ Сверните налево от лестницы
        5️⃣ Пройдите в сторону окон и зеркал 
        6️⃣ Слева от вас будет белая дверь с надписью <b>"ПРОФКОМ СТУДЕНТОВ МАДИ"</b>

        """

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(проф)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж3.0(проф)(изм).png", "rb"))
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)
        bot.send_message(message.chat.id, text, parse_mode='HTML',reply_markup=markup)


def process_profcom_video(message):
    """Обработка видео-гида Профкома"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/Профком.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎞️ Профком главного корпуса", reply_markup=markup)



    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
    # КОНЕЦ РАЗДЕЛА ПРОФКОМ

    # =======================================================================
    # 7.1 - 7.2. Профком (ТЕКСТОВЫЙ И ВИДЕО ГИД)
    # =======================================================================


# =======================================================================
# 7.1 - 7.2. Музеи (ТЕКСТОВЫЙ И ВИДЕО ГИД)
# =======================================================================

def process_museum_text(message):
    """Обработка текстового гида для музея"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        text = """
            📜 <b>ТЕКСТОВЫЙ ГИД ДО МУЗЕЯ МАДИ</b>

            📍 <b>Подробный маршрут:</b>
            1️⃣ Войдите в главный корпус МАДИ через центральный вход
            2️⃣ Пройдите к левой лестничной площадке
            3️⃣ Поднимитесь на 5 этаж
            4️⃣ Пройдите чуть прямо и слева вы увидите музей МАДИ

            ✨ <b>Особенности:</b>
            • Музей расположен на 5 этаже главного корпуса
            • Ищите вывеску "Музей истории МАДИ"
            """

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(муз)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж5.0(муз)(изм).png", "rb"))
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)
        bot.send_message(message.chat.id, text, parse_mode='HTML',reply_markup=markup)



def process_museum_video(message):
    """Обработка видео-гида для музея"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/Музей МАДИ.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎞️ Музей главного корпуса", reply_markup=markup)



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
# КОНЕЦ РАЗДЕЛА МУЗЕЙ


# =======================================================================
# 9.1 - 9.2. ФИЗИЧЕСКАЯ КУЛЬТУРА
# =======================================================================
def process_sport_selection_text(message):
    """Обработка выбора в текстовом гиде"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "🏋️ Спортзал":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_loc = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc)
        markup.add(btn_back)
        text = """<b>🏋️ СПОРТЗАЛ </b>

        <b>Основные направления:</b>  
        Кафедра осуществляет подготовку студентов по 15+ спортивным дисциплинам, 
        включая футбол, волейбол, баскетбол, плавание, легкую атлетику и шахматы. 
        Занятия проходят в современных спортивных залах главного корпуса и на стадионе "Октябрь". 
        Специально оборудованные тренажерные залы позволяют проводить силовые тренировки, 
        а секции единоборств развивают координацию и выносливость. 
        Для студентов с ограниченными возможностями здоровья разработаны адаптивные программы.

        <b>Достижения и возможности:</b>  
        Ежегодно проводятся межфакультетские соревнования и спартакиады. 
        Лучшие спортсмены представляют МАДИ на всероссийских универсиадах. 
        Кафедра располагает 5 профессиональными тренерами, включами мастера спорта международного класса. 
        Студенты могут получить спортивный разряд и войти в сборную университета. 

        <b>Информация о спортивной базе:</b> 
        Материально - техническое обеспечение дисциплины:
        • спортивные залы,
        • зал для аэробики,
        • тренажерные комнаты,
        • стадион,
        • лаборатория скоростных автомобилей.

        Объекты спортивной инфраструктуры МАДИ задействованы в рамках организации учебного процесса и внеучебной работы 
        с обучающимися и доступны для посещения по утвержденному графику.

        E-mail: kfv@madi.ru
        Телефон: 8 (499) 155-08-93
        Аудитория: 401 (главный корпус)
        <u>Чтобы узнать как <i>добраться</i> до Спортзала нажмите кнопку: Как пройти❓</u>"""
        photo = open('спорт.jpg', 'rb')
        bot.send_photo(message.chat.id, photo,reply_markup=markup)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, process_gym_text)

    elif message.text == "🏟️ Стадион":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_loc = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_loc)
        markup.add(btn_back)
        text = """<b>🏋️ ФИЗИЧЕСКОЕ ВОСПИТАНИЕ </b>

                <b>Основные направления:</b>  
                Кафедра осуществляет подготовку студентов по 15+ спортивным дисциплинам, 
                включая футбол, волейбол, баскетбол, плавание, легкую атлетику и шахматы. 
                Занятия проходят в современных спортивных залах главного корпуса и на стадионе "Октябрь". 
                Специально оборудованные тренажерные залы позволяют проводить силовые тренировки, 
                а секции единоборств развивают координацию и выносливость. 
                Для студентов с ограниченными возможностями здоровья разработаны адаптивные программы.

                <b>Достижения и возможности:</b>  
                Ежегодно проводятся межфакультетские соревнования и спартакиады. 
                Лучшие спортсмены представляют МАДИ на всероссийских универсиадах. 
                Кафедра располагает 5 профессиональными тренерами, включами мастера спорта международного класса. 
                Студенты могут получить спортивный разряд и войти в сборную университета. 

                <b>Информация о спортивной базе:</b> 
                Материально - техническое обеспечение дисциплины:
                • спортивные залы,
                • зал для аэробики,
                • тренажерные комнаты,
                • стадион,
                • лаборатория скоростных автомобилей.

                Объекты спортивной инфраструктуры МАДИ задействованы в рамках организации учебного процесса и внеучебной работы 
                с обучающимися и доступны для посещения по утвержденному графику.

                E-mail: kfv@madi.ru
                Телефон: 8 (499) 155-08-93
                Аудитория: 401 (главный корпус)
                <u>Чтобы узнать как <i>добраться</i> до Стадиона нажмите кнопку: Как пройти❓</u>"""
        photo = open('стадион.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, reply_markup=markup)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, process_stad_text)


def process_gym_text(message):
    """Маршрут до спортзала (текстовый)"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        text = """
        <b>🏋️ МАРШРУТ ДО СПОРТЗАЛА</b>

        1️⃣ Зайдите в <b>МАДИ</b> через <u>центральный вход</u>
        2️⃣ Пройдите к <i>правой лестничной площадке</i>
        3️⃣ Поднимитесь на <b>4 этаж</b>
        4️⃣ От лестницы поверните <u>два раза влево</u>
        5️⃣ Идите по коридору <i>прямо</i>
        6️⃣ Сверните <b>направо</b>
        7️⃣ Идите до <u>конца коридора</u>
        8️⃣ Поверните <b>налево</b>
        9️⃣ Пройдите к <i>конечной двери</i> прямо напротив вас, это и есть вход в спортзал
        """

        # Ваши оригинальные пути к файлам без изменений

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_back)
        media = [
            InputMediaPhoto(open("routes/этаж1.0(физ)(изм).png", "rb")),
            InputMediaPhoto(open("routes/этаж4.0(физ)(изм).png", "rb"))
        ]

        # Отправляем группу медиа
        bot.send_media_group(message.chat.id, media=media)
        bot.send_message(message.chat.id, text, parse_mode='HTML',reply_markup=markup)



def process_stad_text(message):
    """Маршрут до cтадиона (текстовый)"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        text = """
        <b>🏟️ Стадион "Октябрь"</b>

        📍 <b>Как добраться:</b>
        1️⃣ Садитесь в автобус <b>е32</b> и поезжайте до <u>Пехотной улицы</u>
        2️⃣ Перейдите на <i>трамвайную остановку</i>
        3️⃣ Садитесь на трамвай <b>28</b> или <b>31</b> до остановки <b>«Улица Рогова»</b>
        4️⃣ Выйдите на <i>тропинку</i> и идите вдоль забора
        5️⃣ Затем <u>заворачиваем направо</u> в ворота
        6️⃣ Идем прямо до <b>стадиона</b>

        🗺️ <b>Адрес:</b> Москва, ул. 800-летия Москвы, 24с1
        """

        # paths = [
        #     InputMediaPhoto(open(r'C:\Users\LT\Desktop\универ\Практика\Practik\Практика ТГ-бот\изображения и видео для практики\физра\стадион.jpg', 'rb'), caption=text),
        #     InputMediaPhoto(open(r'C:\Users\LT\Desktop\универ\Практика\Practik\Практика ТГ-бот\изображения и видео для практики\физра\стадион мади.jpg', 'rb'))
        # ]
        # bot.send_message(message.chat.id, text, parse_mode='HTML')
        # закрываем файлы
        # paths[0].media.close()
        # paths[1].media.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_back)
        photo = open('стадион мади.jpg', 'rb')
        bot.send_photo(message.chat.id, photo, caption=text,reply_markup=markup)



def process_sport_selection_video(message):
    """Обработка выбора в видео гиде"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "🏋️ Спортзал":

        text = """<b>🎥 ВИДЕО-ГИД ДО СПОРТЗАЛА</b>

                <b>Основные направления:</b>  
                Кафедра  по физическому воспитанию осуществляет подготовку студентов по 15+ спортивным дисциплинам, 
                включая футбол, волейбол, баскетбол, плавание, легкую атлетику и шахматы. 
                Занятия проходят в современных спортивных залах главного корпуса и на стадионе "Октябрь". 
                Специально оборудованные тренажерные залы позволяют проводить силовые тренировки, 
                а секции единоборств развивают координацию и выносливость. 
                Для студентов с ограниченными возможностями здоровья разработаны адаптивные программы.

                <b>Достижения и возможности:</b>  
                Ежегодно проводятся межфакультетские соревнования и спартакиады. 
                Лучшие спортсмены представляют МАДИ на всероссийских универсиадах. 
                Кафедра располагает 5 профессиональными тренерами, включами мастера спорта международного класса. 
                Студенты могут получить спортивный разряд и войти в сборную университета. 

                <b>Информация о спортивной базе:</b> 
                Материально - техническое обеспечение дисциплины:
                • спортивные залы,
                • зал для аэробики,
                • тренажерные комнаты,
                • стадион,
                • лаборатория скоростных автомобилей.

                Объекты спортивной инфраструктуры МАДИ задействованы в рамках организации учебного процесса и внеучебной работы 
                с обучающимися и доступны для посещения по утвержденному графику.

                E-mail: kfv@madi.ru
                Телефон: 8 (499) 155-08-93
                Аудитория: 401 (главный корпус)
                <u>Чтобы узнать как <i>добраться</i> до Спортзала нажмите кнопку: Как пройти❓</u>"""
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_play = types.KeyboardButton("Как пройти❓")
        btn_back = types.KeyboardButton("🔙 Возврат в главное меню")
        markup.add(btn_play)
        markup.add(btn_back)
        bot.send_message(message.chat.id, text, reply_markup=markup)
        bot.register_next_step_handler(message, process_gym_video)



def process_gym_video(message):
    """Отправка видео до спортзала"""
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return
    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/спортивный зал.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎞️ Спортзал главного корпуса", reply_markup=markup)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
# КОНЕЦ РАЗДЕЛА ФИЗИЧЕСКАЯ КУЛЬТУРА


# =======================================================================
# ЦАДИл ВИДЕО-ГИД
# =======================================================================
def tsadi_video(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return

    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/ЦадиЛ.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎞️ ЦАДИл нового корпуса", reply_markup=markup)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=-=-=-=
# КОНЕЦ РАЗДЕЛА ЦАДИл




# =======================================================================
# АКТОВЫЙ ЗАЛ ВИДЕО-ГИД
# =======================================================================
def act_video(message):
    if message.text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return

    if message.text == "Как пройти❓":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btntable2 = types.KeyboardButton('🔙 Возврат в главное меню')
        markup.add(btntable2)
        try:
            with open('media/актовый зал.mp4', 'rb') as video:
                bot.send_video(message.chat.id, video)
        except FileNotFoundError:
            bot.send_message(message.chat.id, "Видео не найдено, попробуйте позже")
        except Exception as e:
            bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")
        bot.send_message(message.chat.id, "🎞️ Актовый зал главного корпуса", reply_markup=markup)













# ========================================================================
# ТРАДИЦИИ(Разработчик: Полиенко Даниил)
# ========================================================================
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
        text = (
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
            bot.send_photo(message.chat.id, photo, caption=text)

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



# ========================================================================
# ПОМОЩЬ(Разработчик: Полиенко Даниил)
# ========================================================================
def objects_corpuses(message):
    text = message.text

    # Назад
    if text == '🔙 Возврат в главное меню':
        handle_back_button(message)
        return

    # Корпуса
    if text == '🏛️ Главный корпус':
        caption = (
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


# ========================================================================
# РАСПИСАНИЕ (Разработчики: Кирилл Тихов, Владимир Панфилов)
# ========================================================================

# Для корректной работы требуются следующие условия:
# Google Chrome версии 138 и выше. Посмотреть версию и обновить ее можно тут: chrome://settings/help
# Chromedriver версии как Chrome. После скачивания требуется распаковать и указать
#   путь к chromedriver.exe в self.service. Скачать можно тут: https://googlechromelabs.github.io/chrome-for-testing/
# Также установить библиотеки: selenium и bs4

user_data = {}


user_data = {}


class MadiScheduleParser:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        self.service = Service(executable_path='/usr/bin/chromedriver')
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
    btn_back = types.KeyboardButton('🔙 Возврат в главное меню')  # Новая кнопка
    markup.add(btn_group, btn_schedule, btn_back)
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
    btn_back = types.InlineKeyboardButton('🔙 Возврат в главное меню', callback_data='back_to_main')
    markup.add(btn_group, btn_schedule, btn_back)

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
        types.InlineKeyboardButton('📅 Получить расписание', callback_data='get_schedule'),
        types.InlineKeyboardButton('🔙 Назад', callback_data='back_to_main')
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

if __name__ == '__main__':
    print('Бот запущен и готов к работе! 🚀')
    bot.polling(none_stop=True)