import telebot
from bot_function import search_workout
# from telebot import types
# import time
from bot_function import random_workout
from bot_function import get_my_stat
from bot_function import get_all_stats
import config

# @Boostyou_bot
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Список доступных комманд /help')


@bot.message_handler(commands=['help'])
def start(message):
    commands = '/my_stats\n/all_stats'
    # bot.send_message(message.chat.id, 'Список команд:\n/sit_up\n/random_workout')
    bot.send_message(message.chat.id, f'Умею запоминать упражнения которые'
                                      f' вы выполнили и выводить статистику\nСписок доcтупных '
                                      f'комманд:\n{commands}')


@bot.message_handler(commands=['my_stats'])
def show_my_stats(message):
    # показать мою статистику
    stat = get_my_stat(message.from_user.username)
    text_message = message.from_user.username + ':\n'
    for workout in stat:
        text_message += f'{workout}: {stat[workout]}\n'
    bot.send_message(message.chat.id, text_message)


@bot.message_handler(commands=['all_stats'])
def show_all_stats(message):
    all_stats = get_all_stats()
    text_message = ''
    for name in all_stats:
        text_message += name + ':\n'
        for workout in all_stats[name]:
            text_message += f'{workout}: {all_stats[name][workout]}\n'
    bot.send_message(message.chat.id, text_message)


# @bot.message_handler(commands=['sit_up'])
# def start(message):
#     bot.send_message(message.from_user.id, 'Сиди ровно кожаный ублюдок, я слежу за тобой!')
#     for i in range(5):
#         time.sleep(10)
#         bot.send_message(message.from_user.id, 'Выпрямил спину ублюдок!')


# @bot.message_handler(commands=['random_workout'])
# def start(message):
#     bot.send_message(message.from_user.id, 'Ну че будем тренить? (иногда...)')
#     for i in range(5):
#         time.sleep(1)
#         bot.send_message(message.from_user.id, random_workout())


@bot.message_handler(content_types=["text"])
def parse_text(message):
    search_workout(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=1)
