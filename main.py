# -*- coding: utf-8 -*-

import telebot
import sqlite3
import cfg
import db
import keys as key
import datetime
import shelve
import subprocess
from time import sleep
from telebot import types
import random
import requests
import time

bot = telebot.TeleBot(cfg.token)

@bot.message_handler()
def message_handler(message):
    try:
        if message.chat.type == "private":
            if message.text == "/start":
                conn = sqlite3.connect("users.db")
                c = conn.cursor()
                id_user = ""
                c.execute("SELECT id_user FROM users WHERE id_user = '" + str(message.chat.id) + "';")
                for id_user, in c.fetchall():
                    pass
                if id_user == "":
                    dateFormatter = '%H/%M/%d/%m/%Y'
                    time_now = datetime.datetime.now().strftime(dateFormatter)
                    c.execute("INSERT INTO users VALUES(?,?,?,?,?)",
                              (message.chat.id, message.chat.username, '0', 'None', time_now))
                    conn.commit()
                    db.dell_mess(message.chat.id, message.message_id)
                    db.send(message.chat.id, "⚡️", key.main())
                    db.send(message.chat.id, cfg.rules, key.agree())
                else:
                    db.dell_mess(message.chat.id, message.message_id)
                    db.send(message.chat.id, "⚡️", key.main())
                    db.send(message.chat.id, "<b>👾 С возвращением!</b>", "")
                conn.close()
            elif "/start" in message.text:
                who_ref = message.text[7:]
                conn = sqlite3.connect("users.db")
                c = conn.cursor()
                id_user = ""
                c.execute("SELECT id_user FROM users WHERE id_user = '" + str(message.chat.id) + "';")
                for id_user, in c.fetchall():
                    pass
                if id_user == "":
                    dateFormatter = '%H/%M/%d/%m/%Y'
                    time_now = datetime.datetime.now().strftime(dateFormatter)
                    c.execute("INSERT INTO users VALUES(?,?,?,?,?)",
                              (message.chat.id, message.chat.username, '0', who_ref, time_now))
                    conn.commit()
                    bot.send_message(who_ref, "<b>🦋 Вы получили 0.5 ч. за приглашённого пользователя!</b>",
                                     reply_markup=key.take_sub(0.5), parse_mode="html")
                    db.dell_mess(message.chat.id, message.message_id)
                    db.send(message.chat.id, "⚡️", key.main())
                    db.send(message.chat.id, cfg.rules, key.agree())
                else:
                    db.dell_mess(message.chat.id, message.message_id)
                    db.send(message.chat.id, "⚡️", key.main())
                    db.send(message.chat.id, "<b>👾 С возвращением!</b>", "")
                conn.close()
            try:
                status = bot.get_chat_member(chat_id=cfg.chat_news, user_id=message.chat.id).status
                st = 1
            except Exception as e:
                st = 0
            if st == 0 or status == 'left':
                db.send(message.chat.id, "❗️Для работы с парсером, вам нужно подписаться на канал с новостями!#СЛИТО В ТГ КАНАЛАХ @END_SOFTWARE AND @END_RAID\n\nhttps://t.me/"+cfg.name_news, key.check_sub())
            else:
                conn = sqlite3.connect("users.db")
                c = conn.cursor()
                status = ''
                c.execute("SELECT ban_status FROM users WHERE id_user = '" + str(message.chat.id) + "';")
                for ban_status, in c.fetchall():
                    status = ban_status
                conn.close()
                if status == 1:
                    db.dell_mess(message.chat.id, message.message_id)
                    db.send(message.chat.id, "<b>⚠️ Вы заблокированы</b>\n\nОбратитесь к модерации..", "")
                else:
                    if "/pr" in message.text:
                        db.dell_mess(message.chat.id, message.message_id)
                        promo_text = message.text[3:]
                        conn = sqlite3.connect("promo.db")
                        c = conn.cursor()
                        promo = ''
                        c.execute("SELECT promo FROM promo_taked WHERE chat_id = '" + str(message.chat.id) + "';")
                        for promo, in c.fetchall():
                            pass
                        if promo == promo_text:
                            db.send(message.chat.id, '<b>⚠️ Вы уже активировали этот промокод!</b>', key.close())
                        else:
                            promo = ''
                            c.execute("SELECT promo, count_give, gived, count_hours FROM promo WHERE promo = '" + str(promo_text) + "';")
                            for promo, count_give, gived, count_hours, in c.fetchall():
                                pass
                            if promo == '':
                                db.send(message.chat.id, '<b>⚠️ Такого промокода не существует!</b>', key.close())
                            else:
                                if int(count_give) == int(gived):
                                    db.send(message.chat.id, '<b>😔 Вы не успели!</b>', key.close())
                                else:
                                    new_gived = int(gived) + 1
                                    c.execute("UPDATE promo SET gived = '" + str(new_gived) + "' WHERE promo = '" + str(promo) + "';")
                                    conn.commit()
                                    bot.send_message(message.chat.id, '<b>🎉 Поздравляем. Вы получили '+str(count_hours)+' ч. подписки!</b>\n\nВыбирайте сервис:', reply_markup=key.take_sub(count_hours), parse_mode="html")
                                    c.execute("INSERT INTO promo_taked VALUES(?,?)", (message.chat.id, promo))
                                    conn.commit()
                        conn.close()
                    elif message.text == "💼 Профиль":
                        try:
                            with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                message_id = f.read()
                            db.dell_mess(message.chat.id, message_id)
                        except:
                            pass
                        db.dell_mess(message.chat.id, message.message_id)
                        conn = sqlite3.connect("users.db")
                        c = conn.cursor()
                        count_ref = 0
                        c.execute("SELECT id_user FROM users WHERE who_ref = '" + str(message.chat.id) + "';")
                        for id_user, in c.fetchall():
                            count_ref+= 1
                        balance_user = 0
                        c.execute("SELECT balance_user FROM balances WHERE id_user = '" + str(message.chat.id) + "';")
                        for balance_user, in c.fetchall():
                            pass
                        conn.close()
                        db.send(message.chat.id, "💰 Ваш баланс: <b>"+str(balance_user)+" руб.</b>\n\n🤖 Количество рефералов: <b>" + str(count_ref) + "</b>", key.prof())
                    elif message.text == "👾 Помощь":
                        try:
                            with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                message_id = f.read()
                            db.dell_mess(message.chat.id, message_id)
                        except:
                            pass
                        db.dell_mess(message.chat.id, message.message_id)
                        db.send(message.chat.id, "<b>📝 По всем вопросам: @vi_coder</b>", "")
                    elif message.text == "☠️ Сервисы":
                        try:
                            with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                message_id = f.read()
                            db.dell_mess(message.chat.id, message_id)
                        except:
                            pass
                        db.dell_mess(message.chat.id, message.message_id)
                        db.send(message.chat.id, "☠️ Выбирайте сервис:", key.services())
                    elif message.text == "⚙️ Настройки":
                        try:
                            with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                message_id = f.read()
                            db.dell_mess(message.chat.id, message_id)
                        except:
                            pass
                        db.dell_mess(message.chat.id, message.message_id)
                        conn = sqlite3.connect("sub.db")
                        c = conn.cursor()
                        keys = types.InlineKeyboardMarkup()
                        count_services = 0
                        c.execute("SELECT id, time_start,duration,status,service FROM subs WHERE id = '" + str(message.chat.id) + "';")
                        for id, time_start, duration, status, service, in c.fetchall():
                            if status == 0:
                                if service == '🇵🇹 OLX.PT':
                                    service_chiper = 'olxpt'
                                elif service == '🇵🇱 OLX.PL':
                                    service_chiper = 'olxpl'
                                elif service == '🇷🇴 OLX.RO':
                                    service_chiper = 'olxro'
                                elif service == '🇰🇿 OLX.kz':
                                    service_chiper = 'olxkz'
                                elif service == '🇧🇬 OLX.bg':
                                    service_chiper = 'olxbg'
                                elif service == '🇺🇦 OLX.ua':
                                    service_chiper = 'olxua'
                                elif service == '🇮🇹 SUBITO.IT':
                                    service_chiper = 'subitoit'
                                elif service == '🇲🇰 Pazar3.mk':
                                    service_chiper = 'pazar3mk'
                                elif service == '🇨🇿 Sbazar.cz':
                                    service_chiper = 'sbazarcz'
                                keys_1 = types.InlineKeyboardButton(text=service, callback_data="settings_"+str(service_chiper))
                                keys.add(keys_1)
                                count_services += 1
                        key_last = types.InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
                        keys.add(key_last)
                        conn.close()
                        if count_services != 0:
                            db.send(message.chat.id, "<b>⚙️Выберите сервис для изменения фильтров:</b>", keys)
                        else:
                            db.send(message.chat.id, "<b>❗️Для использования этой функции - нужна подписка!</b>", key.close())
                    elif db.get_sost(message.chat.id) is True:
                        with shelve.open('data/sost.bd') as bd:
                            sost_num = bd[str(message.chat.id)]
                        if sost_num == 1:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                    message_id = f.read()
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            code = message.text.replace('https://telegram.me/BTC_CHANGE_BOT?start=', '')
                            message_id = bot.send_message(message.chat.id, f"<b>💰 Ваш чек на обработке!</b>\n\nОжидайте..", parse_mode="html")
                            message_id = message_id.id
                            _id = message.chat.id
                            try:
                                subprocess.Popen(['python', 'banker.py', str(code), str(_id)])
                            except Exception as e:
                                return
                            sleep(10)
                            db.dell_mess(message.chat.id, message_id)
                            try:
                                with open('Temp/'+str(message.chat.id)+'_check_btc.txt', "r") as r:
                                    sum = r.read()
                                    if "RUB" in sum:
                                        sum = sum.replace(" RUB", "")
                                    else:
                                        bot.send_message(message.chat.id, "❌ Произошла ошибка")
                                        return
                                if sum == "Неверный код":
                                    bot.send_message(message.chat.id, "❌ Произошла ошибка")
                                elif sum == "":
                                    bot.send_message(message.chat.id, "❌ Произошла ошибка")
                                else:
                                    sum = round(float(sum), 1)
                                    conn = sqlite3.connect("users.db")
                                    c = conn.cursor()
                                    who_ref = 'None'
                                    c.execute("SELECT who_ref FROM users WHERE id_user = '" + str(message.chat.id) + "';")
                                    for who_ref, in c.fetchall():
                                        pass
                                    db.send(message.chat.id, "<b>✅ Баланс пополнен</b>\n\nСумма: <b>"+str(sum) +" руб.</b>", "")
                                    db.add_balance(message.chat.id, sum)
                                    if who_ref != 'None':
                                        sum_2 = round((float(sum) * 0.1), 1)
                                        db.send(who_ref, "<b>✅ Ваш реферал пополнил баланс!</b>\n\nВаша доля: <b>"+str(sum_2) +" руб.</b>", "")
                                        db.add_balance(who_ref, sum_2)
                                with open(f'Temp/{message.chat.id}_check_btc.txt', "w", encoding="utf-8") as w:
                                    w.write("")
                            except:
                                db.send(message.chat.id, '❌ Неверный чек!', '')
                            conn.close()
                            db.shelve_clear(message.chat.id)
                        elif sost_num == 2:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                    message_id = f.read()
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_url_ad.txt', 'w', encoding='utf-8') as f:
                                f.write(str(message.text))
                            db.send(message.chat.id, "<b>🤖 Введите количество объявлений для парса(max - 50):</b>", key.cancel())
                            db.shelve_add(message.chat.id, 3)
                        elif sost_num == 3:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                    message_id = f.read()
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_url_ad.txt', encoding='utf-8') as f:
                                url_check = f.read()
                            try:
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            try:
                                int(message.text)
                                if int(message.text) > 50 or int(message.text) <= 0:
                                    db.send(message.chat.id,'<b>❌ Неверный ввод!</b>\n\nВведите заново количество объявлений для парса(max - 50):',key.cancel())
                                else:
                                    conn = sqlite3.connect("parser.db")
                                    c = conn.cursor()
                                    status = 1
                                    c.execute("SELECT id_user, status FROM parser WHERE id_user = '" + str(message.chat.id) + "';")
                                    for id_user, status, in c.fetchall():
                                        if status == 0:
                                            break
                                    if status == 1:
                                        dateFormatter = '%H/%M/%d/%m/%Y'
                                        time_now = datetime.datetime.now().strftime(dateFormatter)
                                        c.execute("INSERT INTO parser VALUES(?,?,?,?)", (message.chat.id, url_check, time_now, '0'))
                                        conn.commit()
                                        conn = sqlite3.connect("options.db")
                                        c = conn.cursor()
                                        on_off_message = 'OFF'
                                        message_send = 'Hello'
                                        max_ads = '10'
                                        min_year = '2000'
                                        with open('Temp/' + str(message.chat.id) + '_service_parser_olx.txt', encoding='utf-8') as f:
                                            service_chiper = f.read()
                                        c.execute("SELECT id_user, on_off_message, message_send, max_ads, min_year FROM " + str(service_chiper) + " WHERE id_user = '" + str(message.chat.id) + "';")
                                        for id_user, on_off_message, message_send, max_ads, min_year, in c.fetchall():
                                            pass
                                        with open('Temp/' + str(message.chat.id) + '_url_ad.txt', encoding='utf-8') as f:
                                            link = f.read()
                                        x = random.randint(0, 10000000)
                                        try:
                                            proc = subprocess.Popen(['python', 'olx.py', str(link), str(max_ads), str(message.text), str(min_year), str(on_off_message), str(message_send), str(message.chat.id), str(service_chiper[-2:]), str(x)])
                                        except Exception as e:
                                            db.send(message.chat.id,'<b>❌ Произошла ошибка!</b>', key.close())
                                            return
                                        keys = types.InlineKeyboardMarkup()
                                        key_1 = types.InlineKeyboardButton(text="❌ Остановить парсер", callback_data="stop_parser_"+str(proc.pid))
                                        keys.add(key_1)
                                        bot.send_message(message.chat.id, '<b>🦋 Парсер успешно запущен!</b>', parse_mode="html", reply_markup=keys)
                                    else:
                                        db.send(message.chat.id, '<b>❌ Нельзя запускать больше 1 парса!</b>', key.close())
                                    conn.close()
                                    db.shelve_clear(message.chat.id)
                            except Exception as e:
                                db.send(message.chat.id, '<b>❌ Неверный ввод!</b>\n\nВведите заново количество объявлений для парса:', key.cancel())
                        elif sost_num == 4:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                    message_id = f.read()
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_change_message.txt', encoding='utf-8') as f:
                                service_chiper = f.read()
                            try:
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            conn = sqlite3.connect("options.db")
                            c = conn.cursor()
                            c.execute('UPDATE ' + str(service_chiper) + ' SET  message_send = "' + str(message.text) + '" WHERE id_user = "' + str(message.chat.id) + '";')
                            conn.commit()
                            conn.close()
                            db.send(message.chat.id, "✅ Успешно!", "")
                        elif sost_num == 5:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                    message_id = f.read()
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_change_year.txt', encoding='utf-8') as f:
                                service_chiper = f.read()
                            try:
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            conn = sqlite3.connect("options.db")
                            c = conn.cursor()
                            c.execute("UPDATE " + str(service_chiper) + " SET  min_year = '" + str(message.text) + "' WHERE id_user = '" + str(message.chat.id) + "';")
                            conn.commit()
                            conn.close()
                            db.send(message.chat.id, "✅ Успешно!", "")
                        elif sost_num == 6:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                    message_id = f.read()
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_change_ads.txt', encoding='utf-8') as f:
                                service_chiper = f.read()
                            try:
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            conn = sqlite3.connect("options.db")
                            c = conn.cursor()
                            c.execute("UPDATE " + str(service_chiper) + " SET  max_ads = '" + str(message.text) + "' WHERE id_user = '" + str(message.chat.id) + "';")
                            conn.commit()
                            conn.close()
                            db.send(message.chat.id, "✅ Успешно!", "")
                        elif sost_num == 7:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt',encoding='utf-8') as f:
                                    message_id = f.read()
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_url_ad.txt', 'w', encoding='utf-8') as f:
                                f.write(str(message.text))
                            db.send(message.chat.id, "<b>🤖 Введите количество объявлений для парса(max - 50):</b>",key.cancel())
                            db.shelve_add(message.chat.id, 8)
                        elif sost_num == 8:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                    message_id = f.read()
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_url_ad.txt', encoding='utf-8') as f:
                                url_check = f.read()
                            try:
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            try:
                                int(message.text)
                                if int(message.text) > 50 or int(message.text) <= 0:
                                    db.send(message.chat.id,'<b>❌ Неверный ввод!</b>\n\nВведите заново количество объявлений для парса(max - 50):',key.cancel())
                                else:
                                    conn = sqlite3.connect("parser.db")
                                    c = conn.cursor()
                                    status = 1
                                    c.execute("SELECT id_user, status FROM parser WHERE id_user = '" + str(message.chat.id) + "';")
                                    for id_user, status, in c.fetchall():
                                        if status == 0:
                                            break
                                    if status == 1:
                                        dateFormatter = '%H/%M/%d/%m/%Y'
                                        time_now = datetime.datetime.now().strftime(dateFormatter)
                                        c.execute("INSERT INTO parser VALUES(?,?,?,?)",(message.chat.id, url_check, time_now, '0'))
                                        conn.commit()
                                        conn = sqlite3.connect("options.db")
                                        c = conn.cursor()
                                        on_off_message = 'OFF'
                                        message_send = 'Hello'
                                        max_ads_online = '10'
                                        max_ads_offline = '50'
                                        min_year = '2015'
                                        c.execute("SELECT id_user, on_off_message, message_send, max_ads_online, max_ads_offline, min_year FROM subitoit WHERE id_user = '" + str(message.chat.id) + "';")
                                        for id_user, on_off_message, message_send, max_ads_online, max_ads_offline, min_year, in c.fetchall():
                                            pass
                                        with open('Temp/' + str(message.chat.id) + '_url_ad.txt', encoding='utf-8') as f:
                                            link = f.read()
                                        x = random.randint(0, 10000000)
                                        try:
                                            proc = subprocess.Popen(['python', 'subito.py', str(link), str(max_ads_online), str(max_ads_offline), str(message.text), str(min_year), str(on_off_message), str(message_send), str(message.chat.id), str(x)])
                                        except:
                                            db.send(message.chat.id, '<b>❌ Произошла ошибка!</b>', key.close())
                                            return
                                        keys = types.InlineKeyboardMarkup()
                                        key_1 = types.InlineKeyboardButton(text="❌ Остановить парсер",
                                                                           callback_data="stop_parser_" + str(proc.pid))
                                        keys.add(key_1)
                                        bot.send_message(message.chat.id, '<b>🦋 Парсер успешно запущен!</b>',
                                                         parse_mode="html", reply_markup=keys)
                                    else:
                                        db.send(message.chat.id, '<b>❌ Нельзя запускать больше 1 парса!</b>',key.close())
                                    conn.close()
                                    db.shelve_clear(message.chat.id)
                            except Exception as e:
                                db.send(message.chat.id,
                                        '<b>❌ Неверный ввод!</b>\n\nВведите заново количество объявлений для парса:',
                                        key.cancel())
                        elif sost_num == 9:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                    message_id = f.read()
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_change_ads.txt', encoding='utf-8') as f:
                                service_chiper = f.read()
                            try:
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            conn = sqlite3.connect("options.db")
                            c = conn.cursor()
                            c.execute("UPDATE " + str(service_chiper) + " SET  max_ads_online = '" + str(message.text) + "' WHERE id_user = '" + str(message.chat.id) + "';")
                            conn.commit()
                            conn.close()
                            db.send(message.chat.id, "✅ Успешно!", "")
                        elif sost_num == 10:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                    message_id = f.read()
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_change_ads.txt', encoding='utf-8') as f:
                                service_chiper = f.read()
                            try:
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            conn = sqlite3.connect("options.db")
                            c = conn.cursor()
                            c.execute("UPDATE " + str(service_chiper) + " SET  max_ads_offline = '" + str(message.text) + "' WHERE id_user = '" + str(message.chat.id) + "';")
                            conn.commit()
                            conn.close()
                            db.send(message.chat.id, "✅ Успешно!", "")
                        elif sost_num == 13:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                    message_id = f.read()
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_change_ads.txt', encoding='utf-8') as f:
                                service_chiper = f.read()
                            try:
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            conn = sqlite3.connect("options.db")
                            c = conn.cursor()
                            c.execute("UPDATE " + str(service_chiper) + " SET  max_likes = '" + str(message.text) + "' WHERE id_user = '" + str(message.chat.id) + "';")
                            conn.commit()
                            conn.close()
                            db.send(message.chat.id, "✅ Успешно!", "")
                        elif sost_num == 14:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                    message_id = f.read()
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_change_ads.txt', encoding='utf-8') as f:
                                service_chiper = f.read()
                            try:
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            conn = sqlite3.connect("options.db")
                            c = conn.cursor()
                            c.execute("UPDATE " + str(service_chiper) + " SET  max_dislikes = '" + str(message.text) + "' WHERE id_user = '" + str(message.chat.id) + "';")
                            conn.commit()
                            conn.close()
                            db.send(message.chat.id, "✅ Успешно!", "")
                        elif sost_num == 15:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt',encoding='utf-8') as f:
                                    message_id = f.read()
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_url_ad.txt', 'w', encoding='utf-8') as f:
                                f.write(str(message.text))
                            db.send(message.chat.id, "<b>🤖 Введите количество объявлений для парса(max - 50):</b>",key.cancel())
                            db.shelve_add(message.chat.id, 16)
                        elif sost_num == 16:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                    message_id = f.read()
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_url_ad.txt', encoding='utf-8') as f:
                                url_check = f.read()
                            try:
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            try:
                                int(message.text)
                                if int(message.text) > 50 or int(message.text) <= 0:
                                    db.send(message.chat.id,'<b>❌ Неверный ввод!</b>\n\nВведите заново количество объявлений для парса(max - 50):',key.cancel())
                                else:
                                    conn = sqlite3.connect("parser.db")
                                    c = conn.cursor()
                                    status = 1
                                    c.execute("SELECT id_user, status FROM parser WHERE id_user = '" + str(message.chat.id) + "';")
                                    for id_user, status, in c.fetchall():
                                        if status == 0:
                                            break
                                    if status == 1:
                                        dateFormatter = '%H/%M/%d/%m/%Y'
                                        time_now = datetime.datetime.now().strftime(dateFormatter)
                                        c.execute("INSERT INTO parser VALUES(?,?,?,?)", (message.chat.id, url_check, time_now, '0'))
                                        conn.commit()
                                        conn = sqlite3.connect("options.db")
                                        c = conn.cursor()
                                        on_off_message = 'OFF'
                                        message_send = 'Hello'
                                        c.execute("SELECT id_user, on_off_message, message_send FROM pazar3mk WHERE id_user = '" + str(message.chat.id) + "';")
                                        for id_user, on_off_message, message_send, in c.fetchall():
                                            pass
                                        with open('Temp/' + str(message.chat.id) + '_url_ad.txt', encoding='utf-8') as f:
                                            link = f.read()
                                        x = random.randint(0, 10000000)
                                        try:
                                            proc = subprocess.Popen(['python', 'pazar3.py', str(link), str(message.text), str(on_off_message), str(message_send), str(message.chat.id), str(x)])
                                        except:
                                            db.send(message.chat.id, '<b>❌ Произошла ошибка!</b>', key.close())
                                            return
                                        keys = types.InlineKeyboardMarkup()
                                        key_1 = types.InlineKeyboardButton(text="❌ Остановить парсер",
                                                                           callback_data="stop_parser_" + str(proc.pid))
                                        keys.add(key_1)
                                        bot.send_message(message.chat.id, '<b>🦋 Парсер успешно запущен!</b>',
                                                         parse_mode="html", reply_markup=keys)
                                    else:
                                        db.send(message.chat.id, '<b>❌ Нельзя запускать больше 1 парса!</b>',key.close())
                                    conn.close()
                                    db.shelve_clear(message.chat.id)
                            except Exception as e:
                                db.send(message.chat.id,
                                        '<b>❌ Неверный ввод!</b>\n\nВведите заново количество объявлений для парса:',
                                        key.cancel())
                        elif sost_num == 17:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt',encoding='utf-8') as f:
                                    message_id = f.read()
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_url_ad.txt', 'w', encoding='utf-8') as f:
                                f.write(str(message.text))
                            db.send(message.chat.id, "<b>🤖 Введите количество объявлений для парса(max - 50):</b>",key.cancel())
                            db.shelve_add(message.chat.id, 18)
                        elif sost_num == 18:
                            db.dell_mess(message.chat.id, message.message_id)
                            try:
                                with open('Temp/' + str(message.chat.id) + '_message_for_delete.txt', encoding='utf-8') as f:
                                    message_id = f.read()
                            except:
                                pass
                            with open('Temp/' + str(message.chat.id) + '_url_ad.txt', encoding='utf-8') as f:
                                url_check = f.read()
                            try:
                                db.dell_mess(message.chat.id, message_id)
                            except:
                                pass
                            try:
                                int(message.text)
                                if int(message.text) > 50 or int(message.text) <= 0:
                                    db.send(message.chat.id,'<b>❌ Неверный ввод!</b>\n\nВведите заново количество объявлений для парса(max - 50):',key.cancel())
                                else:
                                    conn = sqlite3.connect("parser.db")
                                    c = conn.cursor()
                                    status = 1
                                    c.execute("SELECT id_user, status FROM parser WHERE id_user = '" + str(message.chat.id) + "';")
                                    for id_user, status, in c.fetchall():
                                        if status == 0:
                                            break
                                    if status == 1:
                                        dateFormatter = '%H/%M/%d/%m/%Y'
                                        time_now = datetime.datetime.now().strftime(dateFormatter)
                                        c.execute("INSERT INTO parser VALUES(?,?,?,?)", (message.chat.id, url_check, time_now, '0'))
                                        conn.commit()
                                        conn = sqlite3.connect("options.db")
                                        c = conn.cursor()
                                        on_off_message = 'OFF'
                                        message_send = 'Hello'
                                        max_ads = 100
                                        min_year = 2000
                                        c.execute("SELECT id_user, on_off_message, message_send, max_ads FROM sbazarcz WHERE id_user = '" + str(message.chat.id) + "';")
                                        for id_user, on_off_message, message_send, max_ads, in c.fetchall():
                                            pass
                                        with open('Temp/' + str(message.chat.id) + '_url_ad.txt', encoding='utf-8') as f:
                                            link = f.read()
                                        x = random.randint(0, 10000000)
                                        try:
                                            proc = subprocess.Popen(['python', 'sbazar.py', str(link), str(message.text), str(on_off_message), str(message_send), str(message.chat.id), str(x), str(max_ads), str(min_year)])
                                        except:
                                            db.send(message.chat.id, '<b>❌ Произошла ошибка!</b>', key.close())
                                            return
                                        keys = types.InlineKeyboardMarkup()
                                        key_1 = types.InlineKeyboardButton(text="❌ Остановить парсер",
                                                                           callback_data="stop_parser_" + str(proc.pid))
                                        keys.add(key_1)
                                        bot.send_message(message.chat.id, '<b>🦋 Парсер успешно запущен!</b>',
                                                         parse_mode="html", reply_markup=keys)
                                    else:
                                        db.send(message.chat.id, '<b>❌ Нельзя запускать больше 1 парса!</b>',key.close())
                                    conn.close()
                                    db.shelve_clear(message.chat.id)
                            except Exception as e:
                                db.send(message.chat.id,
                                        '<b>❌ Неверный ввод!</b>\n\nВведите заново количество объявлений для парса:',
                                        key.cancel())
    except Exception as e:
        print(e)
        pass







@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    try:
        try:
            db.shelve_clear(call.message.chat.id)
        except:
            pass
        if call.data == "check_sub":
            try:
                status = bot.get_chat_member(chat_id=cfg.chat_news, user_id=call.message.chat.id).status
                st = 1
            except Exception as e:
                st = 0
            if st != 0 and status != 'left':
                db.dell_mess(call.message.chat.id, call.message.message_id)
                db.send(call.message.chat.id, cfg.rules, key.agree())
            else:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="❌ Вы не подписаны!")
        elif call.data == "agree_start":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            db.send(call.message.chat.id, "<b>👾 Добро пожаловать!#СЛИТО В ТГ КАНАЛАХ @END_SOFTWARE AND @END_RAID</b>", "")
        elif call.data == "ref_prof":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            db.send(call.message.chat.id, "<b>🤖 Реферальная система</b>#СЛИТО В ТГ КАНАЛАХ @END_SOFTWARE AND @END_RAID\n\n▪️При пополнении баланса вашим рефералом - вы получаете <b>10%</b> от пополнения!\n\n▪️За одного реферала вы получата 0.5 ч. подписки на любой сервис!\n\n<a href='https://t.me/SoulParser_bot?start="+str(call.message.chat.id)+"'>Ваша реферальная ссылка</a>", key.back_prof())
        elif call.data == "back_prof":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            count_ref = 0
            c.execute("SELECT id_user FROM users WHERE who_ref = '" + str(call.message.chat.id) + "';")
            for id_user, in c.fetchall():
                count_ref += 1
            balance_user = 0
            c.execute("SELECT balance_user FROM balances WHERE id_user = '" + str(call.message.chat.id) + "';")
            for balance_user, in c.fetchall():
                pass
            conn.close()
            db.send(call.message.chat.id, "💰 Ваш баланс: <b>" + str(balance_user) + " руб.</b>\n\n🤖 Количество рефералов: #СЛИТО В ТГ КАНАЛАХ @END_SOFTWARE AND @END_RAID<b>" + str(count_ref)+ "</b>", key.prof())
        elif call.data == "balance_prof":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            message_id = db.send(call.message.chat.id, '<b>💰 Пополнение</b>\n\nОтправьте чек <b>BTC Banker в RUB</b>:', key.back_pay_in())
            db.shelve_add(call.message.chat.id, 1)
            with open('Temp/' + str(call.message.chat.id) + '_message_for_delete.txt', 'w', encoding='utf-8') as f:
                f.write(str(message_id))
        elif call.data == "back_pay_in":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            count_ref = 0
            c.execute("SELECT id_user FROM users WHERE who_ref = '" + str(call.message.chat.id) + "';")
            for id_user, in c.fetchall():
                count_ref += 1
            balance_user = 0
            c.execute("SELECT balance_user FROM balances WHERE id_user = '" + str(call.message.chat.id) + "';")
            for balance_user, in c.fetchall():
                pass
            conn.close()
            db.send(call.message.chat.id, "💰 Ваш баланс: <b>" + str(balance_user) + " руб.</b>\n\n🤖 Количество рефералов: <b>" + str(count_ref)+ "</b>", key.prof())
        elif call.data == "close":
            db.dell_mess(call.message.chat.id, call.message.message_id)
        elif call.data == "olx_pt":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            t = 0
            c.execute("SELECT id, time_start,duration,status,service, id_sub FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for id, time_start, duration, status, service, id_sub, in c.fetchall():
                if status == 0 and service == '🇵🇹 OLX.PT':
                    time_temp = datetime.datetime.strptime(time_start, '%H/%M/%d/%m/%Y')
                    current_time = datetime.datetime.today()
                    days = current_time - time_temp
                    time_all = int(days.days) * 86400 + int(days.seconds)
                    diff = float(duration) * 3600 - time_all
                    if diff <= 0:
                        c.execute("UPDATE subs SET status = '" + '1' + "' WHERE id_sub = '" + str(id_sub) + "';")
                        conn.commit()
                        bot.send_message(call.message.chat.id, '<b>Ваша подписка истекла 😔</b>\n\nСервис: <b>'+str(service) + '</b>\nДата покупки: <b>'+str(time_start)+'</b>', reply_markup=key.close(), parse_mode="html")
                        t = 2
                    else:
                        t = 1
                    break
            if t == 1:
                db.send(call.message.chat.id, "<b>🦋 Отправьте ссылку на категорию</b>\n\nПример: https://www.olx.pt/telemoveis-e-tablets/\n\n<b>С фильтрами / Без фильтров</b>", key.cancel())
                db.shelve_add(call.message.chat.id, 2)
                with open('Temp/' + str(call.message.chat.id) + '_service_parser_olx.txt', 'w', encoding='utf-8') as f:
                    f.write('olxpt')
            else:
                db.send(call.message.chat.id, "❗️<b>У вас отсутствует подписка</b>\n\n👾 <b>Вы можете: </b>\n- Купить подписку", key.buy_sub('olxpt'))
            conn.close()
        elif call.data == "olx_ua":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            t = 0
            c.execute("SELECT id, time_start,duration,status,service, id_sub FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for id, time_start, duration, status, service, id_sub, in c.fetchall():
                if status == 0 and service == '🇺🇦 OLX.ua':
                    time_temp = datetime.datetime.strptime(time_start, '%H/%M/%d/%m/%Y')
                    current_time = datetime.datetime.today()
                    days = current_time - time_temp
                    time_all = int(days.days) * 86400 + int(days.seconds)
                    diff = float(duration) * 3600 - time_all
                    if diff <= 0:
                        c.execute("UPDATE subs SET status = '" + '1' + "' WHERE id_sub = '" + str(id_sub) + "';")
                        conn.commit()
                        bot.send_message(call.message.chat.id, '<b>Ваша подписка истекла 😔</b>\n\nСервис: <b>'+str(service) + '</b>\nДата покупки: <b>'+str(time_start)+'</b>', reply_markup=key.close(), parse_mode="html")
                        t = 2
                    else:
                        t = 1
                    break
            if t == 1:
                db.send(call.message.chat.id, "<b>🦋 Отправьте ссылку на категорию</b>\n\nПример: https://www.olx.ua/elektronika/\n\n<b>С фильтрами / Без фильтров</b>", key.cancel())
                db.shelve_add(call.message.chat.id, 2)
                with open('Temp/' + str(call.message.chat.id) + '_service_parser_olx.txt', 'w', encoding='utf-8') as f:
                    f.write('olxua')
            else:
                db.send(call.message.chat.id, "❗️<b>У вас отсутствует подписка</b>\n\n👾 <b>Вы можете: </b>\n- Купить подписку", key.buy_sub('olxua'))
            conn.close()
        elif call.data == "olx_pl":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            t = 0
            c.execute("SELECT id, time_start,duration,status,service, id_sub FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for id, time_start, duration, status, service, id_sub, in c.fetchall():
                if status == 0 and service == '🇵🇱 OLX.PL':
                    time_temp = datetime.datetime.strptime(time_start, '%H/%M/%d/%m/%Y')
                    current_time = datetime.datetime.today()
                    days = current_time - time_temp
                    time_all = int(days.days) * 86400 + int(days.seconds)
                    diff = float(duration) * 3600 - time_all
                    if diff <= 0:
                        c.execute("UPDATE subs SET status = '" + '1' + "' WHERE id_sub = '" + str(id_sub) + "';")
                        conn.commit()
                        bot.send_message(call.message.chat.id, '<b>Ваша подписка истекла 😔</b>\n\nСервис: <b>'+str(service) + '</b>\nДата покупки: <b>'+str(time_start)+'</b>', reply_markup=key.close(), parse_mode="html")
                        t = 2
                    else:
                        t = 1
                    break
            if t == 1:
                db.send(call.message.chat.id, "<b>🦋 Отправьте ссылку на категорию</b>\n\nПример: https://www.olx.pl/elektronika/\n\n<b>С фильтрами / Без фильтров</b>", key.cancel())
                db.shelve_add(call.message.chat.id, 2)
                with open('Temp/' + str(call.message.chat.id) + '_service_parser_olx.txt', 'w', encoding='utf-8') as f:
                    f.write('olxpl')
            else:
                db.send(call.message.chat.id, "❗️<b>У вас отсутствует подписка</b>\n\n👾 <b>Вы можете: </b>\n- Купить подписку", key.buy_sub('olxpl'))
            conn.close()
        elif call.data == "olx_ro":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            t = 0
            c.execute("SELECT id, time_start,duration,status,service, id_sub FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for id, time_start, duration, status, service, id_sub, in c.fetchall():
                if status == 0 and service == '🇷🇴 OLX.RO':
                    time_temp = datetime.datetime.strptime(time_start, '%H/%M/%d/%m/%Y')
                    current_time = datetime.datetime.today()
                    days = current_time - time_temp
                    time_all = int(days.days) * 86400 + int(days.seconds)
                    diff = float(duration) * 3600 - time_all
                    if diff <= 0:
                        c.execute("UPDATE subs SET status = '" + '1' + "' WHERE id_sub = '" + str(id_sub) + "';")
                        conn.commit()
                        bot.send_message(call.message.chat.id, '<b>Ваша подписка истекла 😔</b>\n\nСервис: <b>'+str(service) + '</b>\nДата покупки: <b>'+str(time_start)+'</b>', reply_markup=key.close(), parse_mode="html")
                        t = 2
                    else:
                        t = 1
                    break
            if t == 1:
                db.send(call.message.chat.id, "<b>🦋 Отправьте ссылку на категорию</b>\n\nПример: https://www.olx.ro/electronice-si-electrocasnice/\n\n<b>С фильтрами / Без фильтров</b>", key.cancel())
                db.shelve_add(call.message.chat.id, 2)
                with open('Temp/' + str(call.message.chat.id) + '_service_parser_olx.txt', 'w', encoding='utf-8') as f:
                    f.write('olxro')
            else:
                db.send(call.message.chat.id, "❗️<b>У вас отсутствует подписка</b>\n\n👾 <b>Вы можете: </b>\n- Купить подписку", key.buy_sub('olxro'))
            conn.close()
        elif call.data == "olx_kz":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            t = 0
            c.execute("SELECT id, time_start,duration,status,service, id_sub FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for id, time_start, duration, status, service, id_sub, in c.fetchall():
                if status == 0 and service == '🇰🇿 OLX.kz':
                    time_temp = datetime.datetime.strptime(time_start, '%H/%M/%d/%m/%Y')
                    current_time = datetime.datetime.today()
                    days = current_time - time_temp
                    time_all = int(days.days) * 86400 + int(days.seconds)
                    diff = float(duration) * 3600 - time_all
                    if diff <= 0:
                        c.execute("UPDATE subs SET status = '" + '1' + "' WHERE id_sub = '" + str(id_sub) + "';")
                        conn.commit()
                        bot.send_message(call.message.chat.id, '<b>Ваша подписка истекла 😔</b>\n\nСервис: <b>'+str(service) + '</b>\nДата покупки: <b>'+str(time_start)+'</b>', reply_markup=key.close(), parse_mode="html")
                        t = 2
                    else:
                        t = 1
                    break
            if t == 1:
                db.send(call.message.chat.id, "<b>🦋 Отправьте ссылку на категорию</b>\n\nПример: https://www.olx.kz/elektronika/\n\n<b>С фильтрами / Без фильтров</b>", key.cancel())
                db.shelve_add(call.message.chat.id, 2)
                with open('Temp/' + str(call.message.chat.id) + '_service_parser_olx.txt', 'w', encoding='utf-8') as f:
                    f.write('olxkz')
            else:
                db.send(call.message.chat.id, "❗️<b>У вас отсутствует подписка</b>\n\n👾 <b>Вы можете: </b>\n- Купить подписку", key.buy_sub('olxkz'))
            conn.close()
        elif call.data == "olx_bg":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            t = 0
            c.execute("SELECT id, time_start,duration,status,service, id_sub FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for id, time_start, duration, status, service, id_sub, in c.fetchall():
                if status == 0 and service == '🇧🇬 OLX.bg':
                    time_temp = datetime.datetime.strptime(time_start, '%H/%M/%d/%m/%Y')
                    current_time = datetime.datetime.today()
                    days = current_time - time_temp
                    time_all = int(days.days) * 86400 + int(days.seconds)
                    diff = float(duration) * 3600 - time_all
                    if diff <= 0:
                        c.execute("UPDATE subs SET status = '" + '1' + "' WHERE id_sub = '" + str(id_sub) + "';")
                        conn.commit()
                        bot.send_message(call.message.chat.id, '<b>Ваша подписка истекла 😔</b>\n\nСервис: <b>'+str(service) + '</b>\nДата покупки: <b>'+str(time_start)+'</b>', reply_markup=key.close(), parse_mode="html")
                        t = 2
                    else:
                        t = 1
                    break
            if t == 1:
                db.send(call.message.chat.id, "<b>🦋 Отправьте ссылку на категорию</b>\n\nПример: https://www.olx.bg/elektronika/\n\n<b>С фильтрами / Без фильтров</b>", key.cancel())
                db.shelve_add(call.message.chat.id, 2)
                with open('Temp/' + str(call.message.chat.id) + '_service_parser_olx.txt', 'w', encoding='utf-8') as f:
                    f.write('olxbg')
            else:
                db.send(call.message.chat.id, "❗️<b>У вас отсутствует подписка</b>\n\n👾 <b>Вы можете: </b>\n- Купить подписку", key.buy_sub('olxbg'))
            conn.close()
        elif call.data == "subito_it":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            t = 0
            c.execute("SELECT id, time_start,duration,status,service, id_sub FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for id, time_start, duration, status, service, id_sub, in c.fetchall():
                if status == 0 and service == '🇮🇹 SUBITO.IT':
                    time_temp = datetime.datetime.strptime(time_start, '%H/%M/%d/%m/%Y')
                    current_time = datetime.datetime.today()
                    days = current_time - time_temp
                    time_all = int(days.days) * 86400 + int(days.seconds)
                    diff = float(duration) * 3600 - time_all
                    if diff <= 0:
                        c.execute("UPDATE subs SET status = '" + '1' + "' WHERE id_sub = '" + str(id_sub) + "';")
                        conn.commit()
                        bot.send_message(call.message.chat.id, '<b>Ваша подписка истекла 😔</b>\n\nСервис: <b>'+str(service) + '</b>\nДата покупки: <b>'+str(time_start)+'</b>', reply_markup=key.close(), parse_mode="html")
                        t = 2
                    else:
                        t = 1
                    break
            if t == 1:
                db.send(call.message.chat.id, "<b>🦋 Отправьте ссылку на категорию</b>\n\nПример: https://www.subito.it/annunci-italia/vendita/elettronica/\n\n<b>С фильтрами / Без фильтров</b>", key.cancel())
                db.shelve_add(call.message.chat.id, 7)
            else:
                db.send(call.message.chat.id, "❗️<b>У вас отсутствует подписка</b>\n\n👾 <b>Вы можете: </b>\n- Купить подписку", key.buy_sub('subitoit'))
            conn.close()
        elif call.data == "pazar3_mk":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            t = 0
            c.execute("SELECT id, time_start,duration,status,service, id_sub FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for id, time_start, duration, status, service, id_sub, in c.fetchall():
                if status == 0 and service == '🇲🇰 Pazar3.mk':
                    time_temp = datetime.datetime.strptime(time_start, '%H/%M/%d/%m/%Y')
                    current_time = datetime.datetime.today()
                    days = current_time - time_temp
                    time_all = int(days.days) * 86400 + int(days.seconds)
                    diff = float(duration) * 3600 - time_all
                    if diff <= 0:
                        c.execute("UPDATE subs SET status = '" + '1' + "' WHERE id_sub = '" + str(id_sub) + "';")
                        conn.commit()
                        bot.send_message(call.message.chat.id, '<b>Ваша подписка истекла 😔</b>\n\nСервис: <b>'+str(service) + '</b>\nДата покупки: <b>'+str(time_start)+'</b>', reply_markup=key.close(), parse_mode="html")
                        t = 2
                    else:
                        t = 1
                    break
            if t == 1:
                db.send(call.message.chat.id, "<b>🦋 Отправьте ссылку на категорию</b>\n\nПример: https://www.pazar3.mk/oglasi/elektronika/se-prodava-se-kupuva\n\n<b>С фильтрами / Без фильтров</b>", key.cancel())
                db.shelve_add(call.message.chat.id, 15)
            else:
                db.send(call.message.chat.id, "❗️<b>У вас отсутствует подписка</b>\n\n👾 <b>Вы можете: </b>\n- Купить подписку", key.buy_sub('pazar3mk'))
            conn.close()
        elif call.data == "sbazar_cz":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            t = 0
            c.execute("SELECT id, time_start,duration,status,service, id_sub FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for id, time_start, duration, status, service, id_sub, in c.fetchall():
                if status == 0 and service == '🇨🇿 Sbazar.cz':
                    time_temp = datetime.datetime.strptime(time_start, '%H/%M/%d/%m/%Y')
                    current_time = datetime.datetime.today()
                    days = current_time - time_temp
                    time_all = int(days.days) * 86400 + int(days.seconds)
                    diff = float(duration) * 3600 - time_all
                    if diff <= 0:
                        c.execute("UPDATE subs SET status = '" + '1' + "' WHERE id_sub = '" + str(id_sub) + "';")
                        conn.commit()
                        bot.send_message(call.message.chat.id, '<b>Ваша подписка истекла 😔</b>\n\nСервис: <b>'+str(service) + '</b>\nДата покупки: <b>'+str(time_start)+'</b>', reply_markup=key.close(), parse_mode="html")
                        t = 2
                    else:
                        t = 1
                    break
            if t == 1:
                db.send(call.message.chat.id, "<b>🦋 Отправьте ссылку на категорию</b>\n\nПример: https://www.sbazar.cz/29-detsky-bazar\n\n<b>С фильтрами / Без фильтров</b>", key.cancel())
                db.shelve_add(call.message.chat.id, 17)
            else:
                db.send(call.message.chat.id, "❗️<b>У вас отсутствует подписка</b>\n\n👾 <b>Вы можете: </b>\n- Купить подписку", key.buy_sub('sbazarcz'))
            conn.close()
        elif "buy_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            service_chiper = call.data[4:]
            if service_chiper == "olxpt":
                service = '🇵🇹 OLX.PT'
            elif service_chiper == "olxpl":
                service = '🇵🇱 OLX.PL'
            elif service_chiper == "olxro":
                service = '🇷🇴 OLX.RO'
            elif service_chiper == "olxkz":
                service = '🇰🇿 OLX.kz'
            elif service_chiper == "olxbg":
                service = '🇧🇬 OLX.bg'
            elif service_chiper == "olxua":
                service = '🇺🇦 OLX.ua'
            elif service_chiper == "subitoit":
                service = '🇮🇹 SUBITO.IT'
            elif service_chiper == "pazar3mk":
                service = '🇲🇰 Pazar3.mk'
            elif service_chiper == "sbazarcz":
                service = '🇨🇿 Sbazar.cz'
            conn = sqlite3.connect("users.db")
            c = conn.cursor()
            balance_user = 0
            c.execute("SELECT balance_user FROM balances WHERE id_user = '" + str(call.message.chat.id) + "';")
            for balance_user, in c.fetchall():
                pass
            conn.close()
            db.send(call.message.chat.id, '<b>👻 Покупка подписки:</b>\n\nСервис: <b>'+str(service)+'</b>\nБаланс: <b>'+str(balance_user)+' руб.</b>', key.buynow(service_chiper))
        elif call.data == "back_services":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            db.send(call.message.chat.id, "☠️ Выбирайте сервис:", key.services())
        elif "buynow" in call.data:
            temp_1 = call.data.find('_')
            time_buy = call.data[6:temp_1]
            duration = int(time_buy)*24
            service_chiper = call.data[temp_1+1:]
            if service_chiper == "olxpt":
                service = '🇵🇹 OLX.PT'
            elif service_chiper == "olxpl":
                service = '🇵🇱 OLX.PL'
            elif service_chiper == "olxro":
                service = '🇷🇴 OLX.RO'
            elif service_chiper == "olxkz":
                service = '🇰🇿 OLX.kz'
            elif service_chiper == "olxbg":
                service = '🇧🇬 OLX.bg'
            elif service_chiper == "olxua":
                service = '🇺🇦 OLX.ua'
            elif service_chiper == "subitoit":
                service = '🇮🇹 SUBITO.IT'
            elif service_chiper == "sbazarcz":
                service = '🇨🇿 Sbazar.cz'
            if time_buy == '3':
                sum = -400
            elif time_buy == '7':
                sum = -800
            elif time_buy == '31':
                sum = -2000
            status = db.add_balance(call.message.chat.id, sum)
            if status == 'bad':
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="❌ Недостаточно средств!")
            else:
                db.dell_mess(call.message.chat.id, call.message.message_id)
                res = db.send(call.message.chat.id, "🎉", "")
                conn = sqlite3.connect("sub.db")
                c = conn.cursor()
                dateFormatter = '%H/%M/%d/%m/%Y'
                time_now = datetime.datetime.now().strftime(dateFormatter)
                rand = random.randint(1, 1000000000)
                c.execute("INSERT INTO subs VALUES(?,?,?,?,?,?)", (call.message.chat.id, time_now, duration, '0', service, rand))
                conn.commit()
                conn.close()
                sleep(3)
                db.dell_mess(call.message.chat.id, res)
                db.send(call.message.chat.id, "<b>❤️Спасибо за покупку</b>\n\n🙈Теперь вы можете изменять ваши фильтры в настройках!", key.close())
        elif call.data == "subs":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            text = "<b>🦋 Ваши подписки: </b>\n\n"
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            c.execute("SELECT id, time_start,duration,status,service FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for id, time_start, duration, status, service, in c.fetchall():
                if status == 0:
                    time_temp = datetime.datetime.strptime(time_start, '%H/%M/%d/%m/%Y')
                    current_time = datetime.datetime.today()
                    days = current_time - time_temp
                    time_all = int(days.days) * 86400 + int(days.seconds)
                    diff = float(duration) * 3600 - time_all
                    diff = round((float(diff) / 3600), 1)
                    text += "<b>"+str(service)+"</b>\nДата покупки: <b>"+str(time_start)+"</b>\nКуплено: <b>" + str(duration) + " ч.</b>\nОсталось: <b>"+str(diff)+" ч.</b>\n\n"
            conn.close()
            db.send(call.message.chat.id, text, key.back_prof())
        elif "settings_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            service_chiper = call.data[9:]
            if service_chiper == "olxpt":
                service = '🇵🇹 OLX.PT'
            elif service_chiper == "olxpl":
                service = '🇵🇱 OLX.PL'
            elif service_chiper == "olxro":
                service = '🇷🇴 OLX.RO'
            elif service_chiper == "olxkz":
                service = '🇰🇿 OLX.kz'
            elif service_chiper == "olxbg":
                service = '🇧🇬 OLX.bg'
            elif service_chiper == "olxua":
                service = '🇺🇦 OLX.ua'
            elif service_chiper == "subitoit":
                service = '🇮🇹 SUBITO.IT'
            elif service_chiper == "pazar3mk":
                service = '🇲🇰 Pazar3.mk'
            elif service_chiper == "sbazarcz":
                service = '🇨🇿 Sbazar.cz'
            conn = sqlite3.connect("options.db")
            c = conn.cursor()
            id_user = 0
            if service == '🇮🇹 SUBITO.IT':
                c.execute("SELECT id_user, on_off_message, message_send, max_ads_online, max_ads_offline, min_year FROM subitoit WHERE id_user = '" + str(call.message.chat.id) + "';")
                for id_user, on_off_message, message_send, max_ads_online, max_ads_offline, min_year, in c.fetchall():
                    pass
                if id_user == 0:
                    c.execute("INSERT INTO subitoit VALUES(?,?,?,?,?,?)", (call.message.chat.id, 'OFF', '', '15', '50', '2000'))
                    conn.commit()
                    on_off_message = 'OFF'
                    message_send = ''
                    max_ads_online = 15
                    max_ads_offline = 50
                    min_year = 2000
                else:
                    pass
                db.send(call.message.chat.id, "<b>⚙️ Настройки для "+str(service)+":</b>\n\nWhatsApp сообщение: <b>"+str(on_off_message)+" / "+str(message_send)+"</b>\nГод создания аккаунта: <b>"+str(min_year)+"</b>\nАктивных объявлений: <b>"+str(max_ads_online)+"</b>\nЗавершенных объявлений: <b>"+str(max_ads_offline)+"</b>", key.settings_main(service_chiper))
            elif service == '🇲🇰 Pazar3.mk':
                c.execute("SELECT id_user, on_off_message, message_send FROM pazar3mk WHERE id_user = '" + str(call.message.chat.id) + "';")
                for id_user, on_off_message, message_send, in c.fetchall():
                    pass
                if id_user == 0:
                    c.execute("INSERT INTO pazar3mk VALUES(?,?,?)", (call.message.chat.id, 'OFF', ''))
                    conn.commit()
                    on_off_message = 'OFF'
                    message_send = ''
                else:
                    pass
                db.send(call.message.chat.id, "<b>⚙️ Настройки для "+str(service)+":</b>\n\nWhatsApp сообщение: <b>"+str(on_off_message)+" / "+str(message_send)+"</b>", key.settings_main(service_chiper))
            elif service == '🇨🇿 Sbazar.cz':
                c.execute("SELECT id_user, on_off_message, message_send, max_ads FROM "+str(service_chiper)+" WHERE id_user = '" + str(call.message.chat.id) + "';")
                for id_user, on_off_message, message_send, max_ads, in c.fetchall():
                    pass
                if id_user == 0:
                    c.execute("INSERT INTO "+str(service_chiper)+" VALUES(?,?,?,?)", (call.message.chat.id, 'OFF', '', '15'))
                    conn.commit()
                    on_off_message = 'OFF'
                    message_send = ''
                    max_ads = 10
                else:
                    pass
                db.send(call.message.chat.id, "<b>⚙️ Настройки для "+str(service)+":</b>\n\nWhatsApp сообщение: <b>"+str(on_off_message)+" / "+str(message_send)+"</b>\nКоличество объявлений: <b>"+str(max_ads)+"</b>", key.settings_main(service_chiper))
            else:
                c.execute("SELECT id_user, on_off_message, message_send, max_ads, min_year FROM "+str(service_chiper)+" WHERE id_user = '" + str(call.message.chat.id) + "';")
                for id_user, on_off_message, message_send, max_ads, min_year, in c.fetchall():
                    pass
                if id_user == 0:
                    c.execute("INSERT INTO "+str(service_chiper)+" VALUES(?,?,?,?,?)", (call.message.chat.id, 'OFF', '', '15', '2015'))
                    conn.commit()
                    on_off_message = 'OFF'
                    message_send = ''
                    max_ads = 10
                    min_year = 2000
                else:
                    pass
                db.send(call.message.chat.id, "<b>⚙️ Настройки для "+str(service)+":</b>\n\nWhatsApp сообщение: <b>"+str(on_off_message)+" / "+str(message_send)+"</b>\nГод создания аккаунта: <b>"+str(min_year)+"</b>\nКоличество объявлений: <b>"+str(max_ads)+"</b>", key.settings_main(service_chiper))
        elif "main_messages_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            service_chiper = call.data[14:]
            if service_chiper == "olxpt":
                service = '🇵🇹 OLX.PT'
            elif service_chiper == "olxpl":
                service = '🇵🇱 OLX.PL'
            elif service_chiper == "olxro":
                service = '🇷🇴 OLX.RO'
            elif service_chiper == "olxkz":
                service = '🇰🇿 OLX.kz'
            elif service_chiper == "olxbg":
                service = '🇧🇬 OLX.bg'
            elif service_chiper == "olxua":
                service = '🇺🇦 OLX.ua'
            elif service_chiper == "subitoit":
                service = '🇮🇹 SUBITO.IT'
            elif service_chiper == "pazar3mk":
                service = '🇲🇰 Pazar3.mk'
            elif service_chiper == "sbazarcz":
                service = '🇨🇿 Sbazar.cz'
            conn = sqlite3.connect("options.db")
            c = conn.cursor()
            c.execute("SELECT id_user, on_off_message, message_send FROM "+str(service_chiper)+" WHERE id_user = '" + str(call.message.chat.id) + "';")
            for id_user, on_off_message, message_send, in c.fetchall():
                pass
            conn.close()
            db.send(call.message.chat.id, "<b>⚙️ Сообщения для "+str(service)+":</b>\n\n<b>"+str(on_off_message)+" / "+str(message_send)+"</b>\n\nПри переходе в WhatsApp, будет автоматически открываться чат с указанным текстом!", key.main_messages(service_chiper))
        elif "change_status_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            service_chiper = call.data[14:]
            conn = sqlite3.connect("options.db")
            c = conn.cursor()
            c.execute("SELECT on_off_message, message_send FROM "+str(service_chiper)+" WHERE id_user = '" + str(call.message.chat.id) + "';")
            for on_off_message, message_send, in c.fetchall():
                pass
            if on_off_message == "OFF":
                new = "ON"
            else:
                new = "OFF"
            if service_chiper == "olxpt":
                service = '🇵🇹 OLX.PT'
            elif service_chiper == "olxpl":
                service = '🇵🇱 OLX.PL'
            elif service_chiper == "olxro":
                service = '🇷🇴 OLX.RO'
            elif service_chiper == "olxkz":
                service = '🇰🇿 OLX.kz'
            elif service_chiper == "olxbg":
                service = '🇧🇬 OLX.bg'
            elif service_chiper == "olxua":
                service = '🇺🇦 OLX.ua'
            elif service_chiper == "subitoit":
                service = '🇮🇹 SUBITO.IT'
            elif service_chiper == "pazar3mk":
                service = '🇲🇰 Pazar3.mk'
            elif service_chiper == "sbazarcz":
                service = '🇨🇿 Sbazar.cz'
            c.execute("UPDATE "+str(service_chiper)+" SET on_off_message = '" + str(new) + "' WHERE id_user = '" + str(call.message.chat.id) + "';")
            conn.commit()
            conn.close()
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="✅ Готово!")
            db.send(call.message.chat.id, "<b>⚙️ Сообщения для "+str(service)+":</b>\n\n<b>"+str(new)+" / "+str(message_send)+"</b>\n\nПри переходе в WhatsApp, будет автоматически открываться чат с указанным текстом!", key.main_messages(service_chiper))
        elif "change_text_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            service_chiper = call.data[12:]
            with open('Temp/' + str(call.message.chat.id) + '_change_message.txt', 'w', encoding='utf-8') as f:
                f.write(str(service_chiper))
            db.send(call.message.chat.id, "<b>⚙️ Введите новый текст для WhatsApp:\n\n[title] - меняется на название объявления\n[link] - меняется на ссылку объявления</b>", key.cancel())
            db.shelve_add(call.message.chat.id, 4)
        elif "main_year_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            service_chiper = call.data[10:]
            with open('Temp/' + str(call.message.chat.id) + '_change_year.txt', 'w', encoding='utf-8') as f:
                f.write(str(service_chiper))
            db.send(call.message.chat.id, "<b>⚙️ Введите минимальный год создания аккаунта в объявлении:</b>", key.cancel())
            db.shelve_add(call.message.chat.id, 5)
        elif "max_ads_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            service_chiper = call.data[8:]
            with open('Temp/' + str(call.message.chat.id) + '_change_ads.txt', 'w', encoding='utf-8') as f:
                f.write(str(service_chiper))
            db.send(call.message.chat.id, "<b>⚙️ Введите максимальное количество объявлений у продавца:</b>", key.cancel())
            db.shelve_add(call.message.chat.id, 6)
        elif call.data == "back_main_settings":
            db.dell_mess(call.message.chat.id, call.message.message_id)
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            keys = types.InlineKeyboardMarkup()
            count_services = 0
            c.execute("SELECT id, time_start,duration,status,service FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for id, time_start, duration, status, service, in c.fetchall():
                if status == 0:
                    if service == '🇵🇹 OLX.PT':
                        service_chiper = 'olxpt'
                    elif service == '🇵🇱 OLX.PL':
                        service_chiper = 'olxpl'
                    elif service == '🇷🇴 OLX.RO':
                        service_chiper = 'olxro'
                    elif service == '🇰🇿 OLX.kz':
                        service_chiper = 'olxkz'
                    elif service == '🇧🇬 OLX.bg':
                        service_chiper = 'olxbg'
                    elif service == '🇺🇦 OLX.ua':
                        service_chiper = 'olxua'
                    elif service == '🇮🇹 SUBITO.IT':
                        service_chiper = 'subitoit'
                    elif service == '🇲🇰 Pazar3.mk':
                        service_chiper = 'pazar3mk'
                    elif service == '🇨🇿 Sbazar.cz':
                        service_chiper = 'sbazarcz'
                    keys_1 = types.InlineKeyboardButton(text=service, callback_data="settings_" + str(service_chiper))
                    keys.add(keys_1)
                    count_services += 1
            key_last = types.InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
            keys.add(key_last)
            conn.close()
            if count_services != 0:
                db.send(call.message.chat.id, "<b>⚙️Выберите сервис для изменения фильтров:</b>", keys)
            else:
                db.send(call.message.chat.id, "<b>❗️Для использования этой функции - нужна подписка!</b>", key.close())
        elif "stop_parser_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            id = call.data[12:]
            try:
                db.kill(int(id))
            except Exception as e:
                pass
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="♻️ Остановка парсера..")
            conn = sqlite3.connect("parser.db")
            c = conn.cursor()
            c.execute("UPDATE parser SET  status = '" + '1' + "' WHERE id_user = '" + str(call.message.chat.id) + "';")
            conn.commit()
            conn.close()
            db.send(call.message.chat.id, '<b>🦋 Парсер успешно остановлен!</b>', key.close())
        elif "olx_pt_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            hours = call.data[7:]
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            st = ''
            c.execute("SELECT duration, status, id_sub, service FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for duration, status, id_sub, service, in c.fetchall():
                if service == '🇵🇹 OLX.PT':
                    st = status
                else:
                    pass
            if st == '' or str(st) == '1':
                dateFormatter = '%H/%M/%d/%m/%Y'
                time_now = datetime.datetime.now().strftime(dateFormatter)
                rand = random.randint(1, 100000000)
                c.execute("INSERT INTO subs VALUES(?,?,?,?,?,?)", (call.message.chat.id, time_now, hours, '0', '🇵🇹 OLX.PT', rand))
                conn.commit()
            else:
                new_time = float(duration) + float(hours)
                c.execute("UPDATE subs SET duration = '" + str(new_time) + "' WHERE id_sub = '" + str(id_sub) + "';")
                conn.commit()
            db.send(call.message.chat.id, '<b>😍 Наслаждайся</b>', key.close())
            conn.close()
        elif "olx_ua_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            hours = call.data[7:]
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            st = ''
            c.execute("SELECT duration, status, id_sub, service FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for duration, status, id_sub, service, in c.fetchall():
                if service == '🇺🇦 OLX.ua':
                    st = status
                else:
                    pass
            if st == '' or str(st) == '1':
                dateFormatter = '%H/%M/%d/%m/%Y'
                time_now = datetime.datetime.now().strftime(dateFormatter)
                rand = random.randint(1, 100000000)
                c.execute("INSERT INTO subs VALUES(?,?,?,?,?,?)", (call.message.chat.id, time_now, hours, '0', '🇺🇦 OLX.ua', rand))
                conn.commit()
            else:
                new_time = float(duration) + float(hours)
                c.execute("UPDATE subs SET duration = '" + str(new_time) + "' WHERE id_sub = '" + str(id_sub) + "';")
                conn.commit()
            db.send(call.message.chat.id, '<b>😍 Наслаждайся</b>', key.close())
            conn.close()
        elif "olx_pl_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            hours = call.data[7:]
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            st = ''
            c.execute("SELECT duration, status, id_sub, service FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for duration, status, id_sub, service, in c.fetchall():
                if service == '🇵🇱 OLX.PL':
                    st = status
                else:
                    pass
            if st == '' or str(st) == '1':
                dateFormatter = '%H/%M/%d/%m/%Y'
                time_now = datetime.datetime.now().strftime(dateFormatter)
                rand = random.randint(1, 100000000)
                c.execute("INSERT INTO subs VALUES(?,?,?,?,?,?)", (call.message.chat.id, time_now, hours, '0', '🇵🇱 OLX.PL', rand))
                conn.commit()
            else:
                new_time = float(duration) + float(hours)
                c.execute("UPDATE subs SET duration = '" + str(new_time) + "' WHERE id_sub = '" + str(id_sub) + "';")
                conn.commit()
            db.send(call.message.chat.id, '<b>😍 Наслаждайся</b>', key.close())
            conn.close()
        elif "olx_ro_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            hours = call.data[7:]
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            st = ''
            c.execute(
                "SELECT duration, status, id_sub, service FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for duration, status, id_sub, service, in c.fetchall():
                if service == '🇷🇴 OLX.RO':
                    st = status
                else:
                    pass
            if st == '' or str(st) == '1':
                dateFormatter = '%H/%M/%d/%m/%Y'
                time_now = datetime.datetime.now().strftime(dateFormatter)
                rand = random.randint(1, 100000000)
                c.execute("INSERT INTO subs VALUES(?,?,?,?,?,?)",
                          (call.message.chat.id, time_now, hours, '0', '🇷🇴 OLX.RO', rand))
                conn.commit()
            else:
                new_time = float(duration) + float(hours)
                c.execute("UPDATE subs SET duration = '" + str(new_time) + "' WHERE id_sub = '" + str(id_sub) + "';")
                conn.commit()
            db.send(call.message.chat.id, '<b>😍 Наслаждайся</b>', key.close())
            conn.close()
        elif "olx_kz_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            hours = call.data[7:]
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            st = ''
            c.execute(
                "SELECT duration, status, id_sub, service FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for duration, status, id_sub, service, in c.fetchall():
                if service == '🇰🇿 OLX.kz':
                    st = status
                else:
                    pass
            if st == '' or str(st) == '1':
                dateFormatter = '%H/%M/%d/%m/%Y'
                time_now = datetime.datetime.now().strftime(dateFormatter)
                rand = random.randint(1, 100000000)
                c.execute("INSERT INTO subs VALUES(?,?,?,?,?,?)",
                          (call.message.chat.id, time_now, hours, '0', '🇰🇿 OLX.kz', rand))
                conn.commit()
            else:
                new_time = float(duration) + float(hours)
                c.execute("UPDATE subs SET duration = '" + str(new_time) + "' WHERE id_sub = '" + str(id_sub) + "';")
                conn.commit()
            db.send(call.message.chat.id, '<b>😍 Наслаждайся</b>', key.close())
            conn.close()
        elif "olx_bg_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            hours = call.data[7:]
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            st = ''
            c.execute(
                "SELECT duration, status, id_sub, service FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for duration, status, id_sub, service, in c.fetchall():
                if service == '🇧🇬 OLX.bg':
                    st = status
                else:
                    pass
            if st == '' or str(st) == '1':
                dateFormatter = '%H/%M/%d/%m/%Y'
                time_now = datetime.datetime.now().strftime(dateFormatter)
                rand = random.randint(1, 100000000)
                c.execute("INSERT INTO subs VALUES(?,?,?,?,?,?)",
                          (call.message.chat.id, time_now, hours, '0', '🇧🇬 OLX.bg', rand))
                conn.commit()
            else:
                new_time = float(duration) + float(hours)
                c.execute("UPDATE subs SET duration = '" + str(new_time) + "' WHERE id_sub = '" + str(id_sub) + "';")
                conn.commit()
            db.send(call.message.chat.id, '<b>😍 Наслаждайся</b>', key.close())
            conn.close()
        elif "max_online_ads_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            service_chiper = call.data[15:]
            with open('Temp/' + str(call.message.chat.id) + '_change_ads.txt', 'w', encoding='utf-8') as f:
                f.write(str(service_chiper))
            db.send(call.message.chat.id, "<b>⚙️ Введите максимальное количество активных объявлений у продавца:</b>", key.cancel())
            db.shelve_add(call.message.chat.id, 9)
        elif "max_offline_ads_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            service_chiper = call.data[16:]
            with open('Temp/' + str(call.message.chat.id) + '_change_ads.txt', 'w', encoding='utf-8') as f:
                f.write(str(service_chiper))
            db.send(call.message.chat.id, "<b>⚙️ Введите максимальное количество завершенных объявлений у продавца:</b>", key.cancel())
            db.shelve_add(call.message.chat.id, 10)
        elif "dislikes_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            service_chiper = call.data[9:]
            with open('Temp/' + str(call.message.chat.id) + '_change_ads.txt', 'w', encoding='utf-8') as f:
                f.write(str(service_chiper))
            db.send(call.message.chat.id, "<b>⚙️ Введите максимальное количество лайков у продавца:</b>", key.cancel())
            db.shelve_add(call.message.chat.id, 14)
        elif "likes_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            service_chiper = call.data[6:]
            with open('Temp/' + str(call.message.chat.id) + '_change_ads.txt', 'w', encoding='utf-8') as f:
                f.write(str(service_chiper))
            db.send(call.message.chat.id, "<b>⚙️ Введите максимальное количество лайков у продавца:</b>", key.cancel())
            db.shelve_add(call.message.chat.id, 13)
        elif "subito_it_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            hours = call.data[10:]
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            st = ''
            c.execute("SELECT duration, status, id_sub, service FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for duration, status, id_sub, service, in c.fetchall():
                if service == '🇮🇹 SUBITO.IT':
                    st = status
                else:
                    pass
            if st == '' or str(st) == '1':
                dateFormatter = '%H/%M/%d/%m/%Y'
                time_now = datetime.datetime.now().strftime(dateFormatter)
                rand = random.randint(1, 100000000)
                c.execute("INSERT INTO subs VALUES(?,?,?,?,?,?)",(call.message.chat.id, time_now, hours, '0', '🇮🇹 SUBITO.IT', rand))
                conn.commit()
            else:
                new_time = float(duration) + float(hours)
                c.execute("UPDATE subs SET duration = '" + str(new_time) + "' WHERE id_sub = '" + str(id_sub) + "';")
                conn.commit()
            db.send(call.message.chat.id, '<b>😍 Наслаждайся</b>', key.close())
            conn.close()
        elif "pazar3_mk_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            hours = call.data[10:]
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            st = ''
            c.execute("SELECT duration, status, id_sub, service FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for duration, status, id_sub, service, in c.fetchall():
                if service == '🇲🇰 Pazar3.mk':
                    st = status
                else:
                    pass
            if st == '' or str(st) == '1':
                dateFormatter = '%H/%M/%d/%m/%Y'
                time_now = datetime.datetime.now().strftime(dateFormatter)
                rand = random.randint(1, 100000000)
                c.execute("INSERT INTO subs VALUES(?,?,?,?,?,?)",(call.message.chat.id, time_now, hours, '0', '🇲🇰 Pazar3.mk', rand))
                conn.commit()
            else:
                new_time = float(duration) + float(hours)
                c.execute("UPDATE subs SET duration = '" + str(new_time) + "' WHERE id_sub = '" + str(id_sub) + "';")
                conn.commit()
            db.send(call.message.chat.id, '<b>😍 Наслаждайся</b>', key.close())
            conn.close()
        elif "sbazar_cz_" in call.data:
            db.dell_mess(call.message.chat.id, call.message.message_id)
            hours = call.data[10:]
            conn = sqlite3.connect("sub.db")
            c = conn.cursor()
            st = ''
            c.execute("SELECT duration, status, id_sub, service FROM subs WHERE id = '" + str(call.message.chat.id) + "';")
            for duration, status, id_sub, service, in c.fetchall():
                if service == '🇨🇿 Sbazar.cz':
                    st = status
                else:
                    pass
            if st == '' or str(st) == '1':
                dateFormatter = '%H/%M/%d/%m/%Y'
                time_now = datetime.datetime.now().strftime(dateFormatter)
                rand = random.randint(1, 100000000)
                c.execute("INSERT INTO subs VALUES(?,?,?,?,?,?)",(call.message.chat.id, time_now, hours, '0', '🇨🇿 Sbazar.cz', rand))
                conn.commit()
            else:
                new_time = float(duration) + float(hours)
                c.execute("UPDATE subs SET duration = '" + str(new_time) + "' WHERE id_sub = '" + str(id_sub) + "';")
                conn.commit()
            db.send(call.message.chat.id, '<b>😍 Наслаждайся</b>', key.close())
            conn.close()
        elif "checker_nothing" in call.data:
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="🦋 Листай дальше!")
        elif "subito_checker_back_" in call.data:
            temp_1 = call.data.find('/')
            id_parser = int(call.data[20:temp_1])
            number_ad = int(call.data[temp_1 + 1:])
            chat_id = call.message.chat.id
            if number_ad == 0:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="🦋 Назад нельзя!")
            else:
                db.dell_mess(call.message.chat.id, call.message.message_id)
                conn = sqlite3.connect("options.db")
                c = conn.cursor()
                on_off_message = 'OFF'
                message_send = ''
                c.execute("SELECT on_off_message, message_send FROM subitoit WHERE id_user = '" + str(call.message.chat.id) + "';")
                for on_off_message, message_send, in c.fetchall():
                    pass
                conn.close()
                status_message = on_off_message
                message_text = message_send
                conn = sqlite3.connect("parser.db")
                c = conn.cursor()
                count_ads = 0
                c.execute("SELECT img FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
                for img, in c.fetchall():
                    count_ads += 1
                keys = types.InlineKeyboardMarkup()
                keys_1 = types.InlineKeyboardButton(text="<<", callback_data="subito_checker_back_"+str(id_parser)+"/"+str(number_ad-1))
                keys_2 = types.InlineKeyboardButton(text=str(number_ad)+" / "+str(count_ads), callback_data="checker_nothing" + str(id_parser))
                keys_3 = types.InlineKeyboardButton(text=">>", callback_data="subito_checker_next_" + str(id_parser) + "/"+str(number_ad+1))
                keys.add(keys_1, keys_2, keys_3)
                count_check = 1
                c.execute("SELECT title, url, price, name, number, count_max_online, count_max_offline, year, img, gorod FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
                for title, url, price, name, number, count_max_online, count_max_offline, year, img, gorod, in c.fetchall():
                    if count_check == number_ad:
                        count_views = -1
                        c.execute("SELECT id_user FROM parsed_url WHERE url = '" + str(url) + "';")
                        for id_user, in c.fetchall():
                            count_views += 1
                        r = requests.get(img)
                        rand = random.randint(1, 1000000)
                        with open('Temp/' + str(chat_id) + '_temp_photo_' + str(rand) + '.jpeg', 'wb') as fd:
                            for chunk in r.iter_content():
                                fd.write(chunk)
                        photo = open('Temp/' + str(chat_id) + '_temp_photo_' + str(rand) + '.jpeg', 'rb')
                        if status_message == 'ON':
                            message_send = message_text.replace('[title]', title).replace('[link]', url)
                        else:
                            message_send = ''
                        bot.send_photo(chat_id, photo,
                                       caption=f"Название: <b>{title}</b>\n"
                                               f"Цена: <b>{price}</b>\n"
                                               f"Имя: <b>{name}</b>\n"
                                               f"Активных: <b>{count_max_online}</b>\n"
                                               f"Завершенных: <b>{count_max_offline}</b>\n"
                                               f"Опубликовано: <b>{year}</b>\n"
                                               f"Местоположение: <b>{gorod}</b>\n"
                                               f"Номер: <b>+{number}</b>\n\n"
                                               f'Объявление: <a href="'+str(url)+'">*Клик*</a>\n'
                                               f'WhatsApp: <a href="https://api.whatsapp.com/send?phone={number}&text={message_send}">*Клик*</a>\n'
                                               f'Viber: <a href="https://msng.link/o/?{number}=vi">*Клик*</a>\n\n'
                                               f"Видело пользователей: <b>{count_views}</b>",
                                       parse_mode="html", reply_markup=keys)
                    count_check += 1
        elif "subito_checker_next_" in call.data:
            temp_1 = call.data.find('/')
            id_parser = int(call.data[20:temp_1])
            number_ad = int(call.data[temp_1 + 1:])
            chat_id = call.message.chat.id
            conn = sqlite3.connect("parser.db")
            c = conn.cursor()
            count_ads = 0
            c.execute("SELECT img FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
            for img, in c.fetchall():
                count_ads += 1
            conn.close()
            if number_ad > count_ads:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="🦋 Закончились!")
            else:
                conn = sqlite3.connect("options.db")
                c = conn.cursor()
                on_off_message = 'OFF'
                message_send = ''
                c.execute("SELECT on_off_message, message_send FROM subitoit WHERE id_user = '" + str(call.message.chat.id) + "';")
                for on_off_message, message_send, in c.fetchall():
                    pass
                conn.close()
                status_message = on_off_message
                message_text = message_send
                db.dell_mess(call.message.chat.id, call.message.message_id)
                keys = types.InlineKeyboardMarkup()
                keys_1 = types.InlineKeyboardButton(text="<<", callback_data="subito_checker_back_"+str(id_parser)+"/"+str(number_ad-1))
                keys_2 = types.InlineKeyboardButton(text=str(number_ad)+" / "+str(count_ads), callback_data="checker_nothing" + str(id_parser))
                keys_3 = types.InlineKeyboardButton(text=">>", callback_data="subito_checker_next_" + str(id_parser) + "/"+str(number_ad+1))
                keys.add(keys_1, keys_2, keys_3)
                count_check = 1
                conn = sqlite3.connect("parser.db")
                c = conn.cursor()
                c.execute("SELECT title, url, price, name, number, count_max_online, count_max_offline, year, img, gorod FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
                for title, url, price, name, number, count_max_online, count_max_offline, year, img, gorod, in c.fetchall():
                    if count_check == number_ad:
                        count_views = -1
                        c.execute("SELECT id_user FROM parsed_url WHERE url = '" + str(url) + "';")
                        for id_user, in c.fetchall():
                            count_views += 1
                        r = requests.get(img)
                        rand = random.randint(1, 1000000)
                        with open('Temp/' + str(chat_id) + '_temp_photo_' + str(rand) + '.jpeg', 'wb') as fd:
                            for chunk in r.iter_content():
                                fd.write(chunk)
                        photo = open('Temp/' + str(chat_id) + '_temp_photo_' + str(rand) + '.jpeg', 'rb')
                        if status_message == 'ON':
                            message_send = message_text.replace('[title]', title).replace('[link]', url)
                        else:
                            message_send = ''
                        bot.send_photo(chat_id, photo,
                                       caption=f"Название: <b>{title}</b>\n"
                                               f"Цена: <b>{price}</b>\n"
                                               f"Имя: <b>{name}</b>\n"
                                               f"Активных: <b>{count_max_online}</b>\n"
                                               f"Завершенных: <b>{count_max_offline}</b>\n"
                                               f"Опубликовано: <b>{year}</b>\n"
                                               f"Местоположение: <b>{gorod}</b>\n"
                                               f"Номер: <b>+{number}</b>\n\n"
                                               f'Объявление: <a href="'+str(url)+'">*Клик*</a>\n'
                                               f'WhatsApp: <a href="https://api.whatsapp.com/send?phone={number}&text={message_send}">*Клик*</a>\n'
                                               f'Viber: <a href="https://msng.link/o/?{number}=vi">*Клик*</a>\n\n'
                                               f"Видело пользователей: <b>{count_views}</b>",
                                       parse_mode="html", reply_markup=keys)
                    count_check += 1
                conn.close()
        elif "olx_checker_back_" in call.data:
            temp_1 = call.data.find('/')
            id_parser = int(call.data[17:temp_1])
            number_ad = int(call.data[temp_1 + 1:])
            chat_id = call.message.chat.id
            if number_ad == 0:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="🦋 Назад нельзя!")
            else:
                db.dell_mess(call.message.chat.id, call.message.message_id)
                conn = sqlite3.connect("parser.db")
                c = conn.cursor()
                count_ads = 0
                c.execute("SELECT img,url FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
                for img, url, in c.fetchall():
                    service_chiper = url[16:18]
                    count_ads += 1
                conn.close()
                conn = sqlite3.connect("options.db")
                c = conn.cursor()
                on_off_message = 'OFF'
                message_send = ''
                c.execute("SELECT on_off_message, message_send FROM olx"+str(service_chiper)+" WHERE id_user = '" + str(call.message.chat.id) + "';")
                for on_off_message, message_send, in c.fetchall():
                    pass
                status_message = on_off_message
                message_text = message_send
                conn.close()
                conn = sqlite3.connect("parser.db")
                c = conn.cursor()
                keys = types.InlineKeyboardMarkup()
                keys_1 = types.InlineKeyboardButton(text="<<", callback_data="olx_checker_back_"+str(id_parser)+"/"+str(number_ad-1))
                keys_2 = types.InlineKeyboardButton(text=str(number_ad)+" / "+str(count_ads), callback_data="checker_nothing" + str(id_parser))
                keys_3 = types.InlineKeyboardButton(text=">>", callback_data="olx_checker_next_" + str(id_parser) + "/"+str(number_ad+1))
                keys.add(keys_1, keys_2, keys_3)
                count_check = 1
                c.execute("SELECT title, url, price, name, number, count_max_online, count_max_offline, year, img, gorod FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
                for title, url, price, name, number, count_max_online, count_max_offline, year, img, gorod, in c.fetchall():
                    if count_check == number_ad:
                        count_views = -1
                        c.execute("SELECT id_user FROM parsed_url WHERE url = '" + str(url) + "';")
                        for id_user, in c.fetchall():
                            count_views += 1
                        if status_message == 'ON':
                            message_send = message_text.replace('[title]', title).replace('[link]', url)
                        else:
                            message_send = ''
                        bot.send_photo(chat_id, requests.get(img).content,
                                       caption=f"Название: <b>{title}</b>\n"
                                                f"Цена: <b>{price}</b>\n"
                                                f"Имя: <b>{name}</b>\n"
                                                f"Зарегистрирован: <b>{year}</b>\n"
                                                f"Местоположение: <b>{gorod}</b>\n"
                                                f"Номер: <b>+{number}</b>\n\n"
                                                f'Объявление: <a href="'+str(url)+'">*Клик*</a>\n'
                                                f'WhatsApp: <a href="https://api.whatsapp.com/send?phone={number}&text={message_send}">*Клик*</a>\n'
                                                f'Viber: <a href="https://msng.link/o/?{number}=vi">*Клик*</a>\n\n'
                                                f"Видело пользователей: <b>{count_views}</b>",
                                       parse_mode="html", reply_markup=keys)
                    count_check += 1
        elif "olx_checker_next_" in call.data:
            temp_1 = call.data.find('/')
            id_parser = int(call.data[17:temp_1])
            number_ad = int(call.data[temp_1 + 1:])
            chat_id = call.message.chat.id
            conn = sqlite3.connect("parser.db")
            c = conn.cursor()
            count_ads = 0
            c.execute("SELECT img,url FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
            for img, url, in c.fetchall():
                service_chiper = url[16:18]
                count_ads += 1
            conn.close()
            conn = sqlite3.connect("options.db")
            c = conn.cursor()
            on_off_message = 'OFF'
            message_send = ''
            c.execute("SELECT on_off_message, message_send FROM olx" + str(service_chiper) + " WHERE id_user = '" + str(call.message.chat.id) + "';")
            for on_off_message, message_send, in c.fetchall():
                pass
            status_message = on_off_message
            message_text = message_send
            conn.close()
            if number_ad > count_ads:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="🦋 Закончились!")
            else:
                db.dell_mess(call.message.chat.id, call.message.message_id)
                keys = types.InlineKeyboardMarkup()
                keys_1 = types.InlineKeyboardButton(text="<<", callback_data="olx_checker_back_"+str(id_parser)+"/"+str(number_ad-1))
                keys_2 = types.InlineKeyboardButton(text=str(number_ad)+" / "+str(count_ads), callback_data="checker_nothing" + str(id_parser))
                keys_3 = types.InlineKeyboardButton(text=">>", callback_data="olx_checker_next_" + str(id_parser) + "/"+str(number_ad+1))
                keys.add(keys_1, keys_2, keys_3)
                count_check = 1
                conn = sqlite3.connect("parser.db")
                c = conn.cursor()
                c.execute("SELECT title, url, price, name, number, count_max_online, count_max_offline, year, img, gorod FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
                for title, url, price, name, number, count_max_online, count_max_offline, year, img, gorod, in c.fetchall():
                    if count_check == number_ad:
                        count_views = -1
                        c.execute("SELECT id_user FROM parsed_url WHERE url = '" + str(url) + "';")
                        for id_user, in c.fetchall():
                            count_views += 1
                        if status_message == 'ON':
                            message_send = message_text.replace('[title]', title).replace('[link]', url)
                        else:
                            message_send = ''
                        bot.send_photo(chat_id, requests.get(img).content,
                                       caption=f"Название: <b>{title}</b>\n"
                                                f"Цена: <b>{price}</b>\n"
                                                f"Имя: <b>{name}</b>\n"
                                                f"Зарегистрирован: <b>{year}</b>\n"
                                                f"Местоположение: <b>{gorod}</b>\n"
                                                f"Номер: <b>+{number}</b>\n\n"
                                                f'Объявление: <a href="'+str(url)+'">*Клик*</a>\n'
                                                f'WhatsApp: <a href="https://api.whatsapp.com/send?phone={number}&text={message_send}">*Клик*</a>\n'
                                                f'Viber: <a href="https://msng.link/o/?{number}=vi">*Клик*</a>\n\n'
                                                f"Видело пользователей: <b>{count_views}</b>",
                                       parse_mode="html", reply_markup=keys)
                    count_check += 1
                conn.close()
        elif "pazar3_checker_back_" in call.data:
            temp_1 = call.data.find('/')
            id_parser = int(call.data[20:temp_1])
            number_ad = int(call.data[temp_1 + 1:])
            chat_id = call.message.chat.id
            if number_ad == 0:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="🦋 Назад нельзя!")
            else:
                db.dell_mess(call.message.chat.id, call.message.message_id)
                conn = sqlite3.connect("options.db")
                c = conn.cursor()
                on_off_message = 'OFF'
                message_send = ''
                c.execute("SELECT on_off_message, message_send FROM pazar3mk WHERE id_user = '" + str(call.message.chat.id) + "';")
                for on_off_message, message_send, in c.fetchall():
                    pass
                conn.close()
                status_message = on_off_message
                message_text = message_send
                conn = sqlite3.connect("parser.db")
                c = conn.cursor()
                count_ads = 0
                c.execute("SELECT img FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
                for img, in c.fetchall():
                    count_ads += 1
                keys = types.InlineKeyboardMarkup()
                keys_1 = types.InlineKeyboardButton(text="<<", callback_data="pazar3_checker_back_"+str(id_parser)+"/"+str(number_ad-1))
                keys_2 = types.InlineKeyboardButton(text=str(number_ad)+" / "+str(count_ads), callback_data="checker_nothing" + str(id_parser))
                keys_3 = types.InlineKeyboardButton(text=">>", callback_data="pazar3_checker_next_" + str(id_parser) + "/"+str(number_ad+1))
                keys.add(keys_1, keys_2, keys_3)
                count_check = 1
                c.execute("SELECT title, url, price, name, number, img, gorod FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
                for title, url, price, name, number, img, gorod, in c.fetchall():
                    if count_check == number_ad:
                        count_views = -1
                        c.execute("SELECT id_user FROM parsed_url WHERE url = '" + str(url) + "';")
                        for id_user, in c.fetchall():
                            count_views += 1
                        if status_message == 'ON':
                            message_send = message_text.replace('[title]', title).replace('[link]', url)
                        else:
                            message_send = ''
                        bot.send_photo(chat_id, requests.get(img).content,
                                       caption=f"Название: <b>{title}</b>\n"
                                               f"Цена: <b>{price}</b>\n"
                                               f"Имя: <b>{name}</b>\n"
                                               f"Местоположение: <b>{gorod}</b>\n"
                                               f"Номер: <b>+{number}</b>\n\n"
                                               f'Объявление: <a href="'+str(url)+'">*Клик*</a>\n'
                                               f'WhatsApp: <a href="https://api.whatsapp.com/send?phone={number}&text={message_send}">*Клик*</a>\n'
                                               f'Viber: <a href="https://msng.link/o/?{number}=vi">*Клик*</a>\n\n'
                                               f"Видело пользователей: <b>{count_views}</b>",
                                       parse_mode="html", reply_markup=keys)
                    count_check += 1
        elif "pazar3_checker_next_" in call.data:
            temp_1 = call.data.find('/')
            id_parser = int(call.data[20:temp_1])
            number_ad = int(call.data[temp_1 + 1:])
            chat_id = call.message.chat.id
            conn = sqlite3.connect("parser.db")
            c = conn.cursor()
            count_ads = 0
            c.execute("SELECT img FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
            for img, in c.fetchall():
                count_ads += 1
            conn.close()
            if number_ad > count_ads:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="🦋 Закончились!")
            else:
                conn = sqlite3.connect("options.db")
                c = conn.cursor()
                on_off_message = 'OFF'
                message_send = ''
                c.execute("SELECT on_off_message, message_send FROM subitoit WHERE id_user = '" + str(call.message.chat.id) + "';")
                for on_off_message, message_send, in c.fetchall():
                    pass
                conn.close()
                status_message = on_off_message
                message_text = message_send
                db.dell_mess(call.message.chat.id, call.message.message_id)
                keys = types.InlineKeyboardMarkup()
                keys_1 = types.InlineKeyboardButton(text="<<", callback_data="pazar3_checker_back_"+str(id_parser)+"/"+str(number_ad-1))
                keys_2 = types.InlineKeyboardButton(text=str(number_ad)+" / "+str(count_ads), callback_data="checker_nothing" + str(id_parser))
                keys_3 = types.InlineKeyboardButton(text=">>", callback_data="pazar3_checker_next_" + str(id_parser) + "/"+str(number_ad+1))
                keys.add(keys_1, keys_2, keys_3)
                count_check = 1
                conn = sqlite3.connect("parser.db")
                c = conn.cursor()
                c.execute("SELECT title, url, price, name, number, img, gorod FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
                for title, url, price, name, number, img, gorod, in c.fetchall():
                    if count_check == number_ad:
                        count_views = -1
                        c.execute("SELECT id_user FROM parsed_url WHERE url = '" + str(url) + "';")
                        for id_user, in c.fetchall():
                            count_views += 1
                        if status_message == 'ON':
                            message_send = message_text.replace('[title]', title).replace('[link]', url)
                        else:
                            message_send = ''
                        bot.send_photo(chat_id, requests.get(img).content,
                                       caption=f"Название: <b>{title}</b>\n"
                                               f"Цена: <b>{price}</b>\n"
                                               f"Имя: <b>{name}</b>\n"
                                               f"Местоположение: <b>{gorod}</b>\n"
                                               f"Номер: <b>+{number}</b>\n\n"
                                               f'Объявление: <a href="'+str(url)+'">*Клик*</a>\n'
                                               f'WhatsApp: <a href="https://api.whatsapp.com/send?phone={number}&text={message_send}">*Клик*</a>\n'
                                               f'Viber: <a href="https://msng.link/o/?{number}=vi">*Клик*</a>\n\n'
                                               f"Видело пользователей: <b>{count_views}</b>",
                                       parse_mode="html", reply_markup=keys)
                    count_check += 1
                conn.close()
        elif "sbazar_checker_back_" in call.data:
            temp_1 = call.data.find('/')
            id_parser = int(call.data[20:temp_1])
            number_ad = int(call.data[temp_1 + 1:])
            chat_id = call.message.chat.id
            if number_ad == 0:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="🦋 Назад нельзя!")
            else:
                db.dell_mess(call.message.chat.id, call.message.message_id)
                conn = sqlite3.connect("options.db")
                c = conn.cursor()
                on_off_message = 'OFF'
                message_send = ''
                c.execute("SELECT on_off_message, message_send FROM sbazarcz WHERE id_user = '" + str(call.message.chat.id) + "';")
                for on_off_message, message_send, in c.fetchall():
                    pass
                conn.close()
                status_message = on_off_message
                message_text = message_send
                conn = sqlite3.connect("parser.db")
                c = conn.cursor()
                count_ads = 0
                c.execute("SELECT img FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
                for img, in c.fetchall():
                    count_ads += 1
                keys = types.InlineKeyboardMarkup()
                keys_1 = types.InlineKeyboardButton(text="<<",callback_data="sbazar_checker_back_" + str(id_parser) + "/" + str(number_ad - 1))
                keys_2 = types.InlineKeyboardButton(text=str(number_ad) + " / " + str(count_ads),callback_data="checker_nothing" + str(id_parser))
                keys_3 = types.InlineKeyboardButton(text=">>",callback_data="sbazar_checker_next_" + str(id_parser) + "/" + str(number_ad + 1))
                keys.add(keys_1, keys_2, keys_3)
                count_check = 1
                c.execute("SELECT title, url, price, name, number, count_max_online, count_max_offline, year, img, gorod FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
                for title, url, price, name, number, count_max_online, count_max_offline, year, img, gorod, in c.fetchall():
                    if count_check == number_ad:
                        count_views = -1
                        c.execute("SELECT id_user FROM parsed_url WHERE url = '" + str(url) + "';")
                        for id_user, in c.fetchall():
                            count_views += 1
                        if status_message == 'ON':
                            message_send = message_text.replace('[title]', title).replace('[link]', url)
                        else:
                            message_send = ''
                        bot.send_photo(chat_id, requests.get(img).content,
                                       caption=f"Название: <b>{title}</b>\n"
                                               f"Цена: <b>{price}</b>\n"
                                               f"Имя: <b>{name}</b>\n"
                                               f"Местоположение: <b>{gorod}</b>\n"
                                               f"Номер: <b>+{number}</b>\n\n"
                                               f'Объявление: <a href="' + str(url) + '">*Клик*</a>\n'
                                               f'WhatsApp: <a href="https://api.whatsapp.com/send?phone={number}&text={message_send}">*Клик*</a>\n'
                                               f'Viber: <a href="https://msng.link/o/?{number}=vi">*Клик*</a>\n\n'
                                               f"Видело пользователей: <b>{count_views}</b>",
                                       parse_mode="html", reply_markup=keys)
                    count_check += 1
        elif "sbazar_checker_next_" in call.data:
            temp_1 = call.data.find('/')
            id_parser = int(call.data[20:temp_1])
            number_ad = int(call.data[temp_1 + 1:])
            chat_id = call.message.chat.id
            conn = sqlite3.connect("parser.db")
            c = conn.cursor()
            count_ads = 0
            c.execute("SELECT img FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
            for img, in c.fetchall():
                count_ads += 1
            conn.close()
            if number_ad > count_ads:
                bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="🦋 Закончились!")
            else:
                conn = sqlite3.connect("options.db")
                c = conn.cursor()
                on_off_message = 'OFF'
                message_send = ''
                c.execute("SELECT on_off_message, message_send FROM sbazarcz WHERE id_user = '" + str(call.message.chat.id) + "';")
                for on_off_message, message_send, in c.fetchall():
                    pass
                conn.close()
                status_message = on_off_message
                message_text = message_send
                db.dell_mess(call.message.chat.id, call.message.message_id)
                keys = types.InlineKeyboardMarkup()
                keys_1 = types.InlineKeyboardButton(text="<<", callback_data="sbazar_checker_back_" + str(id_parser) + "/" + str(number_ad - 1))
                keys_2 = types.InlineKeyboardButton(text=str(number_ad) + " / " + str(count_ads),callback_data="checker_nothing" + str(id_parser))
                keys_3 = types.InlineKeyboardButton(text=">>", callback_data="sbazar_checker_next_" + str(id_parser) + "/" + str(number_ad + 1))
                keys.add(keys_1, keys_2, keys_3)
                count_check = 1
                conn = sqlite3.connect("parser.db")
                c = conn.cursor()
                c.execute("SELECT title, url, price, name, number, count_max_online, count_max_offline, year, img, gorod FROM parsed_url WHERE id_parser = '" + str(id_parser) + "';")
                for title, url, price, name, number, count_max_online, count_max_offline, year, img, gorod, in c.fetchall():
                    if count_check == number_ad:
                        count_views = -1
                        c.execute("SELECT id_user FROM parsed_url WHERE url = '" + str(url) + "';")
                        for id_user, in c.fetchall():
                            count_views += 1
                        if status_message == 'ON':
                            message_send = message_text.replace('[title]', title).replace('[link]', url)
                        else:
                            message_send = ''
                        bot.send_photo(chat_id, requests.get(img).content,
                                       caption=f"Название: <b>{title}</b>\n"
                                               f"Цена: <b>{price}</b>\n"
                                               f"Имя: <b>{name}</b>\n"
                                               f"Местоположение: <b>{gorod}</b>\n"
                                               f"Номер: <b>+{number}</b>\n\n"
                                               f'Объявление: <a href="' + str(url) + '">*Клик*</a>\n'
                                               f'WhatsApp: <a href="https://api.whatsapp.com/send?phone={number}&text={message_send}">*Клик*</a>\n'
                                               f'Viber: <a href="https://msng.link/o/?{number}=vi">*Клик*</a>\n\n'
                                               f"Видело пользователей: <b>{count_views}</b>",
                                       parse_mode="html", reply_markup=keys)
                    count_check += 1
                conn.close()
    except Exception as e:
        print(e)
        pass


while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(5)
