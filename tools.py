import re, signals, time, random

import cryptocompare

from emoji import emojize

import datetime

import sqlite3

from urllib.request import urlopen, Request

coins = []
map_coins = cryptocompare.get_coin_list()# type :
list_coins = list(map_coins.keys())

map_exchanges = cryptocompare.get_exchanges()
list_exchanges = list(map_exchanges.keys())

# ---------------------------------------------------------------
# SETUP VARIABLES

delay = datetime.timedelta(days=3)

# --------------------------------------------------------------------

boom = emojize(":boom:", use_aliases=True)
fire = emojize(":fire:", use_aliases=True)
zap = emojize(":zap:", use_aliases=True)
bar_chart = emojize(":bar_chart:", use_aliases=True)
uptrend_chart = emojize(":chart_with_upwards_trend:", use_aliases=True)
rocket = emojize(":rocket:", use_aliases=True)
warning = emojize(":warning:", use_aliases=True)
flag = emojize(":checkered_flag:", use_aliases=True)
signal_up = emojize(":signal_strength:", use_aliases=True)
mag = emojize(":mag:", use_aliases=True)



def parsing(text, list_keywords):
    signal = {}
    if any([text.find('#') != -1,text.find('Монета') != -1,text.find('/BTC') != -1]):
        words = re.split('\W+', text.upper())
        coins = list(set(words) & set(list_coins))
        if 'BTC' in coins: coins.remove('BTC')
        if len(coins)<2:
            coin = coins[0]
            i = words.index(coin)
            if words[i - 1] in list_keywords or words[i + 1] in list_keywords or words[i + 2] in list_keywords:
                symbol = coin + '/BTC'
                price_dict = cryptocompare.get_price(coin, curr='BTC')
                price = price_dict[coin]['BTC']
                exchanges = list(set(words) & set(list_exchanges))
                if 0 == len(exchanges): exchanges = ['All Exchanges']

                signal = signals.format_signal(symbol, exchanges, price)
    return signal

def check_signal(signal):
    conn = sqlite3.connect('signals.db')
    db = conn.cursor()
    if signal:
        t = (signal.get('symbol'),)
        query = db.execute("SELECT * FROM signals WHERE {idf}=?".\
                    format(idf='symbol'), t)
        rows = query.fetchall()
        data_signal = datetime.datetime.strptime(signal.get('data'), '%d/%m/%Y')
        for item in rows:
            data_row = datetime.datetime.strptime(item[8],'%d/%m/%Y')
            if data_signal < data_row + delay:
                return True

        db.execute("INSERT INTO Signals (symbol, exchanges, price, stoplost, short, mid, long, data) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",\
            (signal.get('symbol'),signal.get('exchanges'),signal.get('price'),signal.get('stoplost'),signal.get('short'),signal.get('mid'),signal.get('long'),signal.get('data')))
        conn.commit()
        conn.close()
        return False
    else: return False

# ---------------------------------------------------------
# NEW MESSAGE

def create_msg(signal):
    hdrs = {'User-Agent': 'Mozilla / 5.0 (X11 Linux x86_64) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 52.0.2743.116 Safari / 537.36'}
    offset = '"Description":"<p>'

    coin = signal.get('symbol')[:-4]
    market = map_coins.get(coin)
    logo = market.get('ImageUrl')
    url = "http://www.cryptocompare.com"+market.get('Url')

    feed_updated = False
    while feed_updated == False:
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            webpage = urlopen(req).read()
            feed_updated = True
        except:
            time.sleep(10)

    html = webpage.decode("utf8")
    html = html[html.find(offset)+offset.__len__():]
    html = html[:html.find('</p>')]

    symbol = "#"+coin+" / BTC\n\n"
    exchanges = "Buy at "+signal.get('exchanges')+"\n"

    entry_price = " Entry Point: "+ signal.get('price')
    stop_limit = " Stop Lost: "+ signal.get('stoplost')
    target_1 = "  Short Term --> Sell at "+ signal.get('short')
    target_2 = "  Mid Term --> Sell at "+ signal.get('mid')
    target_3 = "  Long Term --> Sell over "+ signal.get('long')

    rating = "Accurancy: " + str(random.randrange(6,9))

    desc = "Info: \n"+html

    msg = boom + boom + boom + "   NEW SIGNAL!!   " + flag + flag + flag + "\n\n"
    msg = msg + symbol + fire + fire + fire + fire +"\n\n"
    msg = msg + signal_up + entry_price + "\n\n"
    msg = msg + warning + stop_limit + "\n\n"
    msg = msg + uptrend_chart + " Profit Targets:\n"
    msg = msg + rocket + target_1 + "\n"
    msg = msg + rocket + rocket + target_2 + "\n"
    msg = msg + rocket + rocket + rocket + target_3 + "\n\n"
    msg = msg + mag + rating +"\n\n"
    msg = msg + signal_up + exchanges + "\n\n"
    msg = msg + bar_chart + "  " + bar_chart + "  " + bar_chart + "  " + bar_chart + "  " + bar_chart + "  " + bar_chart + "\n\n"
    msg = msg + desc +"\n\n"
    msg = msg + zap + "  " + zap + "  " + zap + "  " + zap + "  " + zap + "  " + zap

    return msg


if __name__ == '__main__':
    # TG_API_ID and TG_API_HASH *must* exist or this won't run!
    keys = ['BUY', 'COIN', 'SIGNALS', 'BTC', '\\u041c\\u041e\\u041d\\u0415\\u0422\\u0410', 'BUYING']

    msg1 = '#ICN :\n BUY: 2000-12920\n SELL: 13800-14600-15800\n STOP:NO\n BINANCE'

    msg = '#6-STRAT/BTC(All Exchange ) \n Buy Zone:0.00054/0.00058 \n Sell Zone: \n ' \
          '1-0.00067 \n 2-0.00076 \n 3-0.00092   монета'

           # if any([event.chat.username in list_channels, event.chat.title in list_titles]):
            # Analisi del messaggio
            # si ricava il segnale se il messaggio contiene un segnale
    segnale = parsing(msg, keys)
            # si verifica il segnale non è già stato elaborato

    if check_signal(segnale):
        print ('Segnale già elaborato')
    else:
        print('nuovo segnale')
        new_msg = create_msg(segnale)
        #query = db.execute('SELECT * FROM signals WHERE symbol=?', t)

