# Django Trading Bot
A bot trader with a Django interface for the [Binance](https://www.binance.com/en)'s markets. It's intended to work with cryptocurrencies [Bitcoin(BTC)](https://en.wikipedia.org/wiki/Bitcoin), [Etherum(Eth)](https://en.wikipedia.org/wiki/Ethereum) and [Binance coin(BNB)](https://www.investopedia.com/terms/b/binance-coin-bnb.asp), the latter allowing to benefit a 25% discount on [the transaction fees applied by Binance](https://www.binance.com/en/fee/schedule). If you want to use it with others, you’ll have to adapt the code...  
Completely ignoring fluctuations in the BTC/$, ETH/$ and BNB/$ markets, it's more a miner than a trader with the aim of generating BTC, ETH and BNB. So ***PAY ATTENTION*** to its use if you want to get rich with profits in $.  
Finally, you need a binance account with a minimum balance of 1.05 BNB and the equivalent in BTC and ETH.
> For example, if the price on BNB/BTC market is 0.0026057 and 0.138650 on BNB/ETH market  
> you must have at least 0.00278985 BTC, 0.1455825 ETH and 1.05 BNB
## Trading strategy
To be clear, ***I am not a trader***. So the following strategy may seem simplistic. Don’t hesitate to improve it and let me know if it does.
## Instalation
## Create a PostgreSQL database for the application and a new user
*!!! maybe you have to install [PostgreSQL](https://www.postgresql.org/) !!!*
Connect to PostgreSQL client, create database and new user with privileges:
```shell
$ sudo su - postgres
postgres@somewhere:~$ psql
postgres=# CREATE USER "django_trading_bot";
postgres=# ALTER USER django_trading_bot WITH PASSWORD 'cool';
postgres=# CREATE DATABASE "db_django_trading_bot";
postgres=# GRANT ALL PRIVILEGES ON DATABASE db_django_trading_bot TO django_trading_bot;
postgres=# \q
postgres@somewhere:~$ exit
```
## Clone the application and install the necessary requirements
Clone the folder, go inside, create a virtual environment for Python with virtualenv (*!!! maybe you have to install [virtualenv](https://virtualenv.pypa.io/en/stable/) !!!*), use it, and install all necessary dependencies ([django](https://www.djangoproject.com/foundation/), [django-debug-toolbar](https://django-debug-toolbar.readthedocs.io/en/stable/), [psycopg2-binary](https://pypi.org/project/psycopg2-binary/), [python-binance](https://python-binance.readthedocs.io/en/latest/)):
For python-binance, you need to install python3-dev.
```shell
$ sudo apt-get install python3-dev
$ git clone https://github.com/JBthePenguin/DjangoTradingBot.git
$ cd DjangoTradingBot
$ virtualenv -p python3 env
$ source env/bin/activate
(env)$ pip install -r requirements.txt
```
## Create tables
Make the migrations:
```shell
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```
## Admin site
Create a "superuser" account:
```shell
(env)$ python manage.py createsuperuser
``` 
## Start and use the Application
```shell
(env)$ python manage.py runserver
```
Before using the application, you have to connect to the admin site:
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin)
...and create one bot (don't check is_working and set the quantity of BNB to trade) and before start it, create binance keys (your API and Secret keys), three currencies ('BTC' -> 1, ETH -> 2, BNB -> 3), three markets ('BNBBTC' -> 1, 'ETHBTC' -> 2, 'BNBETH' -> 3), two banks (one with name 'now' and the other 'start') with the same amounts (your start bank), one offset (trade_number -> 1, bnb -> 0, btc -> 0, eth -> 0.001) and one error (type -> 'error').

**NOW, with your favorite browser, go to this url [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to see the visitor interface and [http://127.0.0.1:8000/admin/visitorapp/bot/](http://127.0.0.1:8000/admin/visitorapp/bot/) to start and stop the bot from the admin site**

## DISCLAIMER

I am not responsible for anything done with this bot. You use it at your own risk.
There are no warranties or guarantees expressed or implied. You assume all responsibility and liability.
