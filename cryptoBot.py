# Author: Raffaele Perini
#
# Simple app to monitor and store trends for three cryptocurrency using the following urls:
#    * Bitcoin: https://api.cryptonator.com/api/ticker/btc-usd
#    * Ethereum: https://api.cryptonator.com/api/ticker/eth-usd
#    * Ripple: https://api.cryptonator.com/api/ticker/xrp-usd
#
# Backed using mongoDB:
#   Database: crypto
#   Collection: cr_coll
#
# Data example:
#   {
#    'ticker': 
#          {'base': 'BTC', 
#           'target': 'USD', 
#           'price': '7312.28296110', 
#           'volume': '184418.36463947', 
#           'change': '-11.39511328'}, 
#    'timestamp': 1586270762, 
#    'success': True, 
#    'error': ''
#   }
#


import datetime
import asyncio

import requests 
import json

from pymongo import MongoClient
from bson.json_util import dumps

from multiprocessing import Process,Queue,Pipe
from sender import send


MAIN_URL = 'https://api.cryptonator.com/api/ticker/'

URLs = {'btc-usd', 'eth-usd', 'xrp-usd'}

DELAY_SECONDs = 10

MONGO_CLIENT = MongoClient('mongodb://localhost:27017/')

HEADERS = { 'User-Agent' : 'Ubuntu', # It doens't work without this idkw ¯\_(ツ)_/¯
            'accept':'text/json',
            'content-type':'text/json' }

 
def queryApi(url, headers=HEADERS):
    " Query and return data into JSON format"

    r = requests.get(url = url, headers = headers) 
    if r.status_code == 200:
        data =  r.json() 
        return data
    else:
        return 'Something wrong with the query...'


def storeToMongo(data, mongo_client = MONGO_CLIENT):
    " Store data into Mongo and return id, dummy names for db(=crypto) and collection(=cr_coll)"

    db = mongo_client.crypto
    collection = db.cr_coll
    id = collection.insert_one(data).inserted_id 
    return str(id)


def checkHowManyElements(mongo_client = MONGO_CLIENT):
    " Check how many elements in the db"

    db = mongo_client.crypto
    collection = db.cr_coll
    print('Number of elements: ' + str(collection.count_documents({})))
    return collection.count_documents({})


async def monitoringTask(mongo_client = MONGO_CLIENT):
    ''' Check each URl in URLs, every DELAY_SECONDs, store everything, if reached 10 elements
        the processingTask is notified. '''

    print('-> Monitoring task checked at: ' + str(datetime.datetime.now()))
    for u in URLs:
        storeToMongo(queryApi(MAIN_URL + u)) # Store data

    if checkHowManyElements() > 10:
        await asyncio.create_task(processingTask())# Call processing task
    
    await asyncio.sleep(DELAY_SECONDs)


async def processingTask( mongo_client = MONGO_CLIENT):
    " Pack all the data, serialize it, send it to the Sender and delete from the db "

    print('-> Processing task started at: ' + str(datetime.datetime.now()))
    db = mongo_client.crypto
    collection = db.cr_coll

    # Serialization with bson
    elements = dumps(collection.find()) 

    # Send to sender
    parent_conn, child_conn = Pipe()
    p = Process(target=send, args=(child_conn, elements))
    p.start()
    print(parent_conn.recv()) # Everything went fine

    # Delete all
    collection.delete_many  ({})


async def main():
    print('::::: CryptoBot started at: ' + str(datetime.datetime.now()) + ' :::::')
    
    while True:
        await asyncio.create_task(monitoringTask())
    

# Run
asyncio.run(main())