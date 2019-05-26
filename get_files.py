# -*- coding: utf-8 -*-
# @Author: abhilash
# @Date:   2018-11-08 11:19:08
# @Last Modified by:   abhilash
# @Last Modified time: 2018-11-10 20:26:02

import os

url = 'https://app.cpcbccr.com/aqi_dashboard/download?filename=AQI_all_station'#2018_11_08T11_00_00Z.xlsx'

yr = 2018

#mnts = [2,3,4,5,6,7,8,9,10]
mnts = [11]

dys = [10]

for mnt in mnts:
    for dy in dys:
        for tm in range(24):
            cmd = 'wget --no-check-certificate '+url + str(yr)+'_'+str(mnt).zfill(2)+'_'+str(dy).zfill(2)+'T'+str(tm)+'_00_00Z.xlsx'
            print(cmd)
            os.system(cmd)

# for mnt in mnts:
    
#     if mnt in [1,3,5,7,8,10,12]:
#         lastday = 31
#     elif mnt in [2]:
#         lastday = 28
#     else:
#         lastday = 30
