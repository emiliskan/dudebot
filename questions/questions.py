from random import shuffle
from requests import get
from telebot import TeleBot
from settings import settings
from pydub import AudioSegment
from mongo import mongo
import os


def save_questions(sended_voices):
    """
    clears and saves questions to bd
    neded in upload module

    params:
        sended_voices - array of tuple - questions id's on telegram
    example: 
        [{id: "", file: "fart.mp3"}, {id: "", file: "jerkoff.mp3"}]
    """
    if mongo.clear_values("questions"):
        mongo.add_values("questions", sended_voices)
        return True

    return False


def get_questions():
    collection = mongo.get_values("questions")
    questions = []
    for current in collection:
        questions.append(current["id"])

    shuffle(questions)
    return questions[:5]


def get_the_last_question():
    # he always asks one question at the end
    return "AwACAgIAAxkDAAIB2V-6gbx4xTx9kDSiuMxxRRSCJXl2AAL7CgACSHTYSZsG1PijxVvfHgQ"


def make_interview(chat_id):
    questions = get_questions()
    questions.append(get_the_last_question())

    mongo.clear_values("user_questions_queue")
    user_questions = {
        "chat_id": chat_id,
        "questions": questions,
        "answers": []
    }

    mongo.add_value("user_questions_queue", user_questions)

    return questions[0]  # return the first


def get_user_questions(chat_id):
    return mongo.get_values("user_questions_queue", {"chat_id": chat_id})


def save_new_answer(chat_id, answer_file_id):
    user_questions = get_user_questions(chat_id)

    if len(user_questions) >= 1:
        user_questions = user_questions[0]
    else:
        return 1  # not started yet

    answers = user_questions['answers']
    questions = user_questions['questions']

    answers.append(answer_file_id)
    mongo.update_value("user_questions_queue", {"chat_id": chat_id}, user_questions)

    if len(answers) == len(questions):
        return 2  # we asked all

    return questions[len(answers)]


def started_inreview(chat_id):
    return len(get_user_questions(chat_id)) >= 1


def get_finish_file(chat_id):
    bot = TeleBot(settings.TOKEN)

    user_questions = get_user_questions(chat_id)[0]

    mongo.clear_values("user_questions_queue")

    files_ids = []
    answers_count = len(user_questions['answers'])

    if answers_count == 0:
        return False

    for i in range(0, answers_count):
        questionFileId = user_questions["questions"][i]
        files_ids.append(bot.get_file(questionFileId))

        answerFileId = user_questions["answers"][i]
        files_ids.append(bot.get_file(answerFileId))

    files = []
    cur_dir = os.getcwd()
    for file_info in files_ids:
        file_name = "{}\\finish_files\\{}_v.ogg".format(cur_dir, file_info.file_id)
        if not os.path.exists(file_name):  #
            r = get('https://api.telegram.org/file/bot{0}/{1}'.format(
                settings.TOKEN, file_info.file_path))
            open(file_name, "wb").write(r.content)

        files.append(file_name)

    if len(files) == 0:
        return False

    finish_file = AudioSegment.empty()
    for voice in files:
        finish_file += AudioSegment.from_ogg(voice)
        os.remove(voice)

    file_name = cur_dir + "/finish_files/{}_finish_file.ogg".format(chat_id)
    return finish_file.export(file_name, format="ogg", bitrate="192k")
