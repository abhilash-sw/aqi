# -*- coding: utf-8 -*-
# @Author: abhilash
# @Date:   2018-11-10 11:25:44
# @Last Modified by:   abhilash
# @Last Modified time: 2018-11-10 21:02:06

import numpy as np
import pandas as pd
import os
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from scipy import interpolate
from shapely.geometry import Polygon
from shapely.geometry import Point

def read_data(data_dir):#data_dir='data'
	#data_dir = 'data'

	dates = ['20181104','20181105','20181106','20181107','20181108','20181109','20181110']

	times = np.arange(24)

	all_data = {}

	for dt in dates:
		for tm in times:
			filename = data_dir+'/'+dt+'/download?filename=AQI_all_station'+dt[:4]+'_'+dt[4:6]+'_'+dt[6:]+'T'+str(tm)+'_00_00Z.xlsx'
			if os.path.getsize(filename) == 0:
				continue
			aqis = np.zeros(36)
			#aqis[:] = np.nan
			df =  pd.read_excel(filename,header=3)
			for i in range(8,44):
				try:
					aqis[i-8] = int(df['Current AQI value'][i])
				except:
					aqis[i-8] = np.nan
			all_data[dt+'_'+str(tm)] = aqis
	return all_data

def read_delhi_stations(delhi_station_file):#delhi_station_file='delhi_stations.txt'
	fid = open(delhi_station_file,'r')
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
	
	return lats,lons

def get_delhi_in_lons_lats(delhi_polygon):
	ag_lats = np.linspace(28.37,28.92,200)
	ag_lons = np.linspace(76.8,77.4,200)
	g_lats,g_lons = np.meshgrid(ag_lats,ag_lons)

	g_lats = g_lats.reshape(200**2)
	g_lons = g_lons.reshape(200**2)
	flgs = np.zeros(len(g_lats),dtype=bool)

	for i in range(len(g_lats)):
		if delhi_poly.contains(Point(g_lons[i],g_lats[i])):
			flgs[i] = True

	g_lats_in = g_lats[flgs]
	g_lons_in = g_lons[flgs]
	return g_lons_in,g_lats_in



# def interpo(fnn,aqis,g_lons_in,g_lats_in):
# 	g_aqis_in = fnn(g_lons_in,g_lats_in)
# 	return g_aqis_in

def save_map(g_lons_in,g_lats_in,g_aqis_in,tm): #tm = 20181103_0
	fig,ax = plt.subplots()
	map = Basemap(llcrnrlat=28.37,llcrnrlon=76.8,urcrnrlat=28.92,urcrnrlon=77.4,lon_0=77.14,lat_0=28.64,resolution='i')#, projection='merc')
	map.readshapefile('shapefiles/Archive/wards delimited','delhi')
	ax.plot(lons,lats,'ko',markersize=4,label='AQI Stations')#,zorder=5)
	ax.legend(loc=3)

	if tm[:8] == '20181104':
		dday = '1 Day before Diwali'
	elif tm[:8] == '20181105':
		dday = '1st Day of Diwali'
	elif tm[:8] == '20181106':
		dday = '2nd Day of Diwali'
	elif tm[:8] == '20181107':
		dday = '3rd Day of Diwali'
	elif tm[:8] == '20181108':
		dday = '4th Day of Diwali'
	elif tm[:8] == '20181109':
		dday = '5th Day of Diwali'
	elif tm[:8] == '20181110':
		dday = '1 Day after Diwali'

	tm_tmp = tm[6:8]+'-'+tm[4:6]+'-'+tm[:4]+' '+str(int(tm.split('_')[-1])).zfill(2)+'00  '+dday
	ax.annotate(tm_tmp,xy=(0.05,1.005),xycoords='axes fraction',fontweight='bold',fontsize=13)
	hx = map.hexbin(g_lons_in,g_lats_in,C=g_aqis_in,cmap='jet',vmin=100,vmax=500)
	ax.set_title('Delhi Air Quality Index\n',fontweight='bold',fontsize=18)
	ax.annotate('AQI 1-50:Good    51-100:Satisfactory    101-200:Moderate    201-300:Poor\n                       301-400:Very Poor    401-500:Severe',xy=(-0.12,-0.1),xycoords='axes fraction')
	map.colorbar(hx)
	fig.savefig('plots/'+tm+'.png',dpi=300,bbox_inches='tight')


if __name__ == '__main__':
	all_data = read_data('data')
	lats,lons = read_delhi_stations('delhi_stations.txt')
	
	map = Basemap(llcrnrlat=28.37,llcrnrlon=76.8,urcrnrlat=28.92,urcrnrlon=77.4,lon_0=77.14,lat_0=28.64,resolution='i')
	map.readshapefile('shapefiles/india/gadm36_IND_shp/gadm36_IND_3','ind3',drawbounds=False)
	delhi_poly = Polygon(map.ind3[2006])

	g_lons_in,g_lats_in = get_delhi_in_lons_lats(delhi_poly)

	for k in all_data.keys():
		print(k)
		nan_flg = ~np.isnan(all_data[k])
		nan_lats = lats[nan_flg]
		nan_lons = lons[nan_flg]
		nan_aqis = all_data[k][nan_flg]
		if sum(nan_flg) == 0:
			continue

		#fnn = interpolate.NearestNDInterpolator(np.vstack((lons,lats)).T,all_data[k])
		fnn = interpolate.NearestNDInterpolator(np.vstack((nan_lons,nan_lats)).T,nan_aqis)
		g_aqis_in = fnn(g_lons_in,g_lats_in)
		save_map(g_lons_in,g_lats_in,g_aqis_in,k)
		close('all')

