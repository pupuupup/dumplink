import requests
import telegram
import time
import os
import pause, datetime
from threading import Thread

_bot = telegram.Bot(token=os.environ["TELEGRAM_API_KEY"])
_chatid = os.environ["TELEGRAM_CHAT_ID"]
_apikey = os.environ["ETHERSCAN_API_KEY"]
_chainlink = '0x514910771af9ca656af840dff83e8264ecf986ca'
_url = 'https://etherscan.io/token/'+_chainlink+'?a='
_whale = [
    {'address': '0x75398564ce69b7498da10a11ab06fd8ff549001c', 'amount': 0},
    {'address': '0x5560d001f977df5e49ead7ab0bdd437c4ee3a99e', 'amount': 0},
    {'address': '0xbe6977e08d4479c0a6777539ae0e8fa27be4e9d6', 'amount': 0},
    {'address': '0xe0362f7445e3203a496f6f8b3d51cbb413b69be2', 'amount': 0},
    {'address': '0xdad22a85ef8310ef582b70e4051e543f3153e11f', 'amount': 0},
    {'address': '0xf37c348b7d19b17b29cd5cfa64cfa48e2d6eb8db', 'amount': 0},
]
full = "50,000,000"

def startDumpWatcher():
    whale = {}
    whale = updateQuantities(_whale)
    print(whale)

def alert(whale, dumpedAmount, dumpedWallet):
    dumpedAmount = "{:,}".format(int(dumpedAmount))
    text = "😱 Sergey is dumping "+ str(dumpedAmount) +" links from wallet #"+','.join(dumpedWallet) +"!\n\n"
    texts = []
    count = 1
    for w in whale:
        if count in dumpedWallet:
            texts.append("☑️  Wallet #"+str(count)+"\n"+_url+w+"\n"+"("+"{:,}".format(int(whale[w]))+"/"+full+")\n")
        count = count + 1
    texts = "\n".join(texts)
    text = text + texts
    print(text)
    #_bot.sendMessage(chat_id=_chatid, text=text)

def updateQuantities(whale):
    new = []
    for w in whale:
        r = requests.get('https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress='+_chainlink+'&address='+w['address']+'&tag=latest&apikey='+_apikey)
        new.append({'address': w['address'], 'amount': (float(r.json()['result']) * 0.000000000000000001)})
        time.sleep(0.5)
    return new

class DumpWatcher(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        startDumpWatcher()

DumpWatcher()
while True:
    pass
