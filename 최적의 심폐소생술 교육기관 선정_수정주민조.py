#!/usr/bin/env python
# coding: utf-8

# In[1]:


import folium
import pandas as pd
import json
import re
import webbrowser
import requests
import os
from collections import defaultdict
from folium import plugins
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
from folium import Marker
import branca.colormap as cm
from branca.colormap import linear


# In[2]:


from IPython.core.display import display, HTML
display(HTML("<style>.container { width:85% !important; }</style>"))


# In[3]:


os.getcwd()


# In[4]:


with open('./boundary.json' , mode='rt', encoding='utf-8') as f:
   geo = json.loads(f.read())
   f.close()
    

administrative = pd.read_csv('population.csv', encoding = 'euc-kr')
administrative.columns = ['code', 'population']
administrative['code'] = administrative.code.map(lambda x : str(x).zfill(5))
administrative.head(1)


# In[5]:


publicsport = pd.read_csv('전국공공체육시설.csv', encoding = 'utf-8')


# In[6]:


selectsport = pd.read_excel('선정공공체육시설.xlsx')


# In[7]:


colormap = linear.Spectral_09.scale(
  administrative.population.min(),
  administrative.population.max()
)

def reversed_colormap(existing):
    return cm.LinearColormap(
        colors=list(reversed(existing.colors)),
        vmin=existing.vmin, vmax=existing.vmax
    )
reverse = reversed_colormap(colormap)

reverse


# In[8]:


population_dict = administrative.set_index('code')['population']
color_dict = {str(key): reverse(population_dict[key]) for key in population_dict.keys()}
color_dict


# In[9]:


m = folium.Map(
    location=[37.528043, 126.980238],
    zoom_start=11,
#     tiles='Stamen Toner'
)

fg_0 = folium.FeatureGroup(name='인구수히트맵').add_to(m)
fg_1 = folium.FeatureGroup(name='전체공공체육시설', show=False).add_to(m)
fg_2 = folium.FeatureGroup(name='선정공공체육시설').add_to(m)

folium.GeoJson(
    geo,
    name='인구수',
    style_function=lambda feature: {
        'fillColor': color_dict[feature['properties']['SIG_CD']],
        'color': 'black',
        'weight': 1,
        'dashArray': '5, 5',
        'fillOpacity': 0.8,
    }
).add_to(fg_0)

reverse.caption='Population choropleth map'
reverse.add_to(m)

for _, row in publicsport.iterrows():
    folium.CircleMarker(location = [row['위도'], row['경도']],
                        radius = 2,
                        popup = folium.Popup(row['시설명'], min_width=300, max_width=300),
                        fill_color='black',
                        fill=True,
                        color= 'green', 
                        ).add_to(fg_1)
    
for _, row in selectsport.iterrows():
    Marker(location = [row['위도'], row['경도']],
           popup = folium.Popup(row['시설명'], min_width=300, max_width=300),
           icon=folium.Icon(color='black',icon='heart', prefix='fa'),
           tooltip='시설명',
           ).add_to(fg_2)
    
    

minimap = plugins.MiniMap(toggle_display = True,
                          zoom_animation=True,
                          width=150, height=150,
                          )
m.add_child(minimap)


folium.LayerControl(collapsed=True).add_to(m)

m

