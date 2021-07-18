import telebot
from my_class import AdAstra
import os
import requests

with open('BOT_TOKEN.txt') as tok:
    bot = telebot.TeleBot(tok.read())

# Global variables


location = ''
month = ''
time = '22:00:00'


# Dialog with the bot

def light_pol(id, class_object):
    bot.send_message(id, "Light pollution map (your location in the center):")
    bot.send_photo(id, open('image1.png', 'rb'))
    os.remove('image1.png')
    bot.send_message(id, 'SQM: ' + class_object.av['light_pol'][0] + '\n' +
                     'NELM: ' + class_object.av['light_pol'][1])


@bot.message_handler(content_types=['text'])
def start(user_message):
    if user_message.text == 'start':
        bot.send_message(user_message.from_user.id,
                         'Type your city in format "city, country" or decimal'
                         ' geographic coordinates of your location in format'
                         ' "latitude, longitude" (preferable).'
                         ' Type "examples" to get examples.')
        bot.register_next_step_handler(user_message, set_location)
    else:
        bot.send_message(user_message.from_user.id, 'For activating'
                                                    ' type "start".')


def set_location(user_message):
    if user_message.text == 'examples':
        bot.send_message(user_message.from_user.id,
                         '''City format: London, UK
                            Coordinates format: 51.509865, 0
                         ''')
        bot.register_next_step_handler(user_message, set_location)
    else:
        global location
        location = user_message.text
        bot.send_message(user_message.from_user.id, 'Type the number of the'
                                                    ' month in which you plan '
                                                    'to conduct observations:')
        bot.register_next_step_handler(user_message, set_month)


def set_month(user_message):
    global month
    month = user_message.text
    bot.send_message(user_message.from_user.id, 'Type the time in which'
                                                ' you plan to conduct'
                                                ' observations '
                                                '(default - 22:00:00, if it is'
                                                ' ok type "default"):')
    bot.register_next_step_handler(user_message, set_time)


def set_time(user_message):
    if user_message.text == 'default':
        pass
    else:
        global time
        time = user_message.text
    result(user_message)


# Generating answer

def result(user_message):
    var = AdAstra(location, month, time)
    results = var()
    # This dict we get when exception was thrown
    if results == {'0': '0'}:
        bot.send_message(user_message.from_user.id, 'Wrong input.')
    # Not empty dict we get when data was found successfully
    elif results:
        message = 'Address: ' + results['address']+'\n\n' + \
                  'Timezone: ' + results['timezone']+'\n\n' + \
                  'Average humidity: ' + results['hum']+'%\n\n' + \
                  'Average visibility: ' + results['vis'] + 'km\n\n' + \
                  'Average cloudcover: ' + results['hum'] + '%'

        bot.send_message(user_message.from_user.id, message)
        light_pol(user_message.from_user.id, var)

    # Empty dict we get when data wasn't found by api
    # but all the typed data was correct
    else:
        bot.send_message(user_message.from_user.id, 'It seems nobody lives'
                                                    ' here or you typed wrong'
                                                    ' data. No weather data.'
                                                    ' But do not worry, here'
                                                    ' is Chuck Norris fact'
                                                    ' right for you!')
        bot.send_message(user_message.from_user.id, requests.get(
            'https://api.chucknorris.io/jokes/random').json()['value'])
        light_pol(user_message.from_user.id, var)


bot.polling(none_stop=True)
