import telebot
import pymysql
import pymysql.cursors
from MySQLrequests import MySQLRequest

# Инициализация
TOKEN = r"1801737865:AAGQroqS0QitNBRVmqP58TQLWtjrl57CP38"
bot = telebot.TeleBot(TOKEN)
dataBase_bot = pymysql.connect(
    host="remotemysql.com",
    user="5SbqamHdMU",
    password="RqcFw1HOoz",
    database="5SbqamHdMU",
)
cursor = dataBase_bot.cursor()

# Запрос на получение всех пар из таблицы
cursor.execute(MySQLRequest.getAllPairs)
# Создать кортеж из данных в таблице
AllPairs = cursor.fetchall()

for row in AllPairs:
    print("id: ", row[0], " first_expr: ", row[1], " second expr: ", row[2])
