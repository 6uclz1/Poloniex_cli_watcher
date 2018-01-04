# system
import sys
import os
import time

# pip
import json
import poloniex
from termcolor import colored
import requests
import numpy as np
from tabulate import tabulate

POLO = poloniex.Poloniex()
URL = 'https://api.coinmarketcap.com/v1/global/'

CRYPTS = ['USDT_BTC',
          'USDT_XRP',
          'USDT_ETH',
          'USDT_ETC',
          'USDT_LTC',
          'BTC_XEM']

headers = ['crypt_name', 'last_price', 'change_per', 'per_bar']
crypt_list = []


def min_max(x, axis=None):
    min = x.min(axis=axis, keepdims=True)
    max = x.max(axis=axis, keepdims=True)
    result = (x-min)/(max-min)
    return result


def CRYPTO_parser(CRYPTO, crypt_name):
    percentChange = float(CRYPTO['percentChange'])
    percentChange = percentChange * 100
    if percentChange > 0:
        colored_percentChange = colored(percentChange, 'green')
    else:
        colored_percentChange = colored(percentChange, 'red')

    last_low_high_price = np.array([float(CRYPTO['last']),
                                    float(CRYPTO['low24hr']),
                                    float(CRYPTO['high24hr'])])
    last_low_high_price = min_max(last_low_high_price)
    last_price_percent = int(round(last_low_high_price[0] * 100, 0))
    last_price_place = int((last_price_percent // 5) - 1)
    percent_bar = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                   '-', '-', '-', '-', '-', '-', '-', '-', '-']
    percent_bar.insert(last_price_place, ' + ')
    bar = str(''.join(map(str, percent_bar)))
    crypt_list = [crypt_name, CRYPTO['last'], colored_percentChange, bar]
    return crypt_list


while True:
    CRYPTS_list = []
    resp = requests.get(url=URL)
    data = json.loads(resp.text)
    for crypt in CRYPTS:
        crypt_ticker = POLO.returnTicker()[crypt]
        crypt_list = CRYPTO_parser(crypt_ticker, crypt)
        CRYPTS_list.append(crypt_list)
    print ('')
    print tabulate(CRYPTS_list, headers, tablefmt="fancy_grid")
    sys.stdout.write('total market cap : ')
    print('%f' % data['total_market_cap_usd'])
    sys.stdout.write('24h volume       :  ')
    print('%f' % data['total_24h_volume_usd'])
    print('')
    time.sleep(30)
    os.system('cls' if os.name == 'nt' else 'clear')
