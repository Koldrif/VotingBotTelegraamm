import telebot
import random
import pymysql
import pymysql.cursors
from MySQLrequests import *


class User:
    def __init__(
            self,
            telegrammMessege,
            dbCursor,
            telegrammBot,
            isStats=False):
        self.Messege = telegrammMessege
        self.UserId = telegrammMessege.from_user.id
        self.UserName = telegrammMessege.from_user.first_name
        self.UserCursor = dbCursor
        # Запрос в базу данных для получения вопросов
        dbCursor.execute(getAllPairs)
        self.AllPairs = dbCursor.fetchall()
        self.PairsList = []
        # преобразование кортежа в массив
        for item in self.AllPairs:
            self.PairsList.append(item)
        self.VotedPairs = []
        self.selectedPair = ()
        self.VotesResult = []
        # Если пользователь не запрашивает получение статистики
        if(not isStats):
            self.offerNewVote(telegrammMessege, telegrammBot)

    # Получить случайную пару из тех, что еще не использовались в голосовании
    def get_random_pair(self):
        randIndex = random.randrange(len(self.PairsList))
        self.selectedPair = self.PairsList[randIndex]
        print("Log:\tСгенерирована новая пара:\nPair: ", self.selectedPair)
        self.PairsList.pop(randIndex)

    # Получить новую пару и предложить пользователю проголосовать
    def offerNewVote(self, message, bot):
        self.get_random_pair()
        bot.send_message(
            message.from_user.id,
            f'Укажите вариант, который вам больше всего нравится:\n\n1. {self.selectedPair[1]}\n2. {self.selectedPair[2]}')

    # Получить статистику по отвеченным вопросам
    def getStats(self, message):
        Query = getVotedIds(self.VotedPairs)
        print(
            f"Log:\t{message.from_user.first_name} ввел комманду: [ /stop ]\nQuery is: ")
        print(Query)
        self.UserCursor.execute(Query)
        self.VotesResult = self.UserCursor.fetchall()

    # Получить статистику по всем вопросам
    def getAllStats(self, message):
        Query = "SELECT * FROM `5SbqamHdMU`.`link_table`"
        print(
            f"Log:\t{message.from_user.first_name} ввел комманду: [ Статистика ]\nQuery is: ")
        print(Query)
        self.VotedPairs = self.AllPairs
        self.UserCursor.execute(Query)
        self.VotesResult = self.UserCursor.fetchall()
