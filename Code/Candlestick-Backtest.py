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
    #Coin=pd.read_csv('d://csv//EthBinance.csv',parse_dates=True)
    
    Coin['Quote'] = Coin['Quote asset volume']
    Coin['Mean'] = Coin.Quote/Coin.Volume
    Coin['Mean'] = Coin['Mean'].fillna(method='backfill')
    #----------Candlestick------------
    #----------Parameters-------------
    #-----------Initialize------------ 
    Coin['MAO1'] = 0
    Range = (Coin.High - Coin.Low)
    Coin['Body'] = 0
    Coin['Body'] = abs(Coin.Close - Coin.Open) / Range
    Coin['Color'] = 0
    Coin.Color[Coin.Close > Coin.Open] = 1
    Coin.Color[Coin.Close < Coin.Open] = -1
    Coin['Upper'] = 0
    Coin.Upper[(Coin.Color == 1)] = (Coin.High - Coin.Close) / Range
    Coin.Upper[(Coin.Color == -1)] = (Coin.High - Coin.Open) / Range
    Coin['Lower'] = 0
    Coin.Lower[(Coin.Color == 1)] = (Coin.Open - Coin.Low) / Range
    Coin.Lower[(Coin.Color == -1)] = (Coin.Close - Coin.Low) / Range
    Coin['OpenP'] = 0
    Coin['OpenP'] = Coin['Open'].shift(1)
    Coin['OpenP'] = Coin['OpenP'].fillna(method='backfill')
    Coin['CloseP'] = 0
    Coin['CloseP'] = Coin['Close'].shift(1)
    Coin['CloseP'] = Coin['CloseP'].fillna(method='backfill')
    Coin['BodyP'] = 0
    Coin['BodyP'] = Coin['Body'].shift(1)
    Coin['BodyP'] = Coin['BodyP'].fillna(method='backfill')
    Coin['HighP'] = 0
    Coin['HighP'] = Coin['High'].shift(1)
    Coin['HighP'] = Coin['HighP'].fillna(method='backfill')
    Coin['LowP'] = 0
    Coin['LowP'] = Coin['Low'].shift(1)
    Coin['LowP'] = Coin['LowP'].fillna(method='backfill')
    Coin['UpperP'] = 0
    Coin['UpperP'] = Coin['Upper'].shift(1)
    Coin['UpperP'] = Coin['UpperP'].fillna(method='backfill')
    Coin['LowerP'] = 0
    Coin['LowerP'] = Coin['Lower'].shift(1)
    Coin['LowerP'] = Coin['LowerP'].fillna(method='backfill')

    Coin['Hummer'] = 0
    z = 0.2
    Coin.Hummer[(Coin.Color == 1) & (Coin.Lower >= (2 * Coin.Body)) & (Coin.Upper <= z) & (Coin.Body >= 0.1)] = 1
    Coin.Hummer[(Coin.Color == -1) & (Coin.Upper >= (2 * Coin.Body)) & (Coin.Lower <= z) & (Coin.Body >= 0.1)] = -1
    
    Coin['Star'] = 0
    Coin.Star[(Coin.Color == 1) & (Coin.CloseP < Coin.Open)] = 1
    Coin.Star[(Coin.Color == -1) & (Coin.CloseP > Coin.Open)] = -1

    Coin['TwoMarabozo']  = 0
    Coin.TwoMarabozo[(Coin.Close > Coin.CloseP) & (Coin.Open > Coin.OpenP) & (Coin.Body > Coin.BodyP) & (Coin.CloseP > Coin.OpenP) & (Coin.Color == 1)] = 1
    Coin.TwoMarabozo[(Coin.Close < Coin.CloseP) & (Coin.Open < Coin.OpenP) & (Coin.Body > Coin.BodyP) & (Coin.CloseP < Coin.OpenP) & (Coin.Color == -1)] = -1                       
    
    Coin['Bullish']  = 0
    Coin.Bullish[(Coin.CloseP < Coin.OpenP) & (Coin.Open <= Coin.CloseP) & (Coin.Close >= Coin.OpenP) & (Coin.Color == 1)] = 1
    Coin.Bullish[(Coin.CloseP > Coin.OpenP) & (Coin.Open >= Coin.CloseP) & (Coin.Close <= Coin.OpenP) & (Coin.Color == -1)] = -1
    
    Coin['Harami']  = 0
    Coin.Harami[(Coin.CloseP < Coin.OpenP) & (Coin.CloseP < Coin.Open) & (Coin.OpenP > Coin.Close) & (Coin.Color == 1) & (((((Coin.Open + Coin.Low) / 2 ) - Coin.CloseP) / ( Coin.OpenP - ((Coin.Close + Coin.High) / 2 ))) >= 1)] = 1
    Coin.Harami[(Coin.CloseP > Coin.OpenP) & (Coin.CloseP > Coin.Open) & (Coin.OpenP < Coin.Close) & (Coin.Color == -1) & (((((Coin.Close + Coin.Low) / 2 ) - Coin.OpenP) / ( Coin.CloseP - ((Coin.Open + Coin.High) / 2 ))) <= 1)] = -1
    
    Coin['Tweezer']  = 0
    Coin.Tweezer[(Coin.CloseP < Coin.OpenP) & ((Coin.Low / Coin.LowP ) >= 1) & ((Coin.Lower + Coin.LowerP) >= (2 * (Coin.Upper + Coin.UpperP))) & (Coin.Color == 1)] = 1
    Coin.Tweezer[(Coin.CloseP > Coin.OpenP) & ((Coin.HighP / Coin.High ) >= 1) & ((Coin.Upper + Coin.UpperP) >= (2 * (Coin.Lower + Coin.LowerP))) & (Coin.Color == -1)] = -1 
    #-------End of Candlestick--------

    ShortB = 0
    ShortS = 0
    
            # تنضیمات مربوط به بازه صعودی
#        i = 0
#        n = 3000

            # تنضیمات مربوط به بازه نزولی
#        i = 3000
#        n = 5500
 
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
           
        if (Coin.iloc[i].Tweezer == -1 or Coin.iloc[i].TwoMarabozo == -1 or Coin.iloc[i].Star == -1) and USD > 0:
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = (USD / Coin.iloc[i].Close)
            USD = 0
            ShortB += 1
            continue
       
        if (Coin.iloc[i].Tweezer == 1 or Coin.iloc[i].TwoMarabozo == 1 or Coin.iloc[i].Star == 1) and Money > 0:
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