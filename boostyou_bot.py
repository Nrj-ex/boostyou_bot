import telebot
from bot_function import search_workout
from bot_function import get_my_stat
from bot_function import get_all_stats
from bot_function import get_my_stat_week
from bot_function import get_all_stats_week
import config

# @Boostyou_bot
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Список доступных комманд /help')

@bot.message_handler(commands=['about'])
def start(message):
    bot.send_message(message.chat.id, 'Ссылка на репозиторий проекта https://github.com/Nrj-ex/boostyou_bot')

@bot.message_handler(commands=['help'])
def start(message):
    commands = '/my_stats\n/my_stats_week\n/all_stats\n/all_stats_week\n/about'
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


@bot.message_handler(commands=['my_stats_week'])
def show_my_stats(message):
    # показать мою статистику
    stat = get_my_stat_week(message.from_user.username)
    text_message = message.from_user.username + ' ' + 'for week' +':\n'
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


@bot.message_handler(commands=['all_stats_week'])
def show_all_stats(message):
    all_stats = get_all_stats_week()
    text_message = ''
    for name in all_stats:
        text_message += name + ' ' + 'for week' +':\n'
        for workout in all_stats[name]:
            text_message += f'{workout}: {all_stats[name][workout]}\n'
    bot.send_message(message.chat.id, text_message)


@bot.message_handler(content_types=["text"])
def parse_text(message):
    search_workout(message)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=1)
