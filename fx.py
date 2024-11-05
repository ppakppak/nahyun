from currency_converter import CurrencyConverter
import datetime
import csv
from dp import *

HIST_CURRENCY = []
BASE_CURRENCY = ['EUR','USD','JPY','GBP','AUD','CAD','CHF','CNY','SEK','MXN','NZD','SGD','HKD','NOK','KRW']
CURRENCY_PAIR = []

PAIR_DATA = []

def make_rate_db():
    for pair in CURRENCY_PAIR:
        try:
            if pair[0] == 'EUR':
                idx1 = -1
            else:
                idx1 = HIST_CURRENCY[0].index(pair[0])
            idx2 = HIST_CURRENCY[0].index(pair[1])  
            values = []
            for i in range(1, len(HIST_CURRENCY)):  
                if pair[0] == 'EUR':
                    rate = float(HIST_CURRENCY[i][idx2])   
                    values.append(round(rate,5))
                else:   
                    s = float(HIST_CURRENCY[i][idx1])
                    t = float(HIST_CURRENCY[i][idx2])
                    w = 1/s
                    rate = t*w
                    values.append(round(rate,5))
            
            PAIR_DATA.append(values)
            
        except Exception as e:
            PAIR_DATA.append(values)
            print(pair[0], pair[1], len(values))
            continue

def make_rev_rate_db():
    for pair in CURRENCY_PAIR:
        try:
            if pair[0] == 'EUR':
                idx1 = -1
            else:
                idx1 = REVERSED_HIST[0].index(pair[0])
            idx2 = REVERSED_HIST[0].index(pair[1])  
            values = []
            for i in range(1, len(REVERSED_HIST)):  
                if pair[0] == 'EUR':
                    rate = float(REVERSED_HIST[i][idx2])   
                    values.append(round(rate,5))
                else:   
                    s = float(REVERSED_HIST[i][idx1])
                    t = float(REVERSED_HIST[i][idx2])
                    w = 1/s
                    rate = t*w
                    values.append(round(rate,5))
            
            PAIR_DATA.append(values)
            
        except Exception as e:
            PAIR_DATA.append(values)
            print(pair[0], pair[1], len(values))
            continue
            


def get_rate(_from, _to, _date):
    try:
        for i in range(1, len(HIST_CURRENCY)):
            if HIST_CURRENCY[i][0] == _date:
                break

        idx1 = HIST_CURRENCY[0].index(_from)
        idx2 = HIST_CURRENCY[0].index(_to)
        s = float(HIST_CURRENCY[i][idx1])
        t = float(HIST_CURRENCY[i][idx2])
        w = 1/s
        rate = t*w
    except Exception as e:
        if _from == 'EUR':
            rate = HIST_CURRENCY[i][idx2]
        else:
            rate = HIST_CURRENCY[i][idx1]
    return rate

def get_rev_rate(_from, _to, _date):
    try:
        for i in range(1, len(REVERSED_HIST)):
            if REVERSED_HIST[i][0] == _date:
                break

        idx1 = REVERSED_HIST[0].index(_from)
        idx2 = REVERSED_HIST[0].index(_to)
        s = float(REVERSED_HIST[i][idx1])
        t = float(REVERSED_HIST[i][idx2])
        w = 1/s
        rate = t*w
    except Exception as e:
        if _from == 'EUR':
            rate = REVERSED_HIST[i][idx2]
        else:
            rate = REVERSED_HIST[i][idx1]
    return rate

def init():
    global REVERSED_HIST
    for i in range(0, len(BASE_CURRENCY)-1):
        from_cur = BASE_CURRENCY[i]
        for j in range(i+1,len(BASE_CURRENCY)):
            to_cur = BASE_CURRENCY[j]
            CURRENCY_PAIR.append([from_cur, to_cur])

    filename = 'eurofxref-hist.csv'
    with open(filename, encoding='utf8', newline='') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            HIST_CURRENCY.append(list(row))
            #print(row)
        HIST_CURRENCY.reverse()
        HIST_CURRENCY.insert(0, HIST_CURRENCY[-1])
        HIST_CURRENCY.pop()

# CurrencyConverter を利用した USD-JPY 為替
def get_currencyconverter_rate() :
    res0 = CurrencyConverter()
    crate = res0.convert(1, 'USD', 'JPY',date=datetime.date(2024, 5, 24))
    print("CurrencyConverter を利用した USD-JPY 為替 ---> ", round(crate, 2), "\n")

def get_partial_data(_pair, _start, _end):
    idx = CURRENCY_PAIR.index(_pair)
    p_data = PAIR_DATA[idx][_start:_end]
    return p_data

# メイン
if __name__ == '__main__':
    #get_currencyconverter_rate()
    init()
    make_rate_db()
    dt = get_partial_data(['USD', 'KRW'], 0, 90)
    dt1 = get_partial_data(['GBP', 'KRW'], 90, 180)
    res = funcDP(0.2, dt,dt,dt,len(dt),dt1,dt1,dt1,len(dt1))
    print()
    # for pair in CURRENCY_PAIR:
    #     get_rate(pair[0], pair[1],'2024-05-24')

    