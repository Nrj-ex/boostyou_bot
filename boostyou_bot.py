import telebot
import time
from bot_function import search_workout
from bot_function import get_my_stat
from bot_function import get_all_stats
import config

# @Boostyou_bot
bot = telebot.TeleBot(config.TOKEN)
client_status = {}

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('/help', '/about')
    bot.send_message(message.chat.id, 'Список доступных комманд: /help', reply_markup=keyboard)


@bot.message_handler(commands=['about'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('/help')
    bot.send_message(message.chat.id, 'Ссылка на репозиторий проекта '
                                      'https://github.com/Nrj-ex/boostyou_bot', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start(message):
    commands = ['/my_stats', '/my_stats_week', '/all_stats',
                '/all_stats_week', '/about']
    #keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    #keyboard.row(*commands)
    bot.send_message(message.chat.id, f'Умею запоминать упражнения которые'
                                      f' вы выполнили и выводить статистику\nСписок доcтупных '
                                      f'комманд:\n'+'\n'.join(commands))




@bot.message_handler(commands=['my_stats'])
def show_my_stats(message):
    # показать мою статистику
    user = message.from_user.username
    stat = get_my_stat(user)
    text_message = user + ':\n'
    for workout in stat:
        text_message += f'{workout}: {stat[workout]}\n'
    bot.send_message(message.chat.id, text_message)


@bot.message_handler(commands=['my_stats_week'])
def show_my_stats(message):
    # показать мою статистику
    user = message.from_user.username
    stat = get_my_stat(user, time_slot=604800)
    text_message = user + ' ' + 'for week' + ':\n'
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
    all_stats = get_all_stats(time_slot=604800)
    text_message = ''
    for name in all_stats:
        text_message += name + ' ' + 'for week' +':\n'
        for workout in all_stats[name]:
            text_message += f'{workout}: {all_stats[name][workout]}\n'
    bot.send_message(message.chat.id, text_message)


@bot.message_handler(commands=['kick_me'])
def kick_me(message):
    client_id = message.from_user.id
    client_status[client_id] = 'wait_for_data'
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('30', '60', '90')
    bot.send_message(client_id, 'Через сколько минут вас пнуть? (не более 200)',
                     reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def parse_text(message):
    search_workout(message)
    client_id = message.from_user.id
    if client_id in client_status and client_status[client_id] == 'wait_for_data':
        timeout = message.text
        if timeout.isdigit() and int(timeout) < 200:
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row('/kick_me', 'Спасибо хватит!')
            time.sleep(int(timeout ))
            bot.send_message(client_id, 'Встань, разомнись, следи за осанкой! ;)',
                             reply_markup=keyboard)
        else:
            keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
            keyboard.row('/kick_me', 'Спасибо хватит!')
            bot.send_message(client_id, 'Ты тупой? написано же число от 1 до 200\n'
                                              '*ворчит* безмозглый кусок мяса...',
                             reply_markup=keyboard)
        del client_status[client_id]





if __name__ == '__main__':
    bot.polling(none_stop=True, interval=1)
