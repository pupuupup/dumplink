import requests
import telegram
import time
import os
import pause, datetime
from threading import Thread

bot = telegram.Bot(token=os.environ["TELEGRAM_API_KEY"])
chatid = os.environ["TELEGRAM_CHAT_ID"]
apikey = os.environ["ETHERSCAN_API_KEY"]
chainlink = '0x514910771af9ca656af840dff83e8264ecf986ca'
url = 'https://etherscan.io/token/'+chainlink+'?a='
whale = {
    '0x75398564ce69b7498da10a11ab06fd8ff549001c': 0,
    '0x5560d001f977df5e49ead7ab0bdd437c4ee3a99e': 0,
    '0xbe6977e08d4479c0a6777539ae0e8fa27be4e9d6': 0,
    '0xe0362f7445e3203a496f6f8b3d51cbb413b69be2': 0,
    '0xdad22a85ef8310ef582b70e4051e543f3153e11f': 0,
    '0xf37c348b7d19b17b29cd5cfa64cfa48e2d6eb8db': 0
}
full = "50,000,000"
prevWhale = whale.copy()

def startDailyCheckup():
    updateQuantities()
    prevWhale = whale.copy()
    while True:
        checkDaily(total())
        later = datetime.datetime.now() + datetime.timedelta(days=1)
        pause.until(later)

def startDumpWatcher():
    updateQuantities()
    prevWhale = whale.copy()
    while True:
        updateQuantities()
        dumpedAmount = checkDumpAmount()
        if dumpedAmount > 0:
            dumpedWallet = checkDumpWallet()
            alert(dumpedAmount, dumpedWallet)
        prevWhale = whale.copy()
        time.sleep(5)

def checkDumpAmount():
    dumped = 0
    for w in whale.keys():
        if whale[w] < prevWhale[w]:
            dumped = dumped +(prevWhale[w] - whale[w])
    return dumped

def checkDumpWallet():
    dumped = []
    count = 1
    for w in whale.keys():
        if whale[w] < prevWhale[w]:
            dumped.append(str(count))
        count = count + 1
    return dumped

def alert(dumpedAmount, dumpedWallet):
    dumpedAmount = "{:,}".format(int(dumpedAmount))
    text = "😱 Sergey is dumping "+ str(dumpedAmount) +" links from wallet #"+','.join(dumpedWallet) +"!\n\n"
    texts = []
    count = 1
    for w in whale.keys():
        if str(count) in dumpedWallet:
            texts.append("☑️  Wallet #"+str(count)+"\n"+url+w+"\n"+"("+"{:,}".format(int(whale[w]))+"/"+full+")\n")
            count = count + 1
    texts = "\n".join(texts)
    text = text + texts

    bot.sendMessage(chat_id=chatid, text=text)
    print(text)

def checkDaily(total):
    total = "{:,}".format(int(total))
    text = "🤓 Daily check up: Total of " + total + " links.\n\n"
    texts = []
    count = 1
    for w in whale.keys():
        texts.append("☑️  Wallet #"+str(count)+"\n"+url+w+"\n"+"("+"{:,}".format(int(whale[w]))+"/"+full+")\n")
        count = count + 1
    texts = "\n".join(texts)
    text = text + texts
    bot.sendMessage(chat_id=chatid, text=text)
    print(text)

def total():
    total = 0
    for w in whale.keys():
        total = whale[w] + total
    return total

def updateQuantities():
    for w in whale.keys():
        r = requests.get('https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress='+chainlink+'&address='+w+'&tag=latest&apikey='+apikey)
        time.sleep(0.5)
        whale[w] = (float(r.json()['result']) * 0.000000000000000001)


class DumpWatcher(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        startDumpWatcher()

class DailyCheckup(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.start()
    def run(self):
        startDailyCheckup()

DumpWatcher()
DailyCheckup()
while True:
    pass
