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
    
    EMA1 = 8
    EMA2 = 4
    Coin['MFM'] = ((Coin.Mean - Coin.Low) - (Coin.High - Coin.Mean) / (Coin.High - Coin.Low))
    Coin['MFV'] = Coin.MFM * Coin.Volume
    Coin['ADL'] = 0
    Coin['ADL'] += Coin['MFV'].shift(1)
    Coin['ChaikinEMA1'] = Coin.Mean.ewm(span=EMA1, min_periods=EMA1 ,adjust=True,ignore_na=False).mean()
    Coin['ChaikinEMA2'] = Coin.Mean.ewm(span=EMA2, min_periods=EMA2 ,adjust=True,ignore_na=False).mean()
    Coin['ChaikinOscillator'] = Coin.ChaikinEMA1 - Coin.ChaikinEMA2
    Coin['Temp1'] = Coin.Mean.shift(1)
    Coin['Temp1'].fillna(method='backfill')
    Coin['UpDown'] = 0
    Coin.UpDown[Coin.Mean > Coin.Temp1] += 1
    Coin.UpDown[Coin.Mean < Coin.Temp1] -= 1
    Coin['Temp2'] = Coin.ChaikinOscillator.shift(1)
    Coin['Temp2'].fillna(method='backfill')
    Coin['FlowChaikin'] = 0
    Coin.FlowChaikin[Coin.ChaikinOscillator > Coin.Temp2] = -1
    Coin.FlowChaikin[Coin.ChaikinOscillator < Coin.Temp2] = 1
    Coin['ChaikinSignal'] = 0
    Coin.ChaikinSignal[Coin.FlowChaikin > Coin.UpDown] = -1
    Coin.ChaikinSignal[Coin.FlowChaikin < Coin.UpDown] = 1
   
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
            
        if Coin.iloc[i].ChaikinSignal == -1 and USD > 0:
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = (USD / Coin.iloc[i].Close)
            USD = 0
            ShortB += 1
            continue
       
        if (Coin.iloc[i].ChaikinSignal == 1 and Money > 0):
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