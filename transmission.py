import numpy as np

def encode_bpsk(bits):
    return 2 * bits - 1  # BPSK : 1 → +1, 0 → -1

def channel_noise(signal, snr_db):
    snr = 10 ** (snr_db / 10)
    power = np.mean(signal**2)
    noise_power = power / snr
    noise = np.random.normal(0, np.sqrt(noise_power), len(signal))
    return signal + noise

def decode_bpsk(received_signal):
    return np.where(received_signal >= 0, 1, 0)
