import pymongo
from settings import settings

client = pymongo.MongoClient(settings.DBCONNECT)
database = client.dudebot