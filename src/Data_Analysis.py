# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 10:44:38 2018

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
from_server = False

df = pd.DataFrame()

if from_server:
    data = get_data(conn_string)
    for i in range(0,len(data)):
        unixtime = data[i][1]
        df_temp = pd.read_json(json.dumps(data[i][2]))
        df_temp['unixtime'] = unixtime
        df = pd.concat([df,df_temp])
else:
    import csv
    reader = csv.reader(open('pg_database.csv'), delimiter='|',quotechar='"')
    i = 0; 
    for row in reader:
        if i==0:
            header = row
        else:
            comma_1 = row[-1].find(',')
            comma_2 = row[-1][(comma_1+1):].find(',')
            unixtime = row[-1][comma_1+1:comma_1+comma_2]
            json_ = row[-1][(comma_1+comma_2+2):]

            df_temp = pd.read_json(json_.replace('"','').replace('\'','"'))
            df_temp['unixtime'] = unixtime
            df = pd.concat([df,df_temp])
        i += 1
        

    
df['date'] = pd.to_datetime(df['unixtime'], unit='s').dt.tz_localize('UTC').dt.tz_convert('Europe/Madrid')
df['day'] = [x.day for x in df['date']]
df['hour'] = [x.hour for x in df['date']]

df['bases_eng_lib'] = df['bases_enganchadas'] + df['bases_libres']
df['bases_bloq'] = df['numero_bases'] - df['bases_eng_lib']
df['bases_enganchadas_sht'] = df.groupby(['nombre'])['bases_enganchadas'].transform(lambda x:(x - x.shift(1)))
df['bases_libres_sht'] = df.groupby(['nombre'])['bases_libres'].transform(lambda x:(x - x.shift(1)))
df['bases_bloq_sht'] = df.groupby(['nombre'])['bases_bloq'].transform(lambda x:(x - x.shift(1)))
df['to_road'] = df.groupby(['nombre'])['bases_enganchadas'].transform(lambda x:-(x - x.shift(1)))
df['to_road'] = df.groupby(['nombre'])['bases_libres'].transform(lambda x:(x - x.shift(1)))

df.index = range(df.shape[0])
#%% FIRST PLOT
def plt_evolution(x,y, ax):
    ax.plot(x,y)
    xaxis_fmt(ax)
    
def xaxis_fmt(ax):
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M', tz=tz.gettz('Europe/Madrid')))
    
circulacion = df.groupby('date')['bases_libres'].apply(sum)

fig, ax = plt.subplots()
x = circulacion.index; y = circulacion.values
plt_evolution(x,y, ax)
ax.set_ylim(bottom=0)

#%% STATIONS INFORMATION

station_cols = ['numero_estacion', 'nombre','latitud','longitud']
station_features = pd.DataFrame(list(df.groupby(station_cols).groups.keys()), columns = station_cols)
#station_features.to_csv('stations_location.csv',index=False)

#%% PLOT ALL STATIONS

station_ocu = ['activada', 'bases_enganchadas', 'bases_libres','no_operativa','numero_bases']
df_melt = pd.melt( df, ['date','unixtime','numero_estacion'], station_ocu, 'key', 'value' )

a = df.pivot(index='unixtime',columns='numero_estacion',values='bases_libres')
a.apply(sum,axis=1)
#pd.plotting.scatter_matrix(a)

%matplotlib inline
fig, ax = plt.subplots(1,1,figsize=(12,6))
for i in range(station_features.shape[0]):
    station_id = station_features['numero_estacion'].iloc[i]
    station_name = station_features['nombre'].iloc[i]
    
    case = df[df['numero_estacion']==station_id]
    case['bases_libres'] + case['bases_enganchadas']
    
    plt.plot(case['date'],1-(case['bases_libres']/case['numero_bases']), marker='.', linewidth=1, label=station_name)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M', tz=tz.gettz('Europe/Madrid')))
    plt.xticks(rotation=90)
    plt.legend()

#%% EXPLORE & UNDERSTAND

data = df.loc[2552:6351]
data['to_road'].sum()
estacion = 'Pio XII'
data_station = data[data['nombre']==estacion]
plt.plot(data_station['date'],data_station['bases_enganchadas'])
plt.xticks(rotation=90)
data_station['bases_enganchadas_sht'] = data_station['bases_enganchadas'] - data_station['bases_enganchadas'].shift(1)
data_station['bases_libres_sht'] = data_station['bases_libres'] - data_station['bases_libres'].shift(1)
data_station['bases_bloq_sht'] = data_station['bases_bloq'] - data_station['bases_bloq'].shift(1)
data_station['to_road'] = -data_station['bases_enganchadas_sht']

#%%
# GET SUBSET
df.groupby('day').apply(sum)
df_subset = df[(df['day']==15) & (df['hour']>6)] #5

#per_ts = df_subset.groupby('date')['to_road'].apply(sum)
#found = 0
#amp = 0
#for i in range(1,per_ts.shape[0]):
#    s = np.zeros(per_ts.shape[0])
#    for j in range(i+1, per_ts.shape[0]):
#        s[j] = s[j-1] + per_ts.iloc[j]
#        if (s[j]==0) & ((j-i) > amp):
#            start=i
#            end=j
#            found=1
#            amp = j-i
#            break
#    if found:
#        break
    

per_ts = df_subset.groupby('date')['to_road'].apply(sum)
per_ts_start = df_subset.groupby('date')['to_road'].apply(lambda x: any(x<0))
per_ts_end = df_subset.groupby('date')['to_road'].apply(lambda x: any(x>0))
s = np.zeros(per_ts.shape[0])
ts_start = 0
#df_subset[(df_subset['date']==df_subset['date'].iloc[0]) & (df_subset['to_road']<0)] = 0
ts_end = 0
for i in range(ts_start+1, per_ts.shape[0]):
    s[i] = s[i-1] + per_ts.iloc[i-1]
    if s[i]==0:
        ts_end=i
#        break
    
plt.plot(per_ts, label='per_ts')
plt.plot(per_ts.index, s, label='accumulate')
plt.axhline(y=0, color='red')
plt.xticks(rotation=90)
plt.legend()

df_study = df_subset[(df_subset['date'] >= per_ts.index[ts_start]) & (df_subset['date'] < per_ts.index[ts_end])]
should_be_zero = df_study.groupby('date')['to_road'].apply(sum).sum()
per_ts_start = df_study.groupby('date')['to_road'].apply(lambda x: any(x<0))
per_ts_end = df_study.groupby('date')['to_road'].apply(lambda x: any(x>0))


#%%
per_ts = df_subset.groupby('date')['to_road'].apply(sum)
ts_start = 0
ts_end = 0
s = np.zeros(per_ts.shape[0])
for i in range(ts_start+1, per_ts.shape[0]):
    s[i] = s[i-1] + per_ts.iloc[i-1]
    if s[i] < 0:
        ts_end=i
        #break
    
df_study = df_subset[(df_subset['date'] >= per_ts.index[ts_start]) & (df_subset['date'] < per_ts.index[ts_end])]
condition_start = df_study.groupby('date')['to_road'].apply(lambda x: any(x<0)) #should be false at start
condition_end = df_study.groupby('date')['to_road'].apply(lambda x: any(x>0)) #should be false at end
    
#%% HACKING OF CONDITIONS
df_study['to_road'].loc[[4672,4681,4685]] = 0
df_study['to_road'].loc[4677] = -5
#%%

H = df_study[['numero_estacion','unixtime','to_road']].values
H = H[np.abs(H[:,2])!=0.0]
m = H.shape[0]

od_matrix = list()         
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
od_matrix['cost'] = 1
n = od_matrix.shape[0]
#%%

# NECESITO A, b, c, upperb, lowerb

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
#%%
#import scipy.io
#scipy.io.savemat('test.mat', dict(A=A, b=b, c=c))

np.savetxt("c.csv", c, delimiter=",", fmt='%.2f', newline='\n', encoding=None)
np.savetxt("b.csv", b, delimiter=",", fmt='%d', newline='\n', encoding=None)
np.savetxt("A.csv", A, delimiter=",", fmt='%d', newline='\n', encoding=None)

#M.tofile('to_file.csv',sep=',',format='%d')
#pd.DataFrame(M).to_csv("pd_DF.csv")
                
#%%

x = pd.read_csv("x.csv")
new_b = pd.read_csv("ax.csv")

od_matrix['k'] = x

solution = od_matrix[od_matrix['k']!=0]
solution.to_csv('solution.csv',index=False)


                
                
                