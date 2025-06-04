import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from transmission import encode_bpsk, channel_noise, decode_bpsk

st.title("Chaîne Numérique avec Séquence Binaire Fixe")

# Séquence manuelle (modifiable si besoin)
bits = np.array([1, 0, 1, 1, 0])
st.write("Séquence binaire émise :", bits)

snr = st.slider("SNR (dB)", 0, 20, 5)

if st.button("Simuler la transmission"):
    modulated = encode_bpsk(bits)
    received = channel_noise(modulated, snr)
    decoded = decode_bpsk(received)

    st.write("Signal modulé :", modulated)
    st.write("Signal reçu :", np.round(received, 2))
    st.write("Bits décodés :", decoded)
    
    errors = np.sum(bits != decoded)
    st.write(f"Erreurs : {errors} / {len(bits)}")

    fig, ax = plt.subplots()
    ax.plot(received, 'o-', label="Signal bruité")
    ax.axhline(0, color='gray', linestyle='--')
    ax.set_title("Signal reçu avec bruit")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
