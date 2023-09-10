# -*- coding: utf-8 -*-
"""
Created on Sun Jul 30 11:17:32 2023

@author: USER
"""

from train import get_train_data,get_stations
from datetime import datetime

stations=get_stations()
menu={i+1:station for i,station in  enumerate(stations)}

print('台鐵訂票查詢系統')

while True:
    print(menu)
    print('='*50)
    try:
        start=eval(input('請輸入起始站(編號，輸入0離開):'))
        if start ==0:
            break
        end=eval(input('請輸入終止站(編號):'))

        startStation=menu[start]
        endStation=menu[end]
    except:
        print('輸入編號錯誤')
        continue
    
    print(f'[{startStation}=>{endStation}]')
    
    if input('是否繼續查詢(y/n)')=='n':
        continue
    
    
    
    ##乘車時間/查詢週期/是否有票
    
    rideDate=input('請輸入乘車時間(ex:2023/7/30):')
    if rideDate =='':
        rideDate=datetime.now().strftime('%Y/%m/%d')
    
    startTime=input('請輸入查詢起始時間(ex:00:00):')
    if startTime =='':
        startTime='00:00'
    endTime=input('請輸入查詢終止時間(ex:23:59):')
    if endTime=='':
        endTime='23:59'
        
    ticket=input('是否需查詢有票(y/n)').lower()
    ticket=True if ticket=='y' else  False
    #if ticket=='y':
        #ticket=True
    #else:
        #ticket=False
        
    print(startStation,endStation,rideDate,startTime,endTime,ticket)
    print('='*100)
    
    df=get_train_data(startStation,endStation,rideDate,startTime,endTime,ticket)
    
    print(df.iloc[:,[0,1,2,3,4,5,9,-1]])

    input('請按任一鍵')
    
print('謝謝使用')
