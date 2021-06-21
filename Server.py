# TODO:

# 1. (Done) повторы вопросов, их не должно быть

# 2. (Done, но чуть-чуть) сделать результаты одним большим сообщением

# 3. (Done) кнопка стоп должна выдавать статистику только по отвеченным за
# прохождение вопросам, по всем это статистика

# 4. (Done) если кнопку старт нажали повторно, при этом не завершив
# текущее прохождение, нужно вывести результаты за текущее прохождение и
# только потом начинать новое

# 5. (Done) ещё забыл проверить, завершает ли кнопка статистика
# прохождение. по идее, лучше, если да, т.е. она полностью идентична стоп,
# но выдаёт статистику по всем вопросам, а не только отвеченным


import random
import threading
import time

import pymysql
import pymysql.cursors
import telebot
from telebot import types, util

from MySQLrequests import *
from User import *

''' Инициализация '''

TOKEN = r"1801737865:AAGQroqS0QitNBRVmqP58TQLWtjrl57CP38"
bot = telebot.TeleBot(TOKEN, parse_mode=None)
dataBase_bot = pymysql.connect(
    host="remotemysql.com",
    user="5SbqamHdMU",
    password="RqcFw1HOoz",
    database="5SbqamHdMU",
)
cursor = dataBase_bot.cursor()

# Инициализировать словарь активных пользователей
UsersDict = {}  # { user_id : ### }

# Сделать кнопки управление для бота
answerMarkup = types.ReplyKeyboardMarkup()
answerMarkup.add('1', '2', 'Статистика', '/stop', '/start')

# Создать уборщика кнопок
MarkupHide = types.ReplyKeyboardRemove()

''' Конец инициализации '''


print("Log:\tБот включился")

# Если пользователь не ввел /start


def userDidntTypeStart(message):
    '''
    userDidntTypeStart(message)

    Если пользователь не ввел /start
    '''
    bot.send_message(message.from_user.id, 'Напишите { /start }')


# Отпрвить большое сообщение кусками
def botSendSplitedMessage(message, CurrentUser):
    '''
    botSendSplitedMessage(message, CurrentUser)

    Отпрвить большое сообщение кусками
    '''
    longText = "Результаты:\n"
    for ind in range(0, len(CurrentUser.VotesResult)):
        VotesSum = CurrentUser.VotesResult[ind][2] + \
            CurrentUser.VotesResult[ind][3]
        tempString = f'\nВ паре: \n" {CurrentUser.VotedPairs[ind][1]} \\ {CurrentUser.VotedPairs[ind][2]} " \n\n' \
            f'  За первый вариант проголосовал {round((CurrentUser.VotesResult[ind][2] * 100 / VotesSum), 2)}%,' \
            f'\n  За второй вариант - {round((CurrentUser.VotesResult[ind][3] * 100 / VotesSum), 2)}%\n'
        if len(longText) + len(tempString) < 3000:
            longText += tempString
            if ind == len(CurrentUser.VotesResult) - 1:
                bot.send_message(CurrentUser.UserId, longText)
        else:
            bot.send_message(CurrentUser.UserId, longText)
            longText = tempString
           
                

    # print(longText)
    # longText = util.split_string(longText, 2978)
    # for eachString in longText:
    #     bot.send_message(CurrentUser.UserId, eachString)


# Бот ловит комманду /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    '''
    send_welcome(message)

    Бот ловит комманду /start
    '''
    global UsersDict

    print("\nБот начал работу с пользователем: ", message.from_user.first_name)
    print("Log\tДобавление пользователя: ", message.from_user.id)
    try:
        UsersDict[str(message.from_user.id)].getStats(message)
        botSendSplitedMessage(message, UsersDict[str(message.from_user.id)])
    except KeyError:
        print("user didn't exist before")
    finally:
        bot.reply_to(
            message,
            f"Добро пожаловать {message.from_user.first_name}",
            reply_markup=answerMarkup)
        UsersDict[str(message.from_user.id)] = User(message, cursor, bot)
        print("Log\tВсе, кто сейчас пользуется ботом:")
        for item in UsersDict:
            print(
                f"User_id: \033[36m{item} \033[37m",
                " with name: \033[36m{ ",
                UsersDict[item].UserName,
                " }\033[37m")


# Бот принимает любой текст
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    '''
    get_text_messages(message)

    Бот принимает любой текст
    '''
    if str(message.from_user.id) in UsersDict.keys():
        CurrentUser = UsersDict[str(message.from_user.id)]

        if message.text.lower() == '/stop' or len(CurrentUser.PairsList) == 0:
            # Если закончились вопросы
            if len(CurrentUser.PairsList) == 0:
                bot.send_message(CurrentUser.UserId,
                                 "Поздравляем! \n\nВы закончили тестирование!")

            # Если пльзователь не голосовал
            elif len(CurrentUser.VotedPairs) == 0 or CurrentUser.VotedPairs == []:
                bot.send_message(
                    CurrentUser.UserId,
                    "Вы не проголосовали ни в одном вопросе!")

            # Вывод результатов
            else:
                print(CurrentUser.VotedPairs)
                CurrentUser.getStats(message)
                botSendSplitedMessage(message, CurrentUser)
            # Обнулить список пар, за ктороые пользователь голосовал
            CurrentUser.VotedPairs = []
            # Удалить пользователя из словаря
            UsersDict.pop(str(CurrentUser.UserId))

        # При выборе пользователем первого варианта
        elif message.text.lower() == '1':
            print(
                f"Log:\t{message.from_user.first_name} выбрал первый вариант")
            # Отправить в базу данных выбор пользователя
            cursor.execute(addVoteToFirstExpr(CurrentUser.selectedPair[0]))
            dataBase_bot.commit()
            bot.send_message(message.from_user.id, 'Выбран первый вариант!')
            # Добавить в список отвеченных опросов и предложить новый опрос
            CurrentUser.VotedPairs.append(CurrentUser.selectedPair)
            CurrentUser.offerNewVote(message, bot)
            print()

        # При выборе пользователем второго варианта
        elif message.text.lower() == '2':
            print(
                f"Log:\t{message.from_user.first_name} выбрал второй вариант")
            # Отправить в базу данных выбор пользователя
            cursor.execute(addVoteToSecondExpr(CurrentUser.selectedPair[0]))
            dataBase_bot.commit()
            bot.send_message(message.from_user.id, 'Выбран второй вариант!')
            # Добавить в список отвеченных опросов и предложить новый опрос
            CurrentUser.VotedPairs.append(CurrentUser.selectedPair)
            CurrentUser.offerNewVote(message, bot)
            print()

        # При выборе пользователем варианта статистика
        elif message.text.lower() == 'статистика':
            # Получить все результаты по голосоанию
            CurrentUser.getAllStats(message)
            botSendSplitedMessage(message, CurrentUser)
            # Удалить пользователя из листа активных пользователей
            UsersDict.pop(str(CurrentUser.UserId))

        # При выборе пользователем не обработанных результатов
        else:
            bot.send_message(
                message.from_user.id,
                'Не понимаю, что это значит.')

    # При выборе статистики без нажатия на кнопку /start
    elif message.text.lower() == 'статистика':
        StatUser = User(message, cursor, bot, True)
        StatUser.getAllStats(message)
        botSendSplitedMessage(message, StatUser)

    # В случае, если пользователь не ввел /start
    # и не нажал на кнопку статистики
    else:
        userDidntTypeStart(message)


def botStartFunc():
    '''
    botStartFunc()

    Запуск бота
    '''
    bot.polling()


def wakeBD():
    '''
    wakeBD()

    Разбудить базу данных
    '''
    while True:
        dataBase_bot.ping()
        print("Log:\tБаза данных: подклюение обновлено")
        time.sleep(10)
    pass


#             """Начало программы"""
# Создать поток для пробуждение БД
bdThread = threading.Thread(name="targetBdThread", target=wakeBD, daemon=True)
# Запустить поток для пробуждение БД
bdThread.start()
# Запустить бота
botStartFunc()
