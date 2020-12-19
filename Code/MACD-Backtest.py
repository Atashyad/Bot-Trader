import pandas as pd
if __name__=='__main__':
 
    USD = 1000
    SumUsd = 1000
    Money = 0
    Price = 0
    LastPrice = 0
    bnb = 0
    Commision = 0.00075
    SumComm = 0
    Coin=pd.read_csv('d://csv//BtcBinance.csv',parse_dates=True)
    
    Coin['Quote'] = Coin['Quote asset volume']
    Coin['Mean'] = Coin.Quote/Coin.Volume
    Coin['Mean'] = Coin['Mean'].fillna(method='backfill') 
    MacdEMA1 = 25
    MacdEMA2 = 21
    SignalEMA = 9
    Coin['MACDEMA1'] = 0
    Coin['MACDEMA2'] = 0
    Coin['MACDEMA1'] = Coin.Mean.ewm(span = MacdEMA1, min_periods=MacdEMA1).mean()
    Coin['MACDEMA2'] = Coin.Mean.ewm(span = MacdEMA2, min_periods=MacdEMA2).mean()
    Coin['MACDEMA1'] = Coin['MACDEMA1'].fillna(method='backfill')
    Coin['MACDEMA2'] = Coin['MACDEMA2'].fillna(method='backfill')
    Coin['MACD'] = Coin.MACDEMA1 - Coin.MACDEMA2
    Coin['Signal'] = 0
    Coin['Signal'] = Coin.MACD.ewm(span =SignalEMA, min_periods=SignalEMA).mean()
    Coin['Signal'] = Coin['Signal'].fillna(method='backfill') 
    Coin['FlowMACD'] = 0
    Coin.FlowMACD[(Coin.MACD < 0) & (Coin.Signal < 0)] = -1
    Coin.FlowMACD[(Coin.MACD > 0) & (Coin.Signal > 0)] = 1
    Coin['Snips'] = 0 
    Coin.Snips[(Coin.MACD < Coin.Signal) & (Coin.FlowMACD == -1)] = -1
    Coin.Snips[(Coin.MACD > Coin.Signal) & (Coin.FlowMACD == 1)] = 1
    
    
    ShortB = 0
    ShortS = 0
 
# تنضیمات مربوط به بازه صعودی
#    i = 0
#    n = 3000

# تنضیمات مربوط به بازه نزولی
#    i = 3000
#    n = 5500
 
# تنضیمات مربوط به بازه خنثی
    i = 15600
    n = 17000 
    while(i<n):
        i += 1
        Price = Coin.iloc[i].Mean
        if bnb  < (USD / 500) :
            bnb += (USD / 500) 
            Temp = (USD / 500) * Commision
            SumComm += Temp
            Temp += (USD/500)
            USD = USD - Temp                              
        
        if Coin.iloc[i].Snips == -1 and USD > 0:
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = (USD / Coin.iloc[i].Close)
            USD = 0
            ShortB += 1
            continue
        
        if Coin.iloc[i].Snips == 1 and Money > 0:
            USD = Money * Coin.iloc[i].Close
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = 0 
            ShortS += 1
  
    SumUsd = USD
    SumUsd += (Money * Coin.iloc[i-1].Mean)
    SumUsd += bnb
   
    print("USD : ",USD)
    print("SumUSD : ",SumUsd)
    print("Sum Commision : ",SumComm)
    print("BNB : ",bnb)
    print("Short Buy : ",ShortB)
    print("Short Sell : ",ShortS)