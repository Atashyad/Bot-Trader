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
    
    AO1 = 18
    AO2 = 36
    Coin['MAO1'] = 0
    Coin['Mid'] = 0
    Coin['Mid'] =  (Coin.Low + Coin.High) / 2
    Coin['MAO1'] = Coin.Mid.ewm(span=AO1, min_periods=AO1 ,adjust=True,ignore_na=False).mean()
    Coin['MAO1'].fillna(method='backfill')
    Coin['MAO2'] = 0
    Coin['MAO2'] = Coin.Mid.ewm(span=AO2, min_periods=AO2 ,adjust=True,ignore_na=False).mean()
    Coin['MAO2'].fillna(method='backfill')
    Coin['AwesomeOscillator'] = Coin.MAO1 - Coin.MAO2 
    Coin['Temp'] = Coin['AwesomeOscillator'].shift(1)
    Coin['Temp'] = Coin['Temp'].fillna(method='backfill') 
    Coin['AOFlow'] = 0
    Coin.AOFlow[(Coin.AwesomeOscillator > Coin.Temp) & (Coin.AwesomeOscillator > 0)] = 1        
    Coin.AOFlow[(Coin.AwesomeOscillator < Coin.Temp) & (Coin.AwesomeOscillator < 0)] = -1
    Coin['Temp1'] = Coin['AOFlow'].shift(1)
    Coin['Temp1'] = Coin['Temp1'].fillna(method='backfill') 
    Coin['AOSignal'] = 0
    Coin.AOSignal[Coin.AOFlow < Coin.Temp1] = 1        
    Coin.AOSignal[Coin.AOFlow > Coin.Temp1] = -1

    ShortB = 0
    ShortS = 0
    
    LastPrice = Coin.iloc[1].High

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
            
        if Coin.iloc[i].AOSignal == -1 and USD > 0:
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = (USD / Coin.iloc[i].Close)
            LastPrice = Coin.iloc[i].Close
            USD = 0
            ShortB += 1
            continue
       
        if (Coin.iloc[i].AOSignal == 1 and Money > 0):
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
   