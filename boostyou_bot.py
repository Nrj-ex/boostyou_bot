import telebot
import time
from bot_function import search_workout
from bot_function import get_my_stat
from bot_function import get_all_stats
import config

# @Boostyou_bot
bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
    keyboard.row('/help', '/about')
    bot.send_message(message.chat.id, 'Список доступных комманд: /help', reply_markup=keyboard)


@bot.message_handler(commands=['about'])
def start(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    url_button = telebot.types.InlineKeyboardButton(text='link to the project',
                                                    url='https://github.com/Nrj-ex/boostyou_bot')
    keyboard.add(url_button)
    bot.send_message(message.chat.id, 'Project information and suggestions on github',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start(message):
    commands = ['/my_stats', '/my_stats_week', '/all_stats',
                '/all_stats_week', '/kick_me' '/about']
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
    keyboard = telebot.types.InlineKeyboardMarkup()
    callback_button_30min = telebot.types.InlineKeyboardButton(text='30 мин', callback_data='30')
    callback_button_60min = telebot.types.InlineKeyboardButton(text='60 мин', callback_data='60')
    callback_button_90min = telebot.types.InlineKeyboardButton(text='90 мин', callback_data='90')
    keyboard.add(callback_button_30min, callback_button_60min,
                 callback_button_90min)
    bot.send_message(message.chat.id, 'Через сколько вас пнуть?', reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def parse_text(message):
    search_workout(message)



@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == '30' or call.data == '60' or call.data == '90':
            timeout = call.data
            if timeout.isdigit() and int(timeout) < 200:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id
                                      , text=f'Я запомнил, напишу через {timeout} минут ;)')
                keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
                keyboard.row('/kick_me', 'Спасибо хватит!')
                time.sleep(int(timeout) * 60)
                bot.send_message(call.message.chat.id, f'Прошло {timeout} минут Встань, '
                                                       f'разомнись, сделай несколько упражнений! ;)',
                                 reply_markup=keyboard)



if __name__ == '__main__':
    bot.polling(none_stop=True, interval=5)
