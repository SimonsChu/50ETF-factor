# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 14:14:15 2019

@author: zhu hanfeng
"""

import pandas as pd 
import numpy as np
import datetime
import math
import matplotlib.pyplot as plt
import statsmodels.api as sm

#Signal=[]
C_P1_value=[]
C_P2_value=[]




ETF_opt_info=pd.read_csv("D:\python学习\ETF\data\Information\Opt_info.csv",encoding='gbk')
ETF=pd.read_csv("D:/python学习/ETF/ETF_asset.csv",encoding='gbk')

ETF_asset=ETF.set_index("trade_date")
#CU_asset=CU_asset.drop(index=['2019-04-25','2019-10-10'])


opt_date=pd.read_csv('D:/python学习/ETF/ETF_option_data.csv')
opt_date2=pd.read_csv("D:/python学习/sample/CU/20190905.csv")



date_list=opt_date['trade_date'].drop_duplicates().tolist()
#opt_date3= opt_date.loc[(opt_date['trade_date']==date_list[0])]
#date_list[264]
#ETF_asset.loc[date_list[1]]['etf']

def find_close_target(s, target):
    length = len(s)
    result=100
    dif=100
    for i in range(0, length):
        if abs(s[i]-1)<dif:
            dif=abs(s[i]-1)
            result=s[i]
    return result


C_P1_value=[]
C_P2_value=[]
C_P1_call_value=[]
C_P1_put_value=[]
for i in range(len(date_list)):
    
    opt_date3=opt_date.loc[(opt_date['trade_date']==date_list[i])]
    


    opt_180921=pd.merge(ETF_opt_info,opt_date3,on='ts_code',how='inner')
    opt_180921['opt_vwap']=opt_180921['amount']/opt_180921['vol']/opt_180921['per_unit']/10000
    opt_180921['ETF_vwap']=ETF_asset.loc[date_list[i]]['etf']
    opt_180921['strike_asset_ratio']=opt_180921['exercise_price']/opt_180921['ETF_vwap']
    opt_180921['maturity_date']=opt_180921['maturity_date'].apply(lambda x:datetime.datetime.strptime(str(x),'%Y%m%d'))
    opt_180921['trade_date']=opt_180921['trade_date'].apply(lambda x:datetime.datetime.strptime(str(x),'%Y%m%d'))
    opt_180921['maturity'] = (opt_180921['maturity_date']-opt_180921['trade_date'])/ np.timedelta64(1, 'D')


    if opt_180921['maturity'].min()>=10:
        opt_180921_use=opt_180921.loc[(opt_180921['maturity']== opt_180921['maturity'].min())]
    elif opt_180921['maturity'].min()<10:
        opt_180921_use=opt_180921.loc[(opt_180921['maturity'] != opt_180921['maturity'].min())]
        opt_180921_use=opt_180921_use.loc[(opt_180921_use['maturity']== opt_180921_use['maturity'].min())]
    
    

    
    
    C_P1=opt_180921_use.loc[opt_180921_use['strike_asset_ratio']==(find_close_target(opt_180921_use['strike_asset_ratio'].values.tolist(), 1))]
    C_P1_call=C_P1.loc[C_P1['call_put'] =='C']
    C_P1_put=C_P1.loc[C_P1['call_put'] =='P']
    C_P1_value.append(sum(C_P1['opt_vwap']))
    C_P1_call_value.append(sum(C_P1_call['opt_vwap']))
    C_P1_put_value.append(sum(C_P1_put['opt_vwap']))

    opt_180921_useful_call=opt_180921_use.loc[ (opt_180921_use['call_put'] =='C') &(opt_180921_use['strike_asset_ratio']<0.95)]
    opt_180921_useful_put=opt_180921_use.loc[ (opt_180921_use['call_put'] =='P') &(opt_180921_use['strike_asset_ratio']>1.05)]
    C_P2=pd.concat([opt_180921_useful_call,opt_180921_useful_put])
    C_P2_value.append(sum(C_P2['opt_vwap']*C_P2['oi'])/sum(C_P2['oi']))
   


Factor=pd.DataFrame()  
Factor['trade_date']= ETF['trade_date']   
Factor['C_P1_value'] = C_P1_value
Factor['C_P2_value'] = C_P2_value
Factor=Factor.set_index(Factor['trade_date']) 
Factor=Factor.drop(index=20190425)

Factor2=pd.DataFrame()
Factor2['trade_date']= ETF['trade_date']   
Factor2['C_P1_call_value'] = C_P1_call_value
Factor2['C_P1_put_value'] = C_P1_put_value
Factor2=Factor2.set_index(Factor2['trade_date']) 
Factor2=Factor2.drop(index=20190425)




IF=pd.read_csv('D:\python学习\ETF\IF_Fut_Daily.csv')

IF=pd.merge(IF,ETF,on='trade_date',how='inner')

#IFF=IF.set_index('trade_date')
a=Factor['C_P1_value'] /Factor['C_P2_value'] 
a_m = a.rolling(5).mean().fillna(0)
a_std = a.rolling(5).std().fillna(0)


b=Factor2['C_P1_call_value'] /Factor2['C_P1_put_value'] 
b_m = b.rolling(5).mean().fillna(0)
b_std = b.rolling(5).std().fillna(0)

c=Factor2['C_P1_call_value'] 
c_m = c.rolling(5).mean().fillna(0)
c_std = c.rolling(5).std().fillna(0)

d=Factor2['C_P1_put_value'] 
d_m = d.rolling(5).mean().fillna(0)
d_std = d.rolling(5).std().fillna(0)



signal=[]
#for i in range(len(a)):
#    if (a.iloc[i]<a_m.iloc[i]+0.5*a_std.iloc[i]) and(a.iloc[i] > a_m.iloc[i]-0.5*a_std.iloc[i]):
#        signal.append(0)
#    else:
#        signal.append(np.sign(a.iloc[i]-a_m.iloc[i]))

for i in range(len(a)):
    if (a.iloc[i]<a_m.iloc[i]+0.5*a_std.iloc[i]) and(a.iloc[i] > a_m.iloc[i]-0.5*a_std.iloc[i]):
        signal.append(0)
    elif (a.iloc[i]>a_m.iloc[i]+0.5*a_std.iloc[i]) and (c.iloc[i]>c_m.iloc[i]+0.5*c_std.iloc[i]):
        signal.append(1)
    elif (a.iloc[i]>a_m.iloc[i]+0.5*a_std.iloc[i]) and (d.iloc[i]>d_m.iloc[i]+0.5*d_std.iloc[i]):
        signal.append(-1)
    else:
        signal.append(0)

Signal=signal[:-2]
#signal[:-2]
wadad=IF.open
profit=IF.open.pct_change().shift(-2)
profit=profit[:-2]
results=sm.OLS(profit,Signal).fit()
results.summary()
#Factor.iloc[:-2]['trade_date']
X=Factor.iloc[:-2]['trade_date'].apply(lambda x:datetime.datetime.strptime(str(x),'%Y%m%d'))
Y=profit*Signal
plot(X,Y.cumsum())
plot(X,profit.cumsum())
profit.cumsum().plot(grid=True, figsize=(5,3))
