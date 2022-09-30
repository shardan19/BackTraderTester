import backtrader as bt
import datetime
import strategies
from strategies import SMACross
from strategies import EMACross
from strategies import Stoch
#from strategies import TrendLine
from strategies import MACD_RSI_TestStrategy
from strategies import MACD_RSI
from strategies import RSI_EMA, New, Candle, SmallDeps,BigDeps,EMACross50,TheStrategy,STOCHRSIstr
from strategies import RSI_Stoch,TrendLineS,Bolinger,SmallDepsv2,Bolingerv2
from strategies import ALL, MACDv3,EMAStoch,MACDStoch,BolingerStoch
#from strategies import strategy


from strategies import RSI
import csv
#from strategies import RSIv2

from strategies import MACD


f =open('wyniki.csv', 'w', newline='')
resultcsv = csv.writer(f, delimiter=',')
def createcerebro(x,y):

    if x == 0:
        todate = datetime.datetime.strptime('2022-01-01', '%Y-%m-%d')
        fromdate = datetime.datetime.strptime('2021-10-01', '%Y-%m-%d')
        month = "paździrnik-grudzień"
    elif x == 1:
        todate = datetime.datetime.strptime('2021-10-01', '%Y-%m-%d')
        fromdate = datetime.datetime.strptime('2021-07-01', '%Y-%m-%d')
        month = "lipiec-wrzesień"
    elif x == 2:
        todate = datetime.datetime.strptime('2021-07-01', '%Y-%m-%d')
        fromdate = datetime.datetime.strptime('2021-04-01', '%Y-%m-%d')
        month = "kwiecień-czerwiec"
    elif x == 3:
        todate = datetime.datetime.strptime('2021-04-01', '%Y-%m-%d')
        fromdate = datetime.datetime.strptime('2021-01-01', '%Y-%m-%d')
        month = "styczeń-marzec"

    data_5min = bt.feeds.GenericCSVData(dataname='BTCUSDT-5min-one_year.csv', dtformat=2, compression=5,
                                        timeframe=bt.TimeFrame.Minutes, fromdate=fromdate, todate=todate)
    data_15min = bt.feeds.GenericCSVData(dataname='BTCUSDT-15min-one_year.csv', dtformat=2, compression=15,
                                         timeframe=bt.TimeFrame.Minutes, fromdate=fromdate, todate=todate)
    data_60min = bt.feeds.GenericCSVData(dataname='BTCUSDT-60min-one_year.csv', dtformat=2, compression=60,
                                         timeframe=bt.TimeFrame.Minutes, fromdate=fromdate, todate=todate)
    data_4h = bt.feeds.GenericCSVData(dataname='BTCUSDT-4h-one_year.csv', dtformat=2, compression=240,
                                         timeframe=bt.TimeFrame.Minutes, fromdate=fromdate, todate=todate)
    data_1day = bt.feeds.GenericCSVData(dataname='BTCUSDT-1day-one_year.csv', dtformat=2, fromdate=fromdate,
                                        todate=todate)
    print(x,y)
    cerebro=0
    #cerebro = bt.Cerebro(cheat_on_open=True)
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(200.0)
    cerebro.broker.setcommission(commission=0.001, margin=False)
    if y == 4:
        cerebro.adddata(data_1day)
        timeinte = "24h"
        if x==0:
            resultcsv.writerow(["24h"])
            resultcsv.writerow(["Czas", "wszystkie", "wygrane", "stratne", "kapital koncowy"])
    elif y == 2:
        cerebro.adddata(data_60min)
        timeinte = "60min"
        if x==0:
            resultcsv.writerow(["60min"])
            resultcsv.writerow(["Czas", "wszystkie", "wygrane", "stratne", "kapital koncowy"])
    elif y == 1:
        cerebro.adddata(data_15min)
        timeinte = "15min"
        if x==0:
            resultcsv.writerow(["15min"])
            resultcsv.writerow(["Czas", "wszystkie", "wygrane", "stratne", "kapital koncowy"])
    elif y == 0:
        cerebro.adddata(data_5min)
        timeinte = "5min"
        if x==0:
            resultcsv.writerow(["5min"])
            resultcsv.writerow(["Czas", "wszystkie", "wygrane", "stratne", "kapital koncowy"])
    elif y == 3:
        cerebro.adddata(data_4h)
        timeinte = "4h"
        if x==0:
            resultcsv.writerow(["4h"])
            resultcsv.writerow(["Czas", "wszystkie", "wygrane", "stratne", "kapital koncowy"])
    strat_params = {'dataframe':y}
    cerebro.addstrategy(Bolinger)
    #cerebro.addstrategy(SmallDepsv2,strat_params)

    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name="trades")

    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    results = cerebro.run()

    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
    pkwargs = dict(style='candle' ,fmt_x_ticks = ' ',plotyticks=[10,-100],plotyhlines=[50,-300],plothlines=[20,-300],
        #fmt_x_data = '%Y-%b-%d'
                   )
    results[0].analyzers.getbyname("trades").get_analysis()
    #print(results[0].analyzers.getbyname("trades").get_analysis())
    total = results[0].analyzers.getbyname("trades").get_analysis()['total']['total']
    #print(total)
    totalwon = 0
    totallos = 0
    if total >0 :
        open = results[0].analyzers.getbyname("trades").get_analysis()['total']['open']
        if total==1 and open ==1:
            print("no finished trades")
            total = 0
        else:
            totalwon = results[0].analyzers.getbyname("trades").get_analysis()['won']['total']
            totallos = results[0].analyzers.getbyname("trades").get_analysis()['lost']['total']
            print('total trades: %.2f' % total)
            print('total won trades: %.2f' %totalwon)
            print('total lose trades: %.2f' %totallos)
    resultcsv.writerow([month, total, totalwon, totallos,cerebro.broker.getvalue() ])

    cerebro.plot(**pkwargs)

    cerebro.runstop()
y=3
while y<5:
    x=0
    while x<4:
        createcerebro(x,y)
        x+=1
    y+=1



