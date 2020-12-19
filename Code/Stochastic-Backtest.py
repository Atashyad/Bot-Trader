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
    
    #---------------Stochastic--------  
    #---------------Parameters--------
    StochasticK = 24
    StochasticD = 15
    #--------------Initialize--------- 
    Coin['LowStochastic'] = 0
    Coin['LowStochastic'] = Coin.Low.rolling(StochasticK , min_periods=StochasticK).min()
    Coin['LowStochastic'] = Coin['LowStochastic'].fillna(method='backfill')
    Coin['HighStochastic'] = 0
    Coin['HighStochastic'] = Coin.High.rolling(StochasticK , min_periods=StochasticK).max()
    Coin['HighStochastic'] = Coin['HighStochastic'].fillna(method='backfill')
    Coin['Stochastic1'] = ((Coin.Close - Coin.LowStochastic) / (Coin.HighStochastic - Coin.LowStochastic)) * 100
    Coin['Stochastic'] = Coin.Stochastic1.ewm(span=StochasticD, min_periods=StochasticD ,adjust=True,ignore_na=False).mean()
    Coin['Stochastic'] = Coin['Stochastic'].fillna(method='backfill')
    Coin['Temp'] = Coin.Stochastic.shift(1)
    Coin['Temp'] = Coin['Temp'].fillna(method='backfill')
    Coin['FlowStochastic'] = 0
    Coin.FlowStochastic[Coin.Stochastic > Coin.Temp] += 1
    Coin.FlowStochastic[Coin.Stochastic < Coin.Temp] -= 1
    Coin['StochasticPeak'] = 0
    Coin.StochasticPeak[Coin.Stochastic > 80] += 1
    Coin.StochasticPeak[Coin.Stochastic < 20] -= 1

    ShortB = 0
    ShortS = 0
  
# تنضیمات مربوط به بازه صعودی
    i = 0
    n = 3000

# تنضیمات مربوط به بازه نزولی
#    i = 3000
#    n = 5500
 
# تنضیمات مربوط به بازه خنثی
#    i = 15600
#    n = 17000 
    while(i<n):
        i += 1
        Price = Coin.iloc[i].Mean
        if bnb  < (USD / 500) :
            bnb += (USD / 500) 
            Temp = (USD / 500) * Commision
            SumComm += Temp
            Temp += (USD/500)
            USD = USD - Temp                              
            
        if Coin.iloc[i].StochasticPeak == -1 and USD > 0:
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = (USD / Coin.iloc[i].Close)
            LastPrice = Coin.iloc[i].Close
            USD = 0
            ShortB += 1
            continue
    
        if Coin.iloc[i].StochasticPeak == 1 and Money > 0:
            USD = Money * Coin.iloc[i].Close
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = 0 
            LastPrice = Coin.iloc[i].Close
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
