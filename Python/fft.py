import numpy as np 
import matplotlib.pyplot as plt 
import math

pi = math.pi
f_s = 44100 #サンプリングレート
t_fin = 1 #終了時間(秒)
dt = 1/ f_s #サンプリング周期
N = int(f_s * t_fin) #サンプル数
t = np.arange(0, t_fin, dt)

#波の初期化
num_waves = 20 #5つの波を生成(任意の数)
makewave = np.zeros_like(t)


#ランダムな周波数の波の生成
for i in range(num_waves):
    frequency = np.random.uniform(100 , 200) #周波数が100Hzから500Hzの範囲(任意)
    ampli = np.random.uniform(1 , 10)

 #振幅の範囲が2から30(任意)

    wave = ampli * np.sin(2 * pi * frequency * t)

    makewave += wave #合成波の生成

#グラフの描画
plt.plot(t, makewave) #時間領域のグラフ
plt.xlim(0,0.3) #横軸の範囲
plt.show()   

#tの関数をfの関数にする
y_fft = np.fft.fft(makewave) # 離散フーリエ変換
freq = np.fft.fftfreq(N, d=dt) # 周波数を割り当て
Amp = abs(y_fft/(N/2)) #振幅の大きさ

### 音波のスペクトル ###
plt.plot(freq[1:int(N/2)], Amp[1:int(N/2)]) #A-f グラフのプロット
plt.xlim(50 , 250) # 横軸
plt.show()

### IFFT: fの関数をtの関数にする ###
y_ifft = np.fft.ifft(y_fft)

### 逆変換したグラフ: もとの波形を復元 ###
plt.plot(t, y_ifft.real) # 実部しかいらない
plt.xlim(0, 0.1)
plt.show()



