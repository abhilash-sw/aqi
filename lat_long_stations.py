# -*- coding: utf-8 -*-
# @Author: abhilash
# @Date:   2018-11-08 12:52:33
# @Last Modified by:   abhilash
# @Last Modified time: 2018-11-08 13:06:04
from geopy.geocoders import Nominatim
import pandas as pd

ff = r'data/20181107/download?filename=AQI_all_station2018_11_07T20_00_00Z.xlsx'

df = pd.read_excel(ff,header=3)

geolocator = Nominatim(user_agent="try")

sts = []

fid = open('station_lat_long.txt','w')

for i in range(len(df)):
	print(df['Station Name'][i])
	ll = geolocator.geocode(df['Station Name'][i].split(' - ')[0])
	sts.append(ll)
	if ll==None:
		fid.write(df['Station Name'][i] + '\t' + 'NA'+'\t' + 'NA' +'\n')
		continue
	fid.write(df['Station Name'][i] + '\t' + str(ll.latitude)+'\t' + str(ll.longitude)+'\n')

fid.close()