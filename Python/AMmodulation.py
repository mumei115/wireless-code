import numpy as np 
import matplotlib.pyplot as plt 
import math

#パラメーター設定
pi = math.pi
f_s = 44100 #サンプリングレート
t_fin = 1 #終了時間(秒)
dt = 1/ f_s #サンプリング周期
N = int(f_s * t_fin) #サンプル数
t = np.arange(0, t_fin, dt)
fre1 = 100 #搬送波の周波数
fre2 = 5 #入力信号の周波数
A_s = 2 #搬送波の振幅
A_m = 1 #入力信号の振幅

makewave = np.zeros_like(t)
#搬送波生成
carrier = A_s * np.cos(2 * pi * fre1 * t) 

#入力波生成
modulator = A_m * np.sin(2 * pi * fre2 * t)

#AM変調
am_wave = (A_s + A_m * modulator) * carrier



#グラフの描画
plt.figure(figsize=(10, 6))
plt.plot(t, carrier) 
plt.title('Carrier Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.xlim(0,0.1) 
plt.ylim(-3,3)
plt.show()  

#グラフの描画
plt.figure(figsize=(10, 6))
plt.plot(t, am_wave) 
plt.title('AMmodulation')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.xlim(0,1) 
plt.ylim(-10,10)
plt.show()  


