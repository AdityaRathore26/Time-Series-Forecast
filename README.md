# Time-Series-Forecast
Firstly the Flow values recorded at every 10 min interval for 2 years by Flow meters is imported.
HBZ1.xlsx contains the raw data set containing 100344 observations.
In forecasting1.py the time series model is explained stepwise from data cleaning to getting the forecasted flows. 
Keep this in mind that forecasted value depends on the amount of data you're using to train the model.
These forecasted values are then used in untitled1.py to get the water supply schedule pertaining to optimum storage incurred and returns the total cost of supplying per unit water.
