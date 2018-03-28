from os.path import isfile
import sqlite3 as lite
import datetime

if __name__ == '__main__':
    if not isfile('signals.db'):
        print ('Init DB...')
        conn = lite.connect('signals.db')

        c = conn.cursor()

        # Create table
        c.execute("DROP TABLE IF EXISTS Signals")
        c.execute("CREATE TABLE Signals(id INTEGER PRIMARY KEY, symbol TEXT, exchanges TEXT, price TEXT, stoplost TEXT, short TEXT, mid TEXT, long TEXT, data TEXT)")
        conn.commit()

        conn.close()

        conn = lite.connect('signals.db')
        c = conn.cursor()

        c.execute("INSERT INTO Signals(symbol, exchanges, price, stoplost, short, mid, long, data) VALUES ('BTC/BTC','All Exchange','0.000','0.000','0.000','0.000','0.000','00000')")

        c.execute("INSERT INTO Signals(symbol, exchanges, price, stoplost, short, mid, long, data) VALUES ('STRAT/BTC', 'All Exchanges', '0.000568', '0.000510', '0.000620', '0.000730', '0.000850', '20/03/2018')")
        conn.commit()

        conn.close()

        conn = lite.connect('signals.db')
        c = conn.cursor()

        c.execute("SELECT * FROM Signals")
        all_rows = c.fetchall()
        print(all_rows)

        conn.close()
    else:
        print ('DB esistente')
