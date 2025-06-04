import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from transmission import encode_bpsk, channel_noise, decode_bpsk

st.set_page_config(page_title="Chaîne de Transmission", layout="wide")
st.title("Chaîne de Transmission Numérique - Sélection Manuelle des Bits")

st.markdown("### 1. Choisissez vos 10 bits :")

# 10 ComboBox alignées horizontalement
cols = st.columns(10)
bits = []
for i, col in enumerate(cols):
    bit = col.selectbox(f"Bit {i+1}", options=[0, 1], key=f"bit{i}")
    bits.append(bit)

bits = np.array(bits)

# Slider pour le SNR
st.markdown("### 2. Choisissez le niveau de bruit (SNR en dB) :")
snr = st.slider("SNR (Signal to Noise Ratio)", min_value=0, max_value=20, value=5)

if st.button("Simuler la transmission"):
    modulated = encode_bpsk(bits)
    received = channel_noise(modulated, snr)
    decoded = decode_bpsk(received)

    errors = np.sum(bits != decoded)

    st.markdown("### 3. Résultats de la transmission")
    st.write(f"🔢 Bits transmis : {bits.tolist()}")
    st.write(f"🔄 Bits reçus : {decoded.tolist()}")
    st.write(f"❌ Erreurs : {errors} / {len(bits)}")

    # Affichage du signal bruité
    fig, ax = plt.subplots()
    ax.plot(received, 'o-', label="Signal bruité")
    ax.axhline(0, color='gray', linestyle='--')
    ax.set_title("Signal reçu (modulé et bruité)")
    ax.set_xlabel("Index du bit")
    ax.set_ylabel("Amplitude")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
