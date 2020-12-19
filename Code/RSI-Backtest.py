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
    Coin['Mean'].fillna(method='backfill')
    Coin['temp'] = Coin['Mean'].shift(1)
    Coin['temp'] = Coin['temp'].fillna(method='bfill')
    Coin['Change'] = Coin.Mean - Coin.temp
   

    #---------------RSI---------------  
    #---------------Parameters--------
    RSIPeriod = 6
    #--------------Initialize--------- 
    Coin['Temp'] = Coin['Close'].shift(1)
    Coin['Temp'] = Coin['Temp'].fillna(method='backfill')
    Coin['Positive'] = 0
    Coin['Positive'] = Coin.Close - Coin.Temp
    Coin.Positive[Coin.Positive < 0] = 0
    Coin['Negative'] = 0
    Coin['Negative'] = Coin.Temp - Coin.Close
    Coin.Negative[Coin.Negative < 0] = 0
    #--RSI is beter than RSI2 & RSI3--
    Coin['MPW'] = 0
    Coin['MPW'] = Coin.Positive.ewm(span=RSIPeriod, min_periods=RSIPeriod ,adjust=True,ignore_na=False).mean()
    Coin['MPW'] = Coin['MPW'].fillna(method='backfill')
    Coin['MNW'] = 0
    Coin['MNW'] = Coin.Negative.ewm(span=RSIPeriod, min_periods=RSIPeriod ,adjust=True,ignore_na=False).mean()
    Coin['MNW'] = Coin['MNW'].fillna(method='backfill')
    RS = Coin.MPW / Coin.MNW
    RSI = 100.0 - (100.0 / (1.0 + RS))

    Coin['RSI'] = RSI
    Coin['RSIPrev'] = 0
    Coin['RSIPrev'] = Coin['RSI'].shift(1)
  
    Coin['RSISignal'] = 0
    Coin.RSISignal[Coin.RSI < 30] = -1        
    Coin.RSISignal[Coin.RSI > 70] = 1

    Coin['MPW2'] = 0
    Coin['MPW2'] =  Coin.Positive.ewm(span=RSIPeriod * 6, min_periods=RSIPeriod * 6 ,adjust=True,ignore_na=False).mean()
    Coin['MPW2'] = Coin['MPW2'].fillna(method='backfill')
    Coin['MNW2'] = 0
    Coin['MNW2'] = Coin.Negative.ewm(span=RSIPeriod * 6, min_periods=RSIPeriod * 6 ,adjust=True,ignore_na=False).mean()
    Coin['MNW2'] = Coin['MNW2'].fillna(method='backfill')
    RS2 = Coin.MPW2 / Coin.MNW2
    RSI2 = 100.0 - (100.0 / (1.0 + RS2))
    Coin['RSI2'] = RSI2
            
    Coin['RSISignal4'] = 0
    Coin.RSISignal4[(Coin.RSI < 50) & (Coin.RSI2 > 55)] = -1        
    Coin.RSISignal4[(Coin.RSI > 50) & (Coin.RSI2 < 45)] = 1
    
    #------------End of RSI------------  
    ShortB = 0
    ShortS = 0
    LastPrice = Coin.iloc[1].High

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

        if Coin.iloc[i].RSISignal4 == -1 and USD > 0:
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = (USD / Coin.iloc[i].Close)
            USD = 0
            ShortB += 1
            continue

        if (Coin.iloc[i].RSISignal4 == 1 and Money > 0):
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