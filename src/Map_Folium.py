# -*- coding: utf-8 -*-
"""
Created on Sun Jun  3 17:17:07 2018

@author: Inigo
"""
#%%

import geojson 
import json
import pandas as pd
import numpy as np
aparcabicis = geojson.load(open("C:/Users/Inigo/Desktop/dBici/20069_aparcabicis.geojson"))
bidegorri = geojson.load(open("C:/Users/Inigo/Desktop/dBici/20069_bidegorri.geojson"))
stations_features = pd.read_csv("C:/Users/Inigo/Desktop/dBici/stations_location.csv")

#%%

from math import sin, cos, sqrt, atan2, radians

def mercator_distance(latA,lonA,latB,lonB):
    R = 6373.0 * 1000   # approximate radius of earth in m
    lat1, lon1 = radians(latA), radians(lonA)
    lat2, lon2 = radians(latB), radians(lonB)
    dlon = lon2 - lon1
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a)) 
    distance = R * c
    return distance #in m
def mercator_dist(a,b):
    return mercator_distance(a[0],a[1],b[0],b[1])

    
#%%

solution = pd.read_csv('solution.csv')
solution['k'][np.isnan(solution['k'])]=1
routes = pd.read_csv('routes.csv')

features = []; cont = 0;
for i in range(solution.shape[0]):
    print(i)
    origin = int(solution['origin'].iloc[i])
    destination = int(solution['destination'].iloc[i])
    ori_ts = solution['ori_ts'].iloc[i]
    des_ts = solution['des_ts'].iloc[i]
    t_initial = ori_ts
    
    route = routes[(routes['origin'] == origin) & (routes['destination'] == destination)].iloc[0]
    route_coordinates = json.loads(route['route'])
#    route_times = np.round(np.linspace(ori_ts*1000, des_ts*1000,len(route_coordinates))).tolist()

    total_d = sum(mercator_dist(route_coordinates[k],route_coordinates[k+1]) for k in range(len(route_coordinates)-1))
    speed_ratio = total_d/abs(des_ts-ori_ts)
    
    d_basic = 35
    route_coordinates_new, route_times_new = [],[]
    for k in range(len(route_coordinates)-1):
        d_ = mercator_dist(route_coordinates[k],route_coordinates[k+1])
        npoints = int(np.floor(d_/d_basic))
    
        lons = np.round(np.linspace(route_coordinates[k][0],route_coordinates[k+1][0],2+npoints),6)
        lats = np.round(np.linspace(route_coordinates[k][1],route_coordinates[k+1][1],2+npoints),6)
        
        [route_coordinates_new.append([lons[m],lats[m]]) for m in range(2+npoints)  if [lons[m],lats[m]] not in route_coordinates_new]
        
        t_final = np.round(t_initial + (d_/speed_ratio))
        route_times = np.round(np.linspace(t_initial*1000, t_final*1000, 2+npoints)).tolist()
        [route_times_new.append(m) for m in route_times if m not in route_times_new]
        t_initial = t_final
    for _ in range(int(solution['k'].iloc[i])):
        features.append({
                        'type': 'Feature',
                        'geometry': {
                                'type': 'LineString',
                                'coordinates': route_coordinates_new,
                                },
                        'properties': {
                                'style':{'color':'#100000', 'weight':1, 'opacity':0},
                                'times': (np.array(route_times_new) + 60*_).tolist()
                                }
                    })
    if len(features)>100:
        json.dump(features,open('features_'+str(cont)+'.json', 'w'))
        cont = cont + 1
        features = []

json.dump(features,open('features_'+str(cont)+'.json', 'w'))

#%%

v_lat = np.linspace(43.292,43.330,40)
v_lon = np.linspace(-2.021,-1.947,40)

#%%
from folium import plugins
import folium
m = folium.Map(
    location=[43.312134, -1.981296],
    zoom_start=14,
    tiles='CartoDB positron'
)

folium.plugins.TimestampedGeoJson(data={
    'type': 'FeatureCollection',
    'features': features[0:2]
    }, loop=True, add_last_point=True, period='PT5S', duration='PT5M'
).add_to(m)

#ESTACIONES
for i in range(stations_features.shape[0]):
    point = stations_features.iloc[i]
    folium.CircleMarker(
            location=[point['latitud'], point['longitud']], 
            popup=point['nombre'],
            radius=5, 
            color = '#1f81dd', fill_color='#6e44ff',fill_opacity=0.7, fill=True,
            icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
    
#APARCABICIS
#for i in range(len(aparcabicis['features'])):
for i in range(0):
    point = aparcabicis['features'][i]['geometry']['coordinates']
    folium.CircleMarker(
            location=[point[1], point[0]], 
            popup='Alo',
            radius=3, 
            color = '#cccccc', fill_color='#cccccc',fill_opacity=0.7, fill=True,
            icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
#    folium.Marker(
#            location=[point[1], point[0]], 
#            popup='Alo',            
#            icon=folium.Icon(color='red', icon='info-sign')
#            ).add_to(m)
#    folium.Marker(
#            location=[47.3489, -124.708],
#            popup=folium.Popup(max_width=450).add_child(
#                    folium.Vega(json.load(open(vis1)), width=450, height=250))
#            ).add_to(m)


def style_function(feature):
    return {
        'color': '#1f81dd',
        'weight': 1,
    }

#folium.GeoJson(
#    'bidegorri.json',
#    name='bidegorri',
#    style_function= style_function
#).add_to(m)

m.save('index.html')
