import pymongo
from settings import settings

client = pymongo.MongoClient(settings.DBCONNECT)
db = client.dude