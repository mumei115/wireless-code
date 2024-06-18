import numpy as np
import matplotlib.pyplot as plt

# ランダムなビット列を生成
num_bits = 10  # ビット数を適宜変更
data = np.random.randint(0, 2, num_bits)

# BPSK変調
def bpsk_modulation(data):
    return 2 * data - 1

modulated_signal = bpsk_modulation(data)

# パラメータ設定
bit_duration = 1      # 各ビットの持続時間
sampling_rate = 100   # サンプリングレート
t = np.arange(0, bit_duration * num_bits, 1 / sampling_rate)

# 変調前のデータ波形の生成
data_waveform = np.repeat(data, sampling_rate)

# BPSK変調後の波形の生成
waveform = np.zeros(len(t))
for i, bit in enumerate(modulated_signal):
    start_index = i * sampling_rate
    end_index = (i + 1) * sampling_rate
    waveform[start_index:end_index] = bit * np.sin(2 * np.pi * 1 * (t[start_index:end_index] - i))

# 変調前のデータ波形のプロット
plt.figure(figsize=(12, 4))
plt.plot(t, data_waveform, drawstyle='steps-post')
plt.title("Original Data Waveform")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid()
plt.show()

# 変調後のBPSK波形のプロット
plt.figure(figsize=(12, 4))
plt.plot(t, waveform)
plt.title("BPSK Modulated Signal Waveform")
plt.xlabel("Time")
plt.ylabel("Amplitude")
plt.grid()
plt.show()
