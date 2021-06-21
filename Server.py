# TODO:

# 1. (Done) повторы вопросов, их не должно быть 

# 2. (Done, но чуть-чуть) сделать результаты одним большим сообщением

# 3. (Done) кнопка стоп должна выдавать статистику только по отвеченным за прохождение вопросам, по всем это статистика

# 4. (Done) если кнопку старт нажали повторно, при этом не завершив текущее прохождение, нужно вывести результаты за текущее прохождение и только потом начинать новое

# 5. (Done) ещё забыл проверить, завершает ли кнопка статистика прохождение. по идее, лучше, если да, т.е. она полностью идентична стоп, но выдаёт статистику по всем вопросам, а не только отвеченным


import random
import threading
import time

import pymysql
import pymysql.cursors
#import schedule
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

# Запрос на получение всех пар словосочетнаий из таблицы
cursor.execute(getAllPairs)

# Создать кортеж из данных в таблице.
# Формат: (id, first_expr, second_expr)
AllPairs = cursor.fetchall()

# Перевод кортежа в массив
PairsList = []
for item in AllPairs:
    PairsList.append(item)

VotedPairs = []

# Взять случайную пару словосочетаний
selectedPair = ()
# Сделать кнопки управление для бота
answerMarkup = types.ReplyKeyboardMarkup()
answerMarkup.add('1', '2', 'Статистика', '/stop', '/start')

# Создать уборщика кнопок
MarkupHide = types.ReplyKeyboardRemove()

''' Конец инициализации '''

UsersDict = {} #{ user_id : ### }

print("Log:\tБот включился")


# Получить случайную пару из тех, что еще не использовались в голосовании
def get_random_pair():
    global selectedPair
    randIndex = random.randrange(len(PairsList))
    selectedPair = PairsList[randIndex]
    print("Log:\tСгенерирована новая пара:\nPair: ", selectedPair)
    PairsList.pop(randIndex)


# Получить новую пару и предложить пользователю проголосовать
def offerNewVote(message):
    get_random_pair()
    bot.send_message(message.from_user.id,
                     f'Укажите вариант, который вам больше всего нравится:\n\n1. {selectedPair[1]}\n2. {selectedPair[2]}')


def getStats(message, votedList):
    Query = getVotedIds(votedList)
    print(f"Log:\t{message.from_user.first_name} ввел комманду: [ /stop ]\nQuery is: ")
    print(Query)
    cursor.execute(Query)
    result = cursor.fetchall()
    return result


def userDidntMadeAChoice(message):
    bot.send_message(message.from_user.id, 'Напишите { /start }')

def botSendSplitedMessage(message):
    pass
    

def botSendSplitedMessage(message, CurrentUser):
    longText = "Результаты:\n"
    for ind in range(0, len(CurrentUser.VotesResult)):
                    VotesSum = CurrentUser.VotesResult[ind][2] + CurrentUser.VotesResult[ind][3]
                    longText += f'\nВ паре: \n" {CurrentUser.VotedPairs[ind][1]} \\ {CurrentUser.VotedPairs[ind][2]} " \n\n' \
                                                        f'  За первый вариант проголосовал {round((CurrentUser.VotesResult[ind][2] * 100 / VotesSum), 2)}%,' \
                                                        f'\n  За второй вариант - {round((CurrentUser.VotesResult[ind][3] * 100 / VotesSum), 2)}%\n'
    print(longText)
    longText = util.split_string(longText, 2970)
    for eachString in longText:
        bot.send_message(CurrentUser.UserId, eachString)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    global selectedPair
    global UsersDict
    
    #offerNewVote(message)
    print("\nБот начал работу с пользователем: ", message.from_user.first_name)
    print("Log\tДобавление пользователя: ", message.from_user.id)
    try:
        UsersDict[str(message.from_user.id)].getStats(message)
        botSendSplitedMessage(message, UsersDict[str(message.from_user.id)])
    except KeyError:
        print("user didn't exist before")
    finally:
        bot.reply_to(message, f"Добро пожаловать {message.from_user.first_name}", reply_markup=answerMarkup)
        UsersDict[str(message.from_user.id)] = User(message, cursor, bot)
        print("Log\tВсе, кто сейчас пользуется ботом:")
        for item in UsersDict:
            print(f"User_id: \033[36m{item} \033[37m", " with name: \033[36m{ ", UsersDict[item].UserName, " }\033[37m")



@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global selectedPair
    global VotedPairs
    global AllPairs
    global PairsList
    
    
    if str(message.from_user.id) in UsersDict.keys():
        CurrentUser = UsersDict[str(message.from_user.id)]
   
        if message.text.lower() == '/stop' or len(CurrentUser.PairsList) == 0:
            if len(CurrentUser.PairsList) == 0:
                # TODO : Выводить сообщение, что вопросы кончились 
                bot.send_message(CurrentUser.UserId, "Поздравляем! \n\nВы закончили тестирование!")
                # CurrentUser = User(message, cursor)
                # # Создать кортеж из данных в таблице.
                # # Формат: (id, first_expr, second_expr)
                # CurrentUser.AllPairs = cursor.fetchall()
                
                # Перевод кортежа в массив
                PairsList = []
                for item in AllPairs:
                    PairsList.append(item)
                VotedPairs = []

            if len(CurrentUser.VotedPairs) == 0 or CurrentUser.VotedPairs == []:
                # for item in CurrentUser.AllPairs:
                #     CurrentUser.VotedPairs.append(item)
                bot.send_message(CurrentUser.UserId, "Вы не проголосовали ни в одном вопросе!")
            else:
                print(CurrentUser.VotedPairs)
                CurrentUser.getStats(message)
                botSendSplitedMessage(message, CurrentUser)
            # bot.send_message(message.from_user.id, "Результаты:")
            # for ind in range(0, len(CurrentUser.VotesResult)):
            #     VotesSum = CurrentUser.VotesResult[ind][2] + CurrentUser.VotesResult[ind][3]
            #     bot.send_message(message.from_user.id, f'В паре: \n{CurrentUser.VotedPairs[ind][1]} \\ {CurrentUser.VotedPairs[ind][2]} \n' \
            #                                         f'за первый вариант проголосовал {round((CurrentUser.VotesResult[ind][2] * 100 / VotesSum), 2)}% опрошенных, ' \
            #                                         f'а за второй вариант - {round((CurrentUser.VotesResult[ind][3] * 100 / VotesSum), 2)}%')
            CurrentUser.VotedPairs = []
            UsersDict.pop(str(CurrentUser.UserId))
            # bot.send_message(message.from_user.id, "Спрятаф клавиатуру", reply_markup=MarkupHide)
        elif message.text.lower() == '1':
            # TODO: Сюда установить занос в first_expr_votes
            #if selectedPair == ():
                #userDidntMadeAChoice(message)
            # elif len(VotedPairs) == 0 or VotedPairs == []:
            #     for item in AllPairs:
            #         VotedPairs.append(item)
            #else:
                print(f"Log:\t{message.from_user.first_name} выбрал первый вариант")
                cursor.execute(addVoteToFirstExpr(CurrentUser.selectedPair[0]))
                dataBase_bot.commit()
                bot.send_message(message.from_user.id, 'Выбран первый вариант!')
                CurrentUser.VotedPairs.append(CurrentUser.selectedPair)
                CurrentUser.offerNewVote(message, bot)
                print()
        elif message.text.lower() == '2':
            # TODO: Сюды ебануть занос в second_expr_votes
            #if selectedPair == ():
                #userDidntMadeAChoice(message)
            # elif len(VotedPairs) == 0 or VotedPairs == []:
            #     for item in AllPairs:
            #         VotedPairs.append(item)
            #else:
                print(f"Log:\t{message.from_user.first_name} выбрал второй вариант")
                cursor.execute(addVoteToSecondExpr(CurrentUser.selectedPair[0]))
                dataBase_bot.commit()
                bot.send_message(message.from_user.id, 'Выбран второй вариант!')
                CurrentUser.VotedPairs.append(CurrentUser.selectedPair)
                CurrentUser.offerNewVote(message, bot)
                print()

        elif message.text.lower() == 'статистика':
            # TODO: Сюды ебануть запрос ВСЕЙ статистики
            
            CurrentUser.getAllStats(message)
            botSendSplitedMessage(message, CurrentUser)
            # bot.send_message(message.from_user.id, "Результаты:")
            # for ind in range(0, len(AllVotesResult)):
            #     VotesSum = AllVotesResult[ind][2] + AllVotesResult[ind][3]
            #     bot.send_message(message.from_user.id, f'В паре: \n{AllPairs[ind][1]} \\ {AllPairs[ind][2]} \n' \
            #                                         f'за первый вариант проголосовал {round((AllVotesResult[ind][2] * 100 / VotesSum), 2)}% опрошенных, ' \
            #                                         f'а за второй вариант - {round(AllVotesResult[ind][3] * 100 / VotesSum, 2)}%')
            
            UsersDict.pop(str(CurrentUser.UserId))
        
        else:
            bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')

        #print(CurrentUser.VotedPairs)
    elif message.text.lower() == 'статистика':
        # TODO: Сюды ебануть запрос ВСЕЙ статистики
        StatUser = User(message, cursor, bot, True)
        StatUser.getAllStats(message)
        botSendSplitedMessage(message, StatUser)
        # bot.send_message(message.from_user.id, "Результаты:")
        # for ind in range(0, len(AllVotesResult)):
        #     VotesSum = AllVotesResult[ind][2] + AllVotesResult[ind][3]
        #     bot.send_message(message.from_user.id, f'В паре: \n{AllPairs[ind][1]} \\ {AllPairs[ind][2]} \n' \
        #                                         f'за первый вариант проголосовал {round((AllVotesResult[ind][2] * 100 / VotesSum), 2)}% опрошенных, ' \
        #                                         f'а за второй вариант - {round(AllVotesResult[ind][3] * 100 / VotesSum, 2)}%')
        
        #UsersDict.pop(str(StatUser.UserId))
    else:
        userDidntMadeAChoice(message)


# for row in AllPairs:
# #    print("id: ", row[0], " first_expr: ", row[1], " second expr: ", row[2])
def botStartFunc():
    # try:
    bot.polling()

def wakeBD():
    while True:
        dataBase_bot.ping()
        print("Log:\tБаза данных: подклюение обновлено")
        time.sleep(10)
    pass

"""Начало программы"""
bdThread = threading.Thread(name="targetBdThread", target=wakeBD, daemon=True)
bdThread.start()
botStartFunc() 


    

#     except Exception:
#         print("Oh shit, again, we've got an exception")
#         botStartFunc()




