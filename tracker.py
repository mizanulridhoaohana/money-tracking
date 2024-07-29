import streamlit as st
import json
import os
from datetime import datetime

# Path untuk file JSON
json_file = 'expenses.json'

# Fungsi untuk memuat data dari file JSON
def load_data():
    if os.path.exists(json_file):
        with open(json_file, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    return data

# Fungsi untuk menyimpan data ke file JSON
def save_data(data):
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

# Fungsi untuk menambahkan pengeluaran baru
def add_expense(date, sources, expenses):
    data = load_data()
    new_entry = {
        'date': date,
        'sources': sources,
        'expenses': expenses,
        'total_expenses': sum(exp['amount'] for exp in expenses),
        'total_sources': sum(src['amount'] for src in sources),
        'remaining': sum(src['amount'] for src in sources) - sum(exp['amount'] for exp in expenses)
    }
    data.append(new_entry)
    save_data(data)

# Fungsi untuk menghitung sisa uang
def calculate_remaining(sources, expenses):
    total_expenses = sum(exp['amount'] for exp in expenses)
    total_sources = sum(src['amount'] for src in sources)
    remaining = total_sources - total_expenses
    return remaining

# Streamlit interface
st.title('Aplikasi Pengeluaran Uang')

# Sidebar untuk navigasi
menu = st.sidebar.selectbox('Menu', ['Lihat Riwayat Pengeluaran', 'Catat Pengeluaran'])

# Fitur Lihat Riwayat Pengeluaran
if menu == 'Lihat Riwayat Pengeluaran':
    st.header('Riwayat Pengeluaran')
    data = load_data()
    
    if data:
        for entry in data:
            st.subheader(f"Tanggal: {entry['date']}")
            st.write(f"Sumber Keuangan:")
            for source in entry['sources']:
                st.write(f"{source['name']}: {source['amount']} IDR")
            st.write(f"Total Sumber Keuangan: {entry['total_sources']} IDR")
            st.write(f"Pengeluaran:")
            for expense in entry['expenses']:
                st.write(f"{expense['item']}: {expense['amount']} IDR")
            st.write(f"Total Pengeluaran: {entry['total_expenses']} IDR")
            st.write(f"Sisa Uang: {entry['remaining']} IDR")
            st.write('---')
    else:
        st.write('Belum ada data pengeluaran.')

# Fitur Catat Pengeluaran
elif menu == 'Catat Pengeluaran':
    st.header('Catat Pengeluaran')
    
    # Section 1: Tanggal dan Sumber Keuangan
    st.subheader('Tanggal dan Sumber Keuangan')
    date = st.date_input('Tanggal', datetime.now())
    
    if 'sources' not in st.session_state:
        st.session_state.sources = []
    
    source_name = st.text_input('Nama Sumber Keuangan')
    source_amount = st.number_input('Jumlah Sumber Keuangan', min_value=0)
    
    if st.button('Tambahkan Sumber Keuangan'):
        if source_name and source_amount > 0:
            st.session_state.sources.append({'name': source_name, 'amount': source_amount})
            st.success(f'Sumber keuangan {source_name} sebesar {source_amount} IDR berhasil ditambahkan.')
        else:
            st.error('Nama Sumber Keuangan dan Jumlah harus diisi.')

    st.write('Daftar Sumber Keuangan:')
    total_sources = sum(src['amount'] for src in st.session_state.sources)
    
    for src in st.session_state.sources:
        st.write(f"{src['name']}: {src['amount']} IDR")
    st.write(f"Total Sumber Keuangan: {total_sources} IDR")
    
    # Section 2: Nama Barang dan Nominal Pengeluaran
    st.subheader('Nama Barang dan Nominal Pengeluaran')
    if 'expenses' not in st.session_state:
        st.session_state.expenses = []
    
    item = st.text_input('Nama Barang')
    amount = st.number_input('Nominal Pengeluaran', min_value=0)
    
    if st.button('Tambahkan Pengeluaran'):
        if item and amount > 0:
            st.session_state.expenses.append({'item': item, 'amount': amount})
            st.success(f'Pengeluaran untuk {item} sebesar {amount} IDR berhasil ditambahkan.')
        else:
            st.error('Nama Barang dan Nominal Pengeluaran harus diisi.')

    st.write('Daftar Pengeluaran:')
    total_expenses = sum(exp['amount'] for exp in st.session_state.expenses)
    remaining = calculate_remaining(st.session_state.sources, st.session_state.expenses)
    
    for exp in st.session_state.expenses:
        st.write(f"{exp['item']}: {exp['amount']} IDR")
    
    st.write(f"Total Pengeluaran: {total_expenses} IDR")
    st.write(f"Sisa Uang: {remaining} IDR")
    
    if st.button('Simpan Pengeluaran'):
        if st.session_state.sources and st.session_state.expenses:
            add_expense(str(date), st.session_state.sources, st.session_state.expenses)
            st.session_state.expenses = []
            st.session_state.sources = []
            st.success('Pengeluaran berhasil disimpan.')
        else:
            st.error('Sumber Keuangan dan Pengeluaran harus diisi.')

# Jalankan aplikasi dengan perintah:
# streamlit run expense_tracker.py
