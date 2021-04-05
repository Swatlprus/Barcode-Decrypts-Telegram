from pyzbar.pyzbar import decode
from PIL import Image
import telebot

token = '' # Токен Telegram бота

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет. Отправь фотографию в хорошем качестве со штрих-кодом') # Функция для приема фотографии со штрих-кодом

@bot.message_handler(content_types= ["photo"])
def barcode(message):
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path) # Скачиваем фотографию, которую нам прислал пользователь

    src = file_info.file_path; # Путь к файлу
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Фотография принята")

    # Пробуем распознать принятую фотографию
    try:
        image_barcode = Image.open(src)
        decoded = decode(image_barcode)
        bot.send_message(message.chat.id, 'Штрих-код продукта: ' + decoded[0].data.decode('utf-8'))
    except Exception as e:
        bot.reply_to(message,'Не удалось распознать штрих-код. Попробуйте другую фотографию')

bot.polling()
