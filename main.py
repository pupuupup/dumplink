import requests
import logging
import telegram
from telegram.ext import Updater, CommandHandler
import time
import os
import pause, datetime
from threading import Thread

_bot = telegram.Bot(token=os.environ["TELEGRAM_API_KEY"])
_updater = Updater(token=os.environ["TELEGRAM_API_KEY"], use_context=True)
_dp = _updater.dispatcher
_chatid = os.environ["TELEGRAM_CHAT_ID"]
_apikey = os.environ["ETHERSCAN_API_KEY"]
_chainlink = '0x514910771af9ca656af840dff83e8264ecf986ca'
_url = 'https://etherscan.io/token/'+_chainlink+'?a='
_whale = [
    {'address': '0x75398564ce69b7498da10a11ab06fd8ff549001c', 'amount': 55000000},
    {'address': '0x5560d001f977df5e49ead7ab0bdd437c4ee3a99e', 'amount': 0},
    {'address': '0xbe6977e08d4479c0a6777539ae0e8fa27be4e9d6', 'amount': 0},
    {'address': '0xe0362f7445e3203a496f6f8b3d51cbb413b69be2', 'amount': 0},
    {'address': '0xdad22a85ef8310ef582b70e4051e543f3153e11f', 'amount': 0},
    {'address': '0xf37c348b7d19b17b29cd5cfa64cfa48e2d6eb8db', 'amount': 0},
]
full = "50,000,000"

def watch():
    whale = {}
    whale = updateQuantities(_whale)
    prevWhale = _whale.copy()
    #prevWhale = whale.copy()
    while True:
        whale = updateQuantities(whale)
        dumpedAmount = getDumpedAmount(whale, prevWhale)
        dumpedWallet = getDumpedWallet(whale, prevWhale)
        prevWhale = whale.copy()
        if dumpedAmount > 0:
            alert(whale, dumpedAmount, dumpedWallet)
        time.sleep(5)

def ls(update, context):
    print('wtf')
    text = "🤓 List of wallet.\n\n"
    texts =[]
    for i in range(0,5):
        texts.append("☑️  Wallet #"+str(i+1)+"\n"+url+w+"\n"+"("+"{:,}".format(int(whale[w]))+"/"+full+")\n")
    text = '\n'.join(texts)
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def listen():
    _dp.add_handler(CommandHandler("ls", ls, pass_args=True))
    _updater.start_polling()

def getDumpedAmount(whale, prevWhale):
    total = 0
    for i in range(0,5):
        if whale[i]['amount'] < prevWhale[i]['amount']:
            total = total + (prevWhale[i]['amount'] - whale[i]['amount'])
    return total

def getDumpedWallet(whale, prevWhale):
    wallets = []
    for i in range(0,5):
        if whale[i]['amount'] < prevWhale[i]['amount']:
            wallets.append(i)
    return wallets

def alert(whale, dumpedAmount, dumpedWallet):
    dumpedAmount = "{:,}".format(int(dumpedAmount))
    dumpedWalletString = []
    for w in dumpedWallet:
        dumpedWalletString.append(str(w+1))
    text = "😱 Sergey is dumping "+ str(dumpedAmount) +" links from wallet #"+','.join(dumpedWalletString) +"!\n\n"
    texts = []
    for i in dumpedWallet:
        texts.append("☑️  Wallet #"+str(i+1)+"\n"+_url+whale[i]['address']+"\n"+"("+"{:,}".format(int(whale[i]['amount']))+"/"+full+")\n")
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

class watcher(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        watch()

class listener(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        listen()

_dp.add_handler(CommandHandler("ls", ls))
_updater.start_polling()
watcher()
listener()

while True:
    pass
