import pandas as pd
import talib
import matplotlib.pyplot as plt
if __name__=='__main__':
    USD = 1000
    SumUsd = 1000
    Money = 0
    Price = 0
    bnb = 0
    Commision = 0.00075
    SumComm = 0
    Coin=pd.read_csv('d://csv//BtcBinance.csv',parse_dates=True)
#    Coin=pd.read_csv('d://csv//NeoBinance.csv',parse_dates=True)
    Coin['Quote'] = Coin['Quote asset volume']
    Coin['Mean'] = Coin.Quote/Coin.Volume
    Coin['Mean'] = Coin['Mean'].fillna(method='backfill')
    
    Coin['temp'] = Coin['Mean'].shift(1)
    Coin['temp'] = Coin['temp'].fillna(method='bfill')
    Coin['Change'] = Coin.Mean - Coin.temp
    
    #---------------ADX---------------  
    #---------------Parameters--------
    EMA1 = 14
    #--------------Initialize--------- 
    Coin['EMA'] = Coin.Mean.ewm(span=EMA1, min_periods=EMA1 ,adjust=True,ignore_na=False).mean()
    Coin['EMA'] = Coin['EMA'].fillna(method='backfill')
    Coin['ADX'] = 0
    Coin['ADX'] = talib.ADX(high=Coin.High,low=Coin.Low,close=Coin.Close,timeperiod=10)
    #---------------End of ADX---------------
   
    #---------------Turtule---------------  
    #---------------Parameters--------
    Enter_Fast=41*24*2
    Exit_Fast=18*24*2
    #--------------Initialize--------- 
    Coin['Long'] = Coin['Close'].rolling(Enter_Fast, min_periods=Enter_Fast).max()
    Coin['Long'] = Coin['Long'].fillna(method='backfill')
    Coin['Short'] = Coin['Close'].rolling(Exit_Fast, min_periods=Exit_Fast).min()
    Coin['Short'] = Coin['Short'].fillna(method='backfill')
    Coin['Long_Close'] = Coin['Close'].rolling(Enter_Fast, min_periods=Enter_Fast).min()
    Coin['Long_Close'] = Coin['Long_Close'].fillna(method='backfill')
    Coin['Short_Close'] = Coin['Close'].rolling(Exit_Fast, min_periods=Exit_Fast).max()
    Coin['Short_Close'] = Coin['Short_Close'].fillna(method='backfill')
    #---------------End of Turtule---------------
    
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
    Coin['RSILong'] = RSI2
    #------------End of RSI------------  

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
    #---------------End of Stochastic--------  

    #---------------CCI--------  
    #---------------Parameters--------
    StochasticK = 24
    StochasticD = 15
    #--------------Initialize---------
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
    #---------------End of CCI--------  

    PeriodTrendLong = 40
# پیاده سازی شاخص های فنی MA بلند مدت و کوتاه مدت
    Coin['MALong'] = 0
    Coin['MALong'] = Coin.Close.ewm(span=PeriodTrendLong * 2, min_periods=PeriodTrendLong * 2,adjust=True,ignore_na=False).mean()
    Coin['MALong'] = Coin['MALong'].fillna(method='backfill')
    Coin['MAShort'] = 0
    Coin['MAShort'] = Coin.Close.ewm(span=PeriodTrendLong , min_periods=PeriodTrendLong ,adjust=True,ignore_na=False).mean()
    Coin['MAShort'] = Coin['MAShort'].fillna(method='backfill')
    Coin['Flow'] = 0
    Coin.Flow[( Coin.MALong > Coin.MAShort ) & ( Coin.MAShort > Coin.Close )] = -1
    Coin.Flow[( Coin.MAShort > Coin.MALong ) & ( Coin.Close > Coin.MAShort )] = 1  

    Buy = 0
    Sell = 0
    
    i = 0
    n = 17000
    z = 25
    while(i<n):
        i += 1
        Price = Coin.iloc[i].Mean
        if bnb  < (USD / 500) :
            bnb += (USD / 500) 
            Temp = (USD / 500) * Commision
            SumComm += Temp
            Temp += (USD/500)
            USD = USD - Temp                              
            
        if (((Coin.iloc[i].RSISignal == -1 or Coin.iloc[i].CCISignal == -1) and Coin.iloc[i].Flow == 1) or ((Coin.iloc[i].StochasticPeak == -1 or Coin.iloc[i].RSISignal == -1) and Coin.iloc[i].Flow == -1) or ((Coin.iloc[i].StochasticPeak == -1 or (Coin.iloc[i].Low < Coin.iloc[i].Short or Coin.iloc[i].High > Coin.iloc[i].Long)) and Coin.iloc[i].Flow == 0)) and USD > 0:
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = (USD / Coin.iloc[i].Close)
            USD = 0
            Buy += 1
            continue
    
        if (((Coin.iloc[i].RSISignal == 1 or Coin.iloc[i].CCISignal == 1) and Coin.iloc[i].Flow == 1) or ((Coin.iloc[i].StochasticPeak == 1 or Coin.iloc[i].RSISignal == 1) and Coin.iloc[i].Flow == -1) or ((Coin.iloc[i].StochasticPeak == 1 or (Coin.iloc[i].High >= Coin.iloc[i].Short_Close or Coin.iloc[i].Low <= Coin.iloc[i].Long_Close)) and Coin.iloc[i].Flow == 0)) and Money > 0:
            USD = Money * Coin.iloc[i].Close
            SumComm += USD * Commision
            bnb -= USD * Commision
            Money = 0 
            Sell += 1
        
    SumUsd = USD
    SumUsd += (Money * Coin.iloc[i-1].Mean)
    SumUsd += bnb
  
    print("USD : ",USD)
    print("SumUSD : ",SumUsd)
    print("Sum Commision : ",SumComm)
    print("BNB : ",bnb)
    print("Buy : ",Buy)
    print("Sell : ",Sell)