# main.py
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

# Configuration de la page Streamlit
st.set_page_config(page_title="Chaîne de Transmission Numérique", layout="wide")
st.title("Chaîne de Transmission Numérique - Simulation Complète")

# Bloc 1 : Saisie manuelle des bits (séquence binaire émise)
st.subheader("1. Séquence binaire émise")
cols = st.columns(10)
bits = []
for i, col in enumerate(cols):
    bits.append(col.selectbox(f"Bit {i+1}", options=[0, 1], key=f"bit_{i}"))
bits = np.array(bits)

# Bloc 2 : Codage en ligne (NRZ ou Manchester)
st.subheader("2. Codage en ligne")
coding_type = st.selectbox("Type de codage en ligne", ["NRZ", "Manchester"])

def encode_line(bits, type="NRZ"):
    if type == "NRZ":
        return 2 * bits - 1  # NRZ: 0 -> -1, 1 -> +1
    elif type == "Manchester":
        manchester = []
        for bit in bits:
            if bit == 0:
                manchester.extend([-1, 1])
            else:
                manchester.extend([1, -1])
        return np.array(manchester)

encoded_signal = encode_line(bits, coding_type)

# Bloc 3 : Filtre d’émission (moyenne glissante)
st.subheader("3. Filtre d'émission")
apply_tx_filter = st.checkbox("Appliquer un filtre d'émission", value=True)

def filtre_moyen(signal, taille=3):
    kernel = np.ones(taille) / taille
    return convolve(signal, kernel, mode='same')

if apply_tx_filter:
    filtered_tx = filtre_moyen(encoded_signal)
else:
    filtered_tx = encoded_signal

# Bloc 4 : Modulation BPSK (déjà -1/+1)
st.subheader("4. Modulation BPSK")
def bpsk_modulate(signal):
    return signal  # Déjà en -1/+1

modulated_signal = bpsk_modulate(filtered_tx)

# Bloc 5 : Canal bruité
st.subheader("5. Canal de propagation (bruit)")
snr_db = st.slider("SNR (Signal-to-Noise Ratio) en dB", 0, 20, 5)

def add_noise(signal, snr_db):
    snr = 10 ** (snr_db / 10)
    power = np.mean(signal**2)
    noise_power = power / snr
    noise = np.random.normal(0, np.sqrt(noise_power), len(signal))
    return signal + noise

noisy_signal = add_noise(modulated_signal, snr_db)

# Bloc 6 : Filtre de réception (optionnel)
st.subheader("6. Filtre de réception")
apply_rx_filter = st.checkbox("Appliquer un filtre de réception", value=True)

if apply_rx_filter:
    filtered_rx = filtre_moyen(noisy_signal)
else:
    filtered_rx = noisy_signal

# Bloc 7 : Récupération de l’horloge + Bloc 8 : Décision
st.subheader("7-8. Récupération de l'horloge et décision")
def recover_and_decide(signal, original_length, coding="NRZ"):
    if coding == "Manchester":
        sampled = signal[1::2]  # Échantillonner au milieu
    else:
        sampled = signal
    sampled = sampled[:original_length]
    return np.where(sampled >= 0, 1, 0)

decoded_bits = recover_and_decide(filtered_rx, len(bits), coding_type)
errors = np.sum(decoded_bits != bits)

# Bloc 9 : Résultats
st.subheader("9. Résultats")
st.write(f"Bits émis : {bits.tolist()}")
st.write(f"Bits reçus : {decoded_bits.tolist()}")
st.write(f"Nombre d'erreurs : {errors} / {len(bits)}")

# Affichage graphique
fig, ax = plt.subplots()
ax.plot(noisy_signal, label="Signal bruité", marker='o')
ax.plot(filtered_rx, label="Signal filtré (réception)", linestyle='--')
ax.axhline(0, color='gray', linestyle=':')
ax.set_title("Signal reçu avec bruit et filtrage")
ax.set_xlabel("Index")
ax.set_ylabel("Amplitude")
ax.legend()
ax.grid(True)
st.pyplot(fig)
