# -*- coding: utf-8 -*-
# @Author: abhilash
# @Date:   2018-11-08 09:10:59
# @Last Modified by:   abhilash
# @Last Modified time: 2018-11-10 19:10:53

from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import interpolate


fid = open('delhi_stations.txt','r')
lines = fid.readlines()
fid.close()

lats = []
lons = []

for l in lines:
	ll = l.split('\t')
	lats.append(float(ll[1]))
	lons.append(float(ll[2][:-1]))
lats = np.array(lats)
lons = np.array(lons)
#############
ff = 'data/20181107/download?filename=AQI_all_station2018_11_07T20_00_00Z.xlsx'
df = pd.read_excel(ff,header=3)

aqis = np.zeros(36)
#aqis[:] = np.nan

for i in range(8,44):
	try:
		aqis[i-8] = int(df['Current AQI value'][i])
	except:
		aqis[i-8] = np.nan

# f = interpolate.interp2d(lons,lats,aqis)#,kind='cubic')
fnn = interpolate.NearestNDInterpolator(np.vstack((lons,lats)).T,aqis)

ag_lats = np.linspace(28.37,28.92,200)
ag_lons = np.linspace(76.8,77.4,200)
g_lats,g_lons = np.meshgrid(ag_lats,ag_lons)

g_lats = g_lats.reshape(200**2)
g_lons = g_lons.reshape(200**2)


#############
# a = []
# b = []
# for mm in map.delhi:
#     for lsd in mm:
#         a.append(lsd[0])
#         b.append(lsd[1])
# a = np.array(a)
# b = np.array(b)

# m = Basemap(llcrnrlat=28.37,llcrnrlon=76.8,urcrnrlat=28.92,urcrnrlon=77.4,lon_0=77.14,lat_0=28.64,resolution='i')#, projection='merc')
# m.plot(a,b)

############
map = Basemap(llcrnrlat=28.37,llcrnrlon=76.8,urcrnrlat=28.92,urcrnrlon=77.4,lon_0=77.14,lat_0=28.64,resolution='i')#, projection='merc')
#map.drawmapboundary()#(fill_color='aqua')
#map.fillcontinents()#(color='#ddaa66',lake_color='aqua')
#map.drawcoastlines()

map.readshapefile('shapefiles/Archive/wards delimited','delhi')

#map.plot(lons,lats,'ro',markersize=6)#,zorder=5)
#########################
# from matplotlib.patches import Polygon
# from matplotlib.collections import PatchCollection
# from matplotlib.patches import PathPatch

# patches   = []

# for shape in map.delhi:
#     patches.append( Polygon(np.array(shape), True) )


#########
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.ops import cascaded_union

map = Basemap(llcrnrlat=28.37,llcrnrlon=76.8,urcrnrlat=28.92,urcrnrlon=77.4,lon_0=77.14,lat_0=28.64,resolution='i')#, projection='merc')
map.readshapefile('shapefiles/Archive/wards delimited','delhi')

###########
patches   = []

for shape in map.delhi:
    patches.append( Polygon(shape) )

tp = cascaded_union(patches[:159]+patches[160:])

####################
map.readshapefile('shapefiles/india/gadm36_IND_shp/gadm36_IND_3','ind3',drawbounds=False)
delhi_poly = Polygon(map.ind3[2006])

####################


flgs = np.zeros(len(g_lats),dtype=bool)

for i in range(len(g_lats)):
	if delhi_poly.contains(Point(g_lons[i],g_lats[i])):
		flgs[i] = True

g_lats_in = g_lats[flgs]
g_lons_in = g_lons[flgs]

g_aqis_in = fnn(g_lons_in,g_lats_in)
#tp.contains(Point(77,28.73))
map.hexbin(g_lons_in,g_lats_in,C=g_aqis_in,linewidths=4)
map.plot(lons,lats,'ko',markersize=4,label='AQI Stations')#,zorder=5)


##########
fig,ax = plt.subplots()
map = Basemap(llcrnrlat=28.37,llcrnrlon=76.8,urcrnrlat=28.92,urcrnrlon=77.4,lon_0=77.14,lat_0=28.64,resolution='i')#, projection='merc')
map.readshapefile('shapefiles/Archive/wards delimited','delhi')
ax.plot(lons,lats,'ko',markersize=4,label='AQI Stations')#,zorder=5)
ax.legend()
hx = map.hexbin(g_lons_in,g_lats_in,C=g_aqis_in)
ax.set_title('Delhi Air Quality Index',fontweight='bold',fontsize=20)
ax.annotate('AQI 1-50:Good    51-100:Satisfactory    101-200:Moderate    201-300:Poor\n               301-400:Very Poor    401-500:Severe',xy=(-0.12,-0.1),xycoords='axes fraction')
map.colorbar(hx)
fig.savefig('test_3.png',dpi=300,bbox_inches='tight')