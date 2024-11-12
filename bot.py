import telebot
from telebot import types  # для указание типов
import config
import random
import json

bot = telebot.TeleBot(config.token)  # токен лежит в файле config.py


@bot.message_handler(commands=['start'])

def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Информация")
    btn2 = types.KeyboardButton("❓ Задать вопрос")
    btn3 = types.InlineKeyboardButton("Мои проекты")
    btn4 = types.KeyboardButton("Связаться со мной")
    btn5 = types.KeyboardButton("Пообщаться с ИИ")
    btn6 = types.KeyboardButton("Поддержать")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id,
                     text="Привет, {0.first_name}! Я презентационный бот, \nобладаю некоторым функционалом:"
                          "\n- у меня есть панель управления"
                          "\n- я могу отвечать на некоторые вопросы".format(
                         message.from_user), reply_markup=markup)

def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Информация")
    button2 = types.KeyboardButton("❓ Задать вопрос")
    button3 = types.InlineKeyboardButton("Мои проекты")
    button4 = types.KeyboardButton("Связаться со мной")
    button5 = types.KeyboardButton("Пообщаться с ИИ")
    button6 = types.KeyboardButton("Поддержать")
    markup.add(button1, button2, button3, button4, button5, button6)
    bot.send_message(message.chat.id, text="Вы вернулись в главное меню", reply_markup=markup)

def ai_bot():
    return bot.send_message(message.chat.id, text="https://t.me/my_magnus_ai_bot")

def message_answer_user(message, link_txt_file = 'message_get.txt'):
    """
    Функция с рандомными ответами пользователю - если ответа на вопрос не предусмотрено
    :param message: параметр по умолчанию
    :param link_txt_file: ссылка на текстовый файл с ответами на вопросы которые не распознаны
    """
    with open(link_txt_file) as file:
        text_lst = file.readlines()
        res = random.choice(text_lst)
        bot.send_message(message.chat.id, text=res)


def links_browser(message, info_preview:str = None, url:str = None):
    """
    Функция для сссылок на сайты
    :param message: значение по умолчанию, передается для контекста чата
    :param info_preview: текст с пояснением, куда будет перенаправлен польззователь
    :param url: ссылка на сайт
    """
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(info_preview, url=url)
    markup.add(button1)
    bot.send_message(message.chat.id,
                     "{0.first_name}! Нажми на кнопку и перейди на сайт)".format(message.from_user),
                     reply_markup=markup)
    types.InlineKeyboardButton(info_preview, url=url)

def contacts(type_cjntact=None):
    """
    пердоставляет контактыне данные из json файла
    :param type_cjntact: 'phone' or 'telegram'
    :return: link or number phone
    """
    if type_cjntact:
        with open("data.json", 'r') as file_js:
            return json.load(file_js)[type_cjntact]


@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == "Информация"):
        bot.send_message(message.chat.id, text="Привеет.. Меня зовут Сергей и этот бот создан в качестве презентации")

    elif (message.text == "Мои проекты"):
        links_browser(message, "Мои проекты github", contacts('github'))

    elif (message.text == "Связаться со мной"):
        bot.send_message(message.chat.id, text="Можете позвонить:")
        bot.send_message(message.chat.id, text=contacts('phone'))
        bot.send_message(message.chat.id, text="или написать в telegram:")
        bot.send_message(message.chat.id, text=contacts('telegram'))

    elif (message.text == "Пообщаться с ИИ"):
        bot.send_message(message.chat.id, text="Вашему вниманию - мой коллега, бот обладающий скромным интеллектом")
        bot.send_message(message.chat.id, text=contacts('bot_ai'))

    elif (message.text == "Поддержать"):
        links_browser(message, "Сайт boosty", contacts('boosty'))

    elif (message.text == "❓ Задать вопрос"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Как меня зовут?")
        btn2 = types.KeyboardButton("Что я могу?")
        back = types.KeyboardButton("Вернуться в главное меню")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Задай мне вопрос", reply_markup=markup)

    elif (message.text == "Как меня зовут?"):
        bot.send_message(message.chat.id, "Я презентационный бот-ассистент..у меня нет имени...")

    elif message.text == "Что я могу?":
        bot.send_message(message.chat.id, text="- Предоставить некоторую информацию о моем создателе")
        bot.send_message(message.chat.id, text="- Поделиться ссылкой бота с ИИ")
        bot.send_message(message.chat.id, text="- Отвечать на некоторые вопросы")

    elif message.text:
        word = message.text.lower()
        for i in ',.!?:;':
            word = word.replace(i,'')
        word = word.split()
        result = []
        list_word = ['контакт', 'телефон', 'звон', 'связаться', 'связь']
        for i in list_word:
            for j in word:
                result.append(i in j)
        result = any(result)
        if result:
            bot.send_message(message.chat.id, text="Можете позвонить:")
            bot.send_message(message.chat.id, text=contacts('phone'))
            bot.send_message(message.chat.id, text="или написать в telegram:")
            bot.send_message(message.chat.id, text=contacts('telegram'))

        elif (message.text == "Вернуться в главное меню"):
            menu(message)

        else:
            message_answer_user(message)

    elif (message.text == "Вернуться в главное меню"):
        menu(message)

    else:
        message_answer_user(message)


bot.polling(none_stop=True)
