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
    
    timeperiod = 15
    
    Coin['SD'] = Coin.Mean.rolling(timeperiod, min_periods=timeperiod).mean()
    Coin['SD'] = Coin['SD'].fillna(method='backfill')
    xhat = Coin.SD - Coin.Mean
    xhat *= xhat
    Coin['SD'] = xhat.rolling(timeperiod, min_periods=timeperiod).sum()
    Coin['SD'] = Coin['SD'].fillna(method='backfill')
    Coin['SD'] = Coin.SD / (timeperiod - 1)
    Coin['SD'] = pow( Coin.SD , 0.5)
    Coin['middle'] = 0
    Coin['middle'] = Coin.Mean.ewm(span=timeperiod, min_periods=timeperiod ,adjust=True,ignore_na=False).mean()
    Coin['middle'] = Coin['middle'].fillna(method='backfill')
    Coin['upper'] = 0
    Coin['upper'] = Coin.middle + Coin.SD
    Coin['lower'] = 0
    Coin['lower'] = Coin.middle - Coin.SD
    
    Coin['CPre'] = Coin['Close'].shift(1)
    Coin['CPre'] = Coin['CPre'].fillna(method='backfill')
    
    Coin['Buy'] = 0
    Coin.Buy[ ( Coin.CPre < Coin.lower ) & ( Coin.Close >= Coin.lower ) ] = -1
    
    Coin['Sell'] = 0
    Coin.Sell[ ( Coin.CPre > Coin.upper ) & ( Coin.Close <= Coin.upper ) ] = 1
    

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

        if Coin.iloc[i].Close <= Coin.iloc[i].middle and USD > 0:
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = (USD / Coin.iloc[i].Close)
            USD = 0
            ShortB += 1
            continue
    
        if (Coin.iloc[i].Sell == 1 and Money > 0):
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
    print("Buy : ",ShortB)
    print("Sell : ",ShortS)