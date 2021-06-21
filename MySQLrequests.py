'''
Файл отвечает за генерацию MySQL запросов
'''
getAllPairs = "SELECT * FROM `dictionary_of_pairs`"


def addVoteToFirstExpr(id_dict):
    '''
    addVoteToFirstExpr(id_dict)

    Добавить голос к первому варианту голосования
    '''
    return f"""UPDATE `5SbqamHdMU`.`link_table` SET `firs_expr_amount_of_votes` = `firs_expr_amount_of_votes` + 1 WHERE `id_dictionary` = {id_dict};"""


def addVoteToSecondExpr(id_dict):
    '''
    addVoteToSecondExpr(id_dict)
    
    Добавить голос к второму варианту голосования
    '''
    return f"""UPDATE `5SbqamHdMU`.`link_table` SET `second_expr_amount_of_votes` = `second_expr_amount_of_votes` + 1 WHERE `id_dictionary` = {id_dict};"""


def getVotedIds(votedList):
    '''
    getVotedIds(votedList)

    Получить результаты голосования из БД
    '''
    if len(votedList) == 0:
        print("votedList is empty")
        return "SELECT * FROM `5SbqamHdMU`.`link_table`"
    if votedList is None:
        print("votedList is None")
        return "SELECT * FROM `5SbqamHdMU`.`link_table`"


    SQLRequest = '''SELECT * FROM `5SbqamHdMU`.`link_table` WHERE `id_dictionary` = '''
    for voted in votedList:
        SQLRequest += str(voted[0]) + " OR `id_dictionary` = "

    return SQLRequest[:len(SQLRequest) - 22] + ";"
