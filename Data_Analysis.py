# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 10:44:38 2018

@author: Inigo
"""
#%%
import json
import requests
import pandas as pd
import numpy as np
import time
import psycopg2

#%%

conn_string = "host='localhost' dbname='dBici' user='postgres' password='root'"

def get_data(conn_string):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stations_data")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

#%%
    
data = get_data(conn_string)

df = pd.DataFrame()
for i in range(len(data)):
    unixtime = data[i][1]
    df_temp = pd.read_json(json.dumps(data[i][2]))
    df_temp['unixtime'] = unixtime
    df = pd.concat([df,df_temp])
    
#%%
    
df['nombre'].value_counts()
