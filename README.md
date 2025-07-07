# plotting_3D_FFM
 python绘制三维有限断层模型，以及转换为GMT适用的数据

## 效果图
![Figure_1](https://github.com/CovMat/plotting_3D_FFM/assets/26203721/c5f62882-e758-4300-85a8-e54375d53bbf)

## 输入数据格式
适用于给出每一个小矩形中心坐标、矩形长宽、走向倾向倾角的情况。例如：
```
     lat_deg     lon_deg    depth_km   length_km    width_km  slp_strk_m  slp_ddip_m    slp_am_m  strike_deg     dip_deg    rake_deg sig_stk_MPa sig_ddi_MPa sig_nrm_MPa
     34.7982     97.5406      0.8874      1.9546      1.8890      0.2690     -0.3206      0.4186    102.8566     69.9500     50.0000      1.7759     -1.5403      0.2174
     34.7925     97.5389      2.6611      1.9548      1.8890      0.2156     -0.2569      0.3354    102.8566     69.8445     50.0000      0.8002     -0.7488      0.0076
     34.7868     97.5372      4.4338      1.9549      1.8890      0.2255     -0.2688      0.3508    102.8567     69.7391     50.0000      0.7526     -0.8695     -0.0233

```

## 转换为GMT绘图要求的数据格式
GMT绘图要求给出每一个小矩形四个顶点的三维坐标，例如：
```
# 数据头段
>  -Z1.800000e-01
 # 经度 纬度 深度
 99.3785  34.5324  -0.0010
 99.3574  34.5279  -0.0010
 99.3569  34.5297  -1.9900
 99.3779  34.5342  -1.9900
>  -Z5.000000e-02
 99.3574  34.5279  -0.0010
 99.3363  34.5233  -0.0010
 99.3358  34.5252  -1.9900
 99.3569  34.5297  -1.9900
...
```

转换方法其实适用简单的三角函数就能计算，关键公式在66-69行：
```
    A = np.array([0,0,0])
    B = np.array([ length_km*np.sin(strike_deg*np.pi/180.0), length_km*np.cos(strike_deg*np.pi/180.0),0 ])
    D = np.array([ width_km*np.cos(dip_deg*np.pi/180.0)*np.cos(strike_deg*np.pi/180.0), width_km*np.cos(dip_deg*np.pi/180.0)*np.sin(strike_deg*np.pi/180.0)*-1.0, -1.0*width_km*np.sin(dip_deg*np.pi/180.0) ])
    C = B + D
```
这里计算出的就是每一个小矩形四个顶点ABCD的坐标

## 赞赏
如果你觉得这个程序有用，不妨微信赞赏一下
![IMG_4252](https://github.com/user-attachments/assets/fde857a7-92d3-449c-947e-907c253cc4aa)
