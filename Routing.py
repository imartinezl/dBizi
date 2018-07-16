# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 13:13:45 2018

@author: Inigo
"""

# =============================================================================
# OpenStreetMap Routing Machine
# =============================================================================
#%%
import sys
egg_path='C:/Program Files/Python36/Lib/site-packages/pyroutelib3-0.8-py3.6.egg'
sys.path.append(egg_path)
egg_path='C:/Program Files/Python36/Lib/site-packages/osmapi-1.1.0-py3.6.egg'
sys.path.append(egg_path)

#%%
import pyroutelib3
from pyroutelib3 import Router # Import the route
import pandas as pd
import numpy as np
#%%
router_cycle = Router("cycle")
router_car = Router("car")
router_cycle = Router(transport="cycle", localfile="map")
router_car = Router(transport="car", localfile="map")

#%%
stations_features = pd.read_csv('stations_location.csv')

routes = []
for i in range(stations_features.shape[0]):
    for j in range(stations_features.shape[0]):
        if i != j:
            start = router_cycle.data.findNode(stations_features['latitud'].iloc[i],stations_features['longitud'].iloc[i])      
            end = router_cycle.data.findNode(stations_features['latitud'].iloc[j],stations_features['longitud'].iloc[j])      
            status, route = router_cycle.doRoute(start, end) 
            print(i,'_',j, '_cycle_', status)

            if status == 'success':
                routeLatLons = list(map(router_cycle.nodeLatLon, route))
                routeLatLons = [list(reversed(x)) for x in routeLatLons]
                routes.append([stations_features['numero_estacion'].iloc[i],
                               stations_features['numero_estacion'].iloc[j],
                               routeLatLons])
            else:
                start = router_car.data.findNode(stations_features['latitud'].iloc[i],stations_features['longitud'].iloc[i])      
                end = router_car.data.findNode(stations_features['latitud'].iloc[j],stations_features['longitud'].iloc[j])      
                status, route = router_car.doRoute(start, end) 
                print(i,'_',j, '_car_', status)
    
                if status == 'success':
                    routeLatLons = list(map(router_car.nodeLatLon, route))
                    routeLatLons = [list(reversed(x)) for x in routeLatLons]
                    routes.append([stations_features['numero_estacion'].iloc[i],
                                   stations_features['numero_estacion'].iloc[j],
                                   routeLatLons])
                
    
routes = pd.DataFrame(routes, columns=['origin','destination','route'])
routes.to_csv('routes.csv', index=False)
#%%

stations_features = pd.read_csv('stations_location.csv')

import requests
from key import key_gh
urltemplate = 'https://graphhopper.com/api/1/route?point={latA},{lonA}&point={latB},{lonB}&vehicle={vehicle}&locale={locale}&key={key}&type=json&points_encoded={points}'

routes = []
for i in range(stations_features.shape[0]):
    for j in range(stations_features.shape[0]):
        if i != j:
            latA_,lonA_ = stations_features['latitud'].iloc[i], stations_features['longitud'].iloc[i]
            latB_,lonB_ = stations_features['latitud'].iloc[j], stations_features['longitud'].iloc[j]

            url = urltemplate.format(latA=latA_, lonA=lonA_, latB=latB_, lonB=lonB_, vehicle='bike', locale='es', key=key_gh,points='false')
            response = requests.get(url)
            
            if response.status_code == 200:
                print(i,'_',j,'success')
                content_type = response.headers['content-type']
                if 'json' in content_type:
                    data = response.json()
                    routeLatLons = data['paths'][0]['points']['coordinates']
                    routeTime = data['paths'][0]['time']
                    routeDist = data['paths'][0]['distance']
                    routes.append([stations_features['numero_estacion'].iloc[i],
                                   stations_features['numero_estacion'].iloc[j],
                                   routeLatLons, routeTime, routeDist])
                
#%%
routes = pd.DataFrame(routes, columns=['origin','destination','route','duration','distance'])
routes.to_csv('routes.csv', index=False)
    
    

