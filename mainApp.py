from telebot import types, TeleBot
import wikipedia

bot = TeleBot('899161541:AAFTse3SCtDR1P0tN-s8mLpgbXdd7t-mud4')
wikipedia.set_lang('uk')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Введи свій пошуковий запит', )


@bot.message_handler(content_types=['text'])
def send_text(message):
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
