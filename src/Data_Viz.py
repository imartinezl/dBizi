# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 18:31:52 2018

@author: Inigo
"""

#%% VISUALIZATION FOR WEBPAGE
import holoviews as hv
hv.extension('bokeh')

import numpy as np
import pandas as pd

od_matrix = pd.read_csv('od_matrix.csv', header=None).astype('int')
od_matrix.columns = ['origin','ori_ts','destination','des_ts','cost']
od_matrix = od_matrix.assign(ordered = od_matrix.ori_ts < od_matrix.des_ts)
od_matrix = od_matrix.assign(source = od_matrix.origin if od_matrix.ordered is True else od_matrix.destination,
                 target = od_matrix.destination if od_matrix.ordered is True else od_matrix.origin)

links = od_matrix.groupby(['source','target']).size().reset_index(name='value')


station_features = pd.read_csv('stations_location.csv')
nodes = hv.Dataset(station_features, 'numero_estacion')

graph = hv.Chord((links, nodes), ['source','target'], ['value']).select(value=(60, None))

%opts Chord [label_index='nombre' color_index='nombre' edge_color_index='source' width=800 height=800]
%opts Chord (cmap='Category20' edge_cmap='Category20')

# Using renderer save
renderer = hv.renderer('bokeh')
renderer.save(graph, 'graph')

## Convert to bokeh figure then save using bokeh
#plot = renderer.get_plot(curve).state
#
#from bokeh.io import output_file, save, show
#save(plot, 'graph.html')
## OR
#output_file("graph.html")
#show(plot)


    