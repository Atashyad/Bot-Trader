import pandas as pd
import matplotlib.pyplot as plt
if __name__=='__main__':
# خواندن اطلاعات به منظور داده کاوی تراکنش های گذشته بورس و یافتن نقاط تغییر روند
    Coin=pd.read_csv('d://csv//BtcBinance.csv',parse_dates=True)
    Coin = Coin[0:500]
    Coin.reset_index(inplace=True,drop=True)
    s = 0
    end = int(Coin.index.max())
    Coin = Coin[['Close']]
    PeriodTrendLong = 40
# پیاده سازی شاخص های فنی MA بلند مدت و کوتاه مدت
    Coin['MALong'] = 0
    Coin['MALong'] = Coin.Close.ewm(span=PeriodTrendLong * 2, min_periods=PeriodTrendLong * 2,adjust=True,ignore_na=False).mean()
    Coin['MALong'] = Coin['MALong'].fillna(method='backfill')
    Coin['MAShort'] = 0
    Coin['MAShort'] = Coin.Close.ewm(span=PeriodTrendLong , min_periods=PeriodTrendLong ,adjust=True,ignore_na=False).mean()
    Coin['MAShort'] = Coin['MAShort'].fillna(method='backfill')
    Coin['Flow'] = 0
    Coin.Flow[( Coin.MALong > Coin.MAShort )] = -1
    Coin.Flow[( Coin.MAShort > Coin.MALong )] = 1  
# تشخیص روند های صعودی و شماره گذاری آنها
    i = 0
    j = 1
    k = False
    while i<=end-s:
        while Coin.iloc[i].Flow == 1 and i<=end-s :            
            Coin['Flow'].iloc[i] += j
            i += 1
            k = True
            if i>end-s:
                break
        if k:
            j += 2
            k = False
        i += 1
# تشخیص روند های نزولی و شماره گذاری آنها
    i = 0
    j = 2
    k = False
    while i<=end-s :
        while (Coin.iloc[i].Flow == -1 or Coin.iloc[i].Flow == 0) and i<=end-s :                   
            if Coin.iloc[i].Flow == 0:
                Coin['Flow'].iloc[i] = -1
            Coin['Flow'].iloc[i] += j
            i += 1
            k = True
            if i>end-s:
                break
        if k:
            j += 2
            k = False
        i += 1   

    Points = pd.DataFrame()
# پیدا کردن ماکزیمم در هر روند صعودی بوسیله گروهبندی روندها بر اساس شماره روند
# پیدا کردن مینیمم در هر روند نزولی بوسیله گروهبندی روندها بر اساس شماره روند
    Points['Maximum'] = 0
    Points['Maximum'] = Coin.groupby('Flow', sort=False)['Close'].max()
    Points['Minimum'] = 0
    Points['Minimum'] = Coin.groupby('Flow', sort=False)['Close'].min()
    Points['Pivot'] = 0
    for j in range(len(Coin)):
        if Coin.iloc[j].Flow == 0:
            continue
        if Coin.iloc[j].Flow % 2 == 0:
            for i in range(len(Points)):
                if i % 2 == 0:
                    Points['Pivot'].iloc[i] = Points['Maximum'].iloc[i]
                else:
                    Points['Pivot'].iloc[i] = Points['Minimum'].iloc[i]
        else:
            for i in range(len(Points)):
                if i % 2 == 0:
                    Points['Pivot'].iloc[i] = Points['Minimum'].iloc[i]
                else:
                    Points['Pivot'].iloc[i] = Points['Maximum'].iloc[i]
        break
# پیدا کردن اندیس نقاط تغییر روند
    Points['index'] = 0
    j = 0
    for i in range(len(Points)):
        while( j < len(Coin)):
            if Points['Pivot'].iloc[i] == Points['Minimum'].iloc[i] and Points['Pivot'].iloc[i] == Coin.iloc[j].Close and Points['index'].iloc[i] == 0:
                    Points['index'].iloc[i] = j
            elif Points['Pivot'].iloc[i] == Points['Maximum'].iloc[i] and Points['Pivot'].iloc[i] == Coin.iloc[j].Close:
                    Points['index'].iloc[i] = j
            j += 1
            if ( j == len(Coin)):
                break
            if Coin.iloc[j].Flow != Coin.iloc[j - 1].Flow:
                break
# نمایش نمودار قیمت زمان
    plt.figure()
    Coin.Close.plot()
    Coin.MALong.plot()
    Coin.MAShort.plot()
    plt.legend(['Close','MA-Long','MA-Short'])
    plt.show()

    Pivot = list()
    PivotIndex = list()
    Pivot = []
    PivotIndex = []
    Pivot.append(Coin.iloc[0].Close)
    PivotIndex.append(0)
    for i in range(len(Points)):
        Pivot.append(Points['Pivot'].iloc[i])
        PivotIndex.append(Points['index'].iloc[i])
    Pivot.append(Coin.iloc[Coin.index.max()].Close)
    PivotIndex.append(Coin.index.max())    
# نمایش نقاط تغییر روند
    plt.plot(PivotIndex, Pivot)
    plt.xlabel('Time')
    plt.ylabel('Pivot')
#    plt.savefig("TimePlot.pdf")
    plt.show()