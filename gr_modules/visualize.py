import matplotlib.pyplot as plt
import numpy as np
#from scipy.interpolate import griddata
import matplotlib.mlab as ml

import rx_processor


gps_lats = []
gps_lons = []
gps_dirs = []
gps_alts = []
rssis = []

print '[info] Reading from files.'

with open('rssi_data', 'r') as f_rssi:
  with open('gps_data', 'r') as f_gps:
    count = 0
    while True:
      gps_dict = f_gps.readline()
      gps_dir = f_gps.readline()
      gps_alt = f_gps.readline()
      rssi = f_rssi.readline()

      if not gps_dict or not gps_dir or not gps_alt or not rssi:
        print '[info] Loaded files. Num readings:', count
        break

      '''
      gps_dict = eval(gps_dict)
      gps_dir = int(gps_dir)
      gps_alt = float(gps_alt)
      rssi = float(rssi)
      '''
      if float(rssi) == -1000000:
        gps_dict = eval(gps_dict)
        gps_lats.append(float(gps_dict['lat']))
        gps_lons.append(float(gps_dict['lon']))
        gps_dirs.append(int(gps_dir))
        gps_alts.append(float(gps_alt))
        rssis.append(-10)
        #bad_rssi.append(count)
      else:
        gps_dict = eval(gps_dict)
        gps_lats.append(float(gps_dict['lat']))
        gps_lons.append(float(gps_dict['lon']))
        gps_dirs.append(int(gps_dir))
        gps_alts.append(float(gps_alt))
        rssis.append(float(rssi))
      count += 1

      
      #(key, val) = gps.split()
      print 'GPS: ', str(gps_dict['lat']), str(gps_dict['lon']), str(gps_alt), str(gps_dir)
      print 'RSSI:', str(rssi)
      

gps_lats = np.array(gps_lats)
gps_lons = np.array(gps_lons)
gps_dirs = np.array(gps_dirs)
gps_alts = np.array(gps_alts)
rssis = np.array(rssis)

xi = np.linspace(gps_lats.min(),gps_lats.max(),1000)
yi = np.linspace(gps_lons.min(),gps_lons.max(),1000)
zi = ml.griddata(gps_lats, gps_lons, rssis, xi, yi, interp='linear')
#NOTE: can also visualize other things like gps_dirs, gps_alts
#zi = ml.griddata(gps_lats, gps_lons, gps_dirs, xi, yi, interp='linear')
#zi = ml.griddata(gps_lats, gps_lons, gps_alts, xi, yi, interp='linear')

# Z is a matrix of x-y values
#zi = griddata((gps_lats, gps_lons), rssis, (xi[None,:], yi[:,None]), method='cubic')
plt.contour(xi, yi, zi, 15, linewidths = 0.5, colors = 'k')
plt.pcolormesh(xi, yi, zi, cmap = plt.get_cmap('rainbow'))
plt.colorbar()
plt.scatter(gps_lats, gps_lons)
plt.xlim(gps_lats.min(), gps_lats.max())
plt.ylim(gps_lons.min(), gps_lons.max())
plt.show()