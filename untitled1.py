# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 21:54:33 2022

@author: abc
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 02:04:54 2022

@author: abc
"""

import pandas as pd
import numpy as np
import pulp



df_small=pd.read_excel("demand_profile.xlsx",index_col="Hours",sheet_name="small")
df_med=pd.read_excel("demand_profile.xlsx",index_col="Hours",sheet_name="medium")
df_large=pd.read_excel("demand_profile.xlsx",index_col="Hours",sheet_name="large")

a=np.arange(0,25)

tco=pulp.LpProblem("TCO",pulp.LpMinimize)
xs=pulp.LpVariable.dicts("xs",(a),lowBound=0,upBound=1000,cat="Countinuous")
z=pulp.LpVariable.dicts("z",([1,2]),lowBound=0,cat="Countinuous")


  
tco+=pulp.lpSum([xs[i] for i in a])==sum(df_large["D"])
    
for i in a:
       
    tco+=z[1]>=(df_large.loc[i,"D"]-xs[i])
    tco+=z[2]>=(xs[i]-df_large.loc[i,"D"])
    
tco+=z[1]+z
tco+=z[1]+z[2]<=2725
tco+=5.5*(z[1]+z[2])+pulp.lpSum(15*xs[i] for i in a)

tco.solve()

print("Status:",pulp.LpStatus[tco.status])
print("Total cost:",pulp.value(tco.objective))



final_out=pd.DataFrame(columns=["D"],index=a)

for i in a:
    final_out.loc[i,"D"]=xs[i].varValue

    
