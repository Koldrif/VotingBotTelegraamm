import telebot
import pymysql
import pymysql.cursors

#инициализация
TOKEN=  r"1801737865:AAGQroqS0QitNBRVmqP58TQLWtjrl57CP38"
bot = telebot.TeleBot(token=TOKEN)
dataBase_bot = pymysql.connect(
                                host="remotemysql.com",
                                user="5SbqamHdMU",
                                password="RqcFw1HOoz",
                                database="5SbqamHdMU",
                                )
cursor = dataBase_bot.cursor()

#Запрос на получение всех пар из таблицы
requestToGetAllPairs = "SELECT * FROM `dictionary_of_pairs`"
cursor.execute(requestToGetAllPairs)

AllPairs =  cursor.fetchall()


for row in AllPairs:
    print("id: " , row[0] , " first_expr: " , row[1] , " second expr: " , row[2])

