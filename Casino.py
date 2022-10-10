#########################################################
# INITIALIZATION VARIABLES

import sqlite3
from random import randint, random

db = sqlite3.connect ('CasinoData.db')  # DataBase
cdb = db.cursor()                       # Cursor of DB

                                        # Create table
cdb.execute ("""CREATE TABLE IF NOT EXISTS users (
    login TEXT (30),
    password TEXT (16),
    cash BIGINT (15)                          
)""")
db.commit()

#########################################################
# FUNCSION

def registrate (user_login, user_pas):
    print ('Регистрация:\n')
    cdb.execute (f"SELECT login FROM users WHERE login = '{user_login}'")
    if cdb.fetchone () is None:
        cdb.execute (f"INSERT INTO users VALUES (?, ?, ?)", (user_login, user_pas, 100))
        db.commit()
    else:
        print ('Вы уже зарегистрированы!')
        show_user(user_login)
        quit ()

#########################################################
    
def show_user(user): 
    for value in cdb.execute (f"SELECT * FROM users WHERE login = '{user}'"):
        print (value)

#########################################################
    
def show_all_user(): 
    for value in cdb.execute (f"SELECT * FROM users"):
        print (value)

#########################################################


def prob_init (user_login):
    cdb.execute (f"SELECT * FROM users WHERE login = '{user_login}'")
    if cdb.fetchone () is None: return print ("Не найден данный логин!"), quit()
    else: return user_login

#########################################################

def delete (user_login):
    prob_init (user_login)
    cdb.execute (f"DELETE FROM users WHERE login = '{user_login}'")
    db.commit()
    print ("Пользователь удалён!")
    initialization()

#########################################################

def zeroing (user_login):
    prob_init (user_login)
    cdb.execute (f"UPDATE users SET cash = 0 WHERE login = '{user_login}'")
    db.commit()
    print ("Ваш баланс = 0!")

#########################################################

def main_table(user_login):
    prob_init (user_login)
    cdb.execute (f"SELECT * from users WHERE login = '{user_login}'")
    cash = cdb.fetchone()[-1]
    # print ('\nВы успешно авторизировались!')
    print (f'{user_login}, Ваш баланс: {cash}')

#########################################################

def cash_up(user_login):
    prob_init (user_login)
    new_cash = int(input_set('Введите сумму пополнения: '))
    cdb.execute (f"SELECT cash FROM users WHERE login = '{user_login}'")
    cash = cdb.fetchone()[0]
    cdb.execute (f"UPDATE users SET cash = {cash + new_cash} WHERE login = '{user_login}'")
    db.commit()
    print (f'{user_login}, Ваш баланс пополнен и равен: {cash + new_cash}')
    
#########################################################

def bet_check (user_login):
    prob_init (user_login)
    cdb.execute (f"SELECT  cash from users WHERE login = '{user_login}'")
    cash = cdb.fetchone()[0]
    try:
        bet = input_set('\nВаша ставка: ')
        if bet in ['quit', 'continue', 'break', 'выход', 'выйти', 'дальше']:
            main_table (user_login)
            play(user_login)
            quit()
        if abs(int(bet)) > cash:
            return print ("Ставка слишком большая!")
        return abs(int(bet))
    except ValueError: 
        print ('Введите цифры!')
        return

#########################################################

def input_set(text=""):
    i = input(text)
    if i in ['setings', 'seting', 'settings', 'setting']:
        setings()
        quit()
    elif i == "": 
        print ("Вы не ввели никаких данных!")
        input_set ()
    else: return i

#########################################################

def initialization():
    print ('Авторизация:\n')
    probs = 3
    while probs >= 0:
        user_login = input_set()
        if user_login in ['setings', 'seting', 'settings', 'setting']: 
            setings()
            quit()
        cdb.execute (f"SELECT login FROM users WHERE login = '{user_login}'")
        if cdb.fetchone() is None:
            print ("Нужна регистрация!")
            print ("Желаете зарегистрироваться сейчас? Y/N: ")
            if input_set () in ['Y', 'y', 'У', 'у']:
                while True:
                    login = input_set ('Login (>30 символов): ')
                    if len(login) > 30: 
                        print ('Введеное кол-во символов превышает лимит')
                        continue
                    password = input_set ('Password (>16 символов): ')
                    if len(password) > 16: 
                        print ('Введеное кол-во символов превышает лимит')
                        continue
                    registrate(login, password)
                    print ("Вы успешно зарегистрировались!\n")
                    play()
                    quit ()
            else:   print ("Для продолжения, нужно зарегистрироваться!"), quit()
        user_pas = input_set ('Password: ')
        cdb.execute (f"SELECT login, password FROM users WHERE login = '{user_login}' AND password = '{user_pas}'")
        if cdb.fetchone() is None:
            if probs == 0:
                print ("К сожалению, вы заблокированы.")
                quit()
            else:
                print (f'Неверный пароль! У вас осталось {probs} попыток')
            probs -= 1
        else:
            return (user_login, user_pas)

#########################################################

def play(user_login = 0):
    if user_login == False:  user_login = initialization()[0]
    print ('\nВ какую игру сыграем?\n1. РандоМит\n2. Однорукий Бандит\n3. Рулетка')
    try:
        result = int(input_set('1/2/3: '))
        if result == 1:  randomid (user_login)
        if result == 2:  slot_machin (user_login)
        if result == 3:  ruletka (user_login)
    except ValueError:
        print ('Введите цифры!') 
        play()
    else: 
        print ()
        main_table(user_login)
        print ('Приходите ещё!\n')
        quit()

#########################################################

def randomid (user_login):
    prob_init(user_login)
    print ('\nКА-ЗИ-НО!\nРандоМит')
    while True:
        cdb.execute (f"SELECT cash from users WHERE login = '{user_login}'")
        cash = cdb.fetchone()[0]
        print ('\nНаигрались? Пишите "выход/quit" для выхода')
        bet = bet_check(user_login)
        if bet is None: continue
        fortune = randint (-20, 20)
        bet_new = (fortune * int(bet) / 10).real
        cash += round (bet_new, 2)
        if fortune >= 0: 
            print (f"Выпало число {fortune}\nВы выйграли: {round(bet_new,2)}")
        elif fortune < 0:
            print (f"Выпало число {fortune}\nВы проиграли: {round(bet_new,2)}")
        if cash < 0: zeroing(user_login)
        else:
            cdb.execute (f"UPDATE users SET cash = {cash:.1f} WHERE login = '{user_login}'")
            db.commit()
            print (f"\nТеперь ваш баланс равен: {cash:.1f}")

#########################################################

def slot_machin (user_login):
    while True:
        prob_init (user_login)
        print ('\nНаигрались? Пишите "выход/quit" для выхода')
        bet = bet_check (user_login)
        if bet is None: continue
        cdb.execute (f"SELECT cash from users WHERE login = '{user_login}'")
        cash = cdb.fetchone()[0]
        table = {'Ѿ':20, 'Ѽ':10, 'Ѻ':5, 'Ѭ':2.5, 'Ѫ':1, 'Ѧ':0.5, 'Ӕ':0.25, 'Ҩ':0.1}
        simbol = [i for i in table.keys ()]
        chance = []
        random_chance = 7
        for i in table:
            print (f'{i}: {table[i]}X', end='       ')
        print ()
        for i in range (7):
            if random () > i * 0.1 + 0.25: random_chance -= 1 
        chance.append (simbol [random_chance])
        while len(chance)<3:
            if random () > 0.5:  chance.append (chance[0])
            else: chance.append (simbol[randint(0,7)])
        if chance [0] == chance [1]: 
            if chance [1] == chance [2]: 
                bet *= table.get (chance [-1])
                print (" ".join (chance), "Вы выйграли! ", bet)
            else: 
                print (" ".join (chance), "Почти! Вы проиграли: ", bet)
                bet -= bet*2
        else: 
            print (" ".join (chance), "Пройгрыш! Вы проиграли: ", bet)
            bet -= bet*2
        cdb.execute (f"UPDATE users SET cash = {cash+bet} WHERE login = '{user_login}'")
        db.commit()
        show_user (user_login)
        # chance = set(simbol)
        # print (simbol,chance)

#########################################################

def ruletka(user_login):
    # prob_init(user_login)
    table_rulet = [i for i in range(1, 37)]
    table_rulet.extend (['1-12', '13-24', '25-36'])
    while True:
        print ('\nНаигрались? Пишите "выход/quit" для выхода')
        bet = bet_check (user_login)
        if bet is None: continue
        # Выведение в терминал стола рулетки
        print ('Выберите куда поставить вашу ставку:\n')
        for i in range (1,37):
            if i < 9:
                print (i, end='   ')
            else: print (i, end='  ')
            if i % 3 == 0: print()
        print (" ".join (table_rulet [-3:]))
        # Проверяем выбор игрока на корректные значения
        while True:
            try:
                number = input_set()
                if number in table_rulet [-3:]:
                    break
                elif number not in table_rulet:
                    print ('Вы введи некорректный номер!')
                    continue
                number = abs(int(number))
                break
            except ValueError:
                print ('Вы введи некорректный номер!')
                continue
        # Выводим число выпавшее на рулетке
        cdb.execute (f"SELECT cash from users WHERE login = '{user_login}'")
        cash = cdb.fetchone()[0]
        print ('Выпало число: ') 
        rulet = randint (1, 36)
        print (rulet)
        # Проверяем выпавшее число со ставкой
        result = 0
        if isinstance (number, int): 
            if rulet == number:
                result = bet * 35
                print(f'Поздравляем! Вы выйграли: {result}')
            else:
                result -= bet
                print(f'Вы проиграли {result}')
        else:
            number = number.split ('-')
            if int(number[0]) <= rulet <= int(number[1]):
                result = bet * 2.5
                print(f'Поздравляем! Вы выйграли: {result}')
            else:
                result -= bet
                print(f'Вы проиграли {result}')
        cdb.execute (f"UPDATE users SET cash = {cash+result} WHERE login = '{user_login}'")
        db.commit()
        print (f'Ваш баланс: {cash+result}')
    

#########################################################

def setings (): 
    print ('''Настройки содержат в себе следующие меню:
    'regis' - Регистрация, 
    'random' - Играть в казино,
    'table' - Главное меню,
    'plays' - Начало программы,
    'zero' - Обнуление,
    'delet' - Удаление,
    'allshow' - Показать всех игроков,
    'quit' - Выйти из программы,
    'show' - Показать информацию об игроке,
    'cashup' - Пополнение баланса у игрока,
    'probin' - Проверка логина на существование,
    'slotmach' - "Однорукий бандит"
    'betcheck' - Проверка ставки у конкретного пользователя,
    'rulet' - Рулетка''')
    word = input()

    sets = {'regis': registrate ,
            'random': randomid ,
            'table': main_table,
            'plays': play,
            'zero': zeroing ,
            'delet': delete,
            'allshow': show_all_user,
            'quit': quit,
            'show': show_user,
            'cashup': cash_up,
            'probin': prob_init,
            'betcheck': bet_check,
            'slotmach': slot_machin,
            'rulet': ruletka}.get (word, "Ошибка, не правильно написана функция!")
    if word in ['regis', 'plays', 'allshow', 'quit']:
        if word == 'regis':    return sets(input ('Log in: '), input ('Password: '))
        else:   return sets() 
    elif word in ['rulet', 'slotmach', 'random', 'table', 'plays', 'zero', 'delet', 'show', 'cashup', 'probin', 'betcheck']: return sets(input ('Log in: '))
    return setings()

#########################################################
# MAIN PROGRAM


def main():
    play()
    cdb.close()
    db.close()

main()

#########################################################
