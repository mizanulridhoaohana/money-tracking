import streamlit as st
from riwayat_pengeluaran import RiwayatPengeluaran
from catat_pengeluaran import CatatPengeluaran

st.title('Hemat WOYYY!! Catet disini😂')

# Sidebar untuk navigasi
menu = st.sidebar.selectbox('Menu', ['Lihat Riwayat Pengeluaran', 'Catat Pengeluaran'])

# Menampilkan fitur berdasarkan pilihan menu
if menu == 'Lihat Riwayat Pengeluaran':
    RiwayatPengeluaran().show()
elif menu == 'Catat Pengeluaran':
    CatatPengeluaran().show()

# Jalankan aplikasi dengan perintah:
# streamlit run App.py
