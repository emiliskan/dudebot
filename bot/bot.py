from telebot import TeleBot, types
from settings import settings
from questions import questions

bot = TeleBot(settings.TOKEN, parse_mode=None)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    text = 'привет {}, я Дудь и сегодня возьму у тебя интервью. Жми начать'.format(message.chat.id)
    keyboard = button("начать")
    bot.send_message(message.chat.id, text, reply_markup=keyboard)

@bot.message_handler(func=lambda message: True)
def echo_all(message):

    chat_id = message.chat.id

    if message.text == "начать":
        finish(chat_id) # finish if there is started interview

        text = "отлично, я буду присылать вопрос, а ты мне отвечай аудиосообщением"
        keyboard = button("завершить")
        bot.send_message(chat_id, text, reply_markup=keyboard)

        first_voice = questions.make_interview(chat_id)
        bot.send_voice(chat_id, first_voice)
    elif message.text == "завершить":
        finish(chat_id)
    else:
        keyboard = button("начать")
        bot.send_message(chat_id, "не понял")        

@bot.message_handler(content_types=['voice'])
def handle_voice(message):

    chat_id = message.chat.id

    next_question = questions.save_new_answer(chat_id, message.voice.file_id)
   
    if next_question == 1:
        keyboard = button("начать") 
        bot.send_message(chat_id, "Интервью не начато, начнем?", reply_markup=keyboard)
    elif next_question == 2:
        finish(chat_id)
    else:
        bot.send_voice(chat_id, next_question)


def button(text):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    start_button = types.KeyboardButton(text)
    keyboard.add(start_button)  

    return keyboard

def finish(chat_id):

    if not questions.started_inreview(chat_id):
        return

    bot.send_message(chat_id, "подожди, я соберу в один файл")
    
    finish_voice = questions.get_finish_file(chat_id)

    keyboard = button("начать")

    if not finish_voice:
        bot.send_message(chat_id, "что-то пошло не так", reply_markup=keyboard)  
        return 

    bot.send_message(chat_id, "готово, лови", reply_markup=keyboard)  

    bot.send_voice(chat_id, finish_voice)

def start():
    bot.polling()
