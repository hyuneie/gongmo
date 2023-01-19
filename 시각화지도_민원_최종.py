#!/usr/bin/env python
# coding: utf-8

# In[1]:


import folium
import pandas as pd
import json
import re
import os
from collections import defaultdict
from folium import plugins
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster
from folium import Marker
import branca.colormap as cm


# In[2]:


pd.set_option('float_format', '{:.2f}'.format)


# In[4]:


os.getcwd()


# In[5]:


dc = pd.read_csv('dead_car1.csv', encoding = 'CP949')
dc2 = pd.read_csv('dead_car2.csv', encoding = 'CP949')
dc3 = pd.read_csv('dead_car3.csv', encoding = 'CP949')
dc4 = pd.read_csv('dead_car4.csv', encoding = 'CP949')
dc5 = pd.read_csv('dead_car5.csv', encoding = 'CP949')
dc6 = pd.read_csv('dead_car6.csv', encoding = 'CP949')
dc7 = pd.read_csv('dead_car7.csv', encoding = 'CP949')
dc8 = pd.read_csv('dead_car8.csv', encoding = 'CP949')
dc9 = pd.read_csv('dead_car9.csv', encoding = 'CP949')
dc10 = pd.read_csv('dead_car10.csv', encoding = 'CP949')
dc11 = pd.read_csv('dead_car11.csv', encoding = 'CP949')
dc12 = pd.read_csv('dead_car12.csv', encoding = 'CP949')


# In[6]:


deadcarint = pd.concat([dc, dc2, dc3, dc4, dc5, dc6, dc7, dc8, dc9, dc10, dc11, dc12])


# In[15]:


deadcarint = pd.read_csv('deadcarint.csv', encoding = 'CP949')


# In[7]:


df = pd.read_excel('1.xlsx')
df2 = pd.read_excel('2.xlsx')
df3 = pd.read_excel('3.xlsx')
df4 = pd.read_excel('4.xlsx')
df5 = pd.read_excel('5.xlsx')
df6 = pd.read_excel('6.xlsx')
df7 = pd.read_excel('7.xlsx')
df8 = pd.read_excel('8.xlsx')
df9 = pd.read_excel('9.xlsx')
df10 = pd.read_excel('10.xlsx')
df11 = pd.read_excel('11.xlsx')
df12 = pd.read_excel('12.xlsx')


# In[8]:


complaints = pd.concat([df,df2, df3, df4, df5, df6, df7, df8, df9 ,df10, df11, df12])


# In[9]:


df2.head()


# In[12]:


df6.describe().round(0).astype(int)


# In[61]:


df['위도'].count()


# In[3]:


complaints.head()


# In[49]:


complaints.describe().round(0).astype(int)


# In[10]:


color_map = cm.LinearColormap(
    colors=['blue', 'green', 'yellow', 'orange', 'red'],
    vmin=0.4, vmax=0.85
).to_step(n=10)

steps=100
gradient_map=defaultdict(dict)
for i in range(steps):
    gradient_map[1/steps*i] = color_map.rgb_hex_str(1/steps*i)


# In[25]:


## 한국 주소 map 구현

seoul1 = folium.Map(location=[37.55, 126.98], 
                    zoom_start=12,
#                     min_zoom = 13,
                    maxZoom=13, 
                    zoom_control=True, 
                    scrollWheelZoom=True, 
                    dragging=True,
                    tiles=None,
                    )
folium.TileLayer(
#     'Stamen Toner',
                 name='전체 주정차민원&교통사고 데이터').add_to(seoul1)


## FeatureGroup 설정

fg_0 = folium.FeatureGroup(name='행정동별분류').add_to(seoul1)
fg_1 = folium.FeatureGroup(name='히트맵').add_to(seoul1)
fg_2 = folium.FeatureGroup(name='주소').add_to(seoul1)
fg_3 = folium.FeatureGroup(name='도로형태', show=False).add_to(seoul1)
fg_4 = folium.FeatureGroup(name='사고유형', show=False).add_to(seoul1)


## 한국 행정동 경계선 지정

with open('./geo1.geojson' , mode='rt', encoding='utf-8') as f:
   geo = json.loads(f.read())
   f.close()
  
folium.GeoJson(
    geo,
    name = 'korea_provinces',
    style_function = lambda x: {'fillColor':'#00000000' ,
    							'color':'black',
                                'weight' :'1'}
).add_to(fg_0)


## 히트맵 그리기

HeatMap(
    data=complaints[['위도', '경도']], 
    radius=11,
    gradient=gradient_map,
#     min_opacity=0.64,
#     min_val=0.64,
#     max_val=0.,
    blur=14,
).add_to(fg_1)


## 히트맵 설명칸 넣기

color_map.caption='전국 주정차위반 모의데이터'
# seoul1.add_child(color_map)
color_map.add_to(seoul1)


## marker 그리기

# for _, row in deadcarint.iterrows():
#     Marker(location = [row['위도'], row['경도']],
#            popup = folium.Popup(row['주소'], min_width=150, max_width=150),
#            icon=folium.Icon(color='red',icon='warning-sign'),
#            tooltip='상세주소',
#            ).add_to(fg_2)

for _, row in deadcarint.iterrows():
    Marker(location = [row['위도'], row['경도']],
           popup = folium.Popup(row['도로형태'], min_width=150, max_width=150),
           icon=folium.Icon(color='black',icon='road'),
           tooltip='도로형태',
           ).add_to(fg_3)

for _, row in deadcarint.iterrows():
    Marker(location = [row['위도'], row['경도']],
           popup = folium.Popup(row['사고유형'], min_width=150, max_width=150),
           icon=folium.Icon(color='cadetblue',icon='remove'),
           tooltip='사고유형',
           ).add_to(fg_4)
    
## 사고유형, circlemaker

# for _, row in deadcarint.iterrows():
#     folium.CircleMarker(location = [row['위도'], row['경도']],
#                   radius = 10,
#                   popup = folium.Popup(row['사고유형_대분류'], min_width=300, max_width=300),
# #                   color = color_select(row)
#                   ).add_to(fg_3)


## markercluster 그리기
    
mc = MarkerCluster(maxClusterRadius = 50, disableClusteringAtZoom=12, control=False)
for _, row in deadcarint.iterrows():
    mc.add_child(    
        Marker(location = [row['위도'], row['경도']],
               popup = folium.Popup(row['주소'], min_width=300, max_width=300),
               icon=folium.Icon(color='red',icon='warning-sign'),
               tooltip='상세주소')
               )

mc.add_to(fg_2)


## 미니맵 그리기

minimap = plugins.MiniMap(toggle_display = True,
                          zoom_animation=True,
#                           tile_layer='Stamen Toner',
                          width=150, height=150,
                          )
seoul1.add_child(minimap)


## FeatureGroup LayerControl

folium.LayerControl(collapsed=True).add_to(seoul1)



seoul1


# In[29]:


from IPython.core.display import display, HTML
display(HTML("<style>.container { width:80% !important; }</style>"))

