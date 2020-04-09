# Author Raffaele Perini
#
# Simple process which wait to be notify by crypto and send the info to an endpoint
#

import datetime
import requests

from multiprocessing import Process,Pipe


URL = 'http://0.0.0.0:5000/cryptos'

HEADERS = { 'auth_token' : '12aw3serxdcrftg987h', # Authentication token
            'accept':'application/json',
            'content-type':'application/json' }


def send(child_conn, data):
    " Send data to the end point"
     
    print('::::: Sender started at: ' + str(datetime.datetime.now()) + ' :::::')
    
    r = requests.post(url = URL, headers = HEADERS, data = data) 
    msg = "Everything sent to the endpoint"
    if not r.text == 'ok':
        msn = 'Something wrong with the query...'

    child_conn.send(msg)
    child_conn.close()