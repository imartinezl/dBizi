# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 10:03:02 2018

@author: Inigo
"""

#%% LIBRARIES IMPORT
import json
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import psycopg2
import datetime
from dateutil import tz

matplotlib.rcParams['timezone'] = 'Europe/Madrid'
#%% CONNECTION WITH RASPBERRY DB

conn_string = "host='localhost' dbname='dBici' user='postgres' password='root'"
from key import conn_string


def get_data(conn_string):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stations_data")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

#%% OBTAIN DATA FROM DB
    
data = get_data(conn_string)

df = pd.DataFrame()
for i in range(len(data)):
    unixtime = data[i][1]
    df_temp = pd.read_json(json.dumps(data[i][2]))
    df_temp['unixtime'] = unixtime
    df = pd.concat([df,df_temp])
    
df['date'] = pd.to_datetime(df['unixtime'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Europe/Madrid') #GET DATE
df['day'] = [x.day for x in df['date']] #GET DAY
df['hour'] = [x.hour for x in df['date']] #GET HOUR
df['minute'] = [x.minute for x in df['date']] #GET HOUR

df['bases_eng_lib'] = df['bases_enganchadas'] + df['bases_libres'] #ENGANCHADAS + LIBRES
df['bases_bloq'] = df['numero_bases'] - df['bases_eng_lib'] # BLOQUEO: si no coincide #bases con #enganchadas + #libres
df['bases_enganchadas_sft'] = df.groupby(['nombre'])['bases_enganchadas'].transform(lambda x:(x - x.shift(1))) 
df['bases_libres_sft'] = df.groupby(['nombre'])['bases_libres'].transform(lambda x:(x - x.shift(1))) 
df['bases_dif'] = df['bases_enganchadas_sft'] + df['bases_libres_sft']

df['to_road'] = df.groupby(['nombre'])['bases_libres'].transform(lambda x:(x - x.shift(1))) 
# TO ROAD: bicis que entran (+) o salen (-) del sistema

df.index = range(df.shape[0])

#%% STATIONS INFORMATION

station_cols = ['numero_estacion', 'nombre','latitud','longitud']
station_features = pd.DataFrame(list(df.groupby(station_cols).groups.keys()), columns = station_cols)
#station_features.to_csv('stations_location.csv',index=False)


#%% GET SUBSET FOR OPTIMIZATION
df.groupby('day').sum()
subset_cond = (df['date'] < "2018-06-08 23:00:00+02:00") & (df['date'] > "2018-06-08 06:00:00+02:00")
df_subset = df[subset_cond]
df_subset = df[(df['day']==6) & (df['hour']>5)  & (df['hour']<24)]
plt.plot(df_subset['date'],df_subset['to_road'])
plt.xticks(rotation=90)

per_ts = df_subset.groupby('date')['to_road'].apply(sum)
ts_start = 0
ts_end = per_ts.shape[0]-1
s = np.zeros(per_ts.shape[0])
for i in range(ts_start+1, per_ts.shape[0]):
    s[i] = s[i-1] + per_ts.iloc[i-1]
    if s[i]==0:
        ts_end=i
#        break
plt.plot(per_ts.index,s, color='darkgreen')
#[plt.axvline("2018-06-" + str(x) + " 23:00:00+02:00", color='red') for x in range(3,22)]
#[plt.axvline("2018-06-" + str(x) + " 07:00:00+02:00", color='blue') for x in range(3,22)]
    
df_study = df_subset[(df_subset['date'] >= per_ts.index[ts_start]) & (df_subset['date'] < per_ts.index[ts_end])]
condition_start = df_study.groupby('date')['to_road'].apply(lambda x: any(x<0)) #should be false at start
condition_end = df_study.groupby('date')['to_road'].apply(lambda x: any(x>0)) #should be false at end
    
#%%# HACKING OF CONDITIONS
# for day 5
df_study['to_road'].loc[[4672,4681,4685]] = 0
df_study['to_road'].loc[4677] = -5
#%%
per_ts = df_subset.groupby('date').apply(sum)
s = df_subset.groupby('numero_estacion')['bases_dif'].apply(np.cumsum)
s = np.cumsum(per_ts['bases_dif'])

s = df_subset.groupby('numero_estacion')['bases_libres_sft'].apply(np.cumsum)
plt.plot(s,marker='.', linewidth=0)
plt.xticks(rotation=90)
plt.axhline(y=0,color='red')
plt.grid()

#%% H: restricciones del sistema (entradas y salidas) 

H = df_study[['numero_estacion','unixtime','to_road']].values
H = H[np.abs(H[:,2])!=0.0]
m = H.shape[0]

od_matrix = list() # od_matrix: variables del sistema (viaje origen destino con tiempos)     
ts = 0
for i in range(m): 
    station = H[i,0]
    timestamp = H[i,1]
    value = H[i,2]
    proposed_rows = (value > 0) &  (H[:,2] < 0) & (H[:,1] > timestamp) & (H[:,0] != station)
    for x in H[proposed_rows,0:2].tolist():
        new_entry = [station, timestamp] + x
        od_matrix.append(new_entry)
    proposed_rows = (value < 0) &  (H[:,2] > 0) & (H[:,1] < timestamp) & (H[:,0] != station)
    for x in H[proposed_rows,0:2].tolist():
        new_entry = [station, timestamp] + x
        od_matrix.append(new_entry)
                
od_matrix = pd.DataFrame(od_matrix)
od_matrix = od_matrix.drop_duplicates()
od_matrix.columns = ['origin','ori_ts','destination','des_ts']

#%% COST ESTIMATION
routes = pd.read_csv('routes.csv')
od_matrix['cost'] = 0.0
for _, row in od_matrix.iterrows():
    if _ % 100==0:
        print(_)
    default_duration = routes['duration'][(row['origin']==routes['origin']) & (row['destination']==routes['destination'])].values.tolist()[-1]/1000
    current_duration = abs(row['des_ts'] - row['ori_ts'])
    od_matrix.at[_,'cost'] = abs(default_duration - current_duration)/default_duration
    if (current_duration < 0.50*default_duration) | (current_duration > 1.50*default_duration):
        od_matrix.at[_,'cost'] = 1000;
    
    
n = od_matrix.shape[0]
od_matrix_ = od_matrix
od_matrix = od_matrix[od_matrix['cost'] != 1000]
n = od_matrix.shape[0]

#%%

# OPTIMIZATION PROBLEM A, b, c, upperb, lowerb

c = od_matrix['cost'].values   
b = np.abs(H[:,2])
A = np.zeros((m,n))

for i in range(m):
    station = H[i,0]
    timestamp = H[i,1]
    value = H[i,2]
    if H[i,2] > 0:
        activated = (od_matrix['origin'] == station) & (od_matrix['ori_ts'] == timestamp)
    else:
        activated = (od_matrix['destination'] == station) & (od_matrix['des_ts'] == timestamp)
    A[i,activated] = 1


A = np.int8(A)
b = np.int8(b)

ss = np.sum(A,axis=1)
#%% TO MATLAB
np.savetxt("c.csv", c, delimiter=",", fmt='%.2f', newline='\n', encoding=None)
np.savetxt("b.csv", b, delimiter=",", fmt='%d', newline='\n', encoding=None)
np.savetxt("A.csv", A, delimiter=",", fmt='%d', newline='\n', encoding=None)

#M.tofile('to_file.csv',sep=',',format='%d')
#pd.DataFrame(M).to_csv("pd_DF.csv")
                
#%% READ SOLUTION FROM MATLAB

x = pd.read_csv("x.csv")
new_b = pd.read_csv("ax.csv")

od_matrix.index = range(n)
od_matrix['k'] = x

solution = od_matrix[od_matrix['k']!=0]
solution.to_csv('solution.csv',index=False)


                
                
                