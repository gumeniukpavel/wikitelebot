from telebot import types, TeleBot
import wikipedia

bot = TeleBot('899161541:AAFTse3SCtDR1P0tN-s8mLpgbXdd7t-mud4')

lang = 'uk'
lang_mess = 'українська'


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Введи свій пошуковий запит', )


@bot.message_handler(commands=['changelang'])
def change_lang_message(message):
    keyboard = types.InlineKeyboardMarkup()
    key_uk = types.InlineKeyboardButton(text='Українська', callback_data='uk')
    keyboard.add(key_uk)
    key_ru = types.InlineKeyboardButton(text='Русский', callback_data='ru')
    keyboard.add(key_ru)
    key_en = types.InlineKeyboardButton(text='English', callback_data='en')
    keyboard.add(key_en)
    bot.send_message(message.chat.id, 'Виберіть мову пошуку', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global lang
    lang = call.data
    bot.send_message(call.message.chat.id, 'Мову пошуку змінено', )


@bot.message_handler(commands=['getlang'])
def change_lang_message(message):
    global lang_mess
    if lang == 'uk':
        lang_mess = 'українська'
    if lang == 'ru':
        lang_mess = 'російська'
    if lang == 'en':
        lang_mess = 'англійська'

    bot.send_message(message.chat.id, 'Ваша мова пошуку ' + lang_mess)


@bot.message_handler(content_types=['text'])
def send_text(message):
    wikipedia.set_lang(lang)
    keyboard = types.ReplyKeyboardMarkup(True, True)
    search_results = wikipedia.search(message.text)
    if search_results:
        for i in search_results:
            if i.lower() == message.text.lower():
                bot.send_message(message.chat.id, wikipedia.summary(i))
                return
            keyboard.add(i)
        bot.send_message(message.chat.id, 'Натисни на потрібний запит: ', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, 'Нічого не знайдено!')


@bot.message_handler(content_types=['sticker'])
def sticker_id(message):
    bot.send_sticker(message.chat.id, message.sticker.file_id)


bot.polling()
