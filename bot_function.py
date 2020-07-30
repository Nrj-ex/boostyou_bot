import time
import random
import json
import csv
import sqlite3 as sql
import config

file_name = config.FILE_NAME
with open('workout.json', 'r', encoding="utf-8") as f:
    workout_bd = json.load(f)


def search_workout(message):
    text_mess = message.text

    #bot.send_message(message.chat.id, text_mess)
    # разбить сообщение по запятой
    split_text = text_mess.lower().split(',')
    # разбить по пробелу
    for i in split_text:
        rand_work = i.split()
        print(rand_work)
    # Есть ли разбитом сообщении упражнение и число
        if len(rand_work) == 2:
            # проверять отлько сообщения из 2 составляющих
            for j in rand_work:
                if j in workout_bd['synonyms']:
                    # сохраняем id упражнения
                    #print(j)
                    id = workout_bd['synonyms'][j]
                    rand_work.remove(j)
                    count = str(rand_work[0])
                    if count.isdigit():
                        user = message.from_user.username
                        date = str(message.date)
                        chatid = str(message.chat.id)
                        # получить название упражнения из бд
                        workout = workout_bd['workouts'][id]
                        save_data = [user, workout, count, date, chatid]
                        # сделать сохранение

                        print(save_data)
                        save_csv('scoring.csv', save_data)
                        save_db(config.DB_NAME, save_data)


def save_db(db_name, data):
    # коннект к бд
    conn = sql.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO `scoring` VALUES ('{data[0]}', "
                   f"'{data[1]}', {data[2]}, {data[3]}, {data[4]})")
    conn.commit()


def save_csv(file_name, data):
    with open(file_name, 'a', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(data)


def sit_up(work_time):
    for i in range(work_time):
        time.sleep(1)
        return 'Выпрями спину'


def work_duration():
    print('Сколько часов будет работать мой господин?\n')
    work_duration = 0
    while True:
        answer = input().split()
        for i in answer:
            if i.isdigit():
                work_duration = round(float(i))
                break
        if work_duration > 0:
            return work_duration
        print('Не понял ты не русский что ли? Спрашиваю сколько пахать будешь?')


def random_workout():
    workout_list = ['отжимания', 'подтягивания', 'приседания', 'пресс']

    def choice_workout(list):
        workout = random.choice(list)
        if workout == 'отжимания' or workout == 'приседания':
            count = random.randint(10, 40)
        elif workout == 'подтягивания':
            count = random.randint(4, 9)
        elif workout == 'пресс':
            count = random.randint(10, 20)
        else:
            count = random.randint(1, 20)
        return workout, count

    # print(choice_workout(workout_list))
    workout, count = choice_workout(workout_list)
    # print('Упражнение: {} - {} повт.'.format(workout, count))
    return 'Упражнение: {} - {} повт.'.format(workout, count)



def get_name(data):
    names = []
    for i in data:
        names.append(i[0])
    return set(names)


def get_scoring(file):
    data = []
    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data


scoring = get_scoring(file_name)


def get_my_stat(name, data=scoring):
    stat = {}
    for i in data:
        if i[0] == name:
            if i[1] in stat:
                stat[i[1]] += int(i[2])
            else:
                stat[i[1]] = int(i[2])
    return stat


def get_all_stats(file=file_name):
    data = get_scoring(file)
    names = get_name(data)
    all_stats = {}
    for name in names:
        all_stats[name] = get_my_stat(name, data)
    return all_stats





