# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 19:19:07 2022

"""

import pandas as pd
import numpy as np
from pmdarima.arima import auto_arima
from pandas import to_datetime
import datetime

df1=pd.read_excel("HBZ1.xlsx",parse_dates=True)
df1=df1[["DATE","FLOW(l/s)"]]
df1.columns=["Date","Flow"]

#all flow values<10 are treated as NA
df1.loc[df1['Flow'] < 20] = np.nan

groupkey=pd.to_datetime(df1.Date.dt.strftime('%Y-%m-%d %H'))
df2=df1.groupby(groupkey).agg({'Flow':'mean'})


def processOutliers(inputSeries):
    inputSeries.reset_index(inplace=True,drop=True)
    
    
    # First quartile (Q1)
    Q1 = np.percentile(inputSeries["Flow"], 25, interpolation = 'midpoint')
  
    # Third quartile (Q3)
    Q3 = np.percentile(inputSeries["Flow"], 75, interpolation = 'midpoint')
  
    # Interquaritle range (IQR)
    IQR = Q3 - Q1
    
    for i in range(len(inputSeries)):
        
        if (inputSeries["Flow"].notna()[i] and (inputSeries.loc[i,"Flow"] < Q1 - 1.5 * IQR)):
            inputSeries.loc[i,"Flow"] = Q1 - 1.5 * IQR
            
        elif (inputSeries["Flow"].notna()[i] and (inputSeries.loc[i,"Flow"] > Q3 + 1.5 * IQR)):
            inputSeries.loc[i,"Flow"] = Q3 + 1.5 * IQR
    
    # inputSeries.reset_index(inplace=True,drop=True)       
            
    return inputSeries



#defining AUTO ARIMA model
def AUTO_ARIMA_model(data,period):
    
    #for weekdays
    arima_model=auto_arima(data,alpha=0,information_criterion='aicc',stepwise=True,seasonal=True,m=24)
    prediction=arima_model.predict(n_periods=period)
    return prediction

df3=df2.copy()
# df4=processOutliers(df3)


#Making Train and Test Data

df3.reset_index(inplace=True)
train = df3[(df3.Date > '2021-10-31') & (df3.Date < '2021-11-24') ]
test=df3[(df3.Date >= '2021-11-24')]

# train=df3[:-len(df3.tail(60))]
# test=df3.tail(60)╢
df_train=train.copy()
df_test=test.copy()


df_train1=processOutliers(df_train)
df_test1=processOutliers(df_test)

df_train1.set_index("Date",inplace=True)
df_test1.set_index("Date",inplace=True)


Test_Forecast=AUTO_ARIMA_model(df_train1,len(df_test1))
Prediction_file=pd.DataFrame(index=df_test1.index)

Prediction_file["Actual_Flow"]=df_test["Flow"]
Prediction_file["Predicted_Flow"]=Test_Forecast


Prediction_file.to_excel("Test_file.xlsx")



#Future_forecasting
df_full=df3[(df3.Date > '2021-08-31') & (df3.Date < '2021-11-27') ]

df_full1=df_full.copy()

df_full2=processOutliers(df_full1)

df_full2.set_index("Date",inplace=True)



Forecast_Data = pd.date_range(df_full2.index[-1], df_full2.index[-1]+datetime.timedelta(days=7), freq='H')
Forecast_Data=pd.DataFrame(Forecast_Data)
Forecast_Data=Forecast_Data[1:]
Forecast_Data.columns=(["Date"])

Forecast_Data.set_index("Date",inplace=True)

period=len(Forecast_Data)

Forecasted_Flow=AUTO_ARIMA_model(df_full2,period)


Forecast_Data["Predicted_Flow"]=Forecasted_Flow

Forecast_Data.to_excel("Future_Forecast.xlsx")











