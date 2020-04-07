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
import requests 
from pymongo import MongoClient


MAIN_URL = 'https://api.cryptonator.com/api/ticker/'

URLs = {'', '', ''}

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


def monitoringTask():
    " Check each URl in URLs, every DELAY_SECONDs"
    return 1

def main():
    print(':::::CryptoBot started at: ' + str(datetime.datetime.now()) + ':::::')
    final_urll = MAIN_URL + 'btc-usd'
    print(storeToMongo(queryApi(url= final_urll)))


if __name__ == "__main__":
    main()