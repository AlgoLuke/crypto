import tools, time, os, urllib

import cryptocompare
from dotenv import load_dotenv

from os.path import join, dirname

from telethon.tl.functions.messages import SendMessageRequest

from telethon import TelegramClient, events
#Uncomment this for debugging
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug('dbg')
logging.info('info')

coins = []
dotenv_path = join(dirname(__file__), 'settings.env')
load_dotenv(dotenv_path)


map_coins = cryptocompare.get_coin_list()# type :
list_coins = list(map_coins.keys())

map_exchanges = cryptocompare.get_exchanges()
list_exchanges = list(map_exchanges.keys())

list_keywords = (os.environ.get('TG_KEYWORDS')).split( )



def main():

    os.system('python setup.py')


    # TG_API_ID and TG_API_HASH *must* exist or this won't run!
    session_name = os.environ.get('TG_SESSION', 'session')

    list_channels = (os.environ.get('TG_CHANNELS')).split( )
    list_titles = (os.environ.get('TG_TITLES')).split('|')

    list_keywords = (os.environ.get('TG_KEYWORDS')).split()

#    file_url = 'https://firebasestorage.googleapis.com/v0/b/cryptosignalbot-0.appspot.com/o/crypto666.session?alt=media&token=8946e052-5df7-4681-9d37-f1aa7a863c5c'
#    fileName, headers = urllib.request.urlretrieve(file_url, 'crypto666.session')
    # os.path.abspath(fileName)
    client = TelegramClient(os.environ.get('TG_SESSION', 'session'), int(os.environ['TG_API_ID']), os.environ['TG_API_HASH'],
        spawn_read_thread=False, proxy=None, update_workers=4
    )


    @client.on(events.NewMessage)
    def my_handler(event: events.NewMessage.Event):
        """

        :type event: object
        """
        global recent_reacts

        if event.is_channel:
            if any([event.chat.username in list_channels, event.chat.title in list_titles]):
                # Analisi del messaggio
                # si ricava il segnale se il messaggio contiene un segnale
                segnale = tools.parsing(event.raw_text, list_keywords)
                # si verifica il segnale non è già stato elaborato

                if tools.check_signal(segnale):
                    print('Segnale già elaborato')
                else:
                    print('nuovo segnale')
                    new_msg = tools.create_msg(segnale)
                    # query = db.execute('SELECT * FROM signals WHERE symbol=?', t)
                    client(SendMessageRequest('tradcryptocoins', new_msg))



    if 'TG_PHONE' in os.environ:
        client.start(phone=os.environ['TG_PHONE'])
    else:
        client.start()

    print('(Press Ctrl+C to stop this)')
    client.idle()


if __name__ == '__main__':
    main()
"""    feed_updated = False
    while feed_updated == False:
        try:
            main()
        except:
            time.sleep(10)"""