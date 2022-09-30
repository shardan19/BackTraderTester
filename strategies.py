import backtrader as bt
from pprint import pprint
from backtrader.indicators import EMA
import datetime
import time

x = 0


# base strategy class
class SuperTrendBand(bt.Indicator):
    """
    Helper inidcator for Supertrend indicator
    """
    params = (('period', 7), ('multiplier', 3))
    lines = ('basic_ub', 'basic_lb', 'final_ub', 'final_lb')

    def __init__(self):
        self.atr = bt.indicators.AverageTrueRange(period=self.p.period)
        self.l.basic_ub = ((self.data.high + self.data.low) / 2) + (self.atr * self.p.multiplier)
        self.l.basic_lb = ((self.data.high + self.data.low) / 2) - (self.atr * self.p.multiplier)

    def next(self):
        if len(self) - 1 == self.p.period:
            self.l.final_ub[0] = self.l.basic_ub[0]
            self.l.final_lb[0] = self.l.basic_lb[0]
        else:
            # =IF(OR(basic_ub<final_ub*,close*>final_ub*),basic_ub,final_ub*)
            if self.l.basic_ub[0] < self.l.final_ub[-1] or self.data.close[-1] > self.l.final_ub[-1]:
                self.l.final_ub[0] = self.l.basic_ub[0]
            else:
                self.l.final_ub[0] = self.l.final_ub[-1]

            # =IF(OR(baisc_lb > final_lb *, close * < final_lb *), basic_lb *, final_lb *)
            if self.l.basic_lb[0] > self.l.final_lb[-1] or self.data.close[-1] < self.l.final_lb[-1]:
                self.l.final_lb[0] = self.l.basic_lb[0]
            else:
                self.l.final_lb[0] = self.l.final_lb[-1]


class SuperTrend(bt.Indicator):
    """
    Super Trend indicator
    """
    params = (('period', 7), ('multiplier', 3))
    lines = ('super_trend',)
    plotinfo = dict(subplot=False)

    def __init__(self):
        self.stb = SuperTrendBand(period=self.p.period, multiplier=self.p.multiplier)

    def next(self):
        if len(self) - 1 == self.p.period:
            self.l.super_trend[0] = self.stb.final_ub[0]
            return

        if self.l.super_trend[-1] == self.stb.final_ub[-1]:
            if self.data.close[0] <= self.stb.final_ub[0]:
                self.l.super_trend[0] = self.stb.final_ub[0]
            else:
                self.l.super_trend[0] = self.stb.final_lb[0]

        if self.l.super_trend[-1] == self.stb.final_lb[-1]:
            if self.data.close[0] >= self.stb.final_lb[0]:
                self.l.super_trend[0] = self.stb.final_lb[0]
            else:
                self.l.super_trend[0] = self.stb.final_ub[0]

class MACDv3(bt.Strategy):
    params = (
        ('dataframe', None),
        #('fastperiod', 12),
        #('slowperoid', 26),
        #('signalperoid', 9),
        ('SL', None),
        ('TP', None),
        ('buyprice', None),
        ('diff', None),
        ('buymacd',None),
        ('diffmacd', None)

    )


    def __init__(self,params=None):
        if params != None:
            for name, val in params.items():
                setattr(self.params, name, val)
        if self.params.dataframe ==0 :
            setattr(self.params, 'SL', 0.01)
            setattr(self.params, 'TP', 0.025)
            setattr(self.params, 'TPmacd', 0.4)
            setattr(self.params, 'dev', -1200)
            setattr(self.params, 'signalperoid', 9)
            setattr(self.params, 'fastperiod', 12)
            setattr(self.params, 'slowperoid', 26)

        elif self.params.dataframe == 1:
            setattr(self.params, 'SL', 0.01)
            setattr(self.params, 'TP', 0.025)
            setattr(self.params, 'TPmacd', 0.4)
            setattr(self.params, 'dev', -1200)
            setattr(self.params, 'signalperoid', 9)
            setattr(self.params, 'fastperiod', 12)
            setattr(self.params, 'slowperoid', 26)

        elif self.params.dataframe == 2:
            setattr(self.params, 'SL', 0.02)
            setattr(self.params, 'TP', 0.025)
            setattr(self.params, 'TPmacd', 0.3)
            setattr(self.params, 'dev', -1100)
            setattr(self.params, 'signalperoid', 7)
            setattr(self.params, 'fastperiod', 12)
            setattr(self.params, 'slowperoid', 26)

        elif self.params.dataframe == 3:
            setattr(self.params, 'SL', 0.01)
            setattr(self.params, 'TP', 0.025)
            setattr(self.params, 'TPmacd', 0.3)
            setattr(self.params, 'dev', -1200)
            setattr(self.params, 'signalperoid', 9)
            setattr(self.params, 'fastperiod', 12)
            setattr(self.params, 'slowperoid', 26)

        elif self.params.dataframe == 4:
            setattr(self.params, 'SL', 0.01)
            setattr(self.params, 'TP', 0.025)
            setattr(self.params, 'TPmacd', 0.4)
            setattr(self.params, 'dev', -1200)
            setattr(self.params, 'signalperoid', 9)
            setattr(self.params, 'fastperiod', 12)
            setattr(self.params, 'slowperoid', 26)

        self.macd = bt.talib.MACD(self.data, plotname='TA_MACD', fastperiod=self.params.fastperiod, slowperoid=self.params.slowperoid, signalperoid=self.params.signalperoid)
        self.macd2 = bt.talib.MACD(self.data, plotname='TA_MACD2', fastperiod=19,
                                  slowperoid=39, signalperoid=9)
        self.Crossing = bt.indicators.CrossOver(self.macd.lines.macd, self.macd.lines.macdsignal,
                                                plotname='Buy_Sell_Line')

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED {}'.format(order.executed.price))

            self.bar_executed = len(self)

        self.order = None
    def next(self):
        if self.params.buyprice !=None:
            diff =self.data.close[0]/self.params.buyprice
            #print(diff)
            setattr(self.params, 'diff', diff)
        if self.params.buymacd !=None:
            if self.macd.lines.macd>0:
                diffmacd = (self.params.buymacd-self.macd.lines.macd) / self.params.buymacd
            else:
                diffmacd =self.params.buymacd/self.macd.lines.macd
            #print(diffmacd)
            setattr(self.params, 'diffmacd', diffmacd)
        # If MACD is above Signal line
        #print(self.macd.lines.macd[0], self.Crossing[0])
        if not self.position:
            if self.Crossing > 0 and self.macd.lines.macd < self.params.dev:
                perc = 100 / self.data.close
                self.buy(size=perc)
                setattr(self.params, 'buyprice', self.data.close[0])
                setattr(self.params, 'buymacd', self.macd.lines.macd[0])
                #print(self.params.buyprice,self.macd.lines.macd[0])
        # If MACD is below Signal line
        # elif self.Crossing < 0 and self.macd.lines.macd > 50:
        if self.position:
            print("buy macd:", self.params.buymacd,"macd line:", self.macd.lines.macd[0],"diff macd:",self.params.diffmacd,"diff:",self.params.diff, "buyp:",self.params.buyprice ,"cp:",self.data.close[0])

            if self.params.diffmacd > 1 + self.params.TPmacd and self.params.diff > 1 + self.params.TP  or self.params.diff < 1 - self.params.SL:
                self.close()
                print("sell")
class RSI(bt.Strategy):
    params = (
        ('dataframe', None),
        ('period',14),
        ('SL', None),
        ('TP', None),
        ('buyprice',None),
        ('diff',None),
        ('testperiod',None),
        ('buyrsi',None)
    )
    def __init__(self,params=None):
        if params != None:
            for name, val in params.items():
                setattr(self.params, name, val)
        if self.params.dataframe ==0 :
            setattr(self.params, 'SL', 0.025)
            setattr(self.params, 'TP', 0.05)
            setattr(self.params, 'testperiod', 21)
            setattr(self.params, 'buyrsi', 17)
        elif self.params.dataframe == 1:
            setattr(self.params, 'SL', 0.026)
            setattr(self.params, 'TP', 0.055)
            setattr(self.params, 'testperiod', 21)
            setattr(self.params, 'buyrsi', 23)
        elif self.params.dataframe == 2:
            setattr(self.params, 'SL', 0.029)
            setattr(self.params, 'TP', 0.06)
            setattr(self.params, 'testperiod', 20)
            setattr(self.params, 'buyrsi', 26)
        elif self.params.dataframe == 3:
            setattr(self.params, 'SL', 0.029)
            setattr(self.params, 'TP', 0.06)
            setattr(self.params, 'testperiod', 19)
            setattr(self.params, 'buyrsi', 30)
        elif self.params.dataframe == 4:
            setattr(self.params, 'SL', 0.03)
            setattr(self.params, 'TP', 0.065)
            setattr(self.params, 'testperiod', 16)
            setattr(self.params, 'buyrsi', 33)
        print("okres obliczenia wskaźnika", self.params.testperiod)
        self.rsi_14 = bt.indicators.RSI(self.data.close, period=self.params.testperiod)
       #print(self.params.dataframe)
        #print(self.params.SLprocent)
    def next(self):
        if self.params.buyprice !=None:
            diff =self.data.close[0]/self.params.buyprice
            #print(diff)
            setattr(self.params, 'diff', diff)
        if self.rsi_14 < self.params.buyrsi:
            if not self.position:
                perc = 100 / self.data.close
                #print(self.params.diff)
                self.buy(size=perc)
                setattr(self.params, 'buyprice', self.data.close[0])

        if self.position:
            if self.params.diff>1+self.params.TP or self.params.diff<1-self.params.SL :
                self.close()



class TrendLineS(bt.Strategy):
    def __init__(self):
        self.sfb=SuperTrendBand()
        self.sf = SuperTrend()
    def next(self):
        if self.data.close[0] < self.sf and not self.position:
            perc = 100 / self.data.close
            # print(perc)
            self.buy(size=perc)
        if self.data.close[0] > self.sf and self.position:
            self.close()
class StochRSI(bt.Indicator):
    lines = ('stochrsi',)
    params = dict(
        period=14,  # to apply to RSI
        pperiod=None,  # if passed apply to HighestN/LowestN, else "period"
    )

    def __init__(self):
        rsi = bt.ind.RSI_Safe(self.data, period=self.p.period, safediv=True)

        pperiod = self.p.pperiod or self.p.period
        maxrsi = bt.ind.Highest(rsi, period=pperiod)
        minrsi = bt.ind.Lowest(rsi, period=pperiod)

        self.l.stochrsi = (rsi - minrsi) / (maxrsi - minrsi)


class STOCHRSIstr(bt.Strategy):

    def __init__(self):
        self.stochRSI=StochRSI()
        #self.stochRSI = bt.talib.STOCHRSI(self.data.close, timeperiod=14, fastk_period=3, fastd_period=3, fastd_matype=0)
        #self.rsi_14 = bt.indicators.RSI(self.data.close, period=14)

    def next(self):
        if self.stochRSI<0.2:
            #print("mniejsze")
            perc = 100 / self.data.close
            # print(perc)
            self.buy(size=perc)
        elif self.stochRSI>0.8:
            #print("wieksze",self.stochRSI)
            self.close()



class MACD(bt.Strategy):
    params = (('fast_LBP', 12), ('slow_LBP', 26), ('max_position', 1), ('signal_LBP', 9))

    def __init__(self):

        self.macd = bt.talib.MACD(self.data, plotname='TA_MACD', fastperiod=12, slowperoid=26, signalperoid=9)
        self.Crossing = bt.indicators.CrossOver(self.macd.lines.macd, self.macd.lines.macdsignal,
                                                plotname='Buy_Sell_Line')

    def next(self):
        perc = 100 / self.data.close
        # If MACD is above Signal line
        #print(self.macd.lines.macd[0], self.Crossing[0])
        if self.Crossing > 0:
            # if self.Crossing > 0 and self.macd.lines.macd < -50:
            if self.position.size < self.params.max_position:
                self.buy(size=perc)

        # If MACD is below Signal line
        # elif self.Crossing < 0 and self.macd.lines.macd > 50:
        elif self.Crossing < 0:
            if self.position.size > 0:
                self.close()
class MACDStoch(bt.Strategy):
    params = (('fast_LBP', 12), ('slow_LBP', 26), ('max_position', 1), ('signal_LBP', 9))

    def __init__(self):

        self.macd = bt.talib.MACD(self.data, plotname='TA_MACD', fastperiod=12, slowperoid=26, signalperoid=9)
        self.Crossing = bt.indicators.CrossOver(self.macd.lines.macd, self.macd.lines.macdsignal,
                                                plotname='Buy_Sell_Line')
        self.stochastic = bt.talib.STOCH(self.data.high, self.data.low, self.data.close, fastk_period=14,
                                         slowk_period=3,
                                         slowd_period=3)
        

    def next(self):
        perc = 100 / self.data.close
        if not self.position:
            if self.Crossing > 0 and self.stochastic<30:

                self.buy(size=perc)

        elif self.Crossing < 0 and self.stochastic>70:

            self.close()


class SMACross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30  # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.SMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        perc = 100 / self.data.close

        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy(size=perc)  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position


class EMACross(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30  # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.EMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.EMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        perc = 100 / self.data.close

        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy(size=perc)  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position
class EMAStoch(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30  # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.EMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.EMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal
        self.stoch=bt.talib.STOCH(self.data.high, self.data.low, self.data.close, fastk_period=5,
                                         slowk_period=3,
                                         slowd_period=3)

    def next(self):
        perc = 100 / self.data.close

        if not self.position:  # not in the market
            if self.crossover > 0 and self.stoch<25:  # if fast crosses slow to the upside
                self.buy(size=perc)  # enter long

        elif self.crossover < 0 and self.stoch>75:  # in the market & cross to the downside
            self.close()  # close long position

class EMACross50(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=8,  # period for the fast moving average
        pslow=50  # period for the slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.EMA(period=self.p.pfast)  # fast moving average
        sma2 = bt.ind.EMA(period=self.p.pslow)  # slow moving average
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # crossover signal

    def next(self):
        perc = 100 / self.data.close

        if not self.position:  # not in the market
            if self.crossover > 0:  # if fast crosses slow to the upside
                self.buy(size=perc)  # enter long

        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position


class Stoch(bt.Strategy):
    # list of parameters which are configurable for the strategy
    params = dict(
        pfast=10,  # period for the fast moving average
        pslow=30  # period for the slow moving average
    )

    def __init__(self):
        # self.trend=bt.talib.HT_TRENDMODE(self.data.close)
        # self.trendline = bt.talib.HT_TRENDLINE(self.data.close)
        self.stochastic = bt.talib.STOCH(self.data.high, self.data.low, self.data.close, fastk_period=14,
                                         slowk_period=3,
                                         slowd_period=3)
        slowk = self.stochastic.lines.slowk
        slowd = self.stochastic.lines.slowd
        self.crossover = bt.ind.CrossOver(slowk, slowd)

    def next(self):
        perc = 100 / self.data.close

        # print(self.stochastic.lines.slowk[0],self.stochastic.lines.slowk[-1])

        if not self.position:  # not in the market
            if self.stochastic.lines.slowd[0] < 20 and self.stochastic.lines.slowk[0] < 20 and \
                    self.stochastic.lines.slowk[0] < self.stochastic.lines.slowd[
                0]:  # if fast crosses slow to the upside
                self.buy(size=perc)  # enter long

        elif self.stochastic.lines.slowd[0] > 80 and self.stochastic.lines.slowk[0] > 80 and \
                self.stochastic.lines.slowk[0] > self.stochastic.lines.slowd[
            0]:  # in the market & cross to the downside
            self.close()  # close long position


class MACD_RSI_TestStrategy(bt.Strategy):
    params = dict(
        fastperiod=1,
        slowperiod=26,
        signalperiod=9,
        rsi_period=14,

        rsi_under=20,
        rsi_over=80
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.movav = bt.talib.MACD(self.datas[0].close, fastperiod=self.params.fastperiod,
                                   slowperiod=self.params.slowperiod, signalperiod=self.params.signalperiod)
        self.rsi = bt.talib.RSI(self.datas[0].close, period=self.params.rsi_period)
        self.order = None
        self.macdabove = False
        self.dataclose = self.datas[0].close

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED {}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED {}'.format(order.executed.price))

            self.bar_executed = len(self)

        self.order = None

    def next(self):

        if self.macdabove == False and self.movav.lines.macd[0] > self.movav.lines.macdsignal[0] and self.rsi.lines[
            0] < self.params.rsi_under:
            self.macdabove = True
            self.log(f'BUY CREATE, {self.dataclose[0]}')
            self.order = self.buy()
        elif self.macdabove == True and self.position and self.rsi.lines[0] > self.params.rsi_over:
            self.macdabove = False
            self.log('SELL CREATE {}'.format(self.dataclose[0]))
            self.order = self.close()


class RSI_EMA(bt.Strategy):
    params = dict(
        fastperiod=10,
        slowperiod=30,
        rsi_period=14,
        rsi_under=20,
        rsi_over=80
    )

    def __init__(self):
        self.rsi = bt.talib.RSI(self.datas[0].close, period=self.params.rsi_period)
        self.rsisignlong = False
        self.rsisignshort = False
        self.slowema = bt.ind.EMA(period=self.params.slowperiod)
        self.fastema = bt.ind.EMA(period=self.params.fastperiod)
        self.ema60 = bt.ind.EMA(period=60)
        # self.ema100 = bt.ind.EMA(period=100)

        self.crossover = bt.ind.CrossOver(self.slowema, self.fastema)

class Bolinger(bt.Strategy):
    def __init__(self):
        self.bband = bt.indicators.BBands(self.data, period=20)

    def next(self):

        perc = 100 / self.data.close
        if self.data.close < self.bband.lines.bot and not self.position:
            self.buy(size=perc)
        elif self.data.close > self.bband.lines.top and self.position:
            self.close()
class BolingerStoch(bt.Strategy):
    def __init__(self):
        self.bband = bt.indicators.BBands(self.data, period=20)
        self.stochastic = bt.talib.STOCH(self.data.high, self.data.low, self.data.close, fastk_period=14,
                                        slowk_period=3,
                                        slowd_period=3)
    def next(self):

        perc = 100 / self.data.close

        if self.data.close < self.bband.lines.bot and not self.position and self.stochastic<30:
            self.buy(size=perc)
        elif self.data.close > self.bband.lines.top and self.position and self.stochastic>70:
            self.close()
class Bolingerv2(bt.Strategy):
    params = (
        ('dataframe', None),
        ('period', 20),
        ('SL', None),
        ('TP', None),
        ('buyprice', None),
        ('diff', None),
        ('testperiod', None),
        ('devfactor',None)

    )

    def __init__(self, params=None):
        if params != None:
            for name, val in params.items():
                setattr(self.params, name, val)
        if self.params.dataframe == 0:
            setattr(self.params, 'SL', 0.025)
            setattr(self.params, 'TP', 0.05)
            setattr(self.params, 'testperiod', 100)
            setattr(self.params, 'devfactor', 5.5)

        elif self.params.dataframe == 1:
            setattr(self.params, 'SL', 0.025)
            setattr(self.params, 'TP', 0.055)
            setattr(self.params, 'testperiod', 60)
            setattr(self.params, 'devfactor', 4)

        elif self.params.dataframe == 2:
            setattr(self.params, 'SL', 0.025)
            setattr(self.params, 'TP', 0.05)
            setattr(self.params, 'testperiod', 58)
            setattr(self.params, 'devfactor', 3.8)

        elif self.params.dataframe == 3:
            setattr(self.params, 'SL', 0.025)
            setattr(self.params, 'TP', 0.06)
            setattr(self.params, 'testperiod', 40)
            setattr(self.params, 'devfactor', 2.6)

        elif self.params.dataframe == 4:
            setattr(self.params, 'SL', 0.25)
            setattr(self.params, 'TP', 0.065)
            setattr(self.params, 'testperiod', 40)
            setattr(self.params, 'devfactor', 2.6)

        print("okres obliczenia wskaźnika", self.params.testperiod)
        self.bband = bt.indicators.BBands(self.data, period=self.params.testperiod, devfactor =self.params.devfactor )

    def next(self):
        if self.params.buyprice !=None:
            diff =self.data.close[0]/self.params.buyprice
            #print(diff)
            setattr(self.params, 'diff', diff)
        perc = 100 / self.data.close
        if self.data.close < self.bband.lines.bot and not self.position:
            self.buy(size=perc)
            setattr(self.params, 'buyprice', self.data.close[0])
        #elif self.data.close > self.bband.lines.top and self.position:
        if self.position:
            if self.params.diff > 1 + self.params.TP or self.params.diff < 1 - self.params.SL:
                self.close()
class ALL(bt.Strategy):
    params = (
        ('atrperiod', 14),  # ATR Period (standard)
        ('atrdist_x', 1.5),  # ATR distance for stop price
        ('atrdist_y', 1.35),  # ATR distance for take profit price
        ('tenkan', 9),
        ('kijun', 26),
        ('senkou', 52),
        ('senkou_lead', 26),  # forward push
        ('chikou', 26),  # backwards push
    )

    def __init__(self):
        self.ema60 = bt.ind.EMA(period=60)
        self.ema30 = bt.ind.EMA(period=30)
        self.ema10 = bt.ind.EMA(period=10)
        self.rsi = bt.talib.RSI(self.datas[0].close, period=14)
        self.macd = bt.talib.MACD(self.data, plotname='TA_MACD', fastperiod=12, slowperoid=26, signalperoid=9)
        self.stochastic = bt.talib.STOCH(self.data.high, self.data.low, self.data.close, fastk_period=14,
                                        slowk_period=3,
                                        slowd_period=3)
        self.bband = bt.indicators.BBands(self.datas[0], period=20)
        # self.ichi = bt.indicators.Ichimoku(self.datas[0],
        #                                    tenkan=self.params.tenkan,
        #                                    kijun=self.params.kijun,
        #                                    senkou=self.params.senkou,
        #                                    senkou_lead=self.params.senkou_lead,
        #                                    chikou=self.params.chikou)


class MACD_RSI(bt.Strategy):
    params = dict(
        fastperiod=12,
        slowperiod=26,
        signalperiod=9,
        rsi_period=14,
        rsi_under=20,
        rsi_over=80
    )

    def __init__(self):
        # self.counter=0

        self.macd = bt.talib.MACD(self.datas[0].close, fastperiod=self.params.fastperiod,
                                  slowperiod=self.params.slowperiod, signalperiod=self.params.signalperiod)
        self.rsi = bt.talib.RSI(self.datas[0].close, period=self.params.rsi_period)
        self.rsisignlong = False
        self.rsisignshort = False
        macdline = self.macd.lines.macd
        macdsignal = self.macd.lines.macdsignal
        self.crossover = bt.ind.CrossOver(macdline, macdsignal)

    def next(self):

        # print(self.macd.lines.macd[0], self.macd.lines.macdsignal[0])
        perc = 100 / self.data.close
        if self.rsi < 30 and not self.position:
            self.rsisignlong = True
        # print(perc)

        if self.rsi > 70 and self.position:
            self.rsisignshort = True
        if self.crossover > 0 and self.rsisignlong == True and not self.position:
            self.buy(size=perc)
            self.rsisignlong = False
        if self.crossover < 0 and self.rsisignshort == True and self.position:
            self.close()
            self.rsisignshort = False


# ----------------
class RSI_Stoch(bt.Strategy):
    params = dict(
        fastperiod=10,
        slowperiod=26,
        signalperiod=9,
        rsi_period=14,
        rsi_under=20,
        rsi_over=80
    )

    def __init__(self):
        self.rsi = bt.talib.RSI(self.datas[0].close, period=self.params.rsi_period)

        self.supertrend = SuperTrend(period=11, multiplier=2)


class New(bt.Strategy):
    # list of parameters which are configurable for the strategy

    params = dict(
        rsi_period=14,  # period for the fast moving average
        buyprices=[],
        percentlist=[],
        averageprice=0,
        procent=0,

    )

    def __init__(self):

        self.rsi = bt.talib.RSI(self.datas[0].close, period=self.params.rsi_period)
        self.params.buyprices = []
        self.params.percentlist = []

    def next(self):

        # print("xx",self.data.close[0])
        perc = 100 / self.data.close
        if self.rsi < 30:  # if fast crosses slow to the upside
            # enter long
            self.params.buyprices.append(self.data.close[1])

            self.params.averageprice = Average(self.params.buyprices)
            self.params.procent = self.data.close[1] / self.params.averageprice
            self.params.percentlist.append(self.params.procent)
            print("d2", self.data.close[1])
            print("perc", self.params.procent)
            print("-1", min(self.params.percentlist))
            if self.params.procent <= (min(self.params.percentlist) * 0.9) or self.params.procent == 1:
                self.buy(size=perc)

        elif self.rsi > 50:  # in the market & cross to the downside
            if self.data.close[0] >= (self.params.averageprice * 1.1):
                self.close()  # close long position
                self.params.buyprices = []
                self.params.percentlist = []


class Candle(bt.Strategy):
    def __init__(self):
        self.marubozu = bt.talib.CDLMORNINGSTAR(self.data.open, self.data.high,
                                                self.data.low, self.data.close, penetration=0.3)

    def next(self):
        perc = 100 / self.data.close
        if self.marubozu[0] == 100:
            self.buy(size=perc)

        elif self.marubozu[0] == -100:
            self.close()
        else:
            print(self.marubozu)


class SmallDeps(bt.Strategy):
    def __init__(self):
        self.rsi_14 = bt.talib.RSI(self.data.close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        self.stochrsi = bt.talib.STOCHRSI(self.data.close, timeperiod=14)
        self.stochastic = bt.talib.STOCH(self.data.high, self.data.low, self.data.close, fastk_period=5,
                                         slowk_period=3,
                                         slowd_period=3)

    def next(self):
        perc = 100 / self.data.close

        if not self.position:
            if self.stochrsi < 25 and self.rsi_14 < 37 and self.stochastic < 25:
                self.buy(size=perc)
                lastprice = self.data.close[0]


        else:

            if self.stochrsi > 75 and self.rsi_14 > 63 and self.stochastic > 75:
                self.close()
class SmallDepsv2(bt.Strategy):
    params = (
        ('dataframe', None),

        ('SL', None),
        ('TP', None),
        ('buyprice', None),
        ('diff', None),
        ('rsiperiod', None),
        ('buyrsi', None),
        ('stochrsiperiod', None),
        ('stochperiod', None),
        ('buystochrsi', None),
        ('buystoch', None),

    )

    def __init__(self, params=None):
        if params != None:
            for name, val in params.items():
                setattr(self.params, name, val)
        if self.params.dataframe == 0:
            setattr(self.params, 'SL', 0.025)
            setattr(self.params, 'TP', 0.05)
            setattr(self.params, 'rsiperiod', 21)
            setattr(self.params, 'stochrsiperiod', 21)

            setattr(self.params, 'buyrsi', 21)
            setattr(self.params, 'buystochrsi', 5)
            setattr(self.params, 'buystoch', 10)
        elif self.params.dataframe == 1:
            setattr(self.params, 'SL', 0.025)
            setattr(self.params, 'TP', 0.05)
            setattr(self.params, 'rsiperiod', 21)
            setattr(self.params, 'stochrsiperiod', 21)

            setattr(self.params, 'buyrsi', 26)
            setattr(self.params, 'buystochrsi', 18)
            setattr(self.params, 'buystoch', 18)
        elif self.params.dataframe == 2:
            setattr(self.params, 'SL', 0.029)
            setattr(self.params, 'TP', 0.055)
            setattr(self.params, 'rsiperiod', 14)
            setattr(self.params, 'stochrsiperiod', 14)

            setattr(self.params, 'buyrsi', 27)
            setattr(self.params, 'buystochrsi', 20)
            setattr(self.params, 'buystoch', 20)
        elif self.params.dataframe == 3:
            setattr(self.params, 'SL', 0.029)
            setattr(self.params, 'TP', 0.055)
            setattr(self.params, 'rsiperiod', 14)
            setattr(self.params, 'stochrsiperiod', 14)

            setattr(self.params, 'buyrsi', 37)
            setattr(self.params, 'buystochrsi', 27)
            setattr(self.params, 'buystoch', 27)
        elif self.params.dataframe == 4:
            setattr(self.params, 'SL', 0.029)
            setattr(self.params, 'TP', 0.055)
            setattr(self.params, 'rsiperiod', 14)
            setattr(self.params, 'stochrsiperiod', 14)

            setattr(self.params, 'buyrsi', 37)
            setattr(self.params, 'buystochrsi', 28)
            setattr(self.params, 'buystoch', 28)
        print("okres obliczenia wskaźnika", self.params.rsiperiod)
        self.rsi = bt.talib.RSI(self.data.close, timeperiod=self.params.rsiperiod)
        self.stochrsi = bt.talib.STOCHRSI(self.data.close, timeperiod=self.params.stochrsiperiod,fastk_period=5, fastd_period=3, fastd_matype=0)
        self.stochastic = bt.talib.STOCH(self.data.high, self.data.low, self.data.close, fastk_period=5,
                                         slowk_period=3,
                                         slowd_period=3)

    def next(self):
        if self.params.buyprice !=None:
            diff =self.data.close[0]/self.params.buyprice
            #print(diff)
            setattr(self.params, 'diff', diff)
        if not self.position:
            if self.stochrsi < self.params.buystochrsi and self.rsi < self.params.buyrsi and self.stochastic < self.params.buystoch:
            
                perc = 100 / self.data.close
                #print(self.params.diff)
                self.buy(size=perc)
                setattr(self.params, 'buyprice', self.data.close[0])

        if self.position:

            if self.params.diff > 1 + self.params.TP or self.params.diff < 1 - self.params.SL:
                self.close()

class BigDeps(bt.Strategy):
    def __init__(self):
        

        self.rsi_14 = bt.talib.RSI(self.data.close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)
        self.stochrsi = bt.talib.STOCHRSI(self.data.close, timeperiod=14)
        self.stochastic = bt.talib.STOCH(self.data.high, self.data.low, self.data.close, fastk_period=5,
                                         slowk_period=3,
                                         slowd_period=3)

    def next(self):
        perc = 100 / self.data.close
        # print(self.stochrsi)
        if not self.position:
            if self.stochrsi < 20 and self.rsi_14 < 22 and self.stochastic < 20:
                self.buy(size=perc)
                # print("xxx")
        else:
            if self.stochrsi > 80 and self.rsi_14 > 78 and self.stochastic > 80:
                self.close()


class TheStrategy(bt.Strategy):
    params = (
        ('atrperiod', 14),  # ATR Period (standard)
        ('atrdist_x', 1.5),  # ATR distance for stop price
        ('atrdist_y', 1.35),  # ATR distance for take profit price
        ('tenkan', 9),
        ('kijun', 26),
        ('senkou', 52),
        ('senkou_lead', 26),  # forward push
        ('chikou', 26),  # backwards push
    )

    def notify_order(self, order):
        if order.status == order.Completed:
            pass

        if not order.alive():
            self.order = None  # indicate no order is pending

    def __init__(self):
        self.ichi = bt.indicators.Ichimoku(self.datas[0],
                                           tenkan=self.params.tenkan,
                                           kijun=self.params.kijun,
                                           senkou=self.params.senkou,
                                           senkou_lead=self.params.senkou_lead,
                                           chikou=self.params.chikou)

        # Cross of tenkan and kijun -
        # 1.0 if the 1st data crosses the 2nd data upwards - long
        # -1.0 if the 1st data crosses the 2nd data downwards - short

        self.tkcross = bt.indicators.CrossOver(self.ichi.tenkan_sen, self.ichi.kijun_sen)

        # To set the stop price
        self.atr = bt.indicators.ATR(self.data, period=self.p.atrperiod)

        # Long Short ichimoku logic
        self.long = bt.And((self.data.close[0] > self.ichi.senkou_span_a(0)),
                           (self.data.close[0] > self.ichi.senkou_span_b(0)),
                           (self.tkcross == 1))

        self.short = bt.And((self.data.close[0] < self.ichi.senkou_span_a(0)),
                            (self.data.close[0] < self.ichi.senkou_span_b(0)),
                            (self.tkcross == -1))

    def start(self):
        self.order = None  # sentinel to avoid operrations on pending order

    def next(self):
        if self.order:
            return  # pending order execution

        if not self.position:  # not in the market
            if self.short:
                self.order = self.sell()
                ldist = self.atr[0] * self.p.atrdist_x
                self.lstop = self.data.close[0] + ldist
                pdist = self.atr[0] * self.p.atrdist_y
                self.take_profit = self.data.close[0] - pdist
            if self.long:
                self.order = self.buy()
                ldist = self.atr[0] * self.p.atrdist_x
                self.lstop = self.data.close[0] - ldist
                pdist = self.atr[0] * self.p.atrdist_y
                self.take_profit = self.data.close[0] + pdist

        else:  # in the market
            pclose = self.data.close[0]
            pstop = self.pstop

            if ((pstop < pclose < self.take_profit) | (pstop > pclose > self.take_profit)):
                self.close()  # Close position


def Average(lst):
    return sum(lst) / len(lst)
