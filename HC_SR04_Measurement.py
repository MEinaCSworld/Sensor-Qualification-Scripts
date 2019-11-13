# -*- coding: utf-8 -*-
"""
Readout of Arduino Uno

@author: zwood
"""

import serial
import statistics
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style = 'darkgrid', font_scale = 1.5, rc = {'figure.figsize':(11,8)})

'''
Set Serial settings to match Arduino settings
Windows serial can be finicky, ensure that the serial connection is 
closed whenever appropriate
'''
ser = serial.Serial('COM3',9600,timeout = 5)
ser.is_open


n = 0
m = 0
l = 0
e = 0
fl_list = list([])
for i in range(500):
    data = ser.readline()
    datastr = data.decode('utf-8')
    
    if datastr[0].isdigit():
        fl = float(datastr)
        fl_list.append(fl)
        n = n + 1
    elif datastr[0].isalpha():
        m = m+1
    else:
        l = l + 1
    print(datastr)
    i = i+1

ser.close()

median = statistics.median(fl_list)
mean = statistics.mean(fl_list)

sigma1 = statistics.stdev(fl_list)
'''Outlier filter
3 sigma above or below median is filtered
'''
uLim = median + 3*sigma1
lLim = median - 3*sigma1

for u in fl_list:
    if u > uLim or u < lLim:
        fl_list.remove(u)
        n = n - 1
        e = e + 1

sigma = statistics.stdev(fl_list)
tot = n + l + e + m
sucRate = n / tot
print('The success rate is' + str(sucRate))
print('The mean is' + str(mean))
print('The stdev is'+ str(sigma))
print('The minimum measurement is' + str(min(fl_list)))
print('The maximum measurement is' + str(max(fl_list)))
print('The range is' + str(max(fl_list)-min(fl_list)))

fig,ax = plt.subplots(1,1)
ax.scatter(range(n),fl_list, label = 'Measurement')
ax.plot((0,n),(mean,mean), color = 'black', label = 'Mean')
ax.plot((0,n),(mean-sigma,mean-sigma),color = 'red',
        label = r'One $\sigma$ from mean', linestyle = '--')
ax.plot((0,n),(mean+sigma,mean+sigma),color = 'red',
        linestyle='--')
ax.set(xlabel = 'Sample number', ylabel = 'Measured Distance (cm)',
       title='300 cm Nominal Distance',xlim = (0,n))
ax.legend(bbox_to_anchor=(1, 1.05))
    

