# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 10:13:52 2018

@author: Inigo
"""
#%%
import json
import requests
import pandas as pd
import numpy as np
import time
import psycopg2

conn_string = "host='localhost' dbname='dBici' user='postgres' password='root'"

def get_data(conn_string):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stations_data")
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return records

def insert_json(conn_string,now,json_data):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    #for i in range(len(json_data)):
     #   query = "INSERT INTO stations_data (unixtime, station_number, json_data) VALUES ({},{},'{}')".format(now,json_data[i]['numero_estacion'],json.dumps(json_data[i]))
      #  cursor.execute(query)
    query = "INSERT INTO stations_data (unixtime, json_data) VALUES ({},'{}')".format(now,json.dumps(json_data))
    cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()
    
link_ = "http://www.donostia.eus/info/ciudadano/Videowall.nsf/estaciones.xsp"

last_state = None
while True:
    response = requests.get(link_)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        now = int(time.time()) 
        if last_state != json_data:
            insert_json(conn_string,now,json_data)
            print("New entry at ",now)
        last_state = json_data
    time.sleep(10)