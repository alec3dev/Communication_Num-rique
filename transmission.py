import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

st.set_page_config(page_title="Chaîne de Transmission Numérique", layout="wide")
st.title("Chaîne de Transmission Numérique - Simulation Complète")

# 1. Saisie utilisateur : bits manuels (10 combobox)
st.subheader("1. Séquence binaire émise")
cols = st.columns(10)
bits = []
for i, col in enumerate(cols):
    bits.append(col.selectbox(f"Bit {i+1}", options=[0, 1], key=f"bit_{i}"))
bits = np.array(bits)

# 2. Codage en ligne : NRZ ou Manchester
st.subheader("2. Codage en ligne")
coding_type = st.selectbox("Type de codage en ligne", ["NRZ", "Manchester"])

def encode_line(bits, type="NRZ"):
    if type == "NRZ":
        return 2 * bits - 1  # NRZ: 0 -> -1, 1 -> +1
    elif type == "Manchester":
        return np.repeat(bits, 2) * 2 - 1  # 0 -> -1,+1 ; 1 -> +1,-1

encoded_signal = encode_line(bits, coding_type)

# 3. Filtre d'émission (simple moyenne glissante)
st.subheader("3. Filtre d'émission")
apply_tx_filter = st.checkbox("Appliquer un filtre d'émission", value=True)

def filtre_moyen(signal, taille=3):
    kernel = np.ones(taille) / taille
    return convolve(signal, kernel, mode='same')

if apply_tx_filter:
    filtered_tx = filtre_moyen(encoded_signal)
else:
    filtered_tx = encoded_signal

# 4. Modulation BPSK
def bpsk_modulate(signal):
    return signal  # signal déjà en -1/+1 (pour NRZ ou Manchester simplifié)

modulated_signal = bpsk_modulate(filtered_tx)

# Canal bruité
db = st.slider("4. SNR (Signal-to-Noise Ratio) en dB", 0, 20, 5)

def add_noise(signal, snr_db):
    snr = 10 ** (snr_db / 10)
    power = np.mean(signal**2)
    noise_power = power / snr
    noise = np.random.normal(0, np.sqrt(noise_power), len(signal))
    return signal + noise

noisy_signal = add_noise(modulated_signal, db)

# 5. Démodulation BPSK
def bpsk_demodulate(signal):
    return np.where(signal >= 0, 1, 0)

# 6. Filtre de réception (symbolique)
st.subheader("5-6. Filtre de réception")
apply_rx_filter = st.checkbox("Appliquer un filtre de réception", value=True)

if apply_rx_filter:
    filtered_rx = filtre_moyen(noisy_signal)
else:
    filtered_rx = noisy_signal

# 7. Récupération de l'horloge + 8. Décision
def recover_and_decide(signal, original_length, coding=coding_type):
    if coding == "Manchester":
        sampled = signal[1::2]  # Prendre un échantillon sur 2 (mi-bit)
    else:
        sampled = signal
    sampled = sampled[:original_length]
    return bpsk_demodulate(sampled)

decoded_bits = recover_and_decide(filtered_rx, len(bits), coding_type)
errors = np.sum(decoded_bits != bits)

# 9. Affichage des résultats
st.subheader("7-9. Résultats")
st.write(f"Bits émis : {bits.tolist()}")
st.write(f"Bits reçus : {decoded_bits.tolist()}")
st.write(f"Erreurs : {errors} / {len(bits)}")

fig, ax = plt.subplots()
ax.plot(noisy_signal, label="Signal bruité")
ax.plot(filtered_rx, label="Filtré (Rx)")
ax.axhline(0, color='gray', linestyle='--')
ax.set_title("Signal bruité et filtré")
ax.legend()
st.pyplot(fig)
