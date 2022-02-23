# -*- coding: utf-8 -*-
import sqlite3
import telebot
import cfg
import shelve
import psutil

bot = telebot.TeleBot(cfg.token)
where_can_find = ["forum", "advertising", "friends"]

#СЛИТО В ТГ КАНАЛАХ @END_SOFTWARE AND @END_RAID
def send(chat_id, text, reply_markup):
    try:
        if reply_markup == '':
            res = bot.send_message(chat_id, text, parse_mode="html", disable_web_page_preview=True)
        else:
            res = bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode="html", disable_web_page_preview=True)
        with open('Temp/' + str(chat_id) + '_message_for_delete.txt', 'w', encoding='utf-8') as f:
            f.write(str(res.id))
        return res.id
    except Exception as e:
        pass


def dell_mess(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        pass


def shelve_add(message_id, id_bd):
    try:
        with shelve.open('data/sost.bd') as bd:
            bd[str(message_id)] = id_bd
    except:
        pass


def shelve_clear(message_id):
    try:
        with shelve.open('data/sost.bd') as bd:
            del bd[str(message_id)]
    except:
        pass


def get_sost(chat_id):
    try:
        with shelve.open('data/sost.bd') as bd:
            if str(chat_id) in bd:
                return True
    except:
        pass


def add_balance(chat_id, balance_2):
    try:
        conn = sqlite3.connect("users.db")
        c = conn.cursor()
        id_user = 0
        c.execute("SELECT id_user, balance_user FROM balances WHERE id_user = '" + str(chat_id) + "';")
        for id_user, balance_user, in c.fetchall():
            pass
        if id_user == 0 and balance_2 > 0:
            c.execute("INSERT INTO balances VALUES(?,?)", (chat_id, balance_2))
            conn.commit()
        else:
            balance_new = float(balance_user)+float(balance_2)
            if balance_new < 0 :
                status = 'bad'
            else:
                status = 'good'
                c.execute("UPDATE balances SET balance_user = '" + str(balance_new) + "' WHERE id_user = '" + str(chat_id) + "';")
                conn.commit()
    except:
        status = 'bad'
    conn.close()
    return status


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()
