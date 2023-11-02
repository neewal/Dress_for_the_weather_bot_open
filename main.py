import os
import schedule
import telebot
from time import sleep
import time
from threading import Thread
import requests
import json
from bs4 import BeautifulSoup
import random
import logging

good = ['хорошего', 'отличного', 'прекрастного', 'вдохновляющего', 'незабываемого', 'прелестного', 'доброго', 'удачного']

#Логирование
logging.basicConfig(level=logging.INFO, force=False, filename="main.log",
                    format="%(asctime)s %(levelname)s %(message)s")

API_TOKEN = "API_Token_BOT"

bot = telebot.TeleBot(API_TOKEN)

chat_id = 'chat_id'

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
здравствуйте. 
я ваш бот персональный помощник, что я умею:
  • к сожелению ничего кроме показания погоды(
""")
    logging.info('Подключился новый пользователь!')

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)

def morning():
    #Weather
    city = 'Ваш город или район'
    link = f"https://www.google.com/search?q=погода+в+{city}"

    headers = {
        "User-Agent" : "Ваш User_Agent"
    }
    responce = requests.get(link, headers=headers)
    print(responce)

    f = '<Response [200]>'

    if str(responce) == str(f):
        logging.info('Подключение прошло успешно ' + '(' + str(responce) + ')')
    else:
        logging.error('Поключение прошло неудачно, не удалось подключится!' + '(' + str(responce) + ')', exc_info=True)


    soup = BeautifulSoup(responce.text, "html.parser")

    # Парсим погоду
    temperature = soup.select("#wob_tm")[0].getText()
    title = soup.select("#wob_dc")[0].getText()
    humidity = soup.select("#wob_hm")[0].getText()
    time = soup.select("#wob_dts")[0].getText()
    wind = soup.select("#wob_ws")[0].getText()

    # Выводим на экран
    print(time, "\n",title)
    print(title)
    print(f"Температура: {temperature}C")
    print(f"Влажность: {humidity}")
    print(f"Ветер: {wind}")
    bot.send_message(chat_id, f"""
доброе утро.
погода на утро в ...:
""")
    bot.send_message(chat_id, f"""\
дата и время: {time}
состояние: {title}
температура: {temperature}С
влажность: {humidity}
ветер: {wind}
""")
    bot.send_message(chat_id, f'Желаю вам {random.choice(good)} дня!')
    print('Погода отправилась')
    logging.info('Погода отправилась')

if __name__ == "__main__":
    schedule.every().day.at("07:00").do(morning)
    Thread(target=schedule_checker).start()


bot.infinity_polling()
bot.polling(none_stop=True)
