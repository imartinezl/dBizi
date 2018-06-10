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

import pyroutelib3
from pyroutelib3 import Router # Import the route
import pandas as pd
import numpy as np
#%%
#router = Router("cycle") # Initialise it
router = Router("car", "map")

#%%
stations_features = pd.read_csv('stations_location.csv')

routes = []
for i in range(stations_features.shape[0]):
    print(i)
    for j in range(stations_features.shape[0]):
        if i != j:
            start = router.data.findNode(stations_features['latitud'].iloc[i],stations_features['longitud'].iloc[i])      
            end = router.data.findNode(stations_features['latitud'].iloc[j],stations_features['longitud'].iloc[j])      
            status, route = router.doRoute(start, end) 
            if status == 'success':
                routeLatLons = list(map(router.nodeLatLon, route))
                routeLatLons = [list(reversed(x)) for x in routeLatLons]
                routes.append([stations_features['numero_estacion'].iloc[i],
                               stations_features['numero_estacion'].iloc[j],
                               routeLatLons])
routes = pd.DataFrame(routes, columns=['origin','destination','route'])
#%%
solution = pd.read_csv('solution.csv')

features = []
for i in range(solution.shape[0]):
    print(i)
    origin = int(solution['origin'].iloc[i])
    destination = int(solution['destination'].iloc[i])
    ori_ts = solution['ori_ts'].iloc[i]
    des_ts = solution['des_ts'].iloc[i]
    
    route_coordinates = routes[(routes['origin'] == origin) & (routes['destination'] == destination)]['route'].iloc[0]
    route_times = np.round(np.linspace(ori_ts*1000, des_ts*1000,len(route_coordinates))).tolist()
    features.append({
                    'type': 'Feature',
                    'geometry': {
                            'type': 'LineString',
                            'coordinates': route_coordinates,
                            },
                    'properties': {
                            'style':{'color':'#100000', 'weight':1, 'opacity':0},
                            'times': route_times
                            }
                })
features