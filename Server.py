import telebot
import random
import pymysql
import pymysql.cursors
from MySQLrequests import *
from telebot import types

# Инициализация
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

# отладка
# print(PairsList)

VotedPairs = []

# Взять случайную пару словосочетаний

selectedPair = ()


def get_random_pair():
    global selectedPair
    randIndex = random.randrange(len(PairsList))
    selectedPair = PairsList[randIndex]
    print(selectedPair)
    PairsList.pop(randIndex)


answerMarkup = types.ReplyKeyboardMarkup()
answerMarkup.add('1', '2', 'Статистика', '/stop', '/start')
MarkupHide = types.ReplyKeyboardRemove()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global selectedPair
    bot.reply_to(message, f"Добро пожаловать {message.from_user.first_name}", reply_markup=answerMarkup)
    get_random_pair()
    bot.send_message(message.from_user.id,
                     f'Укажите вариант, который вам больше всего нравится:\n\n1. {selectedPair[1]}\n2. {selectedPair[2]}')
    print("pair: ", selectedPair)
    print("\nБот начал работу с пользователем: ", message.from_user.first_name)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    global selectedPair
    if message.text.lower() == '1':
        # TODO: Сюда ебануть занос в first_expr_votes
        cursor.execute(addVoteToFirstExpr(selectedPair[0]))
        bot.send_message(message.from_user.id, 'Выбран первый вариант!')
        VotedPairs.append(selectedPair)
        get_random_pair()
        print()
    elif message.text.lower() == '2':
        # TODO: Сюды ебануть занос в second_expr_votes
        cursor.execute(addVoteToSecondExpr(selectedPair[0]))
        bot.send_message(message.from_user.id, 'Выбран второй вариант')
        VotedPairs.append(selectedPair)
        get_random_pair()
    elif message.text.lower() == 'Статистика':
        # TODO: Сюды ебануть запрос ВСЕЙ статистики
        AllVotesResult = []
        bot.send_message(message.from_user.id, "Результаты:")
        for ind in range(0, len(AllVotesResult)):
            VotesSum = AllVotesResult[i][1] + AllVotesResult[i][2]
            bot.send_message(message.from_user.id, f'В паре: \n{AllPairs[i][1]} \\ {AllPairs[i][2]} \n' \
                                                   f'за первый вариант проголосовал {float(AllVotesResult[i][1] / VotesSum)}% опрошенных, ' \
                                                   f'а за второй вариант - {float(AllVotesResult[i][2] / VotesSum)}%')
    elif message.text.lower() == '/stop' or len(PairsList) == 0:
        # TODO: Сюды ебануть запрос результатов опроса
        #'''SELECT * FROM Таблица Залупа WHERE `id_dict` = '''
        Query = getVotedIds(VotedPairs)
        print(Query)
        VotesResult = []
        bot.send_message(message.from_user.id, "Результаты:")
        for ind in range(0, len(VotesResult)):
            VotesSum = VotesResult[i][1] + VotesResult[i][2]
            bot.send_message(message.from_user.id, f'В паре: \n{VotedPairs[i][1]} \\ {VotedPairs[i][2]} \n' \
                                                   f'за первый вариант проголосовал {float(VotesResult[i][1] / VotesSum)}% опрошенных, ' \
                                                   f'а за второй вариант - {float(VotesResult[i][2] / VotesSum)}%')
        bot.send_message(message.from_user.id, "Спрятаф клавиатуру", reply_markup=MarkupHide)
    else:
        bot.send_message(message.from_user.id, 'Не понимаю, что это значит.')


for row in AllPairs:
    print("id: ", row[0], " first_expr: ", row[1], " second expr: ", row[2])

bot.polling()
