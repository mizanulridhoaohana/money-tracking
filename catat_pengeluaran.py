import streamlit as st
import json
import os
from datetime import datetime

class CatatPengeluaran:
    json_file = 'expenses.json'

    @staticmethod
    def load_data():
        if os.path.exists(CatatPengeluaran.json_file):
            with open(CatatPengeluaran.json_file, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []
        return data

    @staticmethod
    def save_data(data):
        with open(CatatPengeluaran.json_file, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def add_expense(date, sources, expenses):
        data = CatatPengeluaran.load_data()
        new_entry = {
            'date': date,
            'sources': sources,
            'expenses': expenses,
            'total': sum(exp['amount'] for exp in expenses)
        }
        data.append(new_entry)
        CatatPengeluaran.save_data(data)

    @staticmethod
    def calculate_remaining(sources, expenses):
        total_source_amount = sum(source['amount'] for source in sources)
        total_expenses = sum(exp['amount'] for exp in expenses)
        remaining = total_source_amount - total_expenses
        return remaining

    def format_number(self, number):
        return f"{number:,}".replace(',', '.')

    def show(self):
        st.header('Catat Pengeluaran')

        # Section 1: Tanggal dan Sumber Keuangan
        st.subheader('Tanggal dan Sumber Keuangan')
        date = st.date_input('Tanggal', datetime.now())
        source = st.text_input('Sumber Keuangan')
        source_amount = st.number_input('Jumlah Sumber Keuangan', min_value=0, format='%d')

        if 'sources' not in st.session_state:
            st.session_state.sources = []

        if st.button('Tambahkan Sumber Uang'):
            if source and source_amount > 0:
                st.session_state.sources.append({'source': source, 'amount': source_amount})
                st.success(f'Sumber uang {source} sebesar {self.format_number(source_amount)} IDR berhasil ditambahkan.')
            else:
                st.error('Sumber Keuangan dan Jumlah Sumber Keuangan harus diisi.')

        # Section 2: Nama Barang dan Nominal Pengeluaran
        st.subheader('Nama Barang dan Nominal Pengeluaran')
        if 'expenses' not in st.session_state:
            st.session_state.expenses = []

        item = st.text_input('Nama Barang')
        amount = st.number_input('Nominal Pengeluaran', min_value=0, format='%d')

        if st.button('Tambahkan Pengeluaran'):
            if item and amount > 0:
                st.session_state.expenses.append({'item': item, 'amount': amount})
                st.success(f'Pengeluaran untuk {item} sebesar {self.format_number(amount)} IDR berhasil ditambahkan.')
            else:
                st.error('Nama Barang dan Nominal Pengeluaran harus diisi.')

        # Tampilkan Daftar Pemasukan
        st.subheader('Daftar Pemasukan:')
        total_sources = sum(source['amount'] for source in st.session_state.sources)
        
        if st.session_state.sources:
            sources_df = {
                'Sumber Keuangan': [source['source'] for source in st.session_state.sources],
                'Nominal Pemasukan (IDR)': [self.format_number(source['amount']) for source in st.session_state.sources]
            }
            st.table(sources_df)
        else:
            st.write('Belum ada pemasukan yang ditambahkan.')

        # Tampilkan Daftar Pengeluaran
        st.subheader('Daftar Pengeluaran:')
        total_expenses = sum(exp['amount'] for exp in st.session_state.expenses)
        remaining = self.calculate_remaining(st.session_state.sources, st.session_state.expenses)
        
        if st.session_state.expenses:
            expenses_df = {
                'Nama Barang': [exp['item'] for exp in st.session_state.expenses],
                'Nominal Pengeluaran (IDR)': [self.format_number(exp['amount']) for exp in st.session_state.expenses]
            }
            st.table(expenses_df)
        else:
            st.write('Belum ada pengeluaran yang ditambahkan.')

        # Tampilkan Total Pemasukan, Total Pengeluaran, dan Sisa Uang
        st.subheader('Ringkasan Keuangan:')
        summary_df = {
            'Deskripsi': ['Total Pemasukan', 'Total Pengeluaran', 'Sisa Uang'],
            'Jumlah (IDR)': [
                self.format_number(total_sources),
                self.format_number(total_expenses),
                self.format_number(remaining)
            ]
        }
        st.table(summary_df)

        if st.button('Simpan Pengeluaran'):
            if st.session_state.sources and st.session_state.expenses:
                self.add_expense(str(date), st.session_state.sources, st.session_state.expenses)
                st.session_state.expenses = []
                st.session_state.sources = []
                st.success('Pengeluaran berhasil disimpan.')
            else:
                st.error('Sumber Keuangan dan Pengeluaran harus diisi.')

# Jalankan aplikasi dengan perintah:
# streamlit run App.py
