import telebot
import random
import pymysql
import pymysql.cursors
from MySQLrequests import *
from telebot import types

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


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global selectedPair
    bot.reply_to(message, f"Добро пожаловать {message.from_user.first_name}", reply_markup=answerMarkup)
    offerNewVote(message)
    print("\nБот начал работу с пользователем: ", message.from_user.first_name)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global selectedPair
    global VotedPairs
    global AllPairs
    global PairsList

    if message.text.lower() == '/stop' or len(PairsList) == 0:
        if len(PairsList) == 0:
            cursor.execute(getAllPairs)
            # Создать кортеж из данных в таблице.
            # Формат: (id, first_expr, second_expr)
            AllPairs = cursor.fetchall()

            # Перевод кортежа в массив
            PairsList = []
            for item in AllPairs:
                PairsList.append(item)
            VotedPairs = []

        if len(VotedPairs) == 0 or VotedPairs == []:
            for item in AllPairs:
                VotedPairs.append(item)
        print(VotedPairs)
        VotesResult = getStats(message, VotedPairs)
        bot.send_message(message.from_user.id, "Результаты:")
        for ind in range(0, len(VotesResult)):
            VotesSum = VotesResult[ind][2] + VotesResult[ind][3]
            bot.send_message(message.from_user.id, f'В паре: \n{VotedPairs[ind][1]} \\ {VotedPairs[ind][2]} \n' \
                                                   f'за первый вариант проголосовал {round((VotesResult[ind][2] * 100 / VotesSum), 2)}% опрошенных, ' \
                                                   f'а за второй вариант - {round((VotesResult[ind][3] * 100 / VotesSum), 2)}%')
        VotedPairs = []
        #bot.send_message(message.from_user.id, "Спрятаф клавиатуру", reply_markup=MarkupHide)
    elif message.text.lower() == '1':
        # TODO: Сюда установить занос в first_expr_votes
        if selectedPair == ():
            userDidntMadeAChoice(message)
        # elif len(VotedPairs) == 0 or VotedPairs == []:
        #     for item in AllPairs:
        #         VotedPairs.append(item)
        else:
            print(f"Log:\t{message.from_user.first_name} выбрал первый вариант")
            cursor.execute(addVoteToFirstExpr(selectedPair[0]))
            dataBase_bot.commit()
            bot.send_message(message.from_user.id, 'Выбран первый вариант!')
            VotedPairs.append(selectedPair)
            offerNewVote(message)
            print()
    elif message.text.lower() == '2':
        # TODO: Сюды ебануть занос в second_expr_votes
        if selectedPair == ():
            userDidntMadeAChoice(message)
        # elif len(VotedPairs) == 0 or VotedPairs == []:
        #     for item in AllPairs:
        #         VotedPairs.append(item)
        else:
            print(f"Log:\t{message.from_user.first_name} выбрал второй вариант")
            cursor.execute(addVoteToSecondExpr(selectedPair[0]))
            dataBase_bot.commit()
            bot.send_message(message.from_user.id, 'Выбран второй вариант!')
            VotedPairs.append(selectedPair)
            offerNewVote(message)
            print()
    elif message.text.lower() == 'статистика':
        # TODO: Сюды ебануть запрос ВСЕЙ статистики

        AllVotesResult = getStats(message, [])
        bot.send_message(message.from_user.id, "Результаты:")
        for ind in range(0, len(AllVotesResult)):
            VotesSum = AllVotesResult[ind][2] + AllVotesResult[ind][3]
            bot.send_message(message.from_user.id, f'В паре: \n{AllPairs[ind][1]} \\ {AllPairs[ind][2]} \n' \
                                                   f'за первый вариант проголосовал {round((AllVotesResult[ind][2] * 100 / VotesSum), 2)}% опрошенных, ' \
                                                   f'а за второй вариант - {round(AllVotesResult[ind][3] * 100 / VotesSum, 2)}%')

    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


# for row in AllPairs:
# #    print("id: ", row[0], " first_expr: ", row[1], " second expr: ", row[2])
def botStartFunc():
    # try:
        bot.polling()
#     except Exception:
#         print("Oh shit, again, we've got an exception")
#         botStartFunc()

botStartFunc()