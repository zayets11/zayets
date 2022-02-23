# -*- coding: UTF-8 -*-
from telethon.sync import TelegramClient
from telethon import functions
from time import sleep
from sys import argv
import re

script, code, _id = argv


def send(code, _id):
    print(code)
    client = TelegramClient('btc', api_id, "api_hash")
    client.start()
    client(functions.messages.StartBotRequest(bot='BTC_CHANGE_BOT',peer='BTC_CHANGE_BOT',start_param=str(code)))
    sleep(3)
    a = client.get_messages("BTC_CHANGE_BOT")
    text = a[0].message
    if "Упс, кажется" in text:
        with open(f'Temp/{_id}_check_btc.txt', "w", encoding="utf-8") as w:
            w.write("Неверный код")
        return
    if "Вы получили" in text:
        m = re.search(r'\((.+)\)', text)
        with open(f'Temp/{_id}_check_btc.txt', "w", encoding="utf-8") as w:
            w.write(str(m.group(1)))
        return



send(code, _id)
