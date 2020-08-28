import json
import sqlite3 as sql
import config

DB_NAME = config.DB_NAME
file_name = config.FILE_NAME
with open('workout.json', 'r', encoding="utf-8") as f:
    workout_bd = json.load(f)


def search_workout(message):
    text_mess = message.text
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
                        save_db(DB_NAME, save_data)


def save_db(db_name, data):
    # коннект к бд
    conn = sql.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO `scoring` VALUES ('{data[0]}', "
                   f"'{data[1]}', {data[2]}, {data[3]}, {data[4]})")
    conn.commit()


def get_my_stat(name, db_name=DB_NAME):
    conn = sql.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT workout, SUM(count) "
                   f"FROM scoring where nickname = '{name}' GROUP BY workout")
    results = cursor.fetchall()
    result = {}
    for i in results:
        result[i[0]] = i[1]
    return result


def get_all_stats(db_name=DB_NAME):
    conn = sql.connect(db_name)
    cursor = conn.cursor()
    cursor.execute(f"SELECT nickname FROM scoring GROUP BY nickname")
    names = cursor.fetchall()
    all_stats = {}
    for name in names:
        print(name[0])
        all_stats[name[0]] = get_my_stat(name[0])
    return all_stats







