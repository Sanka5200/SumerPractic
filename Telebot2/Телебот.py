import telebot, requests
from telebot import types
from bs4 import BeautifulSoup

bot = telebot.TeleBot('6091834368:AAEteMCszZrPp7u2s_p08CxLXwa1gyTCuWw')

@bot.message_handler(commands=['start'])
def start(message):
    mess= f'Жду <b>/help</b>, {message.from_user.first_name} {message.from_user.last_name}'
    bot.send_message(message.chat.id, mess, parse_mode='html')
@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(""))
    bot.send_message(message.chat.id, 'Вау OuO')
@bot.message_handler(commands=['help'])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button0 = types.KeyboardButton("Изменения в расписании")
    button1 = types.KeyboardButton("Привет")
    markup.add(button0,button1)
    bot.send_message(message.chat.id, "Команды бота:", reply_markup=markup)
@bot.message_handler()
def get_user_text(message):
    if message.text == "Привет":
        bot.send_message(message.chat.id, "Приветик", parse_mode='html')
    elif message.text == "Изменения в расписании":
        need = []
        page = []
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://studydep.miigaik.ru',
            'Referer': 'http://studydep.miigaik.ru/semestr/index.php',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 YaBrowser/23.5.4.674 Yowser/2.5 Safari/537.36',
        }

        response = requests.post('http://studydep.miigaik.ru/semestr/index.php', headers=headers,
                                 verify=False)

        soup = BeautifulSoup(response.text, "html.parser")

        page = soup.findAll('td', class_='left-content')
        for need in page:
            if need.find('strong') is not None:
                our_string = str(need.text)
        our_string = our_string.split("Верхняя", 1)[1]
        our_string = our_string.replace("\n", "")
        our_string = our_string.replace("\r", "")
        if our_string == "За последние 24 часа были внесены изменения в расписание занятий для следующих групп:":
            bot.send_message(message.chat.id, 'Изменений в расписании нет', parse_mode='html')
        else:
            bot.send_message(message.chat.id, our_string, parse_mode='html')
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю", parse_mode='html')
bot.polling (none_stop=True)