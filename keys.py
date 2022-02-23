# -*- coding: utf-8 -*-

from telebot import types


def main():
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key.add("☠️ Сервисы")
    key.add("💼 Профиль", "⚙️ Настройки")
    key.add("👾 Помощь")
    return key


def agree():
    key = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text="✅ Ознакомлен", callback_data="agree_start")
    key.add(key_1)
    return key


def prof():
    key = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text="🤖 Рефералы", callback_data="ref_prof")
    key_2 = types.InlineKeyboardButton(text="💰 Пополнение", callback_data="balance_prof")
    key_3 = types.InlineKeyboardButton(text="🦋 Подписки", callback_data="subs")
    key.add(key_1, key_2)
    key.add(key_3)
    return key


def check_sub():
    key = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text="⭐️ Проверить подписку", callback_data="check_sub")
    key.add(key_1)
    return key


def back_prof():
    key = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text="↩️ Вернуться", callback_data="back_prof")
    key.add(key_1)
    return key


def back_pay_in():
    key = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text="❌ Отмена", callback_data="back_pay_in")
    key.add(key_1)
    return key


def services():
    key = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text="🇵🇹 OLX.pt", callback_data="olx_pt")
    key_2 = types.InlineKeyboardButton(text="🇵🇱 OLX.pl", callback_data="olx_pl")
    key_3 = types.InlineKeyboardButton(text="🇷🇴 OLX.ro", callback_data="olx_ro")
    key_4 = types.InlineKeyboardButton(text="🇰🇿 OLX.kz", callback_data="olx_kz")
    key_5 = types.InlineKeyboardButton(text="🇧🇬 OLX.bg", callback_data="olx_bg")
    key_6 = types.InlineKeyboardButton(text="🇺🇦 OLX.ua", callback_data="olx_ua")
    key_7 = types.InlineKeyboardButton(text="🇮🇹 Subito.it", callback_data="subito_it")
    key_8 = types.InlineKeyboardButton(text="🇲🇰 Pazar3.mk", callback_data="pazar3_mk")
    key_9 = types.InlineKeyboardButton(text="🇨🇿 Sbazar.cz", callback_data="sbazar_cz")
    key_last = types.InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
    key.add(key_1, key_2, key_3)
    key.add(key_4, key_5, key_6)
    key.add(key_7, key_8)
    key.add(key_9)
    key.add(key_last)
    return key


def close():
    key = types.InlineKeyboardMarkup()
    key_last = types.InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
    key.add(key_last)
    return key


def buy_sub(service):
    key = types.InlineKeyboardMarkup()
    key_last = types.InlineKeyboardButton(text="Купить", callback_data="buy_"+str(service))
    key.add(key_last)
    return key


def buynow(service):
    key = types.InlineKeyboardMarkup()
    key_1= types.InlineKeyboardButton(text="🦋 3 дня - 400р", callback_data="buynow3_" + str(service))
    key_2 = types.InlineKeyboardButton(text="🦋 7 дней - 800р", callback_data="buynow7_" + str(service))
    key_3 = types.InlineKeyboardButton(text="🦋 31 день - 2000р", callback_data="buynow31_" + str(service))
    key_last = types.InlineKeyboardButton(text="↩️ Вернуться", callback_data="back_services")
    key.add(key_1)
    key.add(key_2)
    key.add(key_3)
    key.add(key_last)
    return key


def cancel():
    key = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text="❌ Отмена", callback_data="close")
    key.add(key_1)
    return key


def settings_main(service):
    key = types.InlineKeyboardMarkup()
    key_1= types.InlineKeyboardButton(text="Сообщение", callback_data="main_messages_" + str(service))
    if service == 'pazar3mk' or service == "sbazarcz":
        pass
        key.add(key_1)
    else:
        key_2 = types.InlineKeyboardButton(text="Год создания", callback_data="main_year_" + str(service))
        key.add(key_1, key_2)
    key_last = types.InlineKeyboardButton(text="↩️ Вернуться", callback_data="back_main_settings")
    if service == 'subitoit':
        key_3 = types.InlineKeyboardButton(text="Активные", callback_data="max_online_ads_" + str(service))
        key_4 = types.InlineKeyboardButton(text="Завершенные", callback_data="max_offline_ads_" + str(service))
        key.add(key_3, key_4)
    elif service == 'pazar3mk':
        pass
    else:
        key_3 = types.InlineKeyboardButton(text="Количество объявлений", callback_data="max_ads_" + str(service))
        key.add(key_3)
    key.add(key_last)
    return key


def main_messages(service):
    key = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text="Вкл/Выкл сообщение", callback_data="change_status_" + str(service))
    key_2 = types.InlineKeyboardButton(text="Изменить текст", callback_data="change_text_" + str(service))
    key_last = types.InlineKeyboardButton(text="❌ Закрыть", callback_data="close")
    key.add(key_1, key_2)
    key.add(key_last)
    return key


def take_sub(hours):
    key = types.InlineKeyboardMarkup()
    key_1 = types.InlineKeyboardButton(text="🇵🇹 OLX.pt", callback_data="olx_pt_"+str(hours))
    key_2 = types.InlineKeyboardButton(text="🇵🇱 OLX.pl", callback_data="olx_pl_" + str(hours))
    key_3 = types.InlineKeyboardButton(text="🇷🇴 OLX.ro", callback_data="olx_ro_" + str(hours))
    key_4 = types.InlineKeyboardButton(text="🇰🇿 OLX.kz", callback_data="olx_kz_" + str(hours))
    key_5 = types.InlineKeyboardButton(text="🇧🇬 OLX.bg", callback_data="olx_bg_" + str(hours))
    key_6 = types.InlineKeyboardButton(text="🇺🇦 OLX.ua", callback_data="olx_ua_" + str(hours))
    key_7 = types.InlineKeyboardButton(text="🇮🇹 Subito.it", callback_data="subito_it_" + str(hours))
    key_8 = types.InlineKeyboardButton(text="🇲🇰 Pazar3.mk", callback_data="pazar3_mk_" + str(hours))
    key_9 = types.InlineKeyboardButton(text="🇨🇿 Sbazar.cz", callback_data="sbazar_cz_" + str(hours))
    key.add(key_1, key_2, key_3)
    key.add(key_4, key_5, key_6)
    key.add(key_7, key_8)
    key.add(key_9)
    return key
