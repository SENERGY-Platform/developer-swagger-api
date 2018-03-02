from pymongo import MongoClient
import os 

db = MongoClient('mongodb://{host}:{port}/'.format(host=os.environ["DB_HOST"], port=os.environ["DB_PORT"]))
