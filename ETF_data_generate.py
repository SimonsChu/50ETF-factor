# -*- coding: utf-8 -*-
"""
Created on Sat Nov  9 14:02:42 2019

@author: zhu hanfeng
"""

import pandas as pd 
import numpy as np
import datetime
import tushare as ts



token='4ab5b15fa513c178b5a92733edb80259aa0203de44fde37fa6025639'
ts.set_token(token)
pro = ts.pro_api()
date=pro.trade_cal(exchange='', start_date='20160201', end_date='20191107')
trade_dates=date.loc[date['is_open']==1]
trade_dates=trade_dates.reset_index()
ETF_option_data=pd.DataFrame()

for i in range(len(trade_dates['cal_date'])):
    a=trade_dates['cal_date'][i]
    b=str('D:/python学习/ETF/data/Curve/')+str(a)+str('.csv')
    df=pd.read_csv(b)
    ETF_option_data=pd.concat([ETF_option_data,df])
'''
CU_option_data=CU_option_data
CU_option_data2=CU_option_data2
CU_option_data3=CU_option_data3

CU_option_data=pd.concat([CU_option_data,CU_option_data2,CU_option_data3])
CU_option_data.to_csv('D:/python学习/sample/CU_option_data.csv') #
'''
ETF_option_data.to_csv('D:/python学习/ETF/ETF_option_data.csv')
