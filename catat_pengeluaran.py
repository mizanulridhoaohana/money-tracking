import streamlit as st
import json
import os
from datetime import datetime

class CatatPengeluaran:
    def __init__(self, email):
        self.email = email
        self.json_file = f'{email}_expenses.json'

    def load_data(self):
        if os.path.exists(self.json_file):
            with open(self.json_file, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
        else:
            data = []
        return data

    def save_data(self, data):
        with open(self.json_file, 'w') as file:
            json.dump(data, file, indent=4)

    def add_expense(self, date, sources, expenses):
        data = self.load_data()
        new_entry = {
            'date': date.strftime('%Y-%m-%d'),  # Convert date to string
            'sources': sources,
            'expenses': expenses,
            'total': sum(exp['amount'] for exp in expenses)
        }
        data.append(new_entry)
        self.save_data(data)

    def calculate_remaining(self, sources, expenses):
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
                st.error('Sumber Keuangan atau Jumlah Sumber Keuangan tidak boleh kosong atau kurang dari 0.')

        # Section 2: Nama Barang dan Nominal Pengeluaran
        st.subheader('Nama Barang dan Nominal Pengeluaran')
        item = st.text_input('Nama Barang')
        amount = st.number_input('Nominal Pengeluaran', min_value=0, format='%d')

        if 'expenses' not in st.session_state:
            st.session_state.expenses = []

        if st.button('Tambahkan Pengeluaran'):
            if item and amount > 0:
                st.session_state.expenses.append({'item': item, 'amount': amount})
                st.success(f'Pengeluaran {item} sebesar {self.format_number(amount)} IDR berhasil ditambahkan.')
            else:
                st.error('Nama Barang atau Nominal Pengeluaran tidak boleh kosong atau kurang dari 0.')

        st.write('Daftar Pemasukan:')
        if st.session_state.sources:
            sources_df = {
                'Sumber Keuangan': [source['source'] for source in st.session_state.sources],
                'Jumlah (IDR)': [self.format_number(source['amount']) for source in st.session_state.sources]
            }
            st.table(sources_df)
            total_sources = sum(source['amount'] for source in st.session_state.sources)
            st.write(f'Total Pemasukan: {self.format_number(total_sources)} IDR')

        st.write('Daftar Pengeluaran:')
        if st.session_state.expenses:
            expenses_df = {
                'Nama Barang': [expense['item'] for expense in st.session_state.expenses],
                'Nominal Pengeluaran (IDR)': [self.format_number(expense['amount']) for expense in st.session_state.expenses]
            }
            st.table(expenses_df)
            total_expenses = sum(exp['amount'] for exp in st.session_state.expenses)
            remaining = self.calculate_remaining(st.session_state.sources, st.session_state.expenses)
            st.write(f'Total Pengeluaran: {self.format_number(total_expenses)} IDR')
            st.write(f'Sisa Uang: {self.format_number(remaining)} IDR')

        if st.button('Simpan Pengeluaran'):
            self.add_expense(date, st.session_state.sources, st.session_state.expenses)
            st.success('Pengeluaran berhasil disimpan.')
            # Reset session state
            st.session_state.sources = []
            st.session_state.expenses = []
