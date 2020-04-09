# Cryptocurrency-checker
Simple app to monitor trends for different cryptocurrencies

## Requirements

* python  >3.7


## How to deploy

First, download and run the MongoDB server:

    $ docker pull mongo

    $ docker run -d -p 27017-27019:27017-27019 --name mongodb mongo

Install requirements:

    $ pip install -r requirements.txt 

In **one** terminal run the endpoint:

    $ python endpoint.py

Then in **another** terminal run the cryptoBot:

    $ python cryptoBot.py

    
