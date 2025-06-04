import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from transmission import generate_bits, encode_bpsk, channel_noise, decode_bpsk

st.title("Chaîne de Transmission Numérique")

# 1. Entrée utilisateur
nb_bits = st.slider("Nombre de bits à transmettre", 10, 1000, 100)
snr = st.slider("SNR (dB)", 0, 20, 5)

if st.button("Simuler"):
    bits = generate_bits(nb_bits)
    modulated = encode_bpsk(bits)
    received = channel_noise(modulated, snr)
    decoded = decode_bpsk(received)

    errors = np.sum(bits != decoded)
    st.write(f"Bits erronés : {errors} sur {nb_bits}")

    fig, ax = plt.subplots()
    ax.plot(received[:50], 'o-', label="Signal bruité")
    ax.set_title("Signal BPSK bruité")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
