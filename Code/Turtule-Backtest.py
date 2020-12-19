import pandas as pd
if __name__=='__main__':
 
    Enter_Fast=41*24*2
    Exit_Fast=18*24*2
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
    Coin['Long'] = Coin['Close'].rolling(Enter_Fast, min_periods=Enter_Fast).max()
    Coin['Long'] = Coin['Long'].fillna(method='backfill')
    Coin['Short'] = Coin['Close'].rolling(Exit_Fast, min_periods=Exit_Fast).min()
    Coin['Short'] = Coin['Short'].fillna(method='backfill')
    Coin['Long_Close'] = Coin['Close'].rolling(Enter_Fast, min_periods=Enter_Fast).min()
    Coin['Long_Close'] = Coin['Long_Close'].fillna(method='backfill')
    Coin['Short_Close'] = Coin['Close'].rolling(Exit_Fast, min_periods=Exit_Fast).max()
    Coin['Short_Close'] = Coin['Short_Close'].fillna(method='backfill')
    
    ShortB = 0
    ShortS = 0
    LongB = 0
    LongS = 0
    LastPrice = Coin.iloc[1].High

# تنضیمات مربوط به بازه صعودی
#    i = 0
#    n = 3000

# تنضیمات مربوط به بازه نزولی
    i = 3000
    n = 5500
 
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
            
        if Coin.iloc[i].Low < Coin.iloc[i].Short and USD > 0:
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = (USD / Coin.iloc[i].Close)
            LastPrice = Coin.iloc[i].Close
            USD = 0
            ShortB += 1
            continue
       
        if (Coin.iloc[i].High > Coin.iloc[i].Long  and USD > 0):
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = Money + (USD / Coin.iloc[i].Close)
            LastPrice=Coin.iloc[i].Close
            USD = 0
            LongB += 1
            continue
    
        if (Coin.iloc[i].High >= Coin.iloc[i].Short_Close and Money > 0):
            USD = Money * Coin.iloc[i].Close
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = 0 
            LastPrice = Coin.iloc[i].Close
            ShortS += 1
        
        if (Coin.iloc[i].Low <= Coin.iloc[i].Long_Close  and Money > 0):
            USD = Money * Coin.iloc[i].Close
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = 0
            LastPrice = Coin.iloc[i].Close
            LongS += 1       
    
    SumUsd = USD
    SumUsd += (Money * Coin.iloc[i-1].Mean)
    SumUsd += bnb
    
    print("USD : ",USD)
    print("SumUSD : ",SumUsd)
    print("Sum Commision : ",SumComm)
    print("BNB : ",bnb)
    print("Short Buy : ",ShortB)
    print("Short Sell : ",ShortS)
    print("Long Buy : ",LongB)
    print("Long Sell : ",LongS)