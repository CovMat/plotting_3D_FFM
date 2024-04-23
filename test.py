## 作者：陈箫翰  GMT中文社区
import numpy as np
import mpl_toolkits.mplot3d as a3
import matplotlib.pyplot as plt
from geopy import distance
import matplotlib.cm as cm
from matplotlib.colors import Normalize

ax = plt.figure().add_subplot(projection='3d')

f = open('slip.dat','r')
lines = f.readlines()
f.close()

# 指定一个原点
lat_0 = 34.4
lon_0 = 99.2
# 
xmin = 999999999
xmax = -99999999
ymin = 999999999
ymax = -99999999
# 指定色条的范围
cmap = cm.rainbow
norm = Normalize(vmin=0, vmax=6)

for line in lines[1:]:
    data = line.split()

    if (len(data)<10):
      continue

    lat_deg = float(data[0])
    lon_deg = float(data[1])
    depth_km = float(data[2])
    length_km = float(data[3])
    width_km = float(data[4])
    strike_deg = float(data[8])
    dip_deg = float(data[9])
    rake_deg = float(data[10])
    slp_am_m = float(data[7])

    # 计算水平方向和原点的距离
    dist_N = distance.distance((lat_0, lon_0), (lat_deg, lon_0)).km
    dist_E = distance.distance((lat_0, lon_0), (lat_0, lon_deg)).km

    #print(dist_N,dist_E)
    # 转换成笛卡尔坐标系
    y = dist_N
    if (lat_deg < lat_0):
      y = -1.0*y
    x = dist_E
    if (lon_deg < lon_0):
      x = -1.0*x
    z = -1.0*depth_km

    if (x>xmax):
      xmax = x
    if (x<xmin):
      xmin = x
    if (y>ymax):
      ymax = y
    if (y<ymin):
      ymin = y

    A = np.array([0,0,0])
    B = np.array([ length_km*np.sin(strike_deg*np.pi/180.0), length_km*np.cos(strike_deg*np.pi/180.0),0 ])
    D = np.array([ width_km*np.cos(dip_deg*np.pi/180.0)*np.cos(strike_deg*np.pi/180.0), width_km*np.cos(dip_deg*np.pi/180.0)*np.sin(strike_deg*np.pi/180.0)*-1.0, -1.0*width_km*np.sin(dip_deg*np.pi/180.0) ])
    C = B + D

    # 得到矩形中心坐标
    RC = (A+C)/2.0-np.array([x,y,z])
    P = np.vstack((A-RC,B-RC,C-RC,D-RC)).tolist()
    rect = a3.art3d.Poly3DCollection([P],linewidths=0.1, edgecolors='black', alpha=.50, facecolors=cmap(norm(slp_am_m)))
    ax.add_collection3d(rect)
ax.set_xlim([xmin,xmax])
ax.set_ylim([ymin,ymax])
ax.set_zlim([-30,0])
# 水平坐标变为经纬度
ax.set_yticklabels(('34.4', '34.5', '34.6', '34.7'))
ax.set_yticks([ 0, \
                distance.distance((lat_0, lon_0), (lat_0+0.1, lon_0)).km, \
                distance.distance((lat_0, lon_0), (lat_0+0.2, lon_0)).km, \
                distance.distance((lat_0, lon_0), (lat_0+0.3, lon_0)).km  ])
ax.set_xticklabels(('99.6','99.2','98.8', '98.4', '98.0'))
ax.set_xticks([ distance.distance((lat_0, lon_0), (lat_0, lon_0+0.4)).km, \
                0, \
                -distance.distance((lat_0, lon_0), (lat_0, lon_0-0.4)).km, \
                -distance.distance((lat_0, lon_0), (lat_0, lon_0-0.8)).km, \
                -distance.distance((lat_0, lon_0), (lat_0, lon_0-1.2)).km ])
ax.set_ylabel('latitude')
ax.set_xlabel('longitude')
ax.set_zlabel('depth (km)')
plt.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax, label="slp_am_m", orientation="horizontal")
plt.show()
