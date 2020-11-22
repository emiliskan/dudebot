import sys
sys.path.append("/settings")
sys.path.append("/bot")
sys.path.append("/questions")
sys.path.append("/db")

from bot import bot

bot.start()