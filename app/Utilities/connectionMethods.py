import mysql.connector
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# REPLACE WITH YOUR CREDENTIALS - THROUGOUT, YOU NEED TO SWAP OUT YOUR DATABASE AND TABLE NAMES
# YOU CAN DO A FIND AND REPLACE FOR mydatabase AND USERS1

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Dpreston123!!",
    database="mydatabase"
)
cur = mydb.cursor()

def getMongoPointer():
    uri = "mongodb+srv://msdsmichael:msdsmichael@cluster0.usgmik3.mongodb.net/?retrywrites=true&w=majority"

    client = MongoClient(uri, server_api=ServerApi('1'))

    try:
        client.admin.command('ping')
    except Exception as e:
        print(e)

    return client

def getmySQLPointer():
    return cur

def getTweetsDB():
    return getMongoPointer()["Twitter"]["Tweets"]

def commit():
    mydb.commit()