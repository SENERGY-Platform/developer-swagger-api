from pymongo import MongoClient
import os 

client = MongoClient('mongodb://{host}:{port}/'.format(host=os.environ["DB_HOST"], port=os.environ["DB_PORT"]))
db = client.swagger