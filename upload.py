import sys
sys.path.append("/settings/")
sys.path.append("/questions/")

import telebot, os 
from settings import settings
from questions import questions

bot = telebot.TeleBot(settings.TOKEN, parse_mode=None)
MYID = settings.MYID

sended_voices = []
for file in os.listdir("voices/"):
    question = open("voices/" + file, mode="rb")
    result = bot.send_voice(MYID, question)
    voice = {
        "id": result.voice.file_id,
        "file": file
    }
    sended_voices.append(voice)

questions.save_questions(sended_voices)

