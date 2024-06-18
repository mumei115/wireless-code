import numpy as np 
import matplotlib.pyplot as plt 
import math

# パラメーター設定
pi = math.pi
f_s = 44100  # サンプリングレート
t_fin = 60   # 終了時間(秒)
dt = 1 / f_s # サンプリング周期
N = int(f_s * t_fin) # サンプル数
t = np.arange(0, t_fin, dt)
fre1 = 152  # 搬送波の周波数
A_s = 100     # 搬送波の振幅

num_waves = 50
makewave = np.zeros_like(t)

# 搬送波生成
carrier = A_s * np.cos(2 * pi * fre1 * t) 



# ランダムな周波数の波の生成
for i in range(num_waves):
    frequency = np.random.uniform(20, 30) # 周波数が20Hzから30Hzの範囲(任意)
    ampli = np.random.uniform(2, 30) # 振幅の範囲が2から30(任意)
    wave = ampli * np.sin(2 * pi * frequency * t)
    makewave += wave # 合成波の生成

# 合成波と搬送波の合成
wave1 = makewave + carrier

# tの関数をfの関数にする
y_fft = np.fft.fft(wave1) # 離散フーリエ変換
freq = np.fft.fftfreq(N, d=dt) # 周波数を割り当て
Amp = abs(y_fft / (N / 2)) # 振幅の大きさ

# 電力スペクトルを計算
power_spectrum = np.abs(y_fft) ** 2 / N

# 結果をプロット
plt.figure(figsize=(10, 6))

# 時間領域の信号
plt.subplot(3, 1, 1)
plt.plot(t, wave1, label='Composite Wave')
plt.title('Time Domain Signal')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.xlim(0 , 60)
plt.legend()
plt.grid()

# 振幅スペクトル
plt.subplot(3, 1, 2)
plt.plot(freq[:N // 2], Amp[:N // 2], label='Amplitude Spectrum')
plt.title('Amplitude Spectrum')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude')
plt.xlim(0 , 200)
plt.legend()
plt.grid()

# 電力スペクトル
plt.subplot(3, 1, 3)
plt.plot(freq[:N // 2], power_spectrum[:N // 2], label='Power Spectrum', color='orange')
plt.title('Power Spectrum')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Power')
plt.xlim(0 , 200)
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()



