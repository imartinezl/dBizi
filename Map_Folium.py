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
estaciones = pd.read_csv("C:/Users/Inigo/Desktop/dBici/stations_location.csv")

#%%

#from folium import plugins
#import sys
#egg_path='C:/Program Files/Python36/Lib/site-packages/folium-0+unknown-py3.6.egg'
#sys.path.append(egg_path)
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
    'features': features
    }, loop=True, add_last_point=True, period='PT5S', duration='PT30S'
).add_to(m)

#ESTACIONES
for i in range(estaciones.shape[0]):
    point = estaciones.iloc[i]
    folium.CircleMarker(
            location=[point['latitud'], point['longitud']], 
            popup=point['nombre'],
            radius=5, 
            color = '#1f81dd', fill_color='#6e44ff',fill_opacity=0.7, fill=True,
            icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
    
#APARCABICIS
#for i in range(len(aparcabicis['features'])):
for i in range(20):
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

folium.GeoJson(
    bidegorri,
    name='bidegorri',
    style_function= style_function
).add_to(m)



    


m.save('index.html')
