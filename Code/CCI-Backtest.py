import pandas as pd
if __name__=='__main__':
# خواندن اطلاعات به منظور داده کاوی تراکنش های گذشته بورس
    Coin=pd.read_csv('d://csv//BtcBinance.csv',parse_dates=True)
# پیاده سازی شاخص فنی CCI
    Coin['Quote'] = Coin['Quote asset volume']
    Coin['Mean'] = Coin.Quote/Coin.Volume
    Coin['Mean'] = Coin['Mean'].fillna(method='backfill')
    timeperiod = 6
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
    Coin['CCI'] = 0
    Coin['CCI'] = (Coin.Close - Coin.middle) / (0.015 * Coin.SD)
    Coin['CCISignal'] = 0
    Coin.CCISignal[Coin.CCI < -100] = -1        
    Coin.CCISignal[Coin.CCI > 100] = 1
# داده کاوی تراکنش های گذشته بورس
    USD = 1000
    SumUsd = 1000
    Money = 0
    bnb = 0
    Commision = 0.00075
    SumComm = 0
    Buy = 0
    Sell = 0
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

        if Coin.iloc[i].CCISignal == -1 and USD > 0:
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = (USD / Coin.iloc[i].Close)
            USD = 0
            Buy += 1
            continue

        if Coin.iloc[i].CCISignal == 1 and Money > 0:
            USD = Money * Coin.iloc[i].Close
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = 0 
            Sell += 1
            
    SumUsd = USD
    SumUsd += (Money * Coin.iloc[i-1].Mean)
    SumUsd += bnb
# محاسبه سود یا ضرر و کمسیون معاملات در انتهای دوره
    print("Sum USDT : ",SumUsd)
    print("Sum Commission : ",SumComm)
    print("BNB : ",bnb)
    print("Buy : ",Buy)
    print("Sell : ",Sell)